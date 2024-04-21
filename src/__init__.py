from flask import Flask
from beartype.claw import beartype_this_package

from src.app import create_app


def main() -> Flask:
    app = create_app()

    return app


if __name__ == "__main__":
    beartype_this_package()
    raise SystemExit(main())
