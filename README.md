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
⚠️ WORK IN PROGRESS
```
docker compose -f deploy/docker/locust.yaml up -d
```
и открыть адрес http://localhost:8089
