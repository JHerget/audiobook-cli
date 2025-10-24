from typing import Callable
import requests as req

class AudiobookApi:
    def __init__(self):
        self.base_url = "https://audiobooks.rumahbatu.online/audiobookshelf/api"
        self.library_id = "7de6c400-dba1-4db3-a3b4-b0f1b8eef92d"
        self.client = req.Session()

    def set_token(self, token: str) -> None:
        self.client.headers.update({ "Authorization": f"Bearer {token}"})

    def get_token(self):
        token = self.client.headers.get("Authorization", "")

        if not token:
            return ""

        return token.split()[-1]

    def login(self, username: str, password: str) -> req.Response:
        response = self.client.post(
            "https://audiobooks.rumahbatu.online/audiobookshelf/login",
            json={
                "username": username,
                "password": password
            }
        )

        if response.ok:
            token = response.json()["user"]["token"]
            self.set_token(token)

        return response

    def get_books(self, sort: str = "media.metadata.title") -> req.Response:
        return self.client.get(
            f"{self.base_url}/libraries/{self.library_id}/items",
            params={
                "sort": sort
            }
        )

    def get_book(self, book_id: str) -> req.Response:
        return self.client.get(
            f"{self.base_url}/items/{book_id}",
        )

    def get_authors(self, sort: str = "name") -> req.Response:
        return self.client.get(
            f"{self.base_url}/libraries/{self.library_id}/authors",
            params={
                "sort": sort
            }
        )

    def download_book(
        self,
        book_id: str,
        download_path: str,
        chunk_size: int = 8192,
        notify: Callable[[float], None] | None = None
    ) -> str:
        file_path = f"{download_path}/{book_id}.zip"

        with self.client.get(
            f"{self.base_url}/items/{book_id}/download",
            params={
                "token": self.get_token()
            },
            stream=True
        ) as r:
            total_size = 0

            book_response = self.get_book(book_id=book_id)
            if book_response.ok:
                files = book_response.json()["libraryFiles"]

                for file in files:
                    total_size += file["metadata"]["size"]

            downloaded = 0

            with open(file_path, "wb") as file:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if not chunk:
                        continue

                    file.write(chunk)
                    downloaded += len(chunk)

                    if notify:
                        notify(downloaded / total_size)

        return file_path
