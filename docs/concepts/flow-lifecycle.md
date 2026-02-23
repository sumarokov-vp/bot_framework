# Жизненный цикл Flow

Flow — это линейная цепочка шагов, которую проходит пользователь в диалоге с ботом. Каждый шаг собирает одну единицу данных.

## Участники

| Участник | Роль |
|----------|------|
| **Handler** | Принимает ввод от пользователя, записывает данные в State |
| **Flow** | Хранит список шагов, итерирует их по порядку |
| **Step** | Проверяет одно поле в State. Если пусто — вызывает Presenter |
| **Presenter** | Формирует и отправляет сообщение пользователю |
| **State** | Pydantic-модель с данными, собранными в процессе flow |

## Процесс

```mermaid
sequenceDiagram
    participant П as Пользователь
    participant H as Handler
    participant St as State
    participant F as Flow
    participant S1 as Step 1
    participant S2 as Step 2
    participant Pr as Presenter

    П->>H: Нажимает кнопку «Начать»
    H->>F: flow.start(user)
    F->>S1: execute(user, state)
    S1->>St: state.name заполнено?
    St-->>S1: Нет
    S1->>Pr: send("Как вас зовут?")
    Pr-->>П: Сообщение в чат

    П->>H: Вводит "Иван"
    H->>St: state.name = "Иван"
    H->>F: flow.route(user)
    F->>S1: execute(user, state)
    S1->>St: state.name заполнено?
    St-->>S1: Да
    S1-->>F: True (готово)
    F->>S2: execute(user, state)
    S2->>St: state.email заполнено?
    St-->>S2: Нет
    S2->>Pr: send("Ваш email?")
    Pr-->>П: Сообщение в чат
```

## Принцип разделения ответственности

```mermaid
flowchart LR
    H[Handler] -->|пишет в| S[State]
    H -->|вызывает| F[Flow.route]
    F -->|итерирует| ST[Steps]
    ST -->|вызывает| P[Presenter]
    P -->|отправляет| U[Пользователю]
```

Ключевые правила:

- **Handler не знает о Presenter** — он только записывает данные и передаёт управление Flow
- **Step не знает о Handler** — он только проверяет State и вызывает Presenter
- **Presenter не знает о Step и Flow** — он только формирует и отправляет сообщение
- **Flow не знает о содержимом шагов** — он только вызывает их по порядку

## Завершение Flow

Когда все шаги вернули `True` (все поля State заполнены), Flow вызывает callback `on_complete`. Обычно это финальный Presenter, который показывает подтверждение.

```mermaid
flowchart LR
    S1[Step 1 ✓] --> S2[Step 2 ✓] --> S3[Step 3 ✓] --> OC[on_complete]
```

## Типичная структура файлов Flow

```
src/flows/my_flow/
├── factory.py            # Сборка зависимостей
├── handlers/             # Обработчики ввода
├── steps/                # Шаги flow
├── presenters/           # Отправка сообщений
├── entities/             # State (Pydantic-модель)
└── repos/                # Хранилище state
```

!!! info "Подробнее"
    Полный пример создания flow с кодом — в разделе [Создание Flow](../examples/creating-flow.md).
