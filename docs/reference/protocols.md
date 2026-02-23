# Протоколы

Все межслойные зависимости описаны через Protocol-интерфейсы с префиксом `I`.

## Протоколы сообщений

| Протокол | Метод | Описание |
|----------|-------|----------|
| `IMessageSender` | `send()` | Отправка сообщения |
| `IMessageReplacer` | `replace()` | Редактирование сообщения |
| `IMessageDeleter` | `delete()` | Удаление сообщения |
| `IDocumentSender` | `send_document()` | Отправка файла |
| `ICallbackAnswerer` | `answer()` | Ответ на callback query |

## Реестры обработчиков

| Протокол | Описание |
|----------|----------|
| `ICallbackHandlerRegistry` | Регистрация callback-обработчиков |
| `IMessageHandlerRegistry` | Регистрация message-обработчиков |

## Репозитории

| Протокол | Слой | Описание |
|----------|------|----------|
| `IRoleRepo` | domain | Получение ролей пользователя |
| `IUserRepo` | domain | CRUD операции с пользователями |
| `IPhraseRepo` | domain | Получение фраз по ключу и языку |
| `ILanguageRepo` | domain | Управление доступными языками |

## Flow

| Протокол | Описание |
|----------|----------|
| `IStepStateStorage` | Хранение state для flow |
| `IFlowStackStorage` | Хранение стека flow |
