import pytest_mock

from instagram_to_discord.sites.instagram.instagram_process import process_instagram


def test_process_instagram(mocker: pytest_mock.mocker):
    mock = mocker.mock()

    do_bar_mock = mocker.patch.object(None, 'do_bar')
    process_instagram()
