"""
Test case for PI tag measures.
.. since: 0.2
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
import os.path
from datetime import datetime
from tempfile import TemporaryDirectory
from dateutil import tz  # type: ignore
import sqlalchemy  # type: ignore
from hamcrest import assert_that, equal_to, calling, raises, is_

from edv_dwh_connector.exceptions import ValueAlreadyExistsError
from edv_dwh_connector.pi.db.pg_pi_tag import PgPITags
from edv_dwh_connector.pi.db.pg_pi_measure import PgPIMeasures, PgPIMeasuresDf
from edv_dwh_connector.exceptions import ValueNotFoundError
from tests.adapted_postgresql import AdaptedPostreSQL, \
    PgDwhForTests


def test_save_new_measure() -> None:
    """
    Tests that it saves new measure.
    """

    with AdaptedPostreSQL() as postgres:
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        tag_code = "AI162003_SCLD"
        date = datetime(
            year=2022, month=1, day=15,
            hour=12, minute=55, second=30, microsecond=177990,
            tzinfo=tz.UTC
        )
        measure = PgPIMeasures(
            PgPITags(dwh).get(tag_code), dwh
        ).add(date=date, value=35.71)
        assert_that(
            measure.tag().code(), equal_to(tag_code),
            "Measure PI Tag should match"
        )
        assert_that(
            measure.date(), equal_to(
                datetime.strptime(
                    date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    "%Y-%m-%d %H:%M:%S.%f"
                ).astimezone(tz.UTC)
            ),
            "PI Tag measure date should match"
        )
        assert_that(
            measure.value(), equal_to(35.71),
            "PI Tag measure value should match"
        )


def test_try_to_add_existent_measure() -> None:
    """
    Try to add an existent measure for a tag.
    """

    with AdaptedPostreSQL() as postgres:
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        tag_code = "AI162003_SCLD"
        date = datetime(
            year=2022, month=1, day=15,
            hour=12, minute=55, second=30, microsecond=177990,
            tzinfo=tz.UTC
        )
        measures = PgPIMeasures(
            PgPITags(dwh).get(tag_code), dwh
        )
        measures.add(date=date, value=35.71)
        assert_that(
            calling(measures.add).with_args(
                date, 12.0
            ),
            raises(ValueAlreadyExistsError),
            "Tag existent measure adding should be rejected"
        )


def test_list_items() -> None:
    """
    Tests that it lists items.
    """

    with AdaptedPostreSQL() as postgres:
        tag_code = "AI162003_SCLD"
        date = datetime(
            year=2022, month=1, day=19,
            hour=15, minute=7, second=12, microsecond=177990,
            tzinfo=tz.UTC
        )
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        measures = PgPIMeasures(
            PgPITags(dwh).get(tag_code), dwh
        )
        measures.add(date=date, value=35.71)
        assert_that(
            len(
                measures.items(
                    datetime(year=2022, month=1, day=19),
                    datetime(year=2022, month=1, day=20)
                )
            ), equal_to(1),
            "Measures of PI Tag should be retrieved"
        )
        assert_that(
            len(measures.items(date.now(), date.now())), equal_to(0),
            "Measures of PI Tag should be empty"
        )


def test_gets_last_measure() -> None:
    """
    Tests that it gets last measure.
    """

    with AdaptedPostreSQL() as postgres:
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        tag_code = "AI162014_SCLD"
        tag = PgPITags(dwh).get(tag_code)
        measures = PgPIMeasures(tag, dwh)
        date1 = datetime(
            year=2022, month=1, day=20, hour=11, minute=20, second=11,
            tzinfo=tz.UTC
        )
        measures.add(date=date1, value=35.71)
        date2 = datetime(
            year=2022, month=1, day=20, hour=11, minute=20, second=11,
            microsecond=896000, tzinfo=tz.UTC
        )
        measures.add(date=date2, value=36.89)
        date3 = datetime(
            year=2022, month=1, day=19, hour=7, minute=30, tzinfo=tz.UTC
        )
        measures.add(date=date3, value=34.05)
        measure = measures.last()
        assert_that(
            measure.date(), equal_to(date2),
            "Should get last date"
        )
        assert_that(
            measure.tag().code(), equal_to(tag_code),
            "Should get tag"
        )


def test_tries_to_gets_last_measure() -> None:
    """
    Tests that it is not able to find last measure.
    """

    with AdaptedPostreSQL() as postgres:
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        tag = PgPITags(dwh).get("AI162014_SCLD")
        assert_that(
            calling(PgPIMeasures(tag, dwh).last).with_args(),
            raises(
                ValueNotFoundError,
                "Last PI measure not found"
            ),
            "Should not be able to get last PI measure"
        )


def test_fetch_as_data_frame() -> None:
    """
    Tests that it fetches as data frame.
    """

    with TemporaryDirectory() as folder:
        with AdaptedPostreSQL() as postgres:
            tag_code = "AI162003_SCLD"
            date = datetime(
                year=2022, month=1, day=19,
                hour=15, minute=7, second=12, microsecond=177000,
                tzinfo=tz.UTC
            )
            dwh = PgDwhForTests(
                sqlalchemy.create_engine(postgres.get_connection_url())
            )
            tag = PgPITags(dwh).get(tag_code)
            measures = PgPIMeasures(
                tag, dwh
            )
            measures.add(date=date, value=35.71)
            mdf = PgPIMeasuresDf(tag, dwh, folder)
            assert_that(
                mdf.frame(
                    datetime(year=2022, month=1, day=19),
                    datetime(year=2022, month=1, day=20)
                ).to_dict(), equal_to(
                    {
                        PgPIMeasuresDf.DATE_TIME: {0: date},
                        PgPIMeasuresDf.VALUE: {0: 35.71},
                        PgPIMeasuresDf.NAME: {0: 'AI162003_SCLD'}
                    }
                ),
                "Measures of PI Tag from data frame should be retrieved"
            )
            assert_that(
                os.path.exists(
                    os.path.join(folder, f'{tag_code}.csv')
                ),
                is_(True),
                "PI Tag Measures CSV file should exists"
            )
