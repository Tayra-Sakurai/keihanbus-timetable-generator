# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Types"""
from typing import TypedDict
from collections.abc import MutableSequence

__all__ = [
    'TimeTableData',
]


class TimeTableData(TypedDict):
    """The time table dictionary type."""
    day: MutableSequence[int]
    course: MutableSequence[str]
    hour: MutableSequence[int]
    minute: MutableSequence[int]
