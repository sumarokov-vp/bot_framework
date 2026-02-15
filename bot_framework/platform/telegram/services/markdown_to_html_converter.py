import html
import re

from bot_framework.platform.telegram.protocols import IMarkdownToHtmlConverter


class MarkdownToHtmlConverter(IMarkdownToHtmlConverter):
    def convert(self, text: str) -> str:
        result = html.escape(text)
        result = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', result)
        result = re.sub(r'__(.+?)__', r'<u>\1</u>', result)
        result = re.sub(r'\*(.+?)\*', r'<i>\1</i>', result)
        result = re.sub(r'_(.+?)_', r'<i>\1</i>', result)
        result = re.sub(r'~~(.+?)~~', r'<s>\1</s>', result)
        result = re.sub(r'`(.+?)`', r'<code>\1</code>', result)
        return result
