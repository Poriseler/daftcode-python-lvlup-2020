from typing import Dict
from hashlib import sha256
from fastapi import FastAPI, Request, Response, status, Cookie, HTTPException, Query, Body, Form
from starlette.responses import RedirectResponse
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


app = FastAPI()
app.secret_key = "wUYwdjICbQP70WgUpRajUwxnGChAKmRtfQgYASazava4p5In7pZpFPggdB4JDjlv"
app.patients=[]

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(jsonable_encoder({"detail": exc.errors(), "body": exc.body}))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcome():
    return "Jakiś powitalny tekst!"

class LoginRq(BaseModel):
    login: str = None
    password: str = Query(None, alias="pass")

@app.post("/login")
def create_cookie(rq: LoginRq):#response: Response
    print(str(rq))
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return "ABC"+str(rq)
    '''print(user)
    print(password)
    if user == "trudnY":
        response.status_code = status.HTTP_302_FOUND
        response.headers["Location"] = "/welcome"
        session_token = sha256(bytes(f"{login}{password}{app.secret_key}", encoding='utf8')).hexdigest()
        response.set_cookie(key="session_token", value=session_token)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED'''

@app.get("/method")
@app.post("/method")
@app.put("/method")
@app.delete("/method")
def get_method(request: Request):
    return {"method": str(request.method)}

class PatientRq(BaseModel):
    name: str
    surename: str


class PatientResp(BaseModel):
    id: int
    patient: Dict


@app.post("/patient", response_model=PatientResp)
def receive_patient(rq: PatientRq): 
    app.patients.append(rq.dict())
    return PatientResp(id=len(app.patients)-1, patient=rq.dict())

@app.get("/patient/{pk}")
def get_patient(pk: int, response: Response, status_code=status.HTTP_200_OK):
    if len(app.patients)>pk:
        return app.patients[pk]
    response.status_code = status.HTTP_204_NO_CONTENT