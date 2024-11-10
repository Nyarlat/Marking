# Запуск приложения с GPU с использованием Docker Compose

Этот проект может быть развернут также с помощью Docker Compose с возможностью работы с GPU.

## Требования

- Установленный Docker и Docker Compose
- NVIDIA GPU и драйвера для работы с CUDA
- Установленный [NVIDIA Docker Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) для поддержки GPU в Docker
- В новых версиях docker desktop по умолчанию есть NVIDIA Toolkit
## Шаги для запуска

В корне проекта выполнить команду 

`docker-compose up -d`

После этого у вас будут развернуты контейнер с PostgreSQL и приложением

Чтобы убедиться, что приложение использует GPU

`docker-compose exec web nvidia-smi`
