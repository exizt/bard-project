#!/bin/bash

if [ -z "$BASH_VERSION" ]; then exec bash "$0" "$@"; exit; fi # bash handling (bash가 아니면 bash로 실행)

# PATH
SCRIPT_PATH=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")") # 스크립트의 경로
SCRIPT_NAME=$(basename $BASH_SOURCE) # 스크립트 명칭
APP_PATH="${SCRIPT_PATH}/../../app"

echo "[${SCRIPT_NAME}] start.."
# 파라미터가 없는 경우는 실행하지 않도록 함.
if [ "$#" -lt 1 ]; then
    echo "[${SCRIPT_NAME}] Parameters are required."
	exit 1
fi

cd $APP_PATH

rm -fv ./blog/migrations/0001_initial.py
rm -fv ./tag_manager/migrations/0001_initial.py
