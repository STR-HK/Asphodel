from fastapi.exceptions import HTTPException
# from starlette.applications import Starlette
from fastapi.params import Depends
# from pydantic import BaseModel
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime
from dateutil.relativedelta import relativedelta
import starlette.status

from ..interface.databases import AuthDB

class AuthDBInterface():
    def __init__(self) -> None:
        pass

    def isTokenExists(self, token):
        # print(f'isTokenExists {AuthDB.select(table_name="auth", field_names=["token"], condition=f"token = "{token}"")}')
        # print()
        a = AuthDB.select(table_name='auth', field_names=['token'], condition=f"token = '{token}'")
        print(f'isTokenExists -> {a}')
        if AuthDB.select(table_name='auth', field_names=['token'], condition=f"token = '{token}'"):
            return True
        else:
            return False
    
    def isExpireExists(self, token):
        print('isExpireExists')
        if AuthDB.select(table_name='auth', field_names=['expire'], condition=f"token = '{token}'")[0][0]:
            return True
        else:
            return False
    
    def isForever(self, token):
        print('isForever')
        if AuthDB.select(table_name='auth', field_names=['forever'], condition=f"token = '{token}'")[0][0] == 1:
            return True
        else:
            return False
    
    def getExpire(self, token):
        print('getExpire')
        return AuthDB.select(table_name='auth', field_names=['expire'], condition=f"token = '{token}'")[0][0]
    
    def deleteRow(self, token):
        print('deleteRow')
        AuthDB.delete(table_name='auth', condition=f"token = '{token}'")
    
    def isTokenValid(self, token):
        print('isTokenValid')
        now = datetime.now()
        expire = datetime.strptime(self.getExpire(token), "%Y-%m-%d %H:%M:%S.%f")
    
        subtracted = expire - now
        if subtracted.days >= 0:
            return True
        else:
            return False
    
    def getTokenSub(self, token):
        print('getTokenSub')
        now = datetime.now()
        expire = datetime.strptime(self.getExpire(token), "%Y-%m-%d %H:%M:%S.%f")
    
        subtracted = expire - now
        return subtracted
    
    def updateExpire(self, expire, token):
        print('updateExpire')
        AuthDB.update(table_name='auth', values={'expire':expire}, condition=f"token = '{token}'")

    def save(self):
        print('save')
        AuthDB.save()


def raiseUnauthorized(detail):
    raise HTTPException(
        status_code=starlette.status.HTTP_401_UNAUTHORIZED,
        detail=detail
    )


def raiseBadRequest(detail):
    raise HTTPException(
        status_code=starlette.status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )


class AuthHandler:
    security = HTTPBearer()

    def __init__(self) -> None:
        self.interface = AuthDBInterface()

    def wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):

        input = auth.credentials
        if self.interface.isTokenExists(input) and self.interface.isForever(input):
            return {"Authorized": "forever"}

        else:
            splitedAuth = input.split("?")
            token = input.split("?")[0]
            
            if self.interface.isTokenExists(token):
                
                if self.interface.isExpireExists(token):

                    if self.interface.isTokenValid(token):
                        return {"Authorized": "{}".format(self.interface.getTokenSub(token))}

                    else:
                        self.interface.deleteRow(token)
                        self.interface.save()
                        raiseUnauthorized("Token Expired")
                
                else:

                    if len(splitedAuth) == 2 and len(splitedAuth[1].split("&")) >= 1:

                        tokenAnalyzed = tokenAnalyze(input)
                        self.interface.updateExpire(
                            tokenAnalyzed["expire_time"], tokenAnalyzed["token"]
                        )
                        self.interface.save()

                        return {"Authorized": "{}".format(self.interface.getTokenSub(token))}
            else:

                raiseBadRequest("Invalid Token")

        raiseBadRequest("Invalid input")

def tokenAnalyze(input):
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

authorization = AuthHandler().wrapper
auth = Depends(authorization)