# Backend FastAPI - Развертывание и разработка

## Содержание

1. [Предварительные требования](#предварительные-требования)
2. [Быстрый старт](#быстрый-старт)
3. [Альтернативные способы запуска](#альтернативные-сособы-запуска)
4. [API Документация](#api-документация)
5. [Полезные команды для разработки](#полезные-команды-для-разработки)


## Предварительные требования
[Содержание](#содержание)

Убедитесь, что у вас установлены:
- Docker и Docker Compose (рекомендуемый способ)
- Python 3.11+ (если запускаете без Docker)
- Git

## Быстрый старт (рекомендуемый способ)
[Содержание](#содержание)
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
- Запускает тестовый почтовый сервис
- Запускает portainer(для Linux)

## Альтернативные способы запуска
[Содержание](#содержание)

### Способ 1: Без Docker (для разработки)
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
### Способ 2: С загрузкой .env файла
```bash
DOTENV_MODE=true uvicorn main:app --reload
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


## API Документация

Вся документация сформирована через автогенерацию FastApi(Swagger):
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Полезные команды для разработки
[Содержание](#содержание)
### Разработка с hot-reload
```bash
# Запуск в режиме разработки
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Просмотр логов в реальном времени
docker-compose logs -f --tail=100
# Ну или просто 
docker-compose up --build
```
### Тестирование производительности
```bash
# Запуск нагрузочного теста
docker exec -it test_client python load_test.py

# Проверка метрик
curl http://localhost:5000/metrics
```
### Устранение неисправностей
Сервис не запускается
```bash
# Проверка занятых портов
ss -tulpn | grep -E ':(5000|5434|9000)'

# Принудительная пересборка
docker-compose down
docker-compose up -d --build --force-recreate
```
Проблемы с БД
```bash
# Проверка подключения к БД
docker exec mail_db pg_isready -U mail_user -d mail_service

# Сброс БД (осторожно!)
docker-compose down -v
docker-compose up -d
```