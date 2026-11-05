# Android-клиент Scenica

Мобильное приложение для зрителей на **Kotlin + Jetpack Compose**. Работает
через публичные эндпоинты backend:

- `POST /public/v1/auth/register`
- `POST /public/v1/auth/login`
- `GET /public/v1/theaters`
- `GET /public/v1/theaters/{theater_id}/shows`
- `GET /public/v1/shows/{show_id}/seats`
- `POST /public/v1/reservations`
- `GET /public/v1/reservations/my`

## Что реализовано

- Compose navigation: Auth → Theaters → Shows → Seats → MyReservations
- Retrofit + Moshi + OkHttp
- Hilt DI
- Хранение JWT-токена в SharedPreferences
- Базовый слой Repository + ViewModel

## Запуск

### 1. Подготовить backend

Из корня проекта Scenica:

1. Установите зависимости Python (если ещё не устанавливали):
   `pip install -r requirements.txt`.
2. Примените миграцию для авторизации клиентов:
   выполните SQL из `migrations/add_customer_auth_columns.sql` в PostgreSQL.
3. Запустите API: `python start_api.py`.
4. Проверьте, что API доступен: [http://localhost:8000/docs](http://localhost:8000/docs).

### 2. Запустить клиент в эмуляторе

1. Откройте каталог `android-client` в Android Studio.
2. Дождитесь `Gradle Sync` и установки SDK/Build Tools, если IDE попросит.
3. Создайте и запустите Android-эмулятор (AVD).
4. Для эмулятора соберите с адресом API:
   `-PapiBaseUrl=http://10.0.2.2:8000/`.
5. Нажмите Run (`Shift+F10`).

### 3. Запустить на физическом устройстве

1. Телефон и компьютер должны быть в одной Wi-Fi-сети.
2. Узнайте локальный IP компьютера (например `192.168.1.100`).
3. При сборке передайте параметр:
   `-PapiBaseUrl=http://<ip-компьютера>:8000/`.
4. Включите USB debugging на телефоне и запустите приложение из Android Studio.
5. Убедитесь, что firewall Windows разрешает входящие подключения к порту `8000`.

## Где задаётся адрес API

Через Gradle property `apiBaseUrl` (см. `app/build.gradle.kts`):

- Эмулятор: `-PapiBaseUrl=http://10.0.2.2:8000/`
- Телефон: `-PapiBaseUrl=http://<ip-компьютера>:8000/`

Если параметр не указан, используется значение по умолчанию
`http://10.0.2.2:8000/`.
