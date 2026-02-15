import re

from bot_framework.platform.telegram.protocols.i_markdown_escaper import IMarkdownEscaper


class MarkdownEscaper(IMarkdownEscaper):
    def escape(self, text: str) -> str:
        return re.sub(r"([_*\[\]()~`>#+=|{}.!-])", r"\\\1", text)
