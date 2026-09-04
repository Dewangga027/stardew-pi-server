from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_expected_module_structure_exists():
    expected_files = [
        "commands/__init__.py",
        "commands/ping.py",
        "commands/status.py",
        "commands/health.py",
        "commands/docker_cmd.py",
        "commands/help.py",

        "services/__init__.py",
        "services/system_service.py",
        "services/docker_service.py",
        "services/nvme_service.py",

        "views/__init__.py",
        "views/help_view.py",

        "utils/__init__.py",
        "utils/formatting.py",
        "utils/health.py",
    ]

    missing = [
        file
        for file in expected_files
        if not (ROOT / file).exists()
    ]

    assert not missing, (
        "Modular project structure is incomplete.\n"
        "Missing files:\n"
        + "\n".join(f"- {file}" for file in missing)
    )


def test_bot_py_remains_entrypoint():
    assert (ROOT / "bot.py").exists()


def test_commands_are_moved_out_of_bot_py():
    bot_file = ROOT / "bot.py"
    content = bot_file.read_text(encoding="utf-8")

    command_decorators = [
        'name="ping"',
        'name="status"',
        'name="health"',
        'name="docker"',
        'name="help"',
    ]

    still_in_bot = [
        command
        for command in command_decorators
        if command in content
    ]

    assert not still_in_bot, (
        "Slash commands should be moved out of bot.py.\n"
        "Still found:\n"
        + "\n".join(f"- {command}" for command in still_in_bot)
    )

def test_all_command_modules_have_register():
    from commands import docker_cmd
    from commands import health
    from commands import help as help_command
    from commands import ping
    from commands import status

    modules = [
        ping,
        status,
        health,
        docker_cmd,
        help_command,
    ]

    for module in modules:
        register = getattr(module, "register", None)

        assert callable(register), (
            f"{module.__name__} harus memiliki "
            "function register(bot, guild)"
        )