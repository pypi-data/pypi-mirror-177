import sys
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets


class OptionsHelpTable(QtWidgets.QTableWidget):
    """
    用于展示PyInstaller选项详情的表格控件
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super(OptionsHelpTable, self).__init__(parent)

        pass
