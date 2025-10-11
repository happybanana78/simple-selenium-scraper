import os, time, platform, requests
from typing import Optional
from docker import DockerClient
from docker.models.containers import Container


class SeleniumContainer:
    def __init__(self, client, port):
        self.client:DockerClient = client
        self.port:int = port
        self.container:Optional[Container] = None
        self.max_retries:int = 10
        self.retry_interval:int = 3  # seconds
        self.container_name:str = f"selenium-{port}"


    def start(self):
        env_vars = {
            'VNC_PASSWORD': os.environ.get('SELENIUM_PASSWORD', 'password'),
        }

        network = os.environ.get('DOCKER_NETWORK_NAME') if os.environ.get('DEBUG') == 'False' else 'bridge'

        arch = platform.machine()
        if arch in ("x86_64", "AMD64"):
            image = "selenium/standalone-chromium"
        else:
            image = "seleniarm/standalone-chromium"

        try:
            self.container = self.client.containers.run(
                image,
                detach=True,
                ports={'4444/tcp': self.port},
                shm_size="4g",
                environment=env_vars,
                network=network,
                name=self.container_name,
            )
        except Exception as e:
            raise Exception(f"Container failed to start properly: {e}")

        if not self.container:
            raise Exception("Container failed to start properly")

        self.container.reload()
        if not self.wait_for_container_running():
            raise Exception("Container failed to start properly")

        if not self.wait_for_selenium_ready():
            self.container.stop()
            self.container.remove()
            raise Exception("Selenium server failed to start within the timeout period")


    def wait_for_container_running(self):
        retries = 0

        while retries < self.max_retries:
            self.container.reload()
            if self.container.status == 'running':
                return True

            time.sleep(self.retry_interval)
            retries += 1
        return False


    def wait_for_selenium_ready(self):
        retries = 0

        if os.environ.get('DEBUG') == 'True':
            url = f"http://localhost:{self.port}/wd/hub/status"
        else:
            url = f"http://{self.container_name}:4444/wd/hub/status"

        while retries < self.max_retries:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return True
            except Exception:
                pass

            time.sleep(self.retry_interval)
            retries += 1

        return False
