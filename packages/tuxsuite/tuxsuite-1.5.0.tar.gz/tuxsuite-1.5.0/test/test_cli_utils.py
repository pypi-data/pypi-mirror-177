# -*- coding: utf-8 -*-

import pytest
from tuxsuite.cli.utils import datediff, file_or_url, key_value, show_log


def test_datediff():
    assert datediff("hello", "hello") == "\x1b[37mhello\x1b[0m"
    assert datediff("hello world", "hello monde") == "\x1b[37mhello \x1b[0mmonde"


def test_key_value(mocker):
    error = mocker.patch("tuxsuite.cli.utils.error", side_effect=Exception)
    assert key_value("HELLO=WORLD") == ("HELLO", "WORLD")
    with pytest.raises(Exception):
        key_value("HELLO=WORLD=1")
    error.assert_called_once_with("Key Value pair not valid: HELLO=WORLD=1")

    error.reset_mock()
    with pytest.raises(Exception):
        key_value("HELLO world")
    error.assert_called_once_with("Key Value pair not valid: HELLO world")


def test_file_or_url():
    url = "http://www.example.com/"
    result = file_or_url(url)
    assert result == url

    with pytest.raises(SystemExit):
        file_or_url("/temp/unknown")


def test_show_log(mocker, build):
    mocker.patch("tuxsuite.build.Build.get_status", return_value={"download_url": ""})
    mocker.patch("tuxsuite.build.Build.warnings_count", return_value=1)
    with pytest.raises(SystemExit):
        show_log(build, False, None)
