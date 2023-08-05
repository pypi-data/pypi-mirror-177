import uuid

from dataclasses import dataclass
from typing import Optional, Tuple

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Checkbox(StateControl):
    title: Optional[str] = None
    checked: Optional[bool] = None
    toggle: Optional[bool] = None

    def to_dict_widget(self, checkbox_dict: dict = None):
        if checkbox_dict is None:
            checkbox_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: Checkbox.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        _widget_providers = []
        if self.title is not None:
            if isinstance(self.title, str):
                checkbox_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        if self.checked is not None:
            if isinstance(self.checked, bool):
                checkbox_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.CHECKED.value: self.checked
                })
            else:
                raise ValueError(f"Unexpected type {type(self.checked)} in checked")

        if self.toggle is not None:
            if isinstance(self.toggle, bool):
                checkbox_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TOGGLE.value: self.toggle
                })
            else:
                raise ValueError(f"Unexpected type {type(self.toggle)} in toggle")

        return checkbox_dict


class CheckboxWidget(Widget, Checkbox):

    def __init__(self,
                 title: Optional[str] = None,
                 checked: Optional[bool] = None,
                 toggle: Optional[bool] = None,
                 **additional
                 ):
        Widget.__init__(self, Checkbox.__name__, **additional)
        Checkbox.__init__(self, title=title, checked=checked, toggle=toggle)
        self._parent_class = Checkbox.__name__
        self._compatibility: Tuple = (Checkbox.__name__,)

    def to_dict_widget(self):
        checkbox_dict = Widget.to_dict_widget(self)
        checkbox_dict = Checkbox.to_dict_widget(self, checkbox_dict)
        return checkbox_dict
