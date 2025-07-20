# Telegram TikTok Bot
Этот проект — бот который скачивает видео по ссылке без водяного знака.
This project is a bot that downloads videos from a link without a watermark.

---

## 📦 Установка и запуск \ Installation and launch

### 1. Скачайте Python 3.10

Скачайте и установите Python 3.10 с официального сайта \ Download and install Python 3.10 from the official website:  
👉 https://www.python.org/downloads/release/python-3100/

---

### 2. Перейдите в папку с ботом \ Go to the bot folder

Откройте терминал или командную строку и перейдите в папку с проектом \ Open the terminal or command prompt and navigate to the project folder:

```bash
cd путь_к_папке_с_ботом___path_to_bot
```

### 3. Установите зависимости \ Install the dependencies
Установите все необходимые библиотеки командой:

```bash
pip install -r requirements.txt
```

### 4. Создайте бота в @BotFather
Перейдите в Telegram и откройте бота @BotFather
Создайте нового бота командой /newbot
Скопируйте токен, который он выдаст

### 5. Настройте bot.py
Отредактируйте файл main.py на строчках 24-26:
```python
bot = Bot(token='ВАШ_ТОКЕН_ОТ_BOTFATHER')
admin='1234567890'  # Ваш Telegram user ID
start_message='Привет ! <b> Отправь мне ссылку на видео которое нужно скачать</b>'#стартовое сообщение
```

### 6. Запустите бота !
Запустите бота командой:
```bash
python bot.py
```

### ✅ Готово!
