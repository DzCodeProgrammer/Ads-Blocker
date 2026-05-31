"""Repository for filter rules — all DB access isolated here."""
from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, func
from backend.models.filter_rule import FilterRule, RuleType


class FilterRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def add(self, rule: FilterRule) -> FilterRule:
        self._db.add(rule)
        self._db.commit()
        self._db.refresh(rule)
        return rule

    def bulk_insert(self, rules: list[FilterRule]) -> int:
        self._db.bulk_save_objects(rules)
        self._db.commit()
        return len(rules)

    def get_by_id(self, rule_id: int) -> Optional[FilterRule]:
        return self._db.get(FilterRule, rule_id)

    def get_all_active(self, rule_type: Optional[RuleType] = None) -> list[FilterRule]:
        stmt = select(FilterRule).where(FilterRule.is_active == True)  # noqa: E712
        if rule_type:
            stmt = stmt.where(FilterRule.rule_type == rule_type)
        return list(self._db.execute(stmt).scalars())

    def get_whitelist(self) -> list[FilterRule]:
        return self.get_all_active(RuleType.WHITELIST)

    def get_blacklist(self) -> list[FilterRule]:
        return self.get_all_active(RuleType.BLACKLIST)

    def delete_by_source(self, source: str) -> int:
        result = self._db.execute(
            delete(FilterRule).where(FilterRule.source == source)
        )
        self._db.commit()
        return result.rowcount

    def count_by_type(self) -> dict[str, int]:
        rows = self._db.execute(
            select(FilterRule.rule_type, func.count()).group_by(FilterRule.rule_type)
        ).all()
        return {row[0].value: row[1] for row in rows}

    def deactivate(self, rule_id: int) -> bool:
        rule = self.get_by_id(rule_id)
        if not rule:
            return False
        rule.is_active = False
        self._db.commit()
        return True
