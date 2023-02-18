import os
import argparse
import shutil
import sys

VENV_PATH = ".venv"
PYTHON_BIN = sys.executable


def getBinPath():
    if os.name == "posix":
        return rf"{VENV_PATH}/bin"
    else:
        return rf"{VENV_PATH}\Scripts"


def main():
    if args.reinstall or args.clean:
        shutil.rmtree(VENV_PATH)
        print(f"Removed {VENV_PATH}")
        if args.clean:
            return
    if not os.path.exists(VENV_PATH):
        if os.name == "posix":
            os.system(f"sudo apt install {PYTHON_BIN}-venv")
        os.system(f"{PYTHON_BIN} -m venv {VENV_PATH}")
        print(f"Created {VENV_PATH}")
    print("Installing dependencies")
    os.system(f"{os.path.join(getBinPath(), 'pip')} install -r setup/requirements.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup script.")
    parser.add_argument("--reinstall", action="store_true", help="Force clean install.")
    parser.add_argument(
        "--clean", action="store_true", help="Removes all dependencies."
    )
    args = parser.parse_args()
    main()
    print("Done")