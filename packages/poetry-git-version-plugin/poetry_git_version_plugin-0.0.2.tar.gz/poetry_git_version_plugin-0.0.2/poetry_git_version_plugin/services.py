import re
import subprocess
from pprint import pprint
from typing import Callable

from cleo.io.io import IO
from packaging.version import VERSION_PATTERN
from poetry.core.version.pep440.parser import parse_pep440

from poetry_git_version_plugin import config
from poetry_git_version_plugin.exceptions import PluginException, plugin_exception_wrapper

VERSION_REGEX_COMPILE = re.compile(r'^\s*' + VERSION_PATTERN + r'\s*$', re.VERBOSE | re.IGNORECASE)


def _run_command(command: str | list):
    """Запуск команд, возвращение ответа, обработка исключения

    Args:
        command (str | list): Выполняемая команда

    Raises:
        RuntimeError: _description_

    Returns:
        _type_: _description_
    """

    if isinstance(command, str):
        command = command.split()

    result = subprocess.run(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    if result.returncode == 0:
        return result.stdout.strip()

    raise RuntimeError(result.stderr)


def validate_version(version_string: str):
    """Проверка версии на PEP 440

    Копипаст метода: from poetry.core.version.pep440.parser import parse_pep440

    Args:
        version_string (str): Версия

    Raises:
        PluginException: Версия не соответствует стандарту

    """

    if VERSION_REGEX_COMPILE.search(version_string) is None:
        raise PluginException(f'Invalid PEP 440 version: "{version_string}"')


def validate_version_decorator(func: Callable):
    def inner(*args, **kwargs):
        version = func(*args, **kwargs)
        validate_version(version)
        return version

    return inner


def get_git_branch() -> str:
    """Получение активной ветки

    Аналог выполнения команды: git branch --show-current

    Returns:
        str: имя ветки

    """

    return _run_command('git branch --show-current')


def get_git_last_tag():
    return _run_command('git describe --tags')


def get_git_tag() -> str:
    """Получение последнего тега

    Аналог выполнения команды: git describe --exact-match --tags HEAD

    Returns:
        str: Последний тег

    """

    return _run_command('git describe --exact-match --tags HEAD')


def get_git_ref() -> str:
    """Получение ref последнего коммита

    Аналог выполнения команды: git show-ref --heads --hash --abbrev

    Returns:
        str: ref последнего комита

    """

    branch = get_git_branch()
    return _run_command('git show-ref --heads --hash --abbrev %s' % branch)


class GitVersionService(object):

    io: IO
    plugin_config: config.PluginConfig

    def __init__(self, io: IO, plugin_config: config.PluginConfig) -> None:
        self.io = io
        self.plugin_config = plugin_config

    def get_git_tag(self):
        self.io.write(f'<b>{config.PLUGIN_NAME}</b>: Find git <b>tag</b>... ')

        try:
            tag = get_git_tag()

        except RuntimeError:
            self.io.write_line('fail')
            return None

        self.io.write_line(f'success, setting dynamic version to: {tag}')

        return tag

    def get_git_last_tag(self):
        from pep440nz.git import head_tag_description
        from pep440nz.version import Version

        self.io.write(f'<b>{config.PLUGIN_NAME}</b>: Find git <b>last tag</b>... ')

        try:
            description = head_tag_description()

        except Exception as ex:
            self.io.write_line('fail')
            raise PluginException(ex.args[0])

        if description.tag == Version.MIN:
            description._Description__tag = Version('0.0.1')  # noqa: WPS437

        tag = f'{description.tag}+{description.post}-{description.hash[:7]}'

        self.io.write_line(f'success, setting dynamic version to: {tag}')

        return tag

    def get_git_ref(self):
        self.io.write(f'<b>{config.PLUGIN_NAME}</b>: Find git <b>ref</b>... ')

        try:
            ref = get_git_ref()

        except RuntimeError:
            self.io.write_line('fail')
            return None

        tag = f'0.0.1+{ref}'

        self.io.write_line(f'success, founded ref: {ref}, setting dynamic version to: {tag}')

        return tag

    @validate_version_decorator
    def get_tag(self) -> str:
        tag = self.get_git_tag()

        if tag is not None:
            return tag

        if self.plugin_config.use_last_tag:
            tag = self.get_git_last_tag()

        if tag is not None:
            return tag

        if self.plugin_config.use_dev_ref:
            tag = self.get_git_ref()

        if tag is not None:
            return tag

        raise PluginException('No Git version found, not extracting dynamic version')
