from __future__ import annotations

import sys
from collections.abc import Generator, Mapping
from pathlib import Path

from packaging.version import Version

from .. import __version__
from .._compat import tomllib
from .._logging import logger, rich_print
from ..errors import CMakeConfigError
from .skbuild_model import ScikitBuildSettings
from .sources import ConfSource, EnvSource, SourceChain, TOMLSource

__all__ = ["SettingsReader"]


def __dir__() -> list[str]:
    return __all__


class SettingsReader:
    def __init__(
        self,
        pyproject_toml: Path,
        config_settings: Mapping[str, str | list[str]],
        verify_conf: bool = True,
    ) -> None:
        with pyproject_toml.open("rb") as f:
            pyproject = tomllib.load(f)

        self.sources = SourceChain(
            EnvSource("SKBUILD"),
            ConfSource(settings=config_settings, verify=verify_conf),
            TOMLSource("tool", "scikit-build", settings=pyproject),
        )
        self.settings = self.sources.convert_target(ScikitBuildSettings)

        if self.settings.minimum_version:
            current_version = Version(__version__)
            minimum_version = Version(self.settings.minimum_version)
            if current_version < minimum_version:
                msg = (
                    f"scikit-build-core version {__version__} is too old. "
                    f"Minimum required version is {self.settings.minimum_version}."
                )
                raise CMakeConfigError(msg)

    def unrecognized_options(self) -> Generator[str, None, None]:
        return self.sources.unrecognized_options(ScikitBuildSettings)

    def validate_may_exit(self) -> None:
        unrecognized = list(self.unrecognized_options())
        if unrecognized:
            if self.settings.strict_config:
                sys.stdout.flush()
                rich_print(
                    "[red][bold]ERROR:[/bold] Unrecognized options:", file=sys.stderr
                )
                for option in unrecognized:
                    rich_print(f"  [red]{option}", file=sys.stderr)
                raise SystemExit(7)
            logger.warning("Unrecognized options: {}", ", ".join(unrecognized))
