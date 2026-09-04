from services.stardew_service import (
    STARDEW_CONTAINER_NAME,
    get_stardew_status,
)


def test_stardew_container_name():
    assert STARDEW_CONTAINER_NAME == "pi5junimo-server"


def test_get_stardew_status_returns_expected_structure():
    status = get_stardew_status()

    assert isinstance(status, dict)

    expected_keys = {
        "exists",
        "name",
        "status",
        "image",
        "uptime",
        "ports",
    }

    assert expected_keys.issubset(status.keys())