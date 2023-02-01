# om-dao-api
Postgres + LetsEncrypt-Nginx-Proxy-Companion + Python + alimbic. Production-ready api bot with database.

Начальная настройка:
```
python -m venv app_venv
source app_venv/bin/activate
app_venv/bin/python -m pip install --upgrade pip
sudo pip3 install --upgrade pip setuptools wheel
pip install poetry
poetry export --without-hashes --format=requirements.txt > requirements.txt
pip install -r requirements.txt
```

Запускаем наш комплекс контейнеров в первый раз находясь в корневой дирректории проекта:
```
docker compose up -d --build
```

Для остановки комплекса контейнеров:
```
docker compose down
```

Для если нам не требуется пересобирать контейнеры и для последующих запусков используем комманду:
```
docker compose up -d
```

Проверить как собрались контейнеры и все ли наместе можно коммандой:
```
docker ps -a
```