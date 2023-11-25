# dev note
개발 관련 노트



# 최근 작업
- 블로그 설정 (블로그 이름 등)을 입력할 수 있는 테이블과 관리자 모드 생성.
    - 템플릿에 반영하는 작업은 아직 안 함.
    - 스킨 설정, 다크모드 설정 등을 다룰 방법이 필요함. json으로 처리할지 고민.
    - 또는 테이블 구조를 좀 더 단순화할 필요가 있을 수도 있음.
- 블로그 배포에 대한 docker를 만들 필요가 있어서 고민.
    - nginx를 이용해서 포워딩도 시키고, wsgi인가 뭔가를 해야한다고도 하고.


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
데이터베이스에 반영 (커넥션 등의 이슈가 있으므로 도커 컨테이너 내에서 실행)
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
    - `./scripts/dev/drop_migrate_files.sh 1`
2. migrate 파일을 생성한다.
    - `docker exec -it blog_app_1 python manage.py makemigrations`
3. 데이터베이스 테이블 삭제
    - `drop_tables.sql` 쿼리를 실행
4. migrate 명령 실행
    - `docker exec -it blog_app_1 python manage.py migrate`

## 마이그레이션 파일 합치기
* 구문: `python manage.py squashmigrations <appname> <from> <to>`


예시:
```shell
python manage.py squashmigrations example 0003 0004
```


# 데이터베이스 구조
## 모델 구조
blog/models
    - Article
    - ArticleContent
    - Section
    - SectionArticle
    - Blog