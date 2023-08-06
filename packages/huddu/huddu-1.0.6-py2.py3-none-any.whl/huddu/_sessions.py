import json

import requests

from ._exceptions import APIException


class Session:
    def __init__(
            self, collection: str, token: str, region: str, base_url: str = "https://connect.huddu.io"
    ):
        self.collection = collection
        self.token = token
        self.region = region
        self.base_url = base_url

    def _request(self, method, params: dict = None, data: dict = None):
        headers = {"Authorization": f"Token {self.token}",
                   "Collection": self.collection,
                   "Region": self.region
                   }

        if data:
            res = requests.request(
                method,
                f"{self.base_url}/documents",
                data=json.dumps(data),
                headers=headers,
            )
        else:
            res = requests.request(
                method, f"{self.base_url}/documents", params=params, headers=headers
            )

        if res.status_code > 299:
            raise APIException(res.json())
        return res.json()

    def create_documents(self, items: list):
        for i in items:
            try:
                i["data"] = json.dumps(i["data"])
            except:
                i["data"] = str(i["data"])
                
        return self._request("POST", data={"items": items})

    def list_documents(
            self,
            ids: list = None,
            limit: int = 25,
            skip: int = 0,
            start: int = 0,
            end: int = 0,
    ):
        params = {}

        if ids:
            params["ids"] = ",".join(ids)
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if limit:
            params["limit"] = limit
        if skip:
            params["skip"] = skip

        return self._request("GET", params=params)

    def delete_documents(self, ids: list):
        return self._request("DELETE", data={"ids": ids})
