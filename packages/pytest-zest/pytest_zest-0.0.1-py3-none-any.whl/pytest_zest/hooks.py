def pytest_addoption(parser):

    group = parser.getgroup("collect")
    group.addoption(
        "--zest",
        action="store_true",
        default=False,
        help="Enable pytest-zest",
        dest="pytest_alembic_enabled",
    )
