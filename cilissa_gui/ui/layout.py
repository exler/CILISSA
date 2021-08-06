from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from cilissa_gui.ui.components import (
    Console,
    Explorer,
    OperationsQueue,
    Properties,
    Workspace,
)


class Layout(QWidget):
    """
    Layout is split into three vertical panels:

    Left panel:
        - Tab widget (Explorer)

    Middle panel:
        - Vertical box layout (Workspace)
        - List widget (Console)

    Right panel:
        - Vertical box layout (Properties)
        - List widget (OperationsQueue)
    """

    def __init__(self) -> None:
        super().__init__()
        self.panels = QHBoxLayout()

        left_panel = self._init_left_panel()
        middle_panel = self._init_middle_panel()
        right_panel = self._init_right_panel()

        self.panels.addLayout(left_panel)
        self.panels.addLayout(middle_panel)
        self.panels.addLayout(right_panel)
        self.setLayout(self.panels)

        self.panels.setStretch(1, 16)

    def _init_left_panel(self) -> QVBoxLayout:
        left_panel = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidget(Explorer())
        scroll_area.setWidgetResizable(True)
        left_panel.addWidget(scroll_area)
        return left_panel

    def _init_middle_panel(self) -> QVBoxLayout:
        middle_panel = QVBoxLayout()
        workspace_box = QGroupBox("Workspace")
        workspace_box.setLayout(Workspace())
        middle_panel.addWidget(workspace_box)
        middle_panel.addWidget(Console())
        return middle_panel

    def _init_right_panel(self) -> QVBoxLayout:
        right_panel = QVBoxLayout()
        properties_box = QGroupBox("Properties")
        properties_box.setLayout(Properties())
        right_panel.addWidget(properties_box)
        right_panel.addWidget(OperationsQueue())
        return right_panel
