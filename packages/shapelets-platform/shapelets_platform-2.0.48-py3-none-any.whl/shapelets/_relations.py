from __future__ import annotations

from typing import Callable, Dict, Generator, List, Optional, Tuple, Union, Any
from typing_extensions import Literal

import shapelets_native as sn
from shapelets_native import ParquetCodec, CSVCodec

import re
import os
import errno
import warnings
import types
import pathlib

from weakref import WeakValueDictionary
from pathlib import Path
from threading import get_ident

import numpy as np
import pandas as pd
import pyarrow
import pyarrow.dataset
import tabulate
import pandas

from .svr import mustang


def _resolveFile(file: str, expanded: bool = False) -> str:
    """
    Utility method that takes a file and tries to resolve any
    tildes and dollar signs against home directories and
    environment variables.

    Useful when dealing with configurations that depend on
    interactive or worker sessions.
    """

    if ("~" in file) or ("$" in file):
        if expanded:
            raise FileNotFoundError(errno.ENOENT, f"[{file}] contains unresolved entries.")
        tmp = os.path.expanduser(file)
        tmp = os.path.expandvars(tmp)
        return _resolveFile(tmp, True)

    return os.path.realpath(file)


class DataSet:
    __slots__ = ('__rel', '__tblObj', '__map_fn')

    def __init__(self, rel: sn.Relation, __map_fn: Callable[[sn.Relation], type]) -> None:
        self.__rel = rel
        self.__tblObj = None
        self.__map_fn = __map_fn

    def __mustang_reg(self):
        if self.__tblObj is None:
            self.__tblObj = self.__map_fn(self.__rel)

    def __iter__(self):
        self.__mustang_reg()
        return iter(self.__tblObj)

    def __check_col(self, col: Union[str, int], existing: List[str], case_insensitive: bool = True) -> str:
        if isinstance(col, int):
            if col < 0 or col >= len(existing):
                raise ValueError(f'Column index {col} is out of bounds')
            return existing[col]

        if isinstance(col, str):
            cc = col.casefold() if case_insensitive else col
            if cc not in existing:
                raise ValueError(f'Unknown column {col}')
            return col

        raise ValueError(f'{col} should be of type string or integer; it is {type(col)}')

    def describe(self) -> pd.DataFrame:
        return self.__rel.describe().to_pandas()

    def head(self, n: int = 5) -> pd.DataFrame:
        r"""
        Returns the first `n` rows as a Pandas DataFrame 

        This function returns the first `n` rows for the object based
        on position. It is useful for quickly testing if your object
        has the right type of data in it.

        For negative values of `n`, this function returns all rows except
        the last `|n|` rows.

        If n is larger than the number of rows, this function returns all rows.

        Parameters
        ----------
        n : int, default 5
            Number of rows to select. Zero is not a permitted value.

        Returns
        -------
        pandas.DataFrame
            The first `n` rows of the caller object in pandas.DataFrame format.
        """

        if n == 0:
            raise ValueError("Argument n should be different to zero")

        if n > 0:
            return DataSet(self.__rel.limit(n, 0), self.__map_fn).to_pandas()

        # n is negative
        nrows = self.__rel.count()
        if nrows == 0:
            return self.to_pandas()

        n = nrows + n  # this is a subtraction
        return DataSet(self.__rel.limit(n, 0), self.__map_fn).to_pandas()

    def tail(self, n: int = 5) -> pd.DataFrame:
        r"""
        Returns the last `n` rows as a Pandas DataFrame.

        This function returns last `n` rows from the object based on
        position. It is useful for quickly verifying data, for example,
        after sorting or appending rows.

        For negative values of `n`, this function returns all rows except
        the first `|n|` rows.

        If n is larger than the number of rows, this function returns all rows.

        Notes
        -----
        Since this method always works from the end of the DataSet, it 
        will force the DataSet to execute in order to determine the 
        total amount of rows.

        Parameters
        ----------
        n : int, default 5
            Number of rows to select.  It cannot be zero.

        Returns
        -------
        pandas.DataFrame
            The last `n` rows of the caller object in pandas.DataFrame format.
        """

        if n == 0:
            raise ValueError("Argument n should be different to zero.")

        nrows = self.__rel.count()
        if nrows == 0:
            return self.to_pandas()

        if n > 0:  # return the last n values
            offset = nrows - n
            return self.limit(n, offset).to_pandas()

        offset = -n  # positive offset to skip n rows
        n = nrows + n  # this is a subtraction
        return self.limit(n, offset).to_pandas()

    def sample(self, method: Literal['reservoir', 'system'] = 'system', size: Union[float, int] = 0.1, seed: Optional[int] = None) -> DataSet:
        if method == 'reservoir':
            if not isinstance(size, int) or size <= 0:
                raise ValueError("Reservoir sampling requires a fixed, absolute number of rows to retrieve")
            return DataSet(self.__rel.reservoir_sample(size), self.__map_fn)

        if method != 'system':
            raise ValueError(f"Unknown sampling method: {method}")

        if not isinstance(size, float) or size <= 0.0 or size >= 1.0:
            raise ValueError("System sampling requires a percentage of rows to retrieve.")

        return DataSet(self.__rel.system_sample(size, seed), self.__map_fn)

    def rename_columns(self, new_names: Dict[Union[int, str], str]) -> DataSet:
        """
        Renames the columns in a DataSet

        Notes
        -----
        Column names are case insensitive

        Parameters
        ----------
        new_names: dictionary 
            Maps existing columns to new columns.  Existing columns may be 
            referenced by position or by name.

        Returns
        -------
        DataSet
            A new DataSet instance where original columns have been renamed 
            to new column names.
        """
        cols = self.__rel.columns
        existing_cols = []
        renamed_cols = []
        for idx, c in enumerate(cols):
            r = new_names.get(idx, None) or new_names.get(c, None) or c
            existing_cols.append('"' + c + '"')
            renamed_cols.append(r)

        return DataSet(self.__rel.rename_columns(existing_cols, renamed_cols), self.__map_fn)

    def select_columns(self,
                       cols: Optional[Union[str, int, List[Union[int, str]]]] = None,
                       pattern: Optional[str] = None,
                       full_match: bool = True,
                       flags: re.RegexFlag = re.RegexFlag.IGNORECASE) -> DataSet:
        """
        Selects or reorganises columns in a DataSet

        Parameters
        ----------
        cols: string, int or a list of strings and/or ints
            The selected columns, either by index or by name, will be ordered by this 
            list.

        pattern: string or regular expression
            Selects all columns matching a regular expression.  The order of the columns
            will the the same as the current dataset.  

        full_match: boolean, defaults to True
            When pattern is given, this flag indicates if `re.fullmatch` should be used to 
            determine if a column is to be dropped; otherwise, the method `re.match` will 
            be used.

        flags: re.RegexFlag, defaults to IGNORECASE
            Flags to be used when compiling the pattern.        

        Notes
        -----
        It is possible to specify cols and pattern simultaneously; in this scenario, columns 
        selected by `cols` will take preference over the selection produced by the regular 
        expression.

        Returns
        -------
        DataSet
            A new DataSet instance.

        """
        keep = []
        ci_keep = []
        ci_cols = list(map(str.casefold, self.__rel.columns))
        if cols is not None:
            if not isinstance(cols, list):
                cols = [cols]
            for c in cols:
                cc = self.__check_col(c, ci_cols)
                if cc.casefold() not in ci_keep:
                    keep.append(cc)
                    ci_keep.append(cc.casefold())

        if pattern is not None:
            r = re.compile(pattern, flags)
            op = r.fullmatch if full_match else r.match
            for c in self.__rel.columns:
                if op(c) is not None and c.casefold() not in ci_keep:
                    keep.append(c)
                    ci_keep.append(c.casefold())

        keep = ['"' + c + '"' for c in keep]  # scape to avoid evaluation
        return DataSet(self.__rel.keep_columns(keep), self.__map_fn)

    def drop_columns(self,
                     cols: Optional[Union[str, int, List[Union[int, str]]]] = None,
                     pattern: Optional[str] = None,
                     full_match: bool = True,
                     flags: re.RegexFlag = re.RegexFlag.IGNORECASE) -> DataSet:
        """
        Drops columns in a DataSet

        Parameters
        ----------
        cols: string, int or a list of string and/or ints
            Selects either single or multiple columns to be drop from the current dataset.
            If the selection is a number, it drops the column by its index.

        pattern: string or regular expression
            Drops all columns matching a regular expression

        full_match: boolean, defaults to True
            When pattern is given, this flag indicates if `re.fullmatch` should be used to 
            determine if a column is to be dropped; otherwise, the method `re.match` will 
            be used.

        flags: re.RegexFlag, defaults to IGNORECASE
            Flags to be used when compiling the pattern.

        Returns
        -------
        DataSet
            A new DataSet instance.
        """

        drop = set()
        ci_cols = list(map(str.casefold, self.__rel.columns))
        if cols is not None:
            if not isinstance(cols, list):
                cols = [cols]
            for c in cols:
                cc = self.__check_col(c, ci_cols)
                drop.add(cc)

        if pattern is not None:
            r = re.compile(pattern, flags)
            op = r.fullmatch if full_match else r.match
            for c in self.__rel.columns:
                if op(c) is not None:
                    drop.add(c)

        # build scaped list
        keep = ['"' + c + '"' for c in self.__rel.columns if c not in drop]
        return DataSet(self.__rel.keep_columns(keep), self.__map_fn)

    def limit(self, n: int = 10, offset: Optional[int] = 0) -> DataSet:
        r"""
        Returns a new DataSet of `n` rows.

        Parameters
        ----------
        n : int, default 10
            Number of rows to select.

        offset: int, optional, defaults to 0.
            Number of rows to skip before taking `n` rows.  This value can be 
            negative or positive.  Positive values refer to the beginning 
            of the dataset, whilst a -1 implies the end of the dataset.

        Notes
        -----
        Please bear in mind that the usage of negative offsets implies the 
        execution of the DataSet to count the current number of rows. 

        Returns
        -------
        DataSet
            A new DataSet, with identical schema to this DataSet but limited 
            to at most `n` rows from an arbitrary `offset`.

        """
        if n <= 0:
            raise ValueError("Argument n should greater than zero.")

        # avoid materializing the relation at all costs
        # if the offset is over the number of rows,
        # the resulting relation will be ok in terms of
        # schema but it will simply have no content
        # whatsoever.
        # nrows = self.__rel.count()

        if (offset < 0):
            nrows = self.__rel.count()
            offset = nrows - offset - n - 1

        return DataSet(self.__rel.limit(n, offset), self.__map_fn)

    def filter(self, func: Callable[[Any], bool]) -> DataSet:
        """
        Returns the Dataset filtered according to the conditions set by a lambda function (func)
        """
        self.__mustang_reg()
        sql = mustang.construct_query_from_lambda_args(self, func=func, frame_depth=1)
        return DataSet(self.__rel.relation_from_query(sql), self.__map_fn)

    def add_column(self, colname: str, *genExpr: types.GeneratorType) -> DataSet:
        """
        Adds a new column (colname) to the Dataset and returns the new Dataset.
        The content of this new column is computed according to a lambda function (func)
        """
        
        if type(*genExpr) is types.FunctionType:
            self.__mustang_reg()
            sql = mustang.construct_query_from_lambda_args(self, func=genExpr[0], frame_depth=1)
            sql = mustang.add_column_to_sql(colname, sql)
        else:
            query = mustang.make_query(genExpr, frame_depth=1, left_join=False)
            sql = mustang.construct_sql_from_query(query)
            sql = mustang.add_column_to_sql(colname, sql)
            
            rest = sql.partition(self.alias)[2]
            expr_relation = rest[2:].partition(',')[0]
            
            cols = self.__rel.columns
            existing_cols = 'SELECT '
            for idx, c in enumerate(cols):
                existing_cols = existing_cols + expr_relation + '.' + '"' + c + '",'
            
            sql = existing_cols + sql      
        
        return DataSet(self.__rel.relation_from_query(sql), self.__map_fn)

    def split_by_column(self, colname: str) -> Dict[str, DataSet]:
        """
        This method returns a dictionary of DataSet, each of them corresponding to the different entries of
        a specific column (colname).
        For example, if DataSet has a column named Vehicle {Car, Motorcycle, Truck} this function will return a dictionary with three DataSet:
        DataSet 1. All rows with colname Vehicle == Car
        DataSet2. All rows with colname Vehicle == Motorcycle
        DataSet3. All rows with colname Vehicle == Truck
        """
        dataset_dict = dict()

        if (colname in self.columns):
            values = self.__rel.keep_columns([colname]).distinct().execute().fetch_all()
            for v in values:
                sql = 'SELECT * FROM ' + self.__rel.alias + ' WHERE "' + colname + '"' + '= \'' + str(v[0]) + '\''
                ds = DataSet(self.__rel.relation_from_query(sql), self.__map_fn)
                dataset_dict[v] = ds

        return dataset_dict

    def sort_by(self, cols: Union[str, int, List[Union[str, int]]], ascending: Optional[Union[bool, List[bool]]] = None) -> DataSet:
        """
        Sets a sorting criteria

        Parameters
        ----------
        cols: string, integer or a list of strings and/or integers
            Selects which columns to sort by, either through name or ordinal position.

        ascending: optional, boolean or list of booleans.
            Determines if the order is ascending (True) or descending (False). When set, 
            it should provide as many entries as in cols.  When unset, if defaults to 
            all ascending.

        """
        ci_cols = list(map(str.casefold, self.__rel.columns))
        if isinstance(cols, (str, int)):
            checkedOrder = True
            if ascending is not None:
                if not isinstance(ascending, bool):
                    raise ValueError("Order should be None or boolean.")
                checkedOrder = ascending
            cc = self.__check_col(cols, ci_cols)
            cc = f'"{cc}"'
            return DataSet(self.__rel.order([(cc, checkedOrder)]), self.__map_fn)

        if isinstance(cols, list):
            checkedOrder = []
            if ascending is None:
                checkedOrder = [True] * len(cols)
            elif isinstance(ascending, list):
                if len(ascending) != len(cols):
                    raise ValueError("Length of order should be the same as the length of cols")
                checkedOrder = ascending
            else:
                raise ValueError("Order should be None or a boolean list")

            ccs = [self.__check_col(cc, ci_cols) for cc in cols]
            pairs = list(zip(ccs, checkedOrder))
            return DataSet(self.__rel.order(pairs), self.__map_fn)

        raise ValueError("cols parameter should be a string or a list of strings.")

    def distinct(self, cols: Union[int, str, List[Union[int, str]]] = None) -> DataSet:
        """
        Returns distinct row values found in this dataset

        Parameters
        ----------
        cols: string, integer or a list of strings and/or integers
            Selects which combination of columns should be used in the operation.

        """
        if cols is not None:
            return self.select_columns(cols).distinct()

        return DataSet(self.__rel.distinct(), self.__map_fn)

    def cross_product(self, other: DataSet) -> DataSet:
        return DataSet(self.__rel.cross_product(other.__rel), self.__map_fn)

    def intersect(self, other: DataSet) -> DataSet:
        return DataSet(self.__rel.intersect(other.__rel), self.__map_fn)

    def minus(self, other: DataSet) -> DataSet:
        return DataSet(self.__rel.minus(other.__rel), self.__map_fn)

    def union(self, other: DataSet) -> DataSet:
        return DataSet(self.__rel.union(other.__rel), self.__map_fn)

    def to_csv(self, file: Union[str, Path],
               delimiter: Optional[str] = None,
               escape: str = '"',
               force_quote: List[str] = [],
               header: bool = True,
               null_string: str = "",
               quote: str = '"',
               date_format: Optional[str] = None,
               timestamp_format: Optional[str] = None,
               compression: Optional[CSVCodec] = None) -> None:
        """
        Materializes a relation and exports the results to a CSV file
        """

        # Check for $ and ~
        expanded = _resolveFile(str(file))
        path = Path(expanded)
        # Create dirs
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        # Check if tsv
        is_tsv = ".tsv" in path.suffix

        options = sn.CSVExportOptions()
        options.has_header = bool(header)
        options.quote = str(quote)
        options.escape = str(escape)
        options.null_string = null_string

        if len(force_quote) > 0:
            # Keep unset unless set with something
            options.force_quote = force_quote

        if delimiter is not None:
            # if given, set regardless of extension
            options.delimiter = str(delimiter)
        elif is_tsv:
            # if not given and tsv
            options.delimiter = "\t"
        else:
            # otherwise, plain old comma
            options.delimiter = ","

        if compression is not None:
            options.compression = compression

        if timestamp_format is not None:
            options.timestamp_format = timestamp_format

        if date_format is not None:
            options.date_format = date_format

        self.__rel.to_csv(str(path), options)

    def to_numpy(self) -> Dict[str, np.array]:
        return self.__rel.execute().to_numpy()

    def to_numpy_batch(self, max_rows: int) -> Generator[Dict[str, np.array], None, None]:
        r = self.__rel.execute()
        done = False
        first_col = None
        while not done:
            batch = r.to_numpy_batch(max_rows)
            if first_col is None:
                first_col = list(batch.keys())[0]
            done = len(batch) == 0 or len(batch[first_col]) < max_rows
            yield batch

    def to_pandas(self) -> pd.DataFrame:
        return self.__rel.execute().to_pandas()

    def to_pandas_batch(self, max_rows: int) -> Generator[pd.DataFrame, None, None]:
        r = self.__rel.execute()
        done = False
        while not done:
            batch = r.to_pandas_batch(max_rows)
            done = len(batch.index) < max_rows
            yield batch

    def to_arrow_table(self, blocks: int) -> pyarrow.lib.Table:
        """
        Returns the full result as a table made of chucks of size approx rowsInBatch
        """
        return self.__rel.execute().to_arrow_table(blocks)

    def to_arrow_record_batch_reader(self, blocks: int) -> pyarrow.lib.RecordBatchReader:
        """
        Returns an object that can be iterated to consume data in blocks.
        """
        return self.__rel.execute().to_arrow_record_batch_reader(blocks)

    def to_parquet(self, file: Union[str, Path], codec: ParquetCodec = ParquetCodec.SNAPPY) -> None:
        # Check for $ and ~
        expanded = _resolveFile(str(file))
        path = Path(expanded)
        # Create dirs
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        self.__rel.to_parquet(str(path), codec)

    def count(self) -> Optional[Tuple[int, ]]:
        """
        Returns the number of rows in this DataSet

        Notes
        -----
        This method forces the execution of this DataSet.

        """
        return self.__rel.count()

    def shape(self) -> Tuple[int, int]:
        """
        Returns the shape of this DataSet, as a tuple containing the number 
        of rows and the column count.

        Notes
        -----
        This method traverses the dataset to count the number of rows.

        """
        return (self.count(), len(self.columns))

    @property
    def alias(self) -> str:
        return self.__rel.alias

    @property
    def columns(self) -> List[str]:
        return self.__rel.columns

    @property
    def schema(self) -> Dict[str, Tuple[np.dtype, str]]:
        return self.__rel.dtypes

    def printSchema(self) -> None:
        objectType = np.dtype("O")
        print("root")
        for cname, value in self.__rel.dtypes.items():
            if value[0] == objectType:
                print(f" |-- {cname}: {value[0]} ({value[1]})")
            else:
                print(f" |-- {cname}: {value[0]}")

    def __len__(self) -> int:
        return self.__rel.count()

    def __tab(self, format: str = "plain") -> str:
        table = [["Column", "NumPy Type", "SQL Type"]]
        for cname, value in self.__rel.dtypes.items():
            table += [[cname, str(value[0]), value[1]]]
        return tabulate.tabulate(table, headers="firstrow", tablefmt=format)

    def _repr_pretty_(self, p, cycle) -> None:
        p.text(self.__tab("plain"))

    def _repr_html_(self) -> str:
        return self.__tab("html")

    def _repr_markdown_(self) -> str:
        return self.__tab("github")

    def _repr_latex_(self) -> str:
        return self.__tab("latex")


