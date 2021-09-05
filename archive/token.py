from fastapi.exceptions import HTTPException
from starlette.applications import Starlette
from fastapi.params import Depends
from pydantic import BaseModel
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ..interface import authInterface
import starlette.status

def initDBTokens():
    """
    SQLITE3 데이터베이스에서 AUTH 값을 읽어와,
    딕셔너리 형태로 tokens에 저장합니다
    """


    """
    함수 내에서 딕셔너리를 만들었으므로 전역변수 선언이 반드시 필요합니다
    """
    global tokens
    tokens = dict()


    """
    각각의 column을 수정 불가 튜플 형식으로 읽어 옵니다
    """
    tokens_read = authInterface.auth_return_tuple_data("token")
    forevers_read = authInterface.auth_return_tuple_data("forever")
    expires_read = authInterface.auth_return_tuple_data("expire")

    print(tokens)


    for t, token in enumerate(tokens_read):
        """
        t -> 커서 ( = 읽어오는 인덱스 부분 )
        tokens_read[t] -> 커서가 적용되지 않은 토큰 값.
        forevers_read[t] -> 커서가 적용되지 않은 영구토큰 참값.
        expires_read[t] -> 커서가 적용되지 않은 남은 시간 값
        """


        """
        읽어온 튜플 데이터는 다시금 튜플을 반환하므로 반드시 [0]을 읽어오아야 합니다
        """
        tokens_read[t] = tokens_read[t][0]
        expires_read[t] = expires_read[t][0]


        """
        DB에는 영구토큰의 참 / 거짓의 값이 1 / 0 으로 바뀌어 저장되므로,
        그것을 다시 복원시켜주는 작업이 필요합니다
        """
        if forevers_read[t][0] == "1":
            forevers_read[t] = True

        elif forevers_read[t][0] == "0":
            forevers_read[t] = False


        """
        딕셔너리인 tokens에 적절한 key와 [영구값, 만료값] 이라는 리스트로 이루어진 value를 집어넣습니다
        """
        tokens[tokens_read[t]] = [forevers_read[t], expires_read[t]]


initDBTokens()

def isTokenExists(token):
    """
    토큰이 tokens 딕셔너리에 있는지 확인하는 함수
    """
    try:
        tokens[token]
        return True
    except:
        return False

def isExpireExists(token):
    """
    토큰의 Expire가 tokens에 존재하는지 확인하는 함수
    """
    if tokens[token][1] == None:
        return False
    else:
        return True

def raiseUnauthorized(detail):
    """
    401 Unauthorized 에러를 발생시킵니다
    """
    raise HTTPException(
        status_code=starlette.status.HTTP_401_UNAUTHORIZED,
        detail=detail
    )


def raiseBadRequest(detail):
    """
    403 Bad Request 에러를 발생시킵니다
    """
    raise HTTPException(
        status_code=starlette.status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )


