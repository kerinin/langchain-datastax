from __future__ import annotations

import os
from pathlib import Path
from typing import TypedDict

import pytest
from astrapy import Database
from astrapy.db import AstraDB

# Getting the absolute path of the current file's directory
ABS_PATH = (Path(__file__)).parent

# Getting the absolute path of the project's root directory
PROJECT_DIR = Path(ABS_PATH).parent.parent


# Loading the .env file if it exists
def _load_env() -> None:
    dotenv_path = Path(PROJECT_DIR) / "tests" / "integration_tests" / ".env"
    if Path(dotenv_path).exists():
        from dotenv import load_dotenv

        load_dotenv(dotenv_path)


def _has_env_vars() -> bool:
    return all(
        [
            "ASTRA_DB_APPLICATION_TOKEN" in os.environ,
            "ASTRA_DB_API_ENDPOINT" in os.environ,
        ]
    )


class AstraDBCredentials(TypedDict):
    token: str
    api_endpoint: str
    namespace: str | None
    environment: str | None


@pytest.fixture(scope="session")
def astra_db_credentials() -> AstraDBCredentials:
    return {
        "token": os.environ["ASTRA_DB_APPLICATION_TOKEN"],
        "api_endpoint": os.environ["ASTRA_DB_API_ENDPOINT"],
        "namespace": os.environ.get("ASTRA_DB_KEYSPACE"),
        "environment": os.environ.get("ASTRA_DB_ENVIRONMENT"),
    }


@pytest.fixture(scope="session")
def database(astra_db_credentials: AstraDBCredentials) -> Database:
    return Database(
        token=astra_db_credentials["token"],
        api_endpoint=astra_db_credentials["api_endpoint"],
        namespace=astra_db_credentials["namespace"],
        environment=astra_db_credentials["environment"],
    )


@pytest.fixture(scope="session")
def core_astra_db(astra_db_credentials: AstraDBCredentials) -> AstraDB:
    return AstraDB(
        token=astra_db_credentials["token"],
        api_endpoint=astra_db_credentials["api_endpoint"],
        namespace=astra_db_credentials["namespace"],
    )


_load_env()
