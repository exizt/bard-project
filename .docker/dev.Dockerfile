# 개발 로컬 환경의 Dockerfile

# 파이썬 패키지를 빌드하기 위한 이미지.
# gcc의 용량이 크기 때문에, 별도로 분리해서 결과물만 복사이동하는 방식.
FROM python:3-alpine AS Builder
# RUN apk add gcc musl-dev mariadb-connector-c-dev
# RUN apk add gcc

# https://github.com/ellerbrock/docker-alpine/blob/master/django/Dockerfile
ENV PY_PACKAGES="\
  django \
  mysqlclient \
  django-environ \
  markdown \
  mdx-breakless-lists \
"

RUN apk update
RUN apk add --no-cache musl-dev mariadb-dev gcc
RUN pip install $PY_PACKAGES --user


# 본격적인 이미지
FROM python:3-alpine

# alpine은 bash가 없다고 하니, 설치를 해야 함.
RUN apk add --no-cache bash
RUN apk add --no-cache mariadb-connector-c

# python의 설치할 pip 패키지를 가져옴
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /srv/app

# 개발 모드에서만 필요함.
RUN pip install django-debug-toolbar

ENTRYPOINT ["tail", "-f", "/dev/null"]