# om-dao-api
Postgres + LetsEncrypt-Nginx-Proxy-Companion + Python + alimbic. Production-ready api with database.

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

Ставим Docker

``` bash
apt-get remove docker docker-engine docker.io containerd runc
apt-get update -y
apt-get install ca-certificates curl gnupg lsb-release -y
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
apt-get update -y
apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
docker --version
curl -L "https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose
docker-compose --version
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