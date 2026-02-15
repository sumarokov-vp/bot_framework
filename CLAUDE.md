# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Bot Framework — переиспользуемая Python-библиотека для создания ботов на любых платформах. Предоставляет готовые компоненты: управление диалоговыми flow, роли и права пользователей, мультиязычность. Построена на принципах Clean Architecture с принудительным контролем зависимостей между слоями. Платформо-специфичные реализации вынесены в отдельные модули (сейчас реализован Telegram, планируются другие платформы).

## Commands

```bash
# Dependency management (using uv)
uv add <package>           # Add production dependency
uv add --dev <package>     # Add development dependency
uv sync                    # Install/sync all dependencies

# Testing
pytest                     # Run all tests
pytest tests/test_file.py  # Run specific test file
pytest -k "test_name"      # Run tests matching pattern

# Linting and type checking (runs automatically via hooks after .py edits)
ruff check .               # Lint check
ruff format .              # Format code
mypy .                     # Type check with mypy
pyright                    # Type check with pyright
lint-imports               # Check import layer violations
```

## Architecture

Библиотека следует Clean Architecture с принудительным контролем импортов (import-linter).

### Layer Hierarchy (top to bottom)

Layers can only import from layers below them (4 layers instead of 13):

```
bot_framework/
├── app/                          # Layer 4: Application (bot_application, migrations)
├── features/                     # Layer 3: Features (user scenarios)
│   ├── menus/                    #   Pre-built menu handlers
│   └── flows/                    #   Dialog flows (request_role_flow)
├── platform/                     # Layer 2: Platform implementations
│   └── telegram/                 #   Telegram-specific (messenger, middleware, registries)
├── domain/                       # Layer 1: Domain logic
│   ├── flow_management/          #   Flow stack navigation (Redis storage)
│   ├── role_management/          #   User roles and permissions
│   ├── language_management/      #   Multilingual phrase support
│   ├── services/                 #   Utility services (formatters, calculators)
│   └── decorators/               #   Role checking decorators
├── core/                         # Layer 0: Foundation (no internal deps)
│   ├── protocols/                #   Abstract interfaces (I-prefixed)
│   ├── entities/                 #   Domain models (Pydantic)
│   └── base_protocols/           #   Generic CRUD protocols
└── data/                         # Static data (outside layers)
```

Dependencies: `app → features → platform → domain → core`

### Key Modules

- **bot_framework.platform.telegram** - Telegram implementations: `TelegramMessenger`, middleware (`EnsureUserMiddleware`), callback/message registries
- **bot_framework.domain.flow_management** - Dialog flow stack with Redis storage: `FlowStackNavigator`, `FlowRegistry`, `RedisFlowStackStorage`
- **bot_framework.domain.role_management** - User roles: `RoleRepo`, `UserRole` entity
- **bot_framework.domain.language_management** - Multilingual: `PhraseRepo`, `LanguageRepo`
- **bot_framework.features.menus** - Pre-built menus: `StartCommandHandler`, `MainMenuSender`, `CommandsMenuSender`
- **bot_framework.features.flows.request_role_flow** - Complete role request flow with factory

### Protocol Pattern

All interfaces use `I` prefix and are Protocol classes. Implementations are in separate modules:
- `core/protocols/i_message_sender.py` → `platform/telegram/services/telegram_messenger.py`

### Role Checking Decorators

Use `@check_roles` for callbacks and `@check_message_roles` for messages. Class must have:
- `allowed_roles: set[RoleName]`
- `role_repo: IRoleRepo`
- `callback_answerer` / `message_sender` (optional, for user feedback)

## Tech Stack

- Python 3.13+
- pyTelegramBotAPI (Telegram Bot API)
- PostgreSQL with psycopg (sync driver)
- Redis (flow state, caching)
- Pydantic (validation)

## Telegram API Null Handling

Fields like `message.from_user`, `callback_query.from_user`, `message.contact` can be `None`. Always check before use:
```python
if not message.from_user:
    raise ValueError("message.from_user is required but was None")
```
