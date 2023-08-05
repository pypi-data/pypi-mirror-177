from __future__ import annotations

import textwrap

import pytest

import scikit_build_core.settings.skbuild_read_settings
from scikit_build_core.settings.skbuild_read_settings import SettingsReader


def test_skbuild_settings_default(tmp_path):
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text("", encoding="utf-8")

    config_settings: dict[str, list[str] | str] = {}

    settings_reader = SettingsReader(pyproject_toml, config_settings)
    settings = settings_reader.settings
    assert list(settings_reader.unrecognized_options()) == []

    assert settings.ninja.minimum_version == "1.5"
    assert settings.ninja.make_fallback
    assert settings.cmake.minimum_version == "3.15"
    assert settings.cmake.args == []
    assert settings.cmake.define == {}
    assert not settings.cmake.verbose
    assert settings.cmake.build_type == "Release"
    assert settings.logging.level == "WARNING"
    assert settings.sdist.include == []
    assert settings.sdist.exclude == []
    assert settings.sdist.reproducible
    assert settings.wheel.packages is None
    assert settings.wheel.py_api == ""
    assert not settings.wheel.expand_macos_universal_tags
    assert settings.strict_config
    assert not settings.experimental
    assert settings.minimum_version is None


def test_skbuild_settings_envvar(tmp_path, monkeypatch):
    monkeypatch.setattr(
        scikit_build_core.settings.skbuild_read_settings, "__version__", "0.1.0"
    )

    monkeypatch.setenv("SKBUILD_NINJA_MINIMUM_VERSION", "1.1")
    monkeypatch.setenv("SKBUILD_NINJA_MAKE_FALLBACK", "0")
    monkeypatch.setenv("SKBUILD_CMAKE_MINIMUM_VERSION", "3.16")
    monkeypatch.setenv("SKBUILD_CMAKE_ARGS", "-DFOO=BAR;-DBAR=FOO")
    monkeypatch.setenv("SKBUILD_CMAKE_DEFINE", "a=1;b=2")
    monkeypatch.setenv("SKBUILD_CMAKE_BUILD_TYPE", "Debug")
    monkeypatch.setenv("SKBUILD_LOGGING_LEVEL", "DEBUG")
    monkeypatch.setenv("SKBUILD_SDIST_INCLUDE", "a;b; c")
    monkeypatch.setenv("SKBUILD_SDIST_EXCLUDE", "d;e;f")
    monkeypatch.setenv("SKBUILD_SDIST_REPRODUCIBLE", "OFF")
    monkeypatch.setenv("SKBUILD_WHEEL_PACKAGES", "j; k; l")
    monkeypatch.setenv("SKBUILD_WHEEL_PY_API", "cp39")
    monkeypatch.setenv("SKBUILD_WHEEL_EXPAND_MACOS_UNIVERSAL_TAGS", "True")
    monkeypatch.setenv("SKBUILD_STRICT_CONFIG", "0")
    monkeypatch.setenv("SKBUILD_EXPERIMENTAL", "1")
    monkeypatch.setenv("SKBUILD_MINIMUM_VERSION", "0.1")
    monkeypatch.setenv("SKBUILD_CMAKE_VERBOSE", "TRUE")

    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text("", encoding="utf-8")

    config_settings: dict[str, list[str] | str] = {}

    settings_reader = SettingsReader(pyproject_toml, config_settings)
    settings = settings_reader.settings
    assert list(settings_reader.unrecognized_options()) == []

    assert settings.ninja.minimum_version == "1.1"
    assert settings.cmake.minimum_version == "3.16"
    assert settings.cmake.args == ["-DFOO=BAR", "-DBAR=FOO"]
    assert settings.cmake.define == {"a": "1", "b": "2"}
    assert settings.cmake.verbose
    assert settings.cmake.build_type == "Debug"
    assert not settings.ninja.make_fallback
    assert settings.logging.level == "DEBUG"
    assert settings.sdist.include == ["a", "b", "c"]
    assert settings.sdist.exclude == ["d", "e", "f"]
    assert not settings.sdist.reproducible
    assert settings.wheel.packages == ["j", "k", "l"]
    assert settings.wheel.py_api == "cp39"
    assert settings.wheel.expand_macos_universal_tags
    assert not settings.strict_config
    assert settings.experimental
    assert settings.minimum_version == "0.1"


