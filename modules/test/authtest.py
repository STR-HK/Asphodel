from Asphodel import app, auth

@app.get("/auth", tags=["Auth"])
async def rooat(auth = auth):
    return auth

# 간단한 auth 함수입니다
# 루트 디텍토리에서 임포트하셔서 자유롭게 사용하세요!