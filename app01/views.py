from django.shortcuts import render,redirect,HttpResponse
from app01 import models
import json
def login(request):
    """
    登录
    """
    if request.method=="GET":
        return render(request, "login.html")
    else:
        user=request.POST.get("username")
        pwd=request.POST.get("password")
        print(user,pwd)
        login_response = {"is_login": False, "error_msg": None}
        if models.Userinfo.objects.filter(user=user,pwd=pwd) or models.Userinfo.objects.filter(emali=user,pwd=pwd):
            login_response["is_login"] = True
        else:
            login_response["error_msg"] = "用户名密码错误！"
        return HttpResponse(json.dumps(login_response))

def index(request):
    if request.method=="GET":
        questionnaire=models.Quesrionnaire.objects.all()
        return render(request,"index.html",{'questionnaire':questionnaire})

def new_questionnaire(request):
    if request.method=="GET":
        questions=models.Question.objects.all()
        return render(request,"new_questionnaire.html",{'questions':questions})
# Create your views here.
