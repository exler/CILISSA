from typing import Union

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from cilissa_gui.widgets import CQImage, CQOperation


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

        self.properties_unselected = PropertiesUnselected()
        self.properties_selected = PropertiesSelected()

        self.addWidget(self.properties_unselected)
        self.addWidget(self.properties_selected)

    @Slot(QWidget)
    def open_selection(self, item: QWidget) -> None:
        self.properties_selected.fill_widget_with_properties(item)
        self.setCurrentWidget(self.properties_selected)

    @Slot()
    def hide_selection(self) -> None:
        self.setCurrentWidget(self.properties_unselected)


class PropertiesSelected(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.inputs = []

        self.add_button = QPushButton("Add")
        self.cancel_button = QPushButton("Cancel")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.setAlignment(Qt.AlignBottom)

        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

    def fill_widget_with_properties(self, item: QWidget) -> None:
        if isinstance(item, CQImage):
            # There is no functionality planned for image properties right now
            return
        elif isinstance(item, CQOperation):
            operation = item.operation()
            properties = operation.get_parameters_dict()
            for key, value in properties.items():
                pass
        else:
            raise TypeError("This slot expects items from the Explorer widget")

    def remove_all_widgets(self) -> None:
        for i in reversed(range(self.count())):
            widget = self.itemAt(i).widget()
            # Remove it from the layout list
            self.removeWidget(widget)
            # Remove it from the GUI
            widget.setParent(None)

    def create_input(self, label: str, default: Union[str, int, None] = None) -> None:
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        layout.addWidget(QLineEdit(str(default)))
        self.addLayout(layout)


class PropertiesUnselected(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.no_selection_text = QLabel("Select a metric or transformation to configure its properties")
        self.no_selection_text.setStyleSheet("QLabel { color: silver; }")

        self.main_layout.addWidget(self.no_selection_text)
        self.setLayout(self.main_layout)
