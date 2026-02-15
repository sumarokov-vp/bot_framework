from typing import Any, Protocol


class IFileDownloaderBot(Protocol):
    def get_file(self, file_id: str) -> Any: ...

    def download_file(self, file_path: str) -> bytes: ...
