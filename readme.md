# Bard Project 개요
블로그 프로젝트
* '나의 개발자 블로그' 전용의 파이썬 기반의 블로그를 만든다.
* 코드는 가급적 범용성이 있게 고려하되, 분명히 전용적이게 만든다.



# 설치되는 패키지
1. `pip install django`: `asgiref`, `sqlparse`
2. `pip install django-environ`: `.env`로 설정이 가능하도록 도와주는 패키지.
3. `pip install django-debug-toolbar`: 개발 단계에서 디버그용 


# 도커 실행
```shell
sudo docker-compose --env-file=.docker/.env up --build --force-recreate -d
```

# 도커로 명령어 실행할 경우
```shell
# 방법 1
sudo docker exec -it blog_app_1 some_commands

# 방법 2
sudo docker exec -it blog_app_1 bash -c ""
```

# migrate
```shell
docker exec -it blog_app_1 python manage.py makemigrations

docker exec -it blog_app_1 python manage.py migrate
```

동작될 쿼리 확인
```shell
docker exec -it blog_app_1 python manage.py sqlmigrate blog 0001
```
