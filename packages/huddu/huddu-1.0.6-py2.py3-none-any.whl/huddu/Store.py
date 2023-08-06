from typing import List

from ._exceptions import SafePutException
from ._responses import make_response
from ._sessions import Session


class Store:
    def __init__(
            self, token: str, collection: str, region: str, base_url: str = "https://connect.huddu.io"
    ):
        self.session = Session(collection, token, region, base_url)

    def put(self, id: str, data: str, safe: bool = True):
        if safe:
            if self.get(id):
                raise SafePutException("Another entry with the same id already exists")

        self.session.create_documents([{"id": id, "data": data}])

    def update(self, id: str, data: str):
        self.session.create_documents([{"id": id, "data": data}])

    def delete(self, id: str):
        self.session.delete_documents([id])

    def fetch(
            self,
            ids: List[str] = None,
            skip: int = 0,
            limit: int = 25,
            start: int = None,
            end: int = None,
    ):
        res = self.session.list_documents(
            ids=ids, skip=skip, limit=limit, start=start, end=end
        )["data"]

        if len(res) > 0:
            return make_response(res)
        return None

    def get(
            self,
            id: str,
            start: int = None,
            end: int = None,
    ):
        res = self.session.list_documents(
            ids=[id], skip=0, limit=1, start=start, end=end
        )["data"]

        res = make_response([res[0]])
        if len(res) > 0:
            return res[0]
        return None
