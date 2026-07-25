import requests
class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8001"):
        self.base_url = base_url.rstrip("/")
        self.execution_timeout = 1800  
    def execute(self, goal: str):
        response = requests.post(
            f"{self.base_url}/execute",
            json={"goal": goal},
            timeout=self.execution_timeout,
        )
        response.raise_for_status()
        return response.json()
    def _upload(self, endpoint: str, file, content_type: str):
        files = {
            "file": (
                file.name,
                file,
                content_type,
            )
        }
        response = requests.post(
            f"{self.base_url}{endpoint}",
            files=files,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
    def upload_pdf(self, file):
        return self._upload("/upload/pdf", file, "application/pdf")
    def upload_csv(self, file):
        return self._upload("/upload/csv", file, "text/csv")
    def upload_database(self, file):
        return self._upload("/upload/db", file, "application/octet-stream")
    def history(self):
        response = requests.get(
            f"{self.base_url}/history",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    def execution(self, execution_id):
        response = requests.get(
            f"{self.base_url}/execution/{execution_id}",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    def health(self):
        response = requests.get(
            f"{self.base_url}/health",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
client = APIClient()