# dev note
개발 관련 노트




# 버전 확인
```
python -m django --version
```
# pip 설치 등
```
pip install django
pip install django-environ
pip install markdown
```

mysqlclient 설치
```
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```
```
pip install mysqlclient
```


# 처음에 프로젝트 생성할 때
```
django-admin startproject app
```



# 앱 추가할 때
퍼미션 부분이 혼란스러워질 수 있으므로, 도커 컨테이너보다는 바로 호스트에서 생성하도록 하자.

앱 추가할 때
```shell
cd app
python manage.py startapp app-name
```

# 마이그레이션
## 마이그레이션 파일 생성
마이그레이션 파일 생성 (로컬에 파이썬이 설치되어 있다면, 로컬에서 다음을 실행)
```shell
cd app
python manage.py makemigrations
```

아니면 도커에서
```shell
docker exec -it blog_app_1 python manage.py makemigrations
```


## 데이터베이스에 반영
데이터베이스에 반영 (커넥션 등의 이슈가 있으므로 도커 내에서 실행)
```
docker exec -it blog_app_1 python manage.py migrate
```

## 쿼리만 확인하기
쿼리만 확인하기
```shell
cd app
python manage.py sqlmigrate blog 0001
```

## 마이그레이션 갱신 시
1. 기존에 생성되었던 migrate 파일을 삭제한다.
2. migrate 명령을 수행한다. 

상세

```
./scripts/dev/drop_migrate_files.sh 1


```
