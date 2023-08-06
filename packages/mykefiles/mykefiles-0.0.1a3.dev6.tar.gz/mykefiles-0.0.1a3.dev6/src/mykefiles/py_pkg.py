#!/usr/bin/env python3
from __future__ import annotations

import os
from typing import Any

import myke

PYENV_VERSION_FILE: str = ".python-base-version"
PYENV_VENV_FILE: str = ".python-version"

VERSION_FILE: str = "VERSION"
REPORT_DIR: str = "public"


@myke.cache()
def _get_package_root() -> str:
    return str(
        myke.read.cfg("setup.cfg").get("options.packages.find", {}).get("where", "src")
    )


@myke.cache()
def _get_package_dirs() -> list[str]:
    return myke.sh_stdout_lines(
        f"""
    find "{_get_package_root()}" \
        -mindepth 2 -maxdepth 2 -name "__init__.py" -exec dirname {{}} \\;
    """
    )


@myke.cache()
def _get_project_name() -> str | None:
    # return myke.sh_stdout("python setup.py --name")
    return myke.read.cfg("setup.cfg").get("metadata", {}).get("name")


@myke.task
def x_py_get_version(_echo: bool = True) -> str:
    value: str = myke.sh_stdout("python setup.py --version")
    if _echo:
        print(value)
    return value


def _assert_unpublished(
    repository: str | None = None,
    version: str | None = None,
) -> list[str]:
    vers_published: list[str] = x_py_get_published(repository=repository, _echo=False)

    if not version:
        version = x_py_get_version(_echo=False)

    if version in vers_published:
        raise SystemExit(
            ValueError(f"Version {version} already published; increment to continue.")
        )

    return vers_published


def _get_next_version(
    repository: str | None = None,
    version: str | None = None,
) -> str:
    if not version:
        version = os.getenv("CI_COMMIT_TAG", None)
        if not version:
            if os.path.exists(VERSION_FILE):
                version = myke.read(VERSION_FILE)
            else:
                version = "0.0.1a1"

    vers_published: list[str] = _assert_unpublished(
        repository=repository, version=version
    )

    # if in CI, but no tag, append next '.dev#' to version
    if os.getenv("CI") and not os.getenv("CI_COMMIT_TAG"):
        i: int = 0
        ver_suffix: str = f"dev{i}"
        next_dev_version: str = f"{version}.{ver_suffix}"
        while next_dev_version in vers_published:
            i += 1
            ver_suffix = f"dev{i}"
            next_dev_version = f"{version}.{ver_suffix}"
        version = next_dev_version

    if not os.path.exists(VERSION_FILE):
        x_py_set_version(version, _echo=False)

    return version


@myke.task
def x_py_set_version(
    version=myke.arg(None, pos=True),
    repository: str | None = None,
    _echo: bool = True,
) -> None:
    version_og: str | None = None
    try:
        version_og = x_py_get_version(_echo=False)
    except myke.exceptions.CalledProcessError:
        pass

    if not version:
        version = _get_next_version(version=version, repository=repository)

    if version_og != version:
        if _echo:
            print(f"{version_og} --> {version}")
        myke.write(path=VERSION_FILE, content=version + os.linesep, overwrite=True)

        if not os.path.exists("MANIFEST.in"):
            myke.write(path="MANIFEST.in", content=f"include {VERSION_FILE}")

        myke.sh(
            r"sed 's/^version.*/version = file: VERSION/' setup.cfg > setup.cfg.tmp "
            r"&& mv setup.cfg.tmp setup.cfg"
        )

    assert version == x_py_get_version(_echo=False)

    for pkg in _get_package_dirs():
        myke.write(
            content=f'__version__ = "{version}"' + os.linesep,
            path=os.path.join(pkg, "__version__.py"),
            overwrite=True,
        )


@myke.task_sh
def x_py_clean():
    return r"""
rm -rf dist build public src/*.egg-info .mypy_cache .pytest_cache .coverage .hypothesis .tox
find . -type f -name "*.rej" -delete
find . -type d -name "__pycache__" | xargs -r rm -rf
"""


@myke.task
def x_py_env(
    version=None,
    name=None,
    extras: list[str] | None = None,
    quiet=False,
) -> None:
    x_py_clean()

    if version:
        myke.sh(f"pyenv local {version}")
    elif os.path.exists(PYENV_VERSION_FILE):
        os.rename(PYENV_VERSION_FILE, PYENV_VENV_FILE)

    if not name:
        name = _get_project_name()

    myke.sh(
        f"""
export PYENV_VIRTUALENV_DISABLE_PROMPT=1 \\
&& pyenv virtualenv-delete -f {name} \\
&& pyenv virtualenv {name} \\
&& mv {PYENV_VENV_FILE} {PYENV_VERSION_FILE} \\
&& pyenv local {name}
"""
    )

    core_reqs = ["pip", "setuptools", "wheel"]

    core_reqs_str: str = "'" + "' '".join(core_reqs) + "'"
    myke.sh(f"pip install --upgrade {core_reqs_str}")

    x_py_requirements(extras=extras, quiet=quiet)


@myke.task
def x_py_requirements(
    extras: list[str] | None = None,
    quiet: bool = False,
) -> None:
    setup_cfg: dict[str, Any] = myke.read.cfg("setup.cfg")

    install_requires: list[str] = [
        x
        for x in setup_cfg.get("options", {}).get("install_requires", "").splitlines()
        if x
    ]

    extras_require: dict[str, str] = setup_cfg.get("options.extras_require", {})

    if extras:
        if not extras_require:
            raise ValueError("Missing value for 'options.extras_require'")
        for e in extras:
            if e not in extras_require:
                raise ValueError(
                    f"Extra requirement '{e}' not one of: "
                    f"{','.join(extras_require.keys())}"
                )

    extra_reqs: list[str] = [
        req
        for grp, reqs in extras_require.items()
        if (not extras or grp in extras)
        for req in reqs.strip().splitlines()
        if req
    ]

    quiet_flag: str = ""
    if quiet:
        quiet_flag = "-q"

    for reqs in install_requires, extra_reqs:
        if reqs:
            reqs = [x.replace("'", '"') for x in reqs]
            reqs_str: str = "'" + "' '".join(reqs) + "'"
            myke.sh(f"pip install {quiet_flag} {reqs_str}")


@myke.task
def x_py_get_published(
    repository: str | None = None, name: str | None = None, _echo: bool = True
) -> list[str]:
    if not name:
        name = _get_project_name()

    pip_args: str = ""
    if repository and repository != "pypi":
        pypirc: str = os.path.join(os.path.expanduser("~"), ".pypirc")
        repo_conf: dict[str, dict[str, str]] = myke.read.cfg(pypirc)
        if repository not in repo_conf:
            raise ValueError(f"Specified repo '{repository}' not found in '{pypirc}'")
        repo_key: str = "repository"
        repo_url: str | None = repo_conf.pop(repository).get(repo_key)
        if not repo_url:
            raise ValueError(
                f"Specified repo '{repository}' has no property '{repo_key}'"
            )

        from urllib.parse import ParseResult, urlparse

        url_parts: ParseResult = urlparse(repo_url)
        pip_args = (
            f"--trusted-host '{url_parts.netloc}' --index-url '{repo_url}/simple'"
        )

    values: list[str] = myke.sh_stdout_lines(
        f"pip install --disable-pip-version-check {pip_args} {name}== 2>&1"
        r" | tr ' ' '\n' | tr -d ',' | tr -d ')' | grep '^v\?[[:digit:]]'"
        r" || true"
    )

    if _echo:
        myke.echo.lines(values)

    return values


@myke.task_sh
def x_py_format() -> str:
    from glob import glob

    pkg_root: str = _get_package_root()

    for p in pkg_root, "tests":
        for f in glob(f"{p}/**/*.py", recursive=True):
            myke.sh(
                f"python -m pyupgrade --py37-plus --exit-zero-even-if-changed '{f}'"
            )

    return f"""
python -m autoflake {pkg_root} ./tests
python -m isort {pkg_root} ./tests
python -m black {pkg_root} ./tests
"""


