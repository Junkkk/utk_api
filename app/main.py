import uvicorn
# import sys
# # sys.path = ['', '..'] + sys.path[1:]
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.routers import router
from fastapi import FastAPI


app = FastAPI()
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = {
        "phone": "Error phone message",
        "email": "Error email message",
        "comment": "Error comment message"
    }
    resp_list = []
    s = str(exc.args.__str__())
    i_list = [i+10 for i in range(len(s)) if s.startswith("{'loc': ('", i)]
    for i in i_list:
        ss = s[i:i+10]
        ss = ss[:ss.find("'")]
        resp_list.append({'name': ss, 'error': errors[ss]})
    return JSONResponse(status_code=422, content=resp_list)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)