from typing import List

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from cilissa.utils import get_parameter_display_name
from cilissa_gui.managers import OperationsManager
from cilissa_gui.widgets import CQOperationItem
from cilissa_gui.widgets.inputs import get_input_widget_for_type


class PropertiesBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Properties")

        self.main_layout = QVBoxLayout()

        self.properties = Properties()

        self.main_layout.addWidget(self.properties)
        self.setLayout(self.main_layout)


class Properties(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()

        self.properties_unselected = PropertiesUnselected(self)
        self.properties_selected = PropertiesSelected(self)

        self.addWidget(self.properties_unselected)
        self.addWidget(self.properties_selected)

    @Slot(QWidget)
    def open_selection(self, item: QWidget) -> None:
        self.properties_selected.remove_all_widgets_from_layout(self.properties_selected.inputs_layout)
        self.properties_selected.remove_all_widgets_from_layout(self.properties_selected.buttons_layout)
        self.properties_selected.clear_instance()
        self.properties_selected.create_instance_widgets(item)
        self.setCurrentWidget(self.properties_selected)

    @Slot()
    def hide_selection(self) -> None:
        self.setCurrentWidget(self.properties_unselected)


class PropertiesSelected(QWidget):
    def __init__(self, parent: QStackedWidget) -> None:
        super().__init__(parent)

        self.main_layout = QVBoxLayout()

        self.operations_manager = OperationsManager()

        self.clear_instance()

        self.inputs_layout = QVBoxLayout()
        self.inputs_layout.setAlignment(Qt.AlignTop)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignBottom)

        self.main_layout.addLayout(self.inputs_layout)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

    def create_instance_widgets(self, item: QWidget) -> None:
        if isinstance(item, CQOperationItem):
            # Item from Explorer
            add = True
            self.instance = item.operation()
            self.create_properties_widgets()
        elif isinstance(item, QListWidgetItem):
            # Item from Operations
            add = False
            row = [index.row() for index in item.listWidget().selectedIndexes()][-1]
            self.instance = self.operations_manager[row]
            self.create_properties_widgets()
        else:
            raise TypeError("This slot expects items from the Explorer widget")

        self.create_buttons(add)

    def create_properties_widgets(self) -> None:
        properties = self.instance.get_parameters_dict()
        if not properties:
            info = QLabel("Chosen operation has no configurable parameters")
            info.setStyleSheet("QLabel { color: darkgray; }")
            info.setWordWrap(True)
            info.setAlignment(Qt.AlignCenter)
            self.inputs_layout.addWidget(info)
            return

        for key, value in properties.items():
            key_type, optional = self.instance.get_parameter_type(key)
            widget_class = get_input_widget_for_type(key_type)
            if widget_class:
                widget = widget_class(
                    label=get_parameter_display_name(key), parameter=key, default=value, optional=optional
                )
                self.widgets.append(widget)
                self.inputs_layout.addWidget(widget)

    def remove_all_widgets_from_layout(self, layout: QLayout) -> None:
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                # Remove it from the layout list
                layout.removeWidget(widget)
                # Remove it from the GUI
                widget.setParent(None)

    def create_buttons(self, add: bool) -> None:
        if add:
            apply_button = QPushButton("Add")
            apply_button.clicked.connect(lambda: self.set_instance_values(add=True))
        else:
            apply_button = QPushButton("Apply")
            apply_button.clicked.connect(lambda: self.set_instance_values(add=False))

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.parent().hide_selection)

        self.buttons_layout.addWidget(apply_button)
        self.buttons_layout.addWidget(cancel_button)

    def clear_instance(self) -> None:
        self.widgets: List[QWidget] = []
        self.instance = None

    def set_instance_values(self, add: bool) -> None:
        for widget in self.widgets:
            parameter = widget.parameter
            value = widget.get_value()
            self.instance.set_parameter(parameter, value)

        if add:
            self.operations_manager.push(self.instance)
            self.operations_manager.changed.emit()


class PropertiesUnselected(QWidget):
    def __init__(self, parent: QStackedWidget) -> None:
        super().__init__(parent)

        self.main_layout = QVBoxLayout()

        self.no_selection_text = QLabel("Select a metric or transformation to configure its properties")
        self.no_selection_text.setStyleSheet("QLabel { color: darkgray; }")
        self.no_selection_text.setWordWrap(True)
        self.no_selection_text.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.no_selection_text)
        self.setLayout(self.main_layout)
