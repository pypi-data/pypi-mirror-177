import pytest
from _pytest.fixtures import FixtureRequest
from jelastic_client import JelasticClientFactory
from jelastic_client.env_info import EnvInfo


def pytest_addoption(parser):
    parser.addoption(
        "--jelastic-api-url",
        action="store",
        required=True,
        type=str,
        help="Jelastic API Url",
    )
    parser.addoption(
        "--jelastic-access-token",
        action="store",
        required=True,
        type=str,
        help="Jelastic Access Token",
    )
    parser.addoption(
        "--jelastic-env-name",
        action="store",
        required=True,
        type=str,
        help="Jelastic Environment Name",
    )


@pytest.fixture(scope="session")
def jelastic_env_name(request: FixtureRequest) -> str:
    jelastic_env_name = request.config.getoption("--jelastic-env-name")
    return jelastic_env_name


@pytest.fixture(scope="session")
def jelastic_api_url(request: FixtureRequest) -> str:
    return request.config.getoption("--jelastic-api-url")


@pytest.fixture(scope="session")
def jelastic_access_token(request: FixtureRequest) -> str:
    return request.config.getoption("--jelastic-access-token")


@pytest.fixture(scope="session")
def jelastic_env_info(
    jelastic_api_url: str, jelastic_access_token: str, jelastic_env_name: str
) -> EnvInfo:
    client_factory = JelasticClientFactory(jelastic_api_url, jelastic_access_token)
    control_client = client_factory.create_control_client()
    env_info = control_client.get_env_info(jelastic_env_name)
    return env_info
