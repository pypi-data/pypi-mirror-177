from __future__ import annotations

import uuid

from dataclasses import dataclass, field
from typing import Optional, Tuple, Union

from ...data_app_utils import TextStyle
from ..widget import AttributeNames, Widget, StateControl


@dataclass
class NumberInput(StateControl):
    title: Optional[str] = None
    value: Optional[Union[int, float]] = None
    default_value: Optional[Union[int, float]] = None
    placeholder: Optional[str] = None
    min: Optional[Union[int, float]] = None
    max: Optional[Union[int, float]] = None
    step: Optional[Union[int, float]] = None
    text_style: Optional[TextStyle] = field(default_factory=lambda: TextStyle())
    units: Optional[str] = None

    def __post_init__(self):
        self.placeholder = "Place your number here" if self.placeholder is None else self.placeholder
        if (self.value is not None):
            self._check_value()
            if (self.max is not None and self.min is not None):
                if (self.max < self.min):
                    raise ValueError("Max value cannot be lower than min")

                if (self.value < self.min or self.value > self.max):
                    raise ValueError("Value must be between min and max")

                if (self.default_value is not None):
                    if (self.default_value < self.min or self.default_value > self.max):
                        raise ValueError("Default value must be between min and max")

    def from_int(self, number: int) -> NumberInput:
        self.value = number
        return self

    def to_int(self) -> int:
        return int(self.value)

    def from_float(self, number: float) -> NumberInput:
        self.value = number
        return self

    def to_float(self) -> float:
        return float(self.value)

    def _check_value(self):

        if (self.value is not None and self.max is not None and self.min is not None):
            if isinstance(self.value, int) or isinstance(self.value, float):
                if (self.max < self.min):
                    raise ValueError("min property cannot be bigger than max")

                if (self.step is not None):
                    if (self.step != 0):
                        if (self.max - self.min) % self.step != 0:
                            raise ValueError("The (max-min) value should be divisible by the step value")
                    else:
                        raise ValueError("step property cannot be zero")

    def to_dict_widget(self, number_dict: dict = None):
        if number_dict is None:
            number_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: NumberInput.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []
        if self.value is not None:
            if isinstance(self.value, (int, float)):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.value
                })
            elif isinstance(self.value, Widget):
                target = {"id": self.value.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.value}: value should be int, flot or another widget")

        if self.title is not None:
            if isinstance(self.title, str):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be string or another widget")

        if self.max is not None:
            if isinstance(self.max, (int, float)):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MAX.value: self.max
                })
            elif isinstance(self.max, Widget):
                target = {"id": self.max.widget_id, "target": AttributeNames.MAX.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Max value should be int, flot or another widget")

        if self.min is not None:
            if isinstance(self.min, (int, float)):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MIN.value: self.min
                })
            elif isinstance(self.min, Widget):
                target = {"id": self.min.widget_id, "target": AttributeNames.MIN.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Min value should be int, flot or another widget")

        if self.step is not None:
            if isinstance(self.step, (int, float)):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.STEP.value: self.step
                })
            elif isinstance(self.step, Widget):
                target = {"id": self.step.widget_id, "target": AttributeNames.STEP.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Step value should be int, flot or another widget")

        if self.placeholder is not None:
            if isinstance(self.placeholder, str):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.PLACEHOLDER.value: self.placeholder
                })
            elif isinstance(self.placeholder, Widget):
                target = {"id": self.placeholder.widget_id, "target": AttributeNames.PLACEHOLDER.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Placeholder should be string or another widget")

        if self.text_style is not None:
            if isinstance(self.text_style, dict):
                for key, value in self.text_style.items():
                    number_dict[AttributeNames.PROPERTIES.value].update({
                        key: value
                    })

        if self.units is not None:
            if isinstance(self.units, str):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.UNITS.value: self.units
                })
            elif isinstance(self.units, Widget):
                target = {"id": self.units.widget_id, "target": AttributeNames.UNITS.value}
                _widget_providers.append(target)

        if _widget_providers:
            self.add_widget_providers(number_dict, _widget_providers)

        return number_dict


class NumberInputWidget(Widget, NumberInput):
    def __init__(self,
                 title: Optional[str] = None,
                 value: Optional[Union[int, float]] = None,
                 default_value: Optional[Union[int, float]] = None,
                 placeholder: Optional[str] = None,
                 min: Optional[Union[int, float]] = None,
                 max: Optional[Union[int, float]] = None,
                 step: Optional[Union[int, float]] = None,
                 text_style: Optional[dict] = None,
                 units: Optional[str] = None,
                 **additional):
        # TODO: Should fail if text_style contains weird keys
        if text_style:
            text_style: TextStyle = text_style
        Widget.__init__(self, NumberInput.__name__, **additional)
        NumberInput.__init__(self, title=title, value=value, default_value=default_value, placeholder=placeholder,
                             min=min, max=max, step=step, text_style=text_style, units=units)
        self._parent_class = NumberInput.__name__
        self._compatibility: Tuple = (int.__name__, float.__name__, NumberInput.__name__)

    def to_dict_widget(self):
        number_dict = Widget.to_dict_widget(self)
        number_dict = NumberInput.to_dict_widget(self, number_dict)
        return number_dict
