"""Enum utility — pick a random member from any StrEnum / IntEnum."""

from __future__ import annotations

import random
from enum import Enum


def get_random_enum_value[E: Enum](enum_cls: type[E]) -> E:
    """Return a random member of *enum_cls*.

    Example::

        from sales_portal_tests.data.sales_portal.country import Country
        random_country = get_random_enum_value(Country)
    """
    return random.choice(list(enum_cls))
