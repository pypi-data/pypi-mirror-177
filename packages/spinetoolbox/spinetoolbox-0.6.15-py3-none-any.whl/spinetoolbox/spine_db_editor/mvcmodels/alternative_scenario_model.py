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
Models to represent alternatives, scenarios and scenario alternatives in a tree.

:authors: P. Vennström (VTT), M. Marin (KTH)
:date:    17.6.2020
"""
import json
from PySide2.QtCore import QMimeData, Qt
from .tree_model_base import TreeModelBase
from .tree_item_utility import StandardDBItem
from .alternative_scenario_item import AlternativeRootItem, ScenarioRootItem


class AlternativeScenarioModel(TreeModelBase):
    """A model to display alternatives and scenarios in a tree view."""

    @staticmethod
    def _make_db_item(db_map):
        return StandardDBItem(db_map)

    @staticmethod
    def _top_children():
        return [AlternativeRootItem(), ScenarioRootItem()]

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def mimeData(self, indexes):
        """
        Builds a dict mapping db name to item type to a list of ids.

        Returns:
            QMimeData
        """
        items = {self.item_from_index(ind): None for ind in indexes}  # NOTE: this avoids dupes and keeps order
        d = {}
        for item in items:
            parent_item = item.parent_item
            db_row = self.db_row(parent_item)
            parent_type = parent_item.item_type
            scen_row = parent_item.parent_item.child_number() if parent_type == "scenario_alternative" else None
            master_key = ";;".join([str(db_row), parent_type, str(scen_row)])
            d.setdefault(master_key, []).append(item.child_number())
        data = json.dumps(d)
        mime = QMimeData()
        mime.setText(data)
        return mime

    def canDropMimeData(self, data, drop_action, row, column, parent):
        if not parent.isValid():
            return False
        if not data.hasText():
            return False
        try:
            data = json.loads(data.text())
        except ValueError:
            return False
        if not isinstance(data, dict):
            return False
        # Check that all source data comes from the same db and parent
        if len(data) != 1:
            return False
        master_key = next(iter(data))
        db_row, parent_type, scen_row = master_key.split(";;")
        db_row = int(db_row)
        if parent_type not in ("alternative", "scenario_alternative"):
            return False
        # Check that target is in the same db as source
        scen_alt_root_item = self.item_from_index(parent)
        if db_row != self.db_row(scen_alt_root_item):
            return False
        if parent_type == "scenario_alternative":
            # Check that reordering only happens within the same scenario
            scen_row = int(scen_row)
            if scen_row != scen_alt_root_item.parent_item.child_number():
                return False
        return True

    def dropMimeData(self, data, drop_action, row, column, parent):
        scen_alt_root_item = self.item_from_index(parent)
        if not hasattr(scen_alt_root_item, "alternative_id_list"):
            # In some rare cases, it is possible that the drop was accepted
            # on a wrong tree item (bug in Qt or canDropMimeData()?).
            # In those cases the type of scen_alt_root_item is StandardTreeItem or ScenarioRootItem.
            return False
        alternative_id_list = scen_alt_root_item.alternative_id_list
        if row == -1:
            row = len(alternative_id_list)
        master_key, alternative_rows = json.loads(data.text()).popitem()
        db_row, parent_type, _parent_row = master_key.split(";;")
        db_row = int(db_row)
        if parent_type == "alternative":
            alt_root_item = self._invisible_root_item.child(db_row).child(0)
            alternative_ids = [alt_root_item.child(row).id for row in alternative_rows]
            alternative_ids = [id_ for id_ in alternative_ids if id_ not in set(alternative_id_list) | {None}]
        elif parent_type == "scenario_alternative":
            alternative_ids = [scen_alt_root_item.child(row).alternative_id for row in alternative_rows]
            alternative_id_list = [id_ for id_ in alternative_id_list if id_ not in alternative_ids]
        alternative_id_list[row:row] = alternative_ids
        db_item = {
            "id": scen_alt_root_item.parent_item.id,
            "alternative_id_list": ",".join([str(id_) for id_ in alternative_id_list]),
        }
        self.db_mngr.set_scenario_alternatives({scen_alt_root_item.db_map: [db_item]})
        return True
