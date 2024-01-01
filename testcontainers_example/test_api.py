from fastapi.testclient import TestClient
from testcontainers.core.container import DockerContainer
import pytest
import time

@pytest.fixture(scope="session")
def fastapi_service():
    with DockerContainer("tiangolo/uvicorn-gunicorn-fastapi:python3.7") as container:
        container.with_exposed_ports(80)
        container.with_bind_mount("./", "/app")
        container.with_env("MODULE_NAME", "app")
        container.with_env("VARIABLE_NAME", "read_root")
        container.start()
        time.sleep(2)  # Wait a bit for the server to start
        url = f"http://{container.get_container_host_ip()}:{container.get_exposed_port(80)}"
        yield TestClient(url)

def test_read_main(fastapi_service):
    response = fastapi_service.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
