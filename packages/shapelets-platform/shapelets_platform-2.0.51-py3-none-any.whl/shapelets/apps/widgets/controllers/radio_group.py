from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple, Union

from .selector import Selector, SelectorWidget


@dataclass
class RadioGroup(Selector):
    value: Optional[Union[int, float, str, any]] = None

    def from_List(self, input_list: List) -> RadioGroup:
        self.value = input_list
        return self

    def _check_value(self):
        pass


class RadioGroupWidget(RadioGroup, SelectorWidget):

    def __init__(self,
                 options: List = [],
                 title: str = None,
                 label_by: str = None,
                 value_by: str = None,
                 value: Union[int, float, str, any] = None,
                 **additional):
        SelectorWidget.__init__(self, options, title, None, label_by, value_by, value, **additional)
        RadioGroup.__init__(self, options=options, title=title, label_by=label_by, value_by=value_by, value=value)

        self._parent_class = self.widget_type = RadioGroup.__name__
        self._compatibility: Tuple = (str.__name__, int.__name__, float.__name__, list.__name__,
                                      List._name, RadioGroup.__name__)