CSVCompression = Literal["None", "GZIP", "ZSTD"]


class SandBox:
    r"""
    A SandBox is an environment where data can be loaded, transformed, extracted and analysed.

    Sandboxes are created through the method `sandbox`.  SandBoxes instances should not be
    shared across threads, but it is perfectly safe to have one sandbox instance per thread
    pointing to the same environment.

    See Also
    --------
    sandbox: Creates new SandBox instances

    """

    __slots__ = ('__factory', '__map_fn', '__weakref__')

    def __init__(self, factory: sn.SandBoxConnection, map_fn: Callable[[sn.Relation], type]) -> None:
        self.__factory = factory
        self.__map_fn = map_fn

    def from_arrow(self, arrowObj: sn.ArrowObj) -> DataSet:
        if not isinstance(arrowObj, (pyarrow.Table, pyarrow.RecordBatchReader, pyarrow.dataset.FileSystemDataset, pyarrow.dataset.InMemoryDataset, pyarrow.dataset.Scanner)):
            raise ValueError(
                "Expected an arrow object of type Table, RecordBatchReader, FileSystemDataset, InMemoryDataset or Scanner")
        return DataSet(self.__factory.arrow(arrowObj), self.__map_fn)

    def from_pandas(self, df: pandas.DataFrame) -> DataSet:
        r"""
        Load a pandas dataset as a relation.
        """
        seen = set()
        replacements = dict()

        for ind, column in enumerate(df.columns):
            lowerColumn = column.lower()
            if lowerColumn in seen:
                replacements[column] = f"{column}_{ind}"
                warnings.warn(f"Column {column} renamed to {replacements[column]}")
            seen.add(lowerColumn)

        if len(replacements) > 0:
            return DataSet(self.__factory.pandas(df.rename(columns=replacements)), self.__map_fn)

        return DataSet(self.__factory.pandas(df), self.__map_fn)

    def from_csv(self, path: Union[str, Path],
                 *,
                 auto_detect: Optional[bool] = True,
                 hive_partitioning: Optional[bool] = False,
                 delimiter: Optional[str] = None, quote: Optional[str] = None,
                 escape: Optional[str] = None, has_header: Optional[bool] = None, null_string: Optional[str] = None,
                 date_format: Optional[str] = None, timestamp_format: Optional[str] = None,
                 sample_size: Optional[int] = None, skip_detection: Optional[bool] = None,
                 compression: Optional[CSVCompression] = None, include_filename: Optional[bool] = None,
                 skip_top_lines: Optional[int] = None) -> DataSet:
        r"""
        Imports a list of csv files as a Relation.

        All files must have the same schema.

        Parameters
        ----------
        path: str or Path, required
            Path to files to load.  It accepts either
            single string or aPath object.

            Use a string value when using wildcards in your path (`*`)
            to match a directory tree structure.  These paths may
            contain references to environment variables (`$var` or `${var}`)
            and home directory expressions (`~`).

            Use paths to specify valid and resoluble paths.

            Paths, either in string or Path object formats, should
            include the file pattern to load (ej: `*.csv`)

        auto_detect: Optional bool; defaults to True
            When set to True, `delimiter`, `quote`, `escape` and `header`
            options will be automatically inferred from the files.

        hive_partitioning: boll, Optional, defaults to False
            Path contains Hive expressions that should be incorporated into
            the loaded dataset.

        delimiter: Optional str
            Specifies the string that separates columns within each line of the file.

        quote: Optional str
            Specifies the quoting string to be used when a data value is quoted.

        escape: Optional str
            Specifies the string that should appear before a data character
            sequence that matches the quote value. The default is the same as
            the quote value (so that the quoting string is doubled if it
            appears in the data).

        has_header: Optional bool
            Specifies that the file contains a header line with the names of
            each column in the file.

        null_string: Optional str
            Specifies the string that represents a NULL value. The default is
            an empty string.

        date_format: Optional str
            Specifies the date format to use when parsing dates.  See the
            notes section.

        timestamp_format: Optional str
            Specifies the date format to use when parsing timestamps.  See
            the notes section.

        sample_size: Optional int
            Option to define number of sample rows for automatic CSV type
            detection.

        skip_detection: Optional bool
            Option to skip type detection for CSV parsing and assume all
            columns to be of type string.

        compression: Optional. One of 'None', 'GZIP', 'ZSTD'
            When not set, it will try automatic detection; otherwise, valid
            values should be none, gzip or zstd.

        include_filename: Optional bool
            Adds an additional column whose value is the file name

        skip_top_lines: Optional int
            The number of lines at the top of the file to skip.

        Notes
        -----
        The following table outlines the different options for parsing `dateFormat` and
        `timestampFormat`:

        +-----------+------------------------------------------------------------------+
        | Specifier | Description                                                      |
        +===========+==================================================================+
        | %a        | Abbreviated weekday name.                                        |
        +-----------+------------------------------------------------------------------+
        | %A        | Full weekday name.                                               |
        +-----------+------------------------------------------------------------------+
        | %w        | Weekday as a decimal number.                                     |
        +-----------+------------------------------------------------------------------+
        | %d        | Day of the month as a zero-padded decimal.                       |
        +-----------+------------------------------------------------------------------+
        | %-d       | Day of the month as a decimal number.                            |
        +-----------+------------------------------------------------------------------+
        | %b        | Abbreviated month name.                                          |
        +-----------+------------------------------------------------------------------+
        | %B        | Full month name.                                                 |
        +-----------+------------------------------------------------------------------+
        | %m        | Month as a zero-padded decimal number.                           |
        +-----------+------------------------------------------------------------------+
        | %-m       | Month as a decimal number.                                       |
        +-----------+------------------------------------------------------------------+
        | %y        | Year without century as a zero-padded decimal number.            |
        +-----------+------------------------------------------------------------------+
        | %-y       | Year without century as a decimal number.                        |
        +-----------+------------------------------------------------------------------+
        | %Y        | Year with century as a decimal number.                           |
        +-----------+------------------------------------------------------------------+
        | %H        | Hour (24-hour clock) as a zero-padded decimal number.            |
        +-----------+------------------------------------------------------------------+
        | %-H       | Hour (24-hour clock) as a decimal number.                        |
        +-----------+------------------------------------------------------------------+
        | %I        | Hour (12-hour clock) as a zero-padded decimal number.            |
        +-----------+------------------------------------------------------------------+
        | %-I       | Hour (12-hour clock) as a decimal number.                        |
        +-----------+------------------------------------------------------------------+
        | %p        | Locale's AM or PM.                                               |
        +-----------+------------------------------------------------------------------+
        | %M        | Minute as a zero-padded decimal number.                          |
        +-----------+------------------------------------------------------------------+
        | %-M       | Minute as a decimal number.                                      |
        +-----------+------------------------------------------------------------------+
        | %S        | Second as a zero-padded decimal number.                          |
        +-----------+------------------------------------------------------------------+
        | %-S       | Second as a decimal number.                                      |
        +-----------+------------------------------------------------------------------+
        | %g        | Millisecond as a decimal number, zero-padded on the left.        |
        +-----------+------------------------------------------------------------------+
        | %f        | Microsecond as a decimal number, zero-padded on the left.        |
        +-----------+------------------------------------------------------------------+
        | %z        | UTC offset in the form +HHMM or -HHMM.                           |
        +-----------+------------------------------------------------------------------+
        | %Z        | Time zone name.                                                  |
        +-----------+------------------------------------------------------------------+
        | %j        | Day of the year as a zero-padded decimal number.                 |
        +-----------+------------------------------------------------------------------+
        | %-j       | Day of the year as a decimal number.                             |
        +-----------+------------------------------------------------------------------+
        | %U        | Week number of the year (Sunday as the first day of the week).   |
        +-----------+------------------------------------------------------------------+
        | %W        | Week number of the year (Monday as the first day of the week).   |
        +-----------+------------------------------------------------------------------+
        | %c        | ISO date and time representation.                                |
        +-----------+------------------------------------------------------------------+
        | %x        | ISO date representation.                                         |
        +-----------+------------------------------------------------------------------+
        | %X        | ISO time representation.                                         |
        +-----------+------------------------------------------------------------------+
        | %%        | A literal '%' character.                                         |
        +-----------+------------------------------------------------------------------+
        """

        options = sn.CSVImportOptions()
        options.auto_detect = auto_detect
        options.hive_partitioning = hive_partitioning
        options.delimiter = delimiter
        options.quote = quote
        options.escape = escape
        options.has_header = has_header
        options.null_string = null_string
        options.date_format = date_format
        options.timestamp_format = timestamp_format
        options.sample_size = sample_size
        options.skip_detection = skip_detection
        options.compression = None if compression is None else compression.lower()
        options.include_filename = include_filename
        options.skip_top_lines = skip_top_lines

        file_expression = path
        if isinstance(path, str):
            file_expression = _resolveFile(path)
        elif isinstance(path, Path):
            file_expression = str(path.resolve())
        else:
            raise ValueError(f"[{path}] didn't resolve any files")

        return DataSet(self.__factory.csv(file_expression, options), self.__map_fn)

    def from_parquet(self,
                     paths: Union[str, Path, List[Union[str, Path]]],
                     *,
                     binary_string: Optional[bool] = False,
                     hive_partitioning: Optional[bool] = False,
                     include_filename: Optional[bool] = False) -> DataSet:
        r"""
        Mounts parquet files

        Parameters
        ----------
        paths: str or Path or a list of str or Paths, required
            Paths to parquet files to load.  It accepts either
            single string or Path objects or a list of them.

            Use a string value when using wildcards in your path (`*`)
            to match a directory tree structure.  These paths may
            contain references to environment variables (`$var` or `${var}`)
            and home directory expressions (`~`).

            Use paths to specify valid and resoluble paths.

            Paths, either in string or Path object formats, should
            include the file pattern to load (ej: `*.parquet`)

        binary_string: boolean, optional, defaults to False
            Treat binary data as strings

        hive_partitioning: boolean, optional, defaults to False
            The directories in paths include Hive expressions that
            should be incorporated into the loaded dataset.

        include_filename: boolean, optional, defaults to False
            When set to true, an additional column will be included
            in the loaded dataset, with the path to the file
            where the data was loaded.
        """
        options = sn.ParquetImportOptions()
        options.binary_string = binary_string
        options.hive_partitioning = hive_partitioning
        options.include_filename = include_filename

        files = []
        if isinstance(paths, (str, Path)):
            files.append(paths)
        elif isinstance(paths, list):
            files = paths.copy()

        files = [_resolveFile(p) if isinstance(p, str) else str(p.resolve()) for p in files]

        return DataSet(self.__factory.parquet(files, options), self.__map_fn)

    def map(self, *genExpr: types.GeneratorType) -> DataSet:
        query = mustang.make_query(genExpr, frame_depth=1, left_join=False)
        sql = mustang.construct_sql_from_query(query)
        return DataSet(self.__factory.relation_from_query(sql), self.__map_fn)

    def from_sql(self, sql: str) -> DataSet:
        r"""
        Returns a Dataset from raw SQL query

        Parameters
        ----------
        sql: str with SQL query in raw format

        """

        return DataSet(self.__factory.relation_from_query(sql), self.__map_fn)

    def load_test_data(self) -> DataSet:
        """
        This function creates a shapelets dataframe with de iris dataset data.
        """
        this_directory = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        data = self.from_csv(
            this_directory / 'iris.csv',
            has_header=False)
        return data.rename_columns(
            {0: 'Sepal_Length', 1: 'Sepal_Width', 2: 'Petal_Length', 3: 'Petal_Width', 4: 'Class'}
        )


_open_handles = WeakValueDictionary()
_open_sandboxes = WeakValueDictionary()


def sandbox(file: Optional[str] = None) -> SandBox:
    """
    Factory method for SandBox instances.

    It validates parameters and ensures a local catalogue of
    SandBoxes and connections per thread are kept to minimise
    the likelihood of threading issues.

    Parameters
    ----------
    file: str, optional; defaults to None
        When set, this parameter should point to a file where
        the SandBox may store its data.  When left unset (default
        behaviour) the SandBox will operate in memory.

    """
    resolved = None if file is None else _resolveFile(file)
    threadId = get_ident()
    clientId = (resolved, threadId)

    if clientId in _open_sandboxes:
        return _open_sandboxes[clientId]

    handle = None
    if resolved not in _open_handles:
        handle = sn.SandBox(file, False, None, [])
        _open_handles[resolved] = handle
    else:
        handle = _open_handles[resolved]

    map_fn = mustang.relation_to_python()

    sandBox = SandBox(handle.connect(), map_fn)
    _open_sandboxes[clientId] = sandBox
    return sandBox
