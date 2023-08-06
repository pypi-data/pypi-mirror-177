######################################################################################################################
# Copyright (C) 2017-2022 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Custom editors for model/view programming.


:author: M. Marin (KTH)
:date:   2.9.2018
"""

from PySide2.QtCore import Qt, Slot, Signal, QSortFilterProxyModel, QEvent, QCoreApplication, QModelIndex, QPoint, QSize
from PySide2.QtWidgets import (
    QLineEdit,
    QTableView,
    QStyledItemDelegate,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QColorDialog,
    QDialog,
    QDialogButtonBox,
    QListView,
    QStyle,
    QLabel,
)
from PySide2.QtGui import QStandardItemModel, QStandardItem, QColor, QIcon, QPixmap, QPainter
from ..helpers import IconListManager, interpret_icon_id, make_icon_id, try_number_from_string


class CustomLineEditor(QLineEdit):
    """A custom QLineEdit to handle data from models."""

    def set_data(self, data):
        """Sets editor's text.

        Args:
            data (Any): anything convertible to string
        """
        if data is not None:
            self.setText(str(data))

    def data(self):
        """Returns editor's text.

        Returns:
            str: editor's text
        """
        return self.text()

    def keyPressEvent(self, event):
        """Prevents shift key press to clear the contents."""
        if event.key() != Qt.Key_Shift:
            super().keyPressEvent(event)


class ParameterValueLineEditor(CustomLineEditor):
    def set_data(self, data):
        if data is not None and not isinstance(data, str):
            self.setAlignment(Qt.AlignRight)
        super().set_data(data)

    def data(self):
        return try_number_from_string(super().data())


class _CustomLineEditDelegate(QStyledItemDelegate):
    """A delegate for placing a CustomLineEditor on the first row of SearchBarEditor."""

    text_edited = Signal("QString")

    def setModelData(self, editor, model, index):
        model.setData(index, editor.data())

    def createEditor(self, parent, option, index):
        """Create editor and 'forward' `textEdited` signal."""
        editor = CustomLineEditor(parent)
        editor.set_data(index.data())
        editor.textEdited.connect(lambda s: self.text_edited.emit(s))  # pylint: disable=unnecessary-lambda
        return editor

    def eventFilter(self, editor, event):
        """Handle all sort of special cases."""
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Tab, Qt.Key_Backtab):
            # Bring focus to parent so tab editing works as expected
            self.parent().setFocus()
            return QCoreApplication.sendEvent(self.parent(), event)
        if event.type() == QEvent.FocusOut:
            # Send event to parent so it gets closed when clicking on an empty area of the table
            return QCoreApplication.sendEvent(self.parent(), event)
        if event.type() == QEvent.ShortcutOverride and event.key() == Qt.Key_Escape:
            # Close editor so we don't need to escape twice to close the parent SearchBarEditor
            self.parent().closeEditor(editor, QStyledItemDelegate.NoHint)
            return True
        return super().eventFilter(editor, event)


class SearchBarEditor(QTableView):
    """A Google-like search bar, implemented as a QTableView with a _CustomLineEditDelegate in the first row."""

    data_committed = Signal()

    def __init__(self, parent, tutor=None):
        """Initializes instance.

        Args:
            parent (QWidget): parent widget
            tutor (QWidget, optional): another widget used for positioning.
        """
        super().__init__(parent)
        self._tutor = tutor
        self._base_offset = QPoint()
        self._original_text = None
        self._orig_pos = None
        self.first_index = QModelIndex()
        self.model = QStandardItemModel(self)
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.filterAcceptsRow = self._proxy_model_filter_accepts_row
        self.setModel(self.proxy_model)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setShowGrid(False)
        self.setMouseTracking(True)
        self.setTabKeyNavigation(False)
        delegate = _CustomLineEditDelegate(self)
        delegate.text_edited.connect(self._handle_delegate_text_edited)
        self.setItemDelegateForRow(0, delegate)

    def set_data(self, current, items):
        """Populates model.

        Args:
            current (str): item that is currently selected from given items
            items (Sequence(str)): items to show in the list
        """
        item_list = [QStandardItem(current)]
        for item in items:
            qitem = QStandardItem(item)
            item_list.append(qitem)
            qitem.setFlags(~Qt.ItemIsEditable)
        self.model.invisibleRootItem().appendRows(item_list)
        self.first_index = self.proxy_model.mapFromSource(self.model.index(0, 0))

    def set_base_offset(self, offset):
        self._base_offset = offset

    def update_geometry(self, option):
        """Updates geometry."""
        self.resizeColumnsToContents()
        self.verticalHeader().setDefaultSectionSize(option.rect.height())
        self._orig_pos = self.pos() + self._base_offset
        if self._tutor:
            self._orig_pos += self._tutor.mapTo(self.parent(), self._tutor.rect().topLeft())
        self.refit()

    def refit(self):
        self.move(self._orig_pos)
        margins = self.contentsMargins()
        table_height = self.verticalHeader().length() + margins.top() + margins.bottom()
        table_width = self.horizontalHeader().length() + margins.left() + margins.right()
        if table_height > self.parent().size().height():
            table_width += self.style().pixelMetric(QStyle.PM_ScrollBarExtent)
        size = QSize(table_width, table_height).boundedTo(self.parent().size())
        self.resize(size)
        # Adjust position if widget is outside parent's limits
        bottom_right = self.mapToGlobal(self.rect().bottomRight())
        parent_bottom_right = self.parent().mapToGlobal(self.parent().rect().bottomRight())
        x_offset = max(0, bottom_right.x() - parent_bottom_right.x())
        y_offset = max(0, bottom_right.y() - parent_bottom_right.y())
        self.move(self.pos() - QPoint(x_offset, y_offset))

    def data(self):
        return self.first_index.data(Qt.EditRole)

    @Slot(str)
    def _handle_delegate_text_edited(self, text):
        """Filters model as the first row is being edited."""
        self._original_text = text
        self.proxy_model.setFilterRegExp("^" + text)
        self.proxy_model.setData(self.first_index, text)
        self.refit()

    def _proxy_model_filter_accepts_row(self, source_row, source_parent):
        """Always accept first row."""
        if source_row == 0:
            return True
        return QSortFilterProxyModel.filterAcceptsRow(self.proxy_model, source_row, source_parent)

    def keyPressEvent(self, event):
        """Sets data from current index into first index as the user navigates
        through the table using the up and down keys.
        """
        super().keyPressEvent(event)
        event.accept()  # Important to avoid unhandled behavior when trying to navigate outside view limits
        # Initialize original text. TODO: Is there a better place for this?
        if self._original_text is None:
            self.proxy_model.setData(self.first_index, event.text())
            self._handle_delegate_text_edited(event.text())
        # Set data from current index in model
        if event.key() in (Qt.Key_Up, Qt.Key_Down):
            current = self.currentIndex()
            if current.row() == 0:
                self.proxy_model.setData(self.first_index, self._original_text)
            else:
                self.proxy_model.setData(self.first_index, current.data())

    def currentChanged(self, current, previous):
        super().currentChanged(current, previous)
        self.edit_first_index()

    def edit_first_index(self):
        """Edits first index if valid and not already being edited."""
        if not self.first_index.isValid():
            return
        if self.isPersistentEditorOpen(self.first_index):
            return
        self.edit(self.first_index)

    def mouseMoveEvent(self, event):
        """Sets the current index to the one hovered by the mouse."""
        if not self.currentIndex().isValid():
            return
        index = self.indexAt(event.pos())
        if index.row() == 0:
            return
        self.setCurrentIndex(index)

    def mousePressEvent(self, event):
        """Commits data."""
        index = self.indexAt(event.pos())
        if index.row() == 0:
            return
        self.proxy_model.setData(self.first_index, index.data(Qt.EditRole))
        self.data_committed.emit()


class CheckListEditor(QTableView):
    """A check list editor."""

    def __init__(self, parent, tutor=None, ranked=False):
        """Initialize class."""
        super().__init__(parent)
        self._tutor = tutor
        self._ranked = ranked
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setShowGrid(False)
        self.setMouseTracking(True)
        self._icons = []
        self._selected = []
        self._items = {}
        self._blank_icon = self._make_icon()

    def _make_icon(self, i=None):
        if not self._ranked:
            return None
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.white)
        if i is not None:
            painter = QPainter(pixmap)
            painter.drawText(0, 0, 16, 16, Qt.AlignCenter, str(i))
            painter.end()
        return QIcon(pixmap)

    def keyPressEvent(self, event):
        """Toggles checked state if the user presses space."""
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Space:
            index = self.currentIndex()
            self.toggle_selected(index)

    def toggle_selected(self, index):
        """Adds or removes given index from selected items.

        Args:
            index (QModelIndex): index to toggle
        """
        item = self.model.itemFromIndex(index).text()
        qitem = self._items[item]
        if item not in self._selected:
            rank = len(self._selected)
            self._select_item(qitem, rank)
            self._selected.append(item)
        else:
            self._selected.remove(item)
            self._deselect_item(qitem, update_ranks=True)

    def _select_item(self, qitem, rank):
        if self._ranked:
            qitem.setData(self._icons[rank], Qt.DecorationRole)
        else:
            qitem.setCheckState(Qt.Checked)

    def _deselect_item(self, qitem, update_ranks=False):
        if self._ranked:
            qitem.setData(self._blank_icon, Qt.DecorationRole)
            if update_ranks:
                for rank, item in enumerate(self._selected):
                    qitem = self._items[item]
                    self._select_item(qitem, rank)
        else:
            qitem.setCheckState(Qt.Unchecked)

    def mouseMoveEvent(self, event):
        """Sets the current index to the one under mouse."""
        index = self.indexAt(event.pos())
        self.setCurrentIndex(index)

    def mousePressEvent(self, event):
        """Toggles checked state of pressed index."""
        index = self.indexAt(event.pos())
        self.toggle_selected(index)

    def set_data(self, items, checked_items):
        """Sets data and updates geometry.

        Args:
            items (Sequence(str)): All items.
            checked_items (Sequence(str)): Initially checked items.
        """
        self._icons = [self._make_icon(i + 1) for i in range(len(items))]
        for item in items:
            qitem = QStandardItem(item)
            qitem.setFlags(~Qt.ItemIsEditable)
            qitem.setData(qApp.palette().window(), Qt.BackgroundRole)  # pylint: disable=undefined-variable
            self._deselect_item(qitem)
            self._items[item] = qitem
            self.model.appendRow(qitem)
        self._selected = [item for item in checked_items if item in items]
        for rank, item in enumerate(self._selected):
            qitem = self._items[item]
            self._select_item(qitem, rank)

    def data(self):
        """Returns a comma separated list of checked items.

        Returns
            str
        """
        return ",".join(self._selected)

    def update_geometry(self, option):
        """Updates geometry."""
        self.resizeColumnsToContents()
        self.verticalHeader().setDefaultSectionSize(option.rect.height())
        margins = self.contentsMargins()
        table_height = self.verticalHeader().length() + margins.top() + margins.bottom()
        table_width = self.horizontalHeader().length() + margins.left() + margins.right()
        if table_height > self.parent().size().height():
            table_width += self.style().pixelMetric(QStyle.PM_ScrollBarExtent)
        size = QSize(table_width, table_height).boundedTo(self.parent().size())
        self.resize(size)
        if self._tutor:
            self.move(self.pos() + self._tutor.mapTo(self.parent(), self._tutor.rect().topLeft()))
        # Adjust position if widget is outside parent's limits
        bottom_right = self.mapToGlobal(self.rect().bottomRight())
        parent_bottom_right = self.parent().mapToGlobal(self.parent().rect().bottomRight())
        x_offset = max(0, bottom_right.x() - parent_bottom_right.x())
        y_offset = max(0, bottom_right.y() - parent_bottom_right.y())
        self.move(self.pos() - QPoint(x_offset, y_offset))


class _IconPainterDelegate(QStyledItemDelegate):
    """A delegate to highlight decorations in a QListWidget."""

    def paint(self, painter, option, index):
        """Paints selected items using the highlight brush."""
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, qApp.palette().highlight())  # pylint: disable=undefined-variable
        super().paint(painter, option, index)


class IconColorEditor(QDialog):
    """An editor to let the user select an icon and a color for an object_class."""

    def __init__(self, parent):
        """Init class."""
        super().__init__(parent)
        icon_size = QSize(32, 32)
        self.icon_mngr = IconListManager(icon_size)
        self.setWindowTitle("Select icon and color")
        self.icon_widget = QWidget(self)
        self.icon_list = QListView(self.icon_widget)
        self.icon_list.setViewMode(QListView.IconMode)
        self.icon_list.setIconSize(icon_size)
        self.icon_list.setResizeMode(QListView.Adjust)
        self.icon_list.setItemDelegate(_IconPainterDelegate(self))
        self.icon_list.setMovement(QListView.Static)
        self.icon_list.setMinimumHeight(400)
        icon_widget_layout = QVBoxLayout(self.icon_widget)
        icon_widget_layout.addWidget(QLabel("Font Awesome icons"))
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Search icons for...")
        icon_widget_layout.addWidget(self.line_edit)
        icon_widget_layout.addWidget(self.icon_list)
        self.color_dialog = QColorDialog(self)
        self.color_dialog.setWindowFlags(Qt.Widget)
        self.color_dialog.setOption(QColorDialog.NoButtons, True)
        self.color_dialog.setOption(QColorDialog.DontUseNativeDialog, True)
        self.button_box = QDialogButtonBox(self)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        top_widget = QWidget(self)
        top_layout = QHBoxLayout(top_widget)
        top_layout.addWidget(self.icon_widget)
        top_layout.addWidget(self.color_dialog)
        layout = QVBoxLayout(self)
        layout.addWidget(top_widget)
        layout.addWidget(self.button_box)
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.icon_mngr.model)
        self.proxy_model.filterAcceptsRow = self._proxy_model_filter_accepts_row
        self.icon_list.setModel(self.proxy_model)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.connect_signals()

    def _proxy_model_filter_accepts_row(self, source_row, source_parent):
        """Filters icons according to search terms."""
        text = self.line_edit.text()
        if not text:
            return QSortFilterProxyModel.filterAcceptsRow(self.proxy_model, source_row, source_parent)
        searchterms = self.icon_mngr.model.index(source_row, 0, source_parent).data(Qt.UserRole + 1)
        return any(text in term for term in searchterms)

    def connect_signals(self):
        """Connects signals to slots."""
        self.line_edit.textEdited.connect(self.proxy_model.invalidateFilter)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def set_data(self, data):
        icon_code, color_code = interpret_icon_id(data)
        self.icon_mngr.init_model()
        for i in range(self.proxy_model.rowCount()):
            index = self.proxy_model.index(i, 0)
            if index.data(Qt.UserRole) == icon_code:
                self.icon_list.setCurrentIndex(index)
                break
        self.color_dialog.setCurrentColor(QColor(color_code))

    def data(self):
        icon_code = self.icon_list.currentIndex().data(Qt.UserRole)
        color_code = self.color_dialog.currentColor().rgb()
        return make_icon_id(icon_code, color_code)
