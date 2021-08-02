from fastapi.exceptions import HTTPException
from starlette.applications import Starlette
from fastapi.params import Depends
from pydantic import BaseModel
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime
from dateutil.relativedelta import relativedelta

from modules import sqlite3_auth as auth

tokens = dict()

# 토큰 목록을 DB에서 받아와 딕셔너리로 만들어주는 함수
def init_tokens():
    global tokens
    tokens = dict()

    tokens_read = auth.auth_return_tuple_data("token")
    forevers_read = auth.auth_return_tuple_data("forever")
    expires_read = auth.auth_return_tuple_data("expire")

    for t, token in enumerate(tokens_read):
        if forevers_read[t][0] == "1":
            forevers_read[t] = True
        else:
            forevers_read[t] = False
        tokens[token[0]] = [forevers_read[t], expires_read[t][0]]


init_tokens()

# 토큰이 tokens 딕셔너리에 있는지 확인하는 함수
def tokenTF(token):
    try:
        tokens[token]
        return True
    except:
        return False


# 토큰의 Expire가 존재하는지 확인하는 함수
def expireExist(token):
    if tokens[token][1] == None:
        return False
    else:
        return True


from modules import sqlite3_auth
from modules import mysqlite3

import starlette.status


def raiseUnauthorized(detail):
    raise HTTPException(
        status_code=starlette.status.HTTP_401_UNAUTHORIZED, detail=detail
    )


def raiseBadRequest(detail):
    raise HTTPException(
        status_code=starlette.status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )


# HTTPBearer를 이용하여 Auth 시스템을 구축함
class AuthHandler:
    security = HTTPBearer()

    def wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        if tokenTF(auth.credentials) and tokens[auth.credentials][0]:
            return {"detail": "Authorized : forever"}
        else:
            splitedAuth = auth.credentials.split("?")
            # 분할된 일회용토큰이 토큰 목록에 존재하는가?
            if tokenTF(splitedAuth[0]):
                # 일회용토큰에 해당하는 Expire가 DB에 존재하는가?
                if expireExist(splitedAuth[0]):
                    # 토큰 분석하기
                    valid = tokenValid(splitedAuth[0])
                    # 토큰 남은 유효기간이 양수라면
                    if valid["boolean"]:
                        return {"detail": "Authorized : {}".format(valid["subtracted"])}
                    # 토큰 남은 유효기간이 음수라면
                    else:
                        # 데이터베이스에서 토큰 지워버리고 리로드
                        sqlite3_auth.auth_remove_row_by_token_name(splitedAuth[0])
                        mysqlite3.commit()
                        init_tokens()
                        # 일회용 인증됨 + Expire 없음 BUT 토큰 만료됨 -> DB에서 지워버림
                        raiseUnauthorized("Token Expired")
                        # return '일회용 인증됨 + Expire 없음 BUT 토큰 만료됨 {} -> DB에서 지워버림'.format(valid[1])
                else:
                    # 분배한 것의 길이가 2 ( = 토큰과 파라미터가 다 있음 )
                    # 분배한 것이 2번째 항목 ( = 파라미터 ) 를 & 를 이용해서 나눈 것의 길이가 1 이상임 ( = 파라미터의 항목이 1개 이상이라는 뜻 )
                    # 둘 다 만족해야 Expire가 있음을 확인함, 단 Expire 파라미터의 항목 유효 여부는 추후 Analyze 부분에서 판독해야 함
                    if len(splitedAuth) == 2 and len(splitedAuth[1].split("&")) >= 1:
                        # 토큰 파라미터 분석 후 토큰과 만료시간을 리턴받고 그걸 DB에 저장
                        tokenAnalyzed = tokenAnalyze(auth.credentials)
                        sqlite3_auth.auth_update_expire(
                            tokenAnalyzed["expire_time"], tokenAnalyzed["token"]
                        )
                        mysqlite3.commit()
                        init_tokens()

                        valid = tokenValid(splitedAuth[0])
                        return {"detail": "Authorized : {}".format(valid["subtracted"])}

            else:
                # 애초에 토큰이 아닙니다
                raiseBadRequest("Invalid Token")
        # 잘못된 입력입니다 -> 토큰 만료일이 설정되지 않았는데 Expire가 없는 경우 / 토큰 만료일이 설정되었는데 Expire가 있는 경우
        raiseBadRequest("Invalid input")


def tokenValid(token):
    now = datetime.now()
    expire = datetime.strptime(tokens[token][1], "%Y-%m-%d %H:%M:%S.%f")

    subtracted = expire - now
    if subtracted.days >= 0:
        return {"boolean": True, "subtracted": subtracted}
    else:
        return {"boolean": False, "subtracted": subtracted}


# 토큰을 분석함
# 1 토큰 파라미터를 분석함 -> 중간의 비정상 항목은 그냥 무시하지만, 모든 항목이 비정상일경우 에러 리턴
# 2 토큰의 만료시간을 도출함
def tokenAnalyze(input_):
    token, parameter = input_.split("?")
    parameter = parameter.split("&")

    for p in range(len(parameter)):
        parameter[p] = parameter[p].split("=")

    now_time = datetime.now()
    expire_time = now_time

    for p in parameter:
        try:
            key, value = p[0], int(p[1])
        except:
            print("param eror")
        # y -> 년 / m -> 월 / d -> 일 / H -> 시간 / M -> 분 / S -> 초
        if key == "y":
            expire_time += relativedelta(years=value)
        elif key == "m":
            expire_time += relativedelta(months=value)
        elif key == "d":
            expire_time += relativedelta(days=value)
        elif key == "H":
            expire_time += relativedelta(hours=value)
        elif key == "M":
            expire_time += relativedelta(minutes=value)
        elif key == "S":
            expire_time += relativedelta(seconds=value)
        else:
            print(key, value, "unexpected!")

    if now_time == expire_time:
        raiseBadRequest("Invalid Parameters")
    return {"token": token, "expire_time": expire_time.strftime("%Y-%m-%d %H:%M:%S.%f")}


from Asphodel import app

# Depends에서는 wrapper 부분만 사용
# HTTPBearer()를 이용하려고 class를 생성하는 것임
wrapper = AuthHandler().wrapper

# token=Depends(wrapper) 가 auth를 해주는 것이며
# 이것은 테스트용 get임
@app.get("/verify")
def verify(token=Depends(wrapper)):
    return token
