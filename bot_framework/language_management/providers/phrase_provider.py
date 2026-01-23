from bot_framework.language_management.providers.protocols import IPhraseProvider
from bot_framework.language_management.repos import PhraseRepo


class PhraseProvider(IPhraseProvider):
    def __init__(self, database_url: str) -> None:
        self._repo = PhraseRepo(database_url=database_url)

    def get_phrase(self, key: str, language_code: str) -> str:
        return self._repo.get_phrase(key=key, language_code=language_code)
