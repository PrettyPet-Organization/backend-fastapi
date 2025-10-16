# Backend FastAPI - Развертывание и разработка


## Предварительные требования
Убедитесь, что у вас установлены:
- Docker и Docker Compose (рекомендуемый способ)
- Python 3.11+ (если запускаете без Docker)
- Git

## Быстрый старт (рекомендуемый способ)
### 1. Клонирование репозитория
```bash
git clone https://github.com/PrettyPet-Organization/backend-fastapi.git
cd backend-fastapi
git checkout develop
```
### 2. Настройка переменных окружения
```bash
# Копируем шаблон и редактируем
cp .env .env
```
Отредактируйте файл .env - замените значения на актуальные для вашего окружения.

### 3. Запуск через Docker
```bash
# На Linux
make docker-run

# На Windows
docker compose up -d
```
Этот способ автоматически:
- Соберет Docker-образ
- Запустит базу данных PostgreSQL
- Запустит FastAPI приложение

Настроит все зависимости

## Альтернативные способы запуска
### Способ 1: С Docker (простой)
```bash
make docker-run
```
### Способ 2: Без Docker (для разработки)
```bash
# Активируйте виртуальное окружение (рекомендуется)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
### Способ 3: С загрузкой .env файла
```bash
DOTENV_MODE=true uvicorn main:app --reload
Примечание: Переменная DOTENV_MODE=true вероятно включает загрузку настроек из .env файла в коде приложения.
```

## Настройка .env файла
Обязательные для изменения параметры в .env:

```env
# Настройки базы данных
PG_USER_NAME=your_username
PG_USER_PASSWORD=your_secure_password
PG_DATABASE_NAME=your_database_name

# Безопасность
SECRET_KEY=your_very_secret_key_here

# Email (если используется)
SENDER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password  # Для Gmail нужен пароль приложения
```
### Проверка работоспособности
После запуска:
- Откройте в браузере: http://localhost:8000
- Документация API: http://localhost:8000/docs
- Альтернативная документация: http://localhost:8000/redoc

Полезные команды
```bash
# Остановка контейнеров
make docker-stop

# Просмотр логов
docker-compose logs -f

# Пересборка и запуск
make docker-rebuild
```

### Рекомендация
- Используйте make docker-run - это самый надежный способ, так как он гарантированно настроит все зависимости и базу данных автоматически.
- После запуска проверьте http://localhost:8000/docs - если документация API открывается, значит все работает корректно!