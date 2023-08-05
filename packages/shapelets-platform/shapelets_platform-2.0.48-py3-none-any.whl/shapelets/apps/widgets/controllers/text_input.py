from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import Tuple, Optional, Union

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class TextInput(StateControl):
    value: Optional[Union[str, int, float]] = None
    title: Optional[str] = None
    text_style: Optional[dict] = None
    markdown: Optional[bool] = None
    placeholder: Optional[str] = None
    multiline: Optional[bool] = None
    toolbar: Optional[bool] = None

    def from_string(self, string: str) -> TextInput:
        self.value = string
        return self

    def to_string(self) -> str:
        return str(self.value)

    def from_int(self, number: int) -> TextInput:
        self.value = number
        return self

    def to_int(self) -> int:
        return int(self.value)

    def from_float(self, number: float) -> TextInput:
        self.value = number
        return self

    def to_float(self) -> float:
        return float(self.value)

    def to_dict_widget(self, text_input_dict: dict = None):
        if text_input_dict is None:
            text_input_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: TextInput.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.value is not None:
            if isinstance(self.value, (str, int, float)):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.value,
                })
            elif isinstance(self.value, Widget):
                target = {"id": self.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Value should be string, int, float or another widget")

        if self.title is not None:
            if isinstance(self.title, str):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.text_style is not None:
            if isinstance(self.text_style, dict):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TEXT_STYLE.value: self.text_style
                })

        if self.markdown is not None:
            if isinstance(self.markdown, bool):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MARKDOWN.value: self.markdown
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Markdown should be boolean")

        if self.placeholder is not None:
            if isinstance(self.placeholder, str):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.PLACEHOLDER.value: self.placeholder
                })
            elif isinstance(self.placeholder, Widget):
                target = {"id": self.placeholder.widget_id, "target": AttributeNames.PLACEHOLDER.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Placeholder should be a string or another widget")

        if self.multiline is not None:
            if isinstance(self.multiline, bool):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MULTI_LINE.value: self.multiline
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Multiline value should be a boolean")

        if self.toolbar is not None:
            if isinstance(self.multiline, bool):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TOOLBAR.value: self.toolbar
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Multiline value should be a boolean")

        if _widget_providers:
            self.add_widget_providers(text_input_dict, _widget_providers)

        return text_input_dict


class TextInputWidget(TextInput, Widget):

    def __init__(self,
                 value: Optional[Union[str, int, float]] = None,
                 title: Optional[str] = None,
                 text_style: Optional[dict] = None,
                 markdown: Optional[bool] = None,
                 placeholder: Optional[str] = None,
                 multiline: Optional[bool] = None,
                 toolbar: Optional[bool] = None,
                 **additional):
        Widget.__init__(self, TextInput.__name__, **additional)
        TextInput.__init__(self, value=value, title=title, text_style=text_style, markdown=markdown,
                           placeholder=placeholder, multiline=multiline, toolbar=toolbar)
        self._parent_class = self.widget_type = TextInput.__name__
        self._compatibility: Tuple = (str.__name__, TextInput.__name__)

    def to_dict_widget(self):
        text_input_dict = Widget.to_dict_widget(self)
        text_input_dict = TextInput.to_dict_widget(self, text_input_dict)
        return text_input_dict
