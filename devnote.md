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



