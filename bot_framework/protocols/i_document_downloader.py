from typing import Protocol


class IDocumentDownloader(Protocol):
    def download_document(self, file_id: str) -> bytes: ...
