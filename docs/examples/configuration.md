# Конфигурация

## Роли (`data/roles.json`)

Определяет доступные роли в системе:

```json
{
  "roles": [
    {"name": "admin", "description": "Администратор"},
    {"name": "manager", "description": "Менеджер"}
  ]
}
```

Роли загружаются при старте `BotApplication`. Назначение ролей пользователям хранится в PostgreSQL.

## Фразы (`data/phrases.json`)

Определяет тексты сообщений на всех поддерживаемых языках:

```json
{
  "mybot.greeting": {
    "ru": "Привет!",
    "en": "Hello!"
  },
  "registration.ask_name": {
    "ru": "Как вас зовут?",
    "en": "What is your name?"
  }
}
```

Каждый ключ — уникальный идентификатор фразы. Значение — объект с переводами, где ключ — код языка.

## Переменные окружения

| Переменная | Описание |
|-----------|----------|
| `BOT_TOKEN` | Токен Telegram-бота (от @BotFather) |
| `DATABASE_URL` | URL подключения к PostgreSQL |
| `REDIS_URL` | URL подключения к Redis |
