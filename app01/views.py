from django.shortcuts import render,redirect,HttpResponse
from app01 import models,forms
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
            request.session["user"]=user
        else:
            login_response["error_msg"] = "用户名密码错误！"
        return HttpResponse(json.dumps(login_response))

def index(request):
    """
    问卷列表页面
    """
    if request.method=="GET":
        questionnaire=models.Quesrionnaire.objects.all()
        return render(request,"index.html",{'questionnaire':questionnaire})

def new_questionnaire(request):
    """
    新建问卷
    """
    if request.method=="GET":
        questions=models.Question.objects.all()
        class_list=models.Classlist.objects.all()
        return render(request,"new_questionnaire.html",{'questions':questions,"class_list":class_list})
    else:
        title=request.POST.get("title")
        cls_id=request.POST.get("cls")
        print(title)
        models.Quesrionnaire.objects.create(title=title,cls_id=cls_id)
        return HttpResponse("")

def edit_questionnaire(request,naire_id):
    if request.method=="GET":
        def create_question():
            question_list = models.Question.objects.filter(questionnaire_id=naire_id)
            if not question_list:
                #新问卷
                form=forms.Quetsion_form()
                yield {"form":form,"question":None,"option_class":"hide","options":forms.Option_form()}
            else:
                #含有问题的问卷
                for question in question_list:
                    form=forms.Quetsion_form(instance=question)
                    temp={"form":form,"question":None,"option_class":"hide","options":None}
                    if question.type==2:
                        temp["option_class"]=""
                        def create_option(que):
                            option_list=models.Option.objects.filter(question=que)
                            for option in option_list:
                                form=forms.Option_form(instance=option)
                                yield {"form":form,"option":option}
                        temp["options"]=create_option(question)
                    yield temp
        return render(request,"edit_questionnaire.html",{"questionform_list":create_question(),})
# Create your views here.
