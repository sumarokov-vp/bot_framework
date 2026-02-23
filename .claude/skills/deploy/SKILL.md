---
name: deploy
description: Деплой документации на сервер. Используй при запросах на деплой, публикацию docs.
---

Деплой документации Bot Framework. $ARGUMENTS

## Инструкции

Делегируй выполнение агенту **devops** со следующей задачей:

1. Прочитай конфигурацию из `.claude/devops.yaml` (секция `servers.docs` и `deploy.docs`)
2. Собери документацию локально: `uv run mkdocs build`
3. Загрузи содержимое `site/` на сервер в директорию из конфига (`remote_dir`)
4. Убедись, что на сервере настроен **Caddy** (не Traefik) для домена из конфига (`domain`):
   - Если Caddy не установлен — установи
   - Если используется Traefik — замени на Caddy
   - Caddyfile должен обслуживать статику из `remote_dir` по домену
5. Проверь, что сайт доступен по HTTPS

Существующие сайты на сервере должны продолжать работать:
- `docs.smartist.dev` → `/var/www/smartist_docs`
- `botframework.smartist.dev` → `/var/www/botframework_docs`

Caddy обслуживает статику из `/var/www/` (не из `/root/`). При обновлении документации синхронизировать в `/var/www/botframework_docs` и выставить права `caddy:caddy`.
