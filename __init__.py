import os
import ctypes
from xml.etree import ElementTree
from gremlin.base_classes import AbstractAction, AbstractFunctor
from gremlin.common import InputType
import gremlin.plugin_manager
import gremlin.ui.input_item
from PySide6 import QtWidgets

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

def press_key(key_code):
    user32 = ctypes.windll.user32
    user32.keybd_event(key_code, 0, 0, 0)
    user32.keybd_event(key_code, 0, 2, 0)

class VolumeControlWidget(gremlin.ui.input_item.AbstractActionWidget):
    """UI widget for the VolumeControl action."""

    def __init__(self, action_data, parent=None):
        super().__init__(action_data, parent=parent)
        self.action_data = action_data

    def _create_ui(self):
        """Creates the UI components."""
        self.action_combobox = QtWidgets.QComboBox()
        self.action_combobox.addItems(["Volume Up", "Volume Down", "Mute"])
        self.main_layout.addWidget(self.action_combobox)
        self.action_combobox.setCurrentText(self.action_data.action)
        self.action_combobox.currentTextChanged.connect(self._action_changed)

    def _populate_ui(self):
        """Populates the UI components."""
        self.action_combobox.setCurrentText(self.action_data.action)

    def _action_changed(self, value):
        self.action_data.action = value
        self.action_modified.emit()

class VolumeControlFunctor(AbstractFunctor):
    """Executes the volume control action when called."""

    def __init__(self, action):
        super().__init__(action)
        self.action = action.action

    def process_event(self, event, value):
        if event.is_pressed:
            if self.action == "Volume Up":
                press_key(VK_VOLUME_UP)
            elif self.action == "Volume Down":
                press_key(VK_VOLUME_DOWN)
            elif self.action == "Mute":
                press_key(VK_VOLUME_MUTE)
        return True

class VolumeControlAction(AbstractAction):
    """Action data for the volume control action."""

    name = "Volume Control"
    tag = "volume_control"

    default_button_activation = (True, True)
    input_types = [InputType.JoystickButton]

    functor = VolumeControlFunctor
    widget = VolumeControlWidget

    def icon(self):
        return f"{os.path.dirname(os.path.realpath(__file__))}/icon.png"

    def __init__(self, parent):
        super().__init__(parent)
        self.action = "Volume Up"

    def _parse_xml(self, node):
        self.action = node.get("action", "Volume Up")

    def _generate_xml(self):
        node = ElementTree.Element(self.tag)
        node.set("action", self.action)
        return node

    def _is_valid(self):
        return True

    def requires_virtual_button(self):
        """Indicates whether this action requires a virtual button."""
        return False

version = 1
name = "volume_control"
create = VolumeControlAction