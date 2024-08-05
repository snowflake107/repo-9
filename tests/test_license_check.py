# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from obs_common import license_check


def test_license_present(tmp_path):
    target = tmp_path / "target.py"
    target.write_text(
        "# This Source Code Form is subject to the terms of the Mozilla Public\n"
        "# License, v. 2.0. If a copy of the MPL was not distributed with this\n"
        "# file, You can obtain one at https://mozilla.org/MPL/2.0/.\n"
    )
    assert license_check.main([str(target)]) == 0


def test_license_missing(tmp_path):
    target = tmp_path / "target.py"
    target.touch()
    assert license_check.main([str(target)]) != 0
