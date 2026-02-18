from typing import Any, Protocol


class IMessageSenderBot(Protocol):
    """Низкоуровневый интерфейс бота платформы для отправки сообщений.

    Абстрагирует API конкретной платформы (Telegram, Facebook и др.).
    Используется внутри реализаций IMessageSender.

    Внутренний интерфейс библиотеки — не предназначен для использования
    в клиентском коде. Используйте IMessageSender.
    """

    def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str | None = None,
        reply_markup: Any = None,
        message_thread_id: int | None = None,
    ) -> Any:
        """Отправить текстовое сообщение через API платформы.

        Args:
            chat_id: ID чата получателя.
            text: Текст сообщения.
            parse_mode: Режим форматирования (например, "HTML", "Markdown").
            reply_markup: Разметка клавиатуры в формате платформы.
            message_thread_id: ID треда для отправки в топик (если поддерживается).
        """
        ...

    def edit_message_text(
        self,
        text: str,
        chat_id: int,
        message_id: int,
        parse_mode: str | None = None,
        reply_markup: Any = None,
    ) -> Any:
        """Редактировать текст ранее отправленного сообщения.

        Args:
            text: Новый текст сообщения.
            chat_id: ID чата.
            message_id: ID сообщения для редактирования.
            parse_mode: Режим форматирования.
            reply_markup: Обновлённая разметка клавиатуры.
        """
        ...

    def delete_message(self, chat_id: int, message_id: int) -> bool:
        """Удалить сообщение из чата.

        Args:
            chat_id: ID чата.
            message_id: ID сообщения для удаления.
        """
        ...

    def send_document(
        self,
        chat_id: int,
        document: Any,
    ) -> Any:
        """Отправить документ (файл) в чат.

        Args:
            chat_id: ID чата получателя.
            document: Файл в формате платформы (file_id, bytes, path).
        """
        ...
