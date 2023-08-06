from __future__ import annotations

from poetry.console.commands.command import Command

from poetry_git_version_plugin import config
from poetry_git_version_plugin.exceptions import PluginException, plugin_exception_wrapper
from poetry_git_version_plugin.services import GitVersionService


class GitVersionCommand(Command):
    name = 'git-version'

    @plugin_exception_wrapper
    def handle(self) -> None:
        self.poetry
