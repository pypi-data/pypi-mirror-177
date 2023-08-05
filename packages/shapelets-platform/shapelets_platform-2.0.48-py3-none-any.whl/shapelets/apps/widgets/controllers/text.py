from __future__ import annotations

import datetime
import uuid

from dataclasses import dataclass
from typing import Optional, Tuple, Union

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Text(StateControl):
    value: Optional[Union[str, int, float]] = None
    title: Optional[str] = None
    text_style: Optional[dict] = None
    markdown: Optional[bool] = None

    def from_string(self, string: str) -> Text:
        self.value = string
        return self

    def to_string(self) -> str:
        return str(self.value)

    def from_int(self, number: int) -> Text:
        self.value = number
        return self

    def to_int(self) -> int:
        return int(self.value)

    def from_float(self, number: float) -> Text:
        self.value = number
        return self

    def to_float(self) -> float:
        return float(self.value)

    @staticmethod
    def from_date_time(dt: datetime.datetime) -> Text:
        return Text(value=str(dt.date))

    def to_dict_widget(self, text_dict: dict = None):
        if text_dict is None:
            text_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: Text.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.value is not None:
            if isinstance(self.value, (str, int, float)):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: str(self.value),
                })
            elif isinstance(self.value, Widget):
                target = {"id": self.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Value should be string, int, float or another widget")

        if self.title is not None:
            if isinstance(self.title, str):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.text_style is not None:
            if isinstance(self.text_style, dict):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TEXT_STYLE.value: self.text_style
                })

        if self.markdown is not None:
            if isinstance(self.markdown, bool):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MARKDOWN.value: self.markdown
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Markdown should be boolean")

        if _widget_providers:
            self.add_widget_providers(text_dict, _widget_providers)

        return text_dict


class TextWidget(Text, Widget):

    def __init__(self,
                 value: Optional[Union[str, int, float]] = None,
                 title: Optional[str] = None,
                 text_style: Optional[dict] = None,
                 markdown: Optional[bool] = False,
                 **additional):
        Widget.__init__(self, Text.__name__, **additional)
        Text.__init__(self, value=value, title=title, text_style=text_style, markdown=markdown)
        self._parent_class = Text.__name__
        self._compatibility: Tuple = (str.__name__, int.__name__, float.__name__, Text.__name__)

    def to_dict_widget(self):
        text_dict = Widget.to_dict_widget(self)
        text_dict = Text.to_dict_widget(self, text_dict)
        return text_dict
