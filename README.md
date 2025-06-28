# Lingue
Оценка производительности простых веб-сервисов на разных языках

### Адреса для тестирования нагрузки
1. `/ping` — простой ping-роут с текстовым ответом

## Запуск тестов

### Запуск сервисов
```
docker compose -f deploy/docker/golang.yaml -f deploy/docker/python.yaml up -d
```

### Locust (ручной запуск)
```
pip install locust
cd deploy/locust
locust --headless -u 1000 -r 10 -t 50 --processes 4 <SERVICE>
```
 где `<SERVICE>` это одно из значений:
 * `Litestar`
 * `Gin`

### Locust (запуск из Docker)
```
docker compose -f deploy/docker/locust.yaml up -d
```
Открыть адрес http://localhost:8089 и использовать для хоста:
1. Golang Gin: `http://gin:8080`
1. Python Litestar: `http://litestar:8000`
