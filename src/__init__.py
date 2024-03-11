from flask import Flask

from .app import create_app


def main() -> Flask:
    app = create_app()

    return app


if __name__ == "__main__":
    raise SystemExit(main())
