# Flow Stack

Один Flow — линейная цепочка шагов без ветвлений. Но иногда внутри flow требуется ответвление: например, при заполнении адреса нужно пройти отдельную цепочку «город → улица → дом».

Flow Stack решает эту задачу — он соединяет несколько flow с возможностью возврата.

## Как это работает

```mermaid
flowchart TB
    subgraph RF["Registration Flow"]
        R1[Шаг: Имя] --> R2[Шаг: Адрес] --> R3[Шаг: Email]
    end

    subgraph AF["Address Flow"]
        A1[Шаг: Город] --> A2[Шаг: Улица] --> A3[Шаг: Дом]
    end

    R2 -->|push| AF
    AF -->|pop_and_return| R3
```

Flow Stack работает как **стек вызовов функций**:

| Операция | Аналогия | Что происходит |
|----------|----------|---------------|
| `push` | Вызов функции | Текущий flow приостанавливается, запускается дочерний |
| `pop_and_return` | Возврат из функции | Дочерний flow завершается, управление возвращается родительскому |
| `terminate` | Выход без возврата | Текущий flow завершается, стек не раскручивается |
| `clear_all` | Сброс | Весь стек очищается (например, при `/start`) |

## Процесс навигации

```mermaid
sequenceDiagram
    participant П as Пользователь
    participant N as Navigator
    participant RF as Registration Flow
    participant AF as Address Flow

    П->>RF: Начинает регистрацию
    RF->>RF: Шаг «Имя» ✓
    RF->>RF: Шаг «Адрес» — нужен новый адрес
    RF->>N: push("add_address")
    N->>AF: Запускает Address Flow
    AF->>П: "Укажите город"
    П->>AF: "Москва"
    AF->>AF: Шаг «Город» ✓ → «Улица» → «Дом» ✓
    AF->>N: pop_and_return()
    N->>RF: Возврат в Registration Flow
    RF->>RF: Шаг «Email»
    RF->>П: "Ваш email?"
```

## Правило

- **Один flow = одна линейная цепочка** без ветвлений
- Как только появляется ответвление — выносить его в отдельный flow
- Flow Stack соединяет flow между собой

## Компоненты

| Компонент | Назначение |
|-----------|-----------|
| **FlowRegistry** | Реестр всех flow по имени |
| **FlowStackNavigator** | Управление стеком: push, pop, terminate, clear |
| **RedisFlowStackStorage** | Хранение стека в Redis |

!!! info "Подробнее"
    Пример использования API Flow Stack — в [README проекта](https://github.com/sumarokov-vp/bot-framework).
