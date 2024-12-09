# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . /app/

WORKDIR /app/admin_panel
# Указываем порт, на котором будет слушать Gunicorn
EXPOSE 8000

# Команда для запуска Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "admin_panel.wsgi:application"]
