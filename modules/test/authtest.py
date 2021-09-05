from Asphodel import app

from modules.certificate.authorization import *

@app.get("/auth")
async def rooat(auth = auth):
    return auth

# 정말 예쁘게 만든 auth 함수입니다
# 루트 디텍토리에서 임포트하셔서 자유롭게 사용하세요!