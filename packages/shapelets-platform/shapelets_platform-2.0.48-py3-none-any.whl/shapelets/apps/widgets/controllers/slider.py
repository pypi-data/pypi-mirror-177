from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from ..widget import AttributeNames, StateControl, Widget


@dataclass
class Slider(StateControl):
    title: str = None
    value: Union[str, int, float, List[int], List[float], List[str]] = None
    min_value: Union[int, float] = None
    max_value: Union[int, float] = None
    step: Union[int, float] = None
    range: Optional[bool] = None
    options: Union[List, dict] = None

    def __post_init__(self):
        if self.value is not None:
            self._check_value()
            self._check_list()
        elif self.value is None and self.min_value is not None:
            self.value = self.min_value

        if self.options is not None and self.min_value is None and self.max_value is None:
            self.min_value = 0
            self.max_value = len(self.options) - 1

        if self.value is not None and self.options is not None:
            # Adjust value to match options
            if isinstance(self.value, List):
                new_values = []
                if isinstance(self.options, List):
                    for value in self.value:
                        for i, option in enumerate(self.options):
                            if option == value:
                                new_values.append(i)
                self.value = new_values
            else:
                if isinstance(self.options, List):
                    for i, option in enumerate(self.options):
                        if option == self.value:
                            self.value = i

    def from_int(self, number: int) -> Slider:
        self.value = number
        self._check_value()
        return self

    def to_int(self) -> int:
        if isinstance(self.value, int) or isinstance(self.value, float):
            return int(self.value)
        else:
            raise ValueError("Slider self.value cannot convert to int")

    def from_float(self, number: float) -> Slider:
        self.value = number
        self._check_value()
        return self

    def to_float(self) -> float:
        if isinstance(self.value, int) or isinstance(self.value, float):
            return float(self.value)
        else:
            raise ValueError("Slider self.value cannot convert to float")

    def from_string(self, number: str) -> Slider:
        self.value = number
        self._check_value()
        return self

    def to_str(self) -> str:
        if isinstance(self.value, str):
            return self.value
        else:
            raise ValueError("Slider self.value type is not a string, conversion is not possible")

    def from_list(self, input_list: List) -> Slider:
        self.value = input_list
        self._check_list()
        return self

    def to_List(self) -> List:
        if isinstance(self.value, List):
            return self.value
        else:
            raise ValueError("Slider self.value type is not a List, conversion is not possible")

    def _check_value(self):
        # if isinstance(self.value, int):
        #     # if value is int and min_value is None, set min_value to 1
        #     # if value is int and max_value is None, set max_value to 100
        #     # if value is int and step is None, set step to 1

        #     if self.min_value is None:
        #         self.min_value = 0

        #     if self.max_value is None:
        #         self.max_value = 100

        #     if self.step is None:
        #         self.step = 1

        # if isinstance(self.value, float):
        #     # if value is float and min_value is None, set min_value to 0.0
        #     # if value is float and max_value is None, set max_value to 1.0
        #     # if value is float and step is None, set step to 0.01

        #     if self.min_value is None:
        #         self.min_value = 0.0

        #     if self.max_value is None:
        #         self.max_value = 1.0

        #     if self.step is None:
        #         self.step = 0.01

        if isinstance(self.value, int) or isinstance(self.value, float):
            if (self.min_value is not None and self.max_value is not None):
                if (self.min_value >= self.max_value):
                    raise ValueError("Property min_value cannot be equal or bigger than max_value")

            if (self.max_value is not None and self.step is not None):
                if (self.step != 0):
                    if (self.max_value - self.min_value) % self.step != 0:
                        raise ValueError("The (max_value-min_value) value should be divisible by the step value")
                else:
                    raise ValueError("step property cannot be zero")

        if isinstance(self.value, str):
            if self.value not in self.options:
                raise ValueError("Property value is not found in options")

        if isinstance(self.value, List):
            self.range = True

    def _check_list(self):
        if isinstance(self.value, List):
            if (len(self.value) != 2):
                raise Exception("Value list property must contain exactly two elements to configure a slider range")
            else:
                if ((isinstance(self.value[0], int) and isinstance(self.value[1], int)) or
                        (isinstance(self.value[0], float) and isinstance(self.value[1], float))):
                    if (self.value[0] >= self.value[1]):
                        raise Exception("First element of list value must be lower than the second one")
                elif isinstance(self.value[0], str) and isinstance(self.value[1], str):
                    if (self.value[0] not in self.options or self.value[1] not in self.options):
                        raise Exception("Elements from value list must be included in options list property")
                    else:
                        idx0 = self.options.index(self.value[0])
                        idx1 = self.options.index(self.value[1])
                        if (idx0 >= idx1):
                            raise Exception(
                                "Value list property: options index of first element must be lower than the second one")

    def to_dict_widget(self, slider_dict: dict = None):
        if slider_dict is None:
            slider_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: Slider.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.title is not None:
            if isinstance(self.title, str):
                slider_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.value is not None:
            if isinstance(self.value, int) \
                    or isinstance(self.value, float) \
                    or isinstance(self.value, str) \
                    or isinstance(self.value, List):
                slider_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.value
                })
            elif isinstance(self.value, Widget):
                target = {"id": self.value.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Value should be a string, int, float or another widget")

        if self.min_value is not None:
            if isinstance(self.min_value, int) or isinstance(self.min_value, float):
                slider_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MIN.value: self.min_value
                })
            elif isinstance(self.min_value, Widget):
                target = {"id": self.min_value.widget_id, "target": AttributeNames.MIN.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Min value should be int, float or another widget")

        if self.max_value is not None:
            if isinstance(self.max_value, int) or isinstance(self.max_value, float):
                slider_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MAX.value: self.max_value
                })
            elif isinstance(self.max_value, Widget):
                target = {"id": self.max_value.widget_id, "target": AttributeNames.MAX.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Max value should be int, float or another widget")

        if self.step is not None:
            if isinstance(self.step, int) or isinstance(self.step, float):
                slider_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.STEP.value: self.step
                })
            elif isinstance(self.step, Widget):
                target = {"id": self.step.widget_id, "target": AttributeNames.STEP.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Step value should be int, float or another widget")

        if self.range is not None:
            if isinstance(self.range, bool):
                slider_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.RANGE.value: self.range
                })
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Range value should be a boolean")

        if self.options is not None:
            if isinstance(self.options, dict):
                slider_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.OPTIONS.value: self.options
                })

            elif isinstance(self.options, List):
                # Adjust list of lists to dict
                # Adjust values in case there is a min value, otherwise 0 will be the first
                initial_count = 0
                if self.min_value is not None:
                    initial_count = self.min_value
                slider_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.OPTIONS.value: {i + initial_count: option for i, option in enumerate(self.options)}
                })
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Options should be a list or a dict")

        if _widget_providers:
            self.add_widget_providers(slider_dict, _widget_providers)

        return slider_dict


class SliderWidget(Slider, Widget):
    def __init__(self,
                 title: str = None,
                 value: Union[str, int, float, List[int], List[float], List[str]] = None,
                 min_value: Union[int, float] = None,
                 max_value: Union[int, float] = None,
                 step: Union[int, float] = None,
                 range: Optional[bool] = None,
                 options: Union[List, dict] = None,
                 **additional):
        Widget.__init__(self, Slider.__name__, **additional)
        Slider.__init__(self, title=title, value=value, min_value=min_value, max_value=max_value, step=step,
                        range=range, options=options)
        self._parent_class = Slider.__name__
        self._compatibility: Tuple = (Slider.__name__, int.__name__, float.__name__)

    def to_dict_widget(self):
        slider_dict = Widget.to_dict_widget(self)
        slider_dict = Slider.to_dict_widget(self, slider_dict)
        return slider_dict