# HTTPBearer를 이용하여 Auth 시스템을 구축함
class AuthHandler:
    security = HTTPBearer()

    def wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):

        input = auth.credentials

        if isTokenExists(input) and tokens[input][0]:
            """
            < 영구토큰 읽어오는 부분 >
            isTokenExists(input) -> Bearer로 입력받은 값이 tokens에 존재하는가
            tokens[input][0] -> tokens 딕셔너리에서 입력값을 찾아서 영구토큰인지 여부를 확인함
            """
            return {"detail": "Authorized : forever"}

        else:
            """
            < 일회용토큰 읽어오는 부분 >
            이 부분은 일회용토큰을 읽어오는 부분임으로 필연적으로 파라미터가 존재하게 됩니다
            따라서 미리 입력받은 값에서 토큰 부분만을 뽑아옵니다

            input.split("?")[0] -> 토큰 & 파라미터 분할의 0번쨰 ( = 토큰부분 )
            """
            splitedAuth = input.split("?")
            token = input.split("?")[0]
            
            if isTokenExists(token):
                """
                < 일회용토큰의 존재 확인 >

                토큰 목록에 존재하는지부터 확인합니다
                존재하지 않는다면 애초에 토큰이 아닙니다
                """
                
                if isExpireExists(token):
                    """
                    < 기존 DB에 Expire가 존재함 >
                    DB에서 Expire가 존재하는지를 확인합니다

                    존재한다면 Expire가 설정된 것으로,
                    
                    """

                    """
                    입력한 토큰의 Expire가 존재함을 확인하였습니다
                    따라서, 본 토큰의 유효기간을 계산합니다
                    """
                    valid = getTokenValid(token)

                    """
                    토큰이 유효하다면 ( = 토큰의 남은 기간이 양수라면 )
                    인증을 마칩니다. -> 정상적인 토큰이므로 pass
                    """
                    if valid["boolean"]:
                        return {"detail": "Authorized : {}".format(valid["subtracted"])}

                    else:
                        """
                        토큰의 유효하지 않다면 ( = 토큰의 남은 기간이 음수라면 )
                        데이터베이스에서 토큰을 지웁니다 -> 다시금 토큰을 불러옵니다
                        그리고 Unauthorized를 발생시킵니다
                        """
                        authInterface.auth_remove_row_by_token_name(token)
                        authInterface.authDB.commit()
                        initDBTokens()
                        raiseUnauthorized("Token Expired") # 만료된 토큰과 같지만 개발중이니 이렇게 표시함
                
                else:
                    """
                    < 기존 DB에 Expire가 존재하지 않음 >
                    존재하지 않는다면, Expire가 설정되지 않은 것입니다
                    -> 정상적인 파라미터가 반드시 요구됩니다

                    이 경우는 정상적인 파라미터가 반드시 요구되므로, 
                    여러가지 조건식을 통해 이를 해결합니다

                    len(splitedAuth) == 2 -> 토큰과 파리미터가 둘 다 있음
                    len(splitedAuth[1].split("&")) >= 1 -> 파라미터의 길이가 1 이상임

                    둘 다 만족하면 파라미터가 있음을 확인 할 수 있습니다만,
                    파라미터의 항목이 유효하지 않을 수 있음으로 이는 추후에 토큰을 Analyze하면서 판독해야 합니다
                    """
                    if len(splitedAuth) == 2 and len(splitedAuth[1].split("&")) >= 1:
                        # 토큰 파라미터 분석 후 토큰과 만료시간을 리턴받고 그걸 DB에 저장
                        """
                        토큰 파라미터를 분석합니다
                        분석을 통하여 토큰의 만료시간을 얻고, 그것을 DB에 저장합니다
                        그리고 토큰을 다시 불러옵니다

                        마지막으로 토큰의 유효성을 검사하고 인증을 마칩니다 -> pass
                        """
                        tokenAnalyzed = tokenAnalyze(input)
                        authInterface.auth_update_expire(
                            tokenAnalyzed["expire_time"], tokenAnalyzed["token"]
                        )
                        authInterface.authDB.commit()
                        initDBTokens()

                        valid = getTokenValid(token)
                        return {"detail": "Authorized : {}".format(valid["subtracted"])}
            else:
                """
                영구토큰은 일단 탈락, 일회용 토큰의 존재 확인 단계에서 탈락했으므로, 
                실존하는 토큰이 아니라고 판단합니다
                """
                raiseBadRequest("Invalid Token")

        # 잘못된 입력입니다 -> 토큰 만료일이 설정되지 않았는데 Expire가 없는 경우 / 토큰 만료일이 설정되었는데 Expire가 있는 경우
        """
        토큰 존재 & 토큰 만료일 미설정됨 & 토큰 만료일 파라미터 있음 ( 이곳에서 걸러지지 않음 )

        선택됨 -> 토큰 존재 & 토큰 만료일 미설정됨 & 토큰 만료일 파라미터 없음

        토큰 존재 & 토큰 만료일 설정됨 & 토큰 만료일 파라미터 있음 ( 이곳에서 걸러지지 않음 )
        
        토큰 존재 & 토큰 만료일 설정됨 & 토큰 만료일 파라미터 없음 ( 이곳에서 걸러지지 않음 )
        """
        raiseBadRequest("Invalid input")


def getTokenValid(token):
    """
    ['boolean'] 은 토큰의 유효성을,
    ['subtracted'] 은 토큰의 유효기간을 반환합니다
    """
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
def tokenAnalyze(input):
    """
    ['token'] 부분은 분리 추출된 토큰을 의미하며,
    ['expire_time'] 은 텍스트 형식의 만료일 datetime 오브젝트입니다
    """
    token, parameter = input.split("?")
    parameter = parameter.split("&")

    for p in range(len(parameter)):
        parameter[p] = parameter[p].split("=")

    now_time = datetime.now()
    expire_time = now_time

    for p in parameter:
        try:
            key, value = p[0], int(p[1])
        except:
            raiseBadRequest("Invalid Parameters")

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


# from Asphodel import app

authorization = AuthHandler().wrapper
auth = Depends(authorization)

# from Asphodel import auth

# @app.get("/verify")
# def verify(auth = auth):
#     return auth

# @app.get('/addtoken')
# def addtoken(token):
#     if token in tokens:
#         return '이미 있는 토큰입니다'
#     return tokens