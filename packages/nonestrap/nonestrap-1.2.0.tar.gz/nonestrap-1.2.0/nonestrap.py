from argparse import ArgumentParser
import os
from pathlib import Path
import pip._internal.main as pip_main
import py_compile
from shutil import SameFileError
import subprocess
import sys
from typing import List
import venv

ADAPTERS_L = (
    "onebot-v11", "ding", "feishu", "telegram", "qqguild", "kaiheila",
    "mirai2", "onebot-v12", "console", "github", "ntchat"
)

BOT_PY_T = """
import nonebot

nonebot.init()

app = nonebot.get_asgi()
driver = nonebot.get_driver()

{ADAPTER_LOAD}

nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
""".strip()

DOTENV_DEV = """
HOST=127.0.0.1
PORT=8080
DEBUG=true
FASTAPI_RELOAD=true
""".strip()

DOTENV_PROD = """
HOST=127.0.0.1
PORT=8080
""".strip()

DOTENV_ALL = """
SUPERUSERS=[]
COMMAND_START=["/", ""]
"""

PYPROJECT = """
[tool.nonebot]
plugins = [{PLUGINS}]
plugin_dirs = ["src/plugins"]
""".strip()


def createvenv(venv_path: Path):
    venv_path.mkdir(exist_ok=True)
    venv.create(venv_path, system_site_packages=False, with_pip=True)


def venvinstall(vp: Path, package: str):
    bindirname = ("Scripts" if sys.platform == "win32" else "bin")
    subprocess.run(
        [(vp / bindirname / "pip").absolute(), "install", "-U", package]
    )


def directinstall(_: Path, package: str):
    pip_main.main(["pip", "install", "-U", package])


def main(
    target: str, packages: List[str], adapters: List[str], env: str,
    _compile: bool, _venv: bool
):
    tp = Path(target)
    tp.mkdir(exist_ok=True)
    if _venv:
        venv_path = tp / ".venv"
        try:
            print("[NOTICE] Creating virtual environment...")
            createvenv(venv_path)
            print("[NOTICE] Successfully created a new virtual environment.")
        except SameFileError:
            print(
                "[NOTICE] Virtual environment already exists. "
                "Delete .venv manually if you don't need it "
                "or the environment is broken."
            )
        install_dir = venv_path
        install = venvinstall
    else:
        install_dir = Path()  # stub
        install = directinstall
    print("[NOTICE] Installing nonebot2...")
    install(install_dir, "nonebot2")
    if adapters:
        print("[NOTICE] Installing adapters for nonebot2...")
        adapter_l = []
        for adp in adapters:
            if adp.startswith("onebot-"):
                _adp = adp.replace("-", ".")
                _aim = adp.replace("-", "_")
                _ain = "onebot"
            else:
                _adp = _ain = _aim = adp
            install(install_dir, f"nonebot-adapter-{_ain}")
            adapter_l.append(
                f"from nonebot.adapters.{_adp} import Adapter as {_aim}"
            )
            adapter_l.append(f"driver.register_adapter({_aim})")
        adapter_t = "\n".join(adapter_l)
        print("[NOTICE] Creating entry file for the bot...")
        botpy = tp / "bot.py"
        with open(botpy, "w") as f:
            f.write(BOT_PY_T.format(ADAPTER_LOAD=adapter_t))
        if _compile:
            py_compile.compile(str(botpy), cfile=str(tp / "bot.pyc"))
            os.remove(botpy)
    print("[NOTICE] Generating misc files...")
    with open(tp / ".env", "w") as f:
        f.write(DOTENV_DEV if env == "dev" else DOTENV_PROD)
        f.write(DOTENV_ALL)
    for pkg in packages:
        install(install_dir, pkg)
    with open(tp / "pyproject.toml", "w") as f:
        f.write(
            PYPROJECT.format(
                PLUGINS=", ".join(
                    f'"{p.replace("-", "_")}"'
                    for p in packages
                    if p.startswith("nonebot-plugin-")
                )
            )
        )
    os.makedirs(tp / "src" / "plugins", exist_ok=True)
    print("[NOTICE] Done!")


def _entry():
    ap = ArgumentParser(
        "nonestrap", description="NoneBot2 bootstrap file generating tool"
    )
    ap.add_argument(
        "-a", "--adapter", action="append", choices=ADAPTERS_L,
        help="specify adapter to register"
    )
    ap.add_argument(
        "-e", "--dotenv", choices=("dev", "prod"), default="dev",
        help="choose .env style"
    )
    ap.add_argument(
        "-C", "--no-compile", action="store_false",
        help="whether not to compile bot.py"
    )
    ap.add_argument(
        "-V", "--no-venv", "--in-venv", action="store_false",
        help="whether not to use venv"
    )
    ap.add_argument("target", help="specify bootstrap target directory")
    ap.add_argument("package", nargs="*", help="install specified packages")
    args = ap.parse_args()
    # print(args)
    main(
        args.target, args.package, args.adapter, args.dotenv, args.no_compile,
        args.no_venv
    )


if __name__ == "__main__":
    _entry()
