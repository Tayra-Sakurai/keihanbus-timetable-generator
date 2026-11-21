# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from src.keihanbus_timetable_generator import load_timetable
import pandas


def test_loader():
    assert isinstance(load_timetable(), pandas.DataFrame)
