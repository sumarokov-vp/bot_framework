from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class MissingTranslationsValidator:
    def validate_and_log_missing(
        self,
        library_languages_path: Path,
        library_phrases_path: Path,
        client_languages_path: Path | None,
        client_phrases_path: Path | None,
        reference_language: str = "ru",
    ) -> None:
        library_language_codes = self._load_language_codes(library_languages_path)
        client_language_codes = (
            self._load_language_codes(client_languages_path)
            if client_languages_path and client_languages_path.exists()
            else set()
        )

        new_language_codes = client_language_codes - library_language_codes
        if not new_language_codes:
            return

        library_phrases = self._load_phrases(library_phrases_path)
        client_phrases = (
            self._load_phrases(client_phrases_path)
            if client_phrases_path and client_phrases_path.exists()
            else {}
        )

        missing_by_language: dict[str, dict[str, str]] = {}

        for lang_code in new_language_codes:
            missing_by_language[lang_code] = {}

            for phrase_key, library_translations in library_phrases.items():
                has_in_library = lang_code in library_translations
                has_in_client = (
                    phrase_key in client_phrases
                    and lang_code in client_phrases[phrase_key]
                )

                if not has_in_library and not has_in_client:
                    reference_text = library_translations.get(reference_language, "")
                    missing_by_language[lang_code][phrase_key] = reference_text

        for lang_code, phrases in missing_by_language.items():
            if not phrases:
                continue

            reference_lines = "\n".join(
                f'  "{key}": "{text}"' for key, text in phrases.items()
            )

            template_lines = "\n".join(
                f'  "{key}": {{\n    "{lang_code}": "<TRANSLATE>"\n  }}'
                for key in phrases
            )

            logger.warning(
                "Missing %s translations detected.\n\n"
                "Russian reference texts (translate these):\n%s\n\n"
                "Add translations to your phrases.json:\n{\n%s\n}",
                lang_code.upper(),
                reference_lines,
                template_lines,
            )

    def _load_language_codes(self, path: Path) -> set[str]:
        if not path.exists():
            return set()

        with path.open(encoding="utf-8") as f:
            data = json.load(f)

        languages = data.get("languages", [])
        return {lang["code"] for lang in languages}

    def _load_phrases(self, path: Path) -> dict[str, dict[str, str]]:
        if not path.exists():
            return {}

        with path.open(encoding="utf-8") as f:
            return json.load(f)
