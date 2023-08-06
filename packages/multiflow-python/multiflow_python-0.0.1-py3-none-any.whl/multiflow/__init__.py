import os
from typing import List, Optional
import requests
from dataclasses import dataclass
import json


def run_workflow(workflow_id: str, api_key: str, args: List[str]) -> List[str]:
    assert api_key is not None, "api_key not provided"
    headers = {
        "accept": "application/json",
    }
    json_data = {
        "apiKey": api_key,
        "args": args,
    }
    response = requests.post(
        f"https://prometheus-api.llm.llc/api/workflow/{workflow_id}",
        headers=headers,
        json=json_data,
    )
    return json.loads(response.content.decode("utf-8"))


def get_type_signature(workflow_id: str, api_key: str):
    url = f"https://prometheus-api.llm.llc/api/workflow/{workflow_id}?apiKey={api_key}"
    headers = {"accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.content.decode("utf-8"))


@dataclass
class Workflow:
    id: str
    api_key: Optional[str] = None

    def __post_init__(self):
        self.api_key = os.environ.get("MULTIFLOW_API_KEY", None)

    def run(self, *args, api_key: Optional[str] = None):
        return run_workflow(self.id, api_key or self.api_key, args)

    def type_signature(self, api_key: Optional[str] = None):
        return get_type_signature(self.id, api_key or self.api_key)
