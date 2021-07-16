from Asphodel import app
from modules import parser

@app.get('/taskmgr/list')
async def taskmgr_import():
    return {'response':parser.return_json_data('*')}