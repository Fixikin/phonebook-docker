# Phonebook Docker Project

## Setup

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/ваш-логин/phonebook-docker.git  
   cd phonebook-docker

2. **Запустите проект:**
   ```bash
   docker compose up -d --build

3. **Инициализация базы данных:**
   При первом запуске автоматически создаются таблицы из db/init.sql.

## Access

### PGAdmin
- Откройте в браузере: http://localhost:5050
- Логин: skachkov-yuriy@mail.ru
- Пароль: Admin123

### Приложение
```bash
docker compose exec app python app.py
```
### PostgreSQL:
- Хост: db (внутри Docker) или localhost (снаружи)
- Порт: 5432
- База данных: phonebook_db
- Пользователь: phonebook
- Пароль: secret
### Остановка проекта
```bash
   docker compose down

