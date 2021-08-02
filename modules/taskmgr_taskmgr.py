from Asphodel import app
import modules.sqlite3_taskmgr as sqlite3_taskmgr


@app.get("/taskmgr/list")
async def taskmgr_import():
    return {"detail": sqlite3_taskmgr.taskmgr_return_json_data("*")}
