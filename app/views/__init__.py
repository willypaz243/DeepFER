from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

views = APIRouter()
templates = Jinja2Templates(directory='app/views/templates')


@views.get('/interviewer', response_class=HTMLResponse)
async def interviewer(request: Request):
    return templates.TemplateResponse('interviewer.html', {'request': request})


@views.get('/applicant', response_class=HTMLResponse)
async def postulant(request: Request):
    return templates.TemplateResponse('applicant.html', {'request': request})