@myke.task_sh
def x_py_check() -> str:
    dirs: list[str] = [_get_package_root(), "./tests"]
    joined_dirs = " ".join(dirs)

    return f"""
python -m flake8 {joined_dirs} || true
python -m pylint -f colorized {joined_dirs} || true
python -m mypy --install-types --non-interactive --html-report public/coverage-types || true
"""


@myke.task
def x_py_test(reports: bool = False) -> None:
    report_args: str = ""

    if reports:
        report_args = f""" \\
        --cov-report xml:{REPORT_DIR}/coverage.xml \\
        --cov-report html:{REPORT_DIR}/coverage \\
        --html {REPORT_DIR}/tests/index.html
        """

    myke.sh(
        f"""
PYTHONPATH={_get_package_root()} pytest --cov=src --cov-report term {report_args}
"""
    )


def _get_pyenv_versions() -> list[str]:
    return [
        x for x in myke.sh_stdout_lines("pyenv versions") if myke.utils.is_version(x)
    ]


@myke.task
def x_py_test_tox() -> None:
    env: dict[str, str] = os.environ.copy()
    cur_ver: str = myke.sh_stdout("pyenv version-name")
    env["PYENV_VERSION"] = ":".join([cur_ver] + _get_pyenv_versions())
    myke.sh("tox", env=env)


# @myke.task
# def x_py_test_versions() -> None:
#     og_venv: Optional[str] = None
#     if os.path.exists(PYENV_VERSION_FILE):
#         og_venv = myke.read(PYENV_VERSION_FILE)

#     proj_name: str = _get_project_name()

#     try:
#         for ver in _get_pyenv_versions():
#             test_env_name = f"test-{proj_name}"
#             x_py_env(ver, name=test_env_name, extras=["tests"], quiet=True)
#             x_py_test()
#             myke.sh(f"pyenv virtualenv-delete -f {test_env_name}")
#     finally:
#         myke.sh(f"pyenv local {proj_name}")
#         if og_venv:
#             myke.write(
#                 path=PYENV_VERSION_FILE, content=og_venv + os.linesep, overwrite=True
#             )


@myke.task
def x_py_mkdocs(serve: bool = False) -> None:

    if serve:
        myke.sh(r"PYTHONPATH=src mkdocs serve --config-file config/mkdocs.yml")
    else:
        myke.sh(r"PYTHONPATH=src mkdocs build --clean --config-file config/mkdocs.yml")

        myke.sh(
            r"""
    echo "<h1>{CI_REPO_NAME}</h1>" > {REPORT_DIR}/index.html
    echo "<h2>Reports:</h2>" >> {REPORT_DIR}/index.html
    echo '<ul style="font-size: 1.5em">' >> {REPORT_DIR}/index.html
    find {REPORT_DIR} -mindepth 1 -maxdepth 1 -type d | sort | while read -r dir; do \
        BASE_DIR="$(basename "$dir")" \
        && echo "<li><a href='$BASE_DIR/' target='_blank'>$BASE_DIR</a></li>" >> {REPORT_DIR}/index.html; \
    done
    echo '</ul>' >> {REPORT_DIR}/index.html
    echo "<p>Ref: {CI_REF}</p>" >> {REPORT_DIR}/index.html
    """.format(
                REPORT_DIR=REPORT_DIR,
                CI_REPO_NAME=os.getenv("CI_REPO_NAME", _get_project_name()),
                CI_REF=os.getenv(
                    "CI_COMMIT_TAG", os.getenv("CI_COMMIT_SHA", "undefined")
                ),
            )
        )


@myke.task
def x_py_reports() -> None:
    x_py_clean()
    x_py_check()
    x_py_test(reports=True)
    x_py_mkdocs()


@myke.task_sh
def x_py_build() -> str:
    return r"""
python -m build
python -m twine check --strict dist/*
pip install --force-reinstall dist/*.whl
"""


@myke.task_sh
def x_py_publish(repository: str = "testpypi", build: bool = False) -> str:
    if build:
        x_py_build()

    return f"""
python -m twine upload --verbose --non-interactive -r {repository} dist/*
"""


@myke.task
def x_py_init() -> None:
    x_py_set_version(None)
    x_py_env()
    x_py_reports()


if __name__ == "__main__":
    myke.main(__file__)
