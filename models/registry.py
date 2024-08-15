from __future__ import annotations

import dataset

from db import LOCAL_DATABASE

from .check import Check


class CheckRegistry:
    def __init__(self):
        self.table: dataset.Table = LOCAL_DATABASE["checks"]

    def add_check(self, check: Check) -> bool:
        db_check = self.table.find_one(check_id=check.check_id)
        if not db_check:
            self.table.insert(check.as_dict())
            return True
        return False

    def get_checks_for_player(self, player: str) -> list[Check]:
        player_checks = self.table.find(receiver=player)
        return [Check(**kwargs) for kwargs in player_checks]

    @property
    def checks(self) -> list[Check]:
        all_checks = self.table.all()
        return [Check(**kwargs) for kwargs in all_checks]


REGISTRY = CheckRegistry()
