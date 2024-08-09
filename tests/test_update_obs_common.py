# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import re

import pytest

from obs_common import update_obs_common


@pytest.fixture
def tmp_cwd(tmp_path):
    orig_wd = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(orig_wd)


def test_update_from_old(tmp_cwd):
    req = tmp_cwd / "requirements.in"
    req.write_text("obs-common @ https://path/to/package.whl\n")
    EXPECT_PATTERN = re.compile(
        "obs-common @ https://github.com/mozilla-services/obs-common/"
        "releases/download/[^/]+/obs_common-[^-]+-py2.py3-none-any.whl\n",
        re.MULTILINE,
    )
    assert update_obs_common.main() == 0
    assert EXPECT_PATTERN.fullmatch(req.read_text())


def test_update_idempotent(tmp_cwd):
    req = tmp_cwd / "requirements.in"
    req.write_text("obs-common @ https://path/to/package.whl\n")
    assert update_obs_common.main() == 0
    expect = req.read_text()
    assert update_obs_common.main() == 0
    assert req.read_text() == expect