def test_skbuild_settings_config_settings(tmp_path, monkeypatch):
    monkeypatch.setattr(
        scikit_build_core.settings.skbuild_read_settings, "__version__", "0.1.0"
    )

    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text("", encoding="utf-8")

    config_settings: dict[str, str | list[str]] = {
        "ninja.minimum-version": "1.2",
        "ninja.make-fallback": "False",
        "cmake.minimum-version": "3.17",
        "cmake.args": ["-DFOO=BAR", "-DBAR=FOO"],
        "cmake.define.a": "1",
        "cmake.define.b": "2",
        "cmake.verbose": "true",
        "cmake.build-type": "Debug",
        "logging.level": "INFO",
        "sdist.include": ["a", "b", "c"],
        "sdist.exclude": "d;e;f",
        "sdist.reproducible": "false",
        "wheel.packages": ["j", "k", "l"],
        "wheel.py-api": "cp39",
        "wheel.expand-macos-universal-tags": "True",
        "strict-config": "false",
        "experimental": "1",
        "minimum-version": "0.1",
    }

    settings_reader = SettingsReader(pyproject_toml, config_settings)
    settings = settings_reader.settings
    assert list(settings_reader.unrecognized_options()) == []

    assert settings.ninja.minimum_version == "1.2"
    assert not settings.ninja.make_fallback
    assert settings.cmake.minimum_version == "3.17"
    assert settings.cmake.args == ["-DFOO=BAR", "-DBAR=FOO"]
    assert settings.cmake.define == {"a": "1", "b": "2"}
    assert settings.cmake.verbose
    assert settings.cmake.build_type == "Debug"
    assert settings.logging.level == "INFO"
    assert settings.sdist.include == ["a", "b", "c"]
    assert settings.sdist.exclude == ["d", "e", "f"]
    assert not settings.sdist.reproducible
    assert settings.wheel.packages == ["j", "k", "l"]
    assert settings.wheel.py_api == "cp39"
    assert settings.wheel.expand_macos_universal_tags
    assert not settings.strict_config
    assert settings.experimental
    assert settings.minimum_version == "0.1"


def test_skbuild_settings_pyproject_toml(tmp_path, monkeypatch):
    monkeypatch.setattr(
        scikit_build_core.settings.skbuild_read_settings, "__version__", "0.1.0"
    )
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text(
        textwrap.dedent(
            """\
            [tool.scikit-build]
            ninja.minimum-version = "1.3"
            ninja.make-fallback = false
            cmake.minimum-version = "3.18"
            cmake.args = ["-DFOO=BAR", "-DBAR=FOO"]
            cmake.define = {a = "1", b = "2"}
            cmake.build-type = "Debug"
            cmake.verbose = true
            logging.level = "ERROR"
            sdist.include = ["a", "b", "c"]
            sdist.exclude = ["d", "e", "f"]
            sdist.reproducible = false
            wheel.packages = ["j", "k", "l"]
            wheel.py-api = "cp39"
            wheel.expand-macos-universal-tags = true
            strict-config = false
            experimental = true
            minimum-version = "0.1"
            """
        ),
        encoding="utf-8",
    )

    config_settings: dict[str, list[str] | str] = {}

    settings_reader = SettingsReader(pyproject_toml, config_settings)
    settings = settings_reader.settings
    assert list(settings_reader.unrecognized_options()) == []

    assert settings.ninja.minimum_version == "1.3"
    assert not settings.ninja.make_fallback
    assert settings.cmake.minimum_version == "3.18"
    assert settings.cmake.args == ["-DFOO=BAR", "-DBAR=FOO"]
    assert settings.cmake.define == {"a": "1", "b": "2"}
    assert settings.cmake.verbose
    assert settings.cmake.build_type == "Debug"
    assert settings.logging.level == "ERROR"
    assert settings.sdist.include == ["a", "b", "c"]
    assert settings.sdist.exclude == ["d", "e", "f"]
    assert not settings.sdist.reproducible
    assert settings.wheel.packages == ["j", "k", "l"]
    assert settings.wheel.py_api == "cp39"
    assert settings.wheel.expand_macos_universal_tags
    assert not settings.strict_config
    assert settings.experimental
    assert settings.minimum_version == "0.1"


def test_skbuild_settings_pyproject_toml_broken(tmp_path, monkeypatch):
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text(
        textwrap.dedent(
            """\
            [tool.scikit-build]
            cmake.minimum-verison = "3.18"
            ninja.minimum-version = "1.3"
            ninja.make-fallback = false
            logger.level = "ERROR"
            """
        ),
        encoding="utf-8",
    )

    config_settings: dict[str, list[str] | str] = {}

    settings_reader = SettingsReader(pyproject_toml, config_settings)
    assert list(settings_reader.unrecognized_options()) == [
        "tool.scikit-build.cmake.minimum-verison",
        "tool.scikit-build.logger",
    ]

    with pytest.raises(SystemExit):
        settings_reader.validate_may_exit()


def test_skbuild_settings_pyproject_conf_broken(tmp_path):
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text("", encoding="utf-8")

    config_settings: dict[str, str | list[str]] = {
        "cmake.minimum-verison": "3.17",
        "ninja.minimum-version": "1.2",
        "ninja.make-fallback": "False",
        "logger.level": "INFO",
    }

    settings_reader = SettingsReader(pyproject_toml, config_settings)
    assert list(settings_reader.unrecognized_options()) == [
        "cmake.minimum-verison",
        "logger",
    ]

    with pytest.raises(SystemExit):
        settings_reader.validate_may_exit()
