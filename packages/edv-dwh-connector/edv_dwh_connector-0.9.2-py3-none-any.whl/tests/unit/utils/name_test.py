"""
Test case for name.
.. since: 0.8
"""
# -*- coding: utf-8 -*-
# Copyright (c) 2022 Endeavour Mining
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to read
# the Software only. Permissions is hereby NOT GRANTED to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from hamcrest import assert_that, equal_to
from edv_dwh_connector.utils.name\
    import NameInLowercaseWithoutSpecialCharacterAndUnit


def test_name_without_unit() -> None:
    """
    Test that name doesn't contain unit.
    """
    assert_that(
        NameInLowercaseWithoutSpecialCharacterAndUnit("As(ppm)").value(),
        equal_to("as")
    )


def test_name_without_special_characters() -> None:
    """
    Test that name doesn't contain special characters.
    """
    assert_that(
        NameInLowercaseWithoutSpecialCharacterAndUnit("Sol_Cu copper").value(),
        equal_to("solcucopper")
    )


def test_name_without_unit_and_special_characters() -> None:
    """
    Test that name doesn't contain special characters.
    """
    assert_that(
        NameInLowercaseWithoutSpecialCharacterAndUnit("Sol_Cu (ppm)").value(),
        equal_to("solcu")
    )
