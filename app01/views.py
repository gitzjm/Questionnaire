# -*- coding: utf-8 -*
from django.shortcuts import render, redirect, HttpResponse
from app01 import models, forms
import json


def login(request):
    """
    登录
    """
    if request.method == "GET":
        return render(request, "login.html")
    else:
        user = request.POST.get("username")
        pwd = request.POST.get("password")
        print(user, pwd)
        login_response = {"is_login": False, "error_msg": None}
        if models.Userinfo.objects.filter(user=user, pwd=pwd) or models.Userinfo.objects.filter(emali=user, pwd=pwd):
            login_response["is_login"] = True
            request.session["user"] = user
        else:
            login_response["error_msg"] = "用户名密码错误！"
        return HttpResponse(json.dumps(login_response))


def index(request):
    """
    问卷列表页面
    """
    if request.method == "GET":
        questionnaire = models.Quesrionnaire.objects.all()
        return render(request, "index.html", {'questionnaire': questionnaire})


def new_questionnaire(request):
    """
    新建问卷
    """
    if request.method == "GET":
        questions = models.Question.objects.all()
        class_list = models.Classlist.objects.all()
        return render(request, "new_questionnaire.html", {'questions': questions, "class_list": class_list})
    else:
        title = request.POST.get("title")
        cls_id = request.POST.get("cls")
        print(title)
        models.Quesrionnaire.objects.create(title=title, cls_id=cls_id)
        return HttpResponse("")


def edit_questionnaire(request, naire_id):
    if request.method == "GET":
        questionnaire = models.Quesrionnaire.objects.filter(id=naire_id).first()

        def create_question():
            question_list = models.Question.objects.filter(questionnaire_id=naire_id)
            if not question_list:
                # 新问卷
                form = forms.Quetsion_form()
                yield {"form": form, "question": None, "option_class": "hide", "options": None}
            else:
                # 含有问题的问卷
                for question in question_list:
                    form = forms.Quetsion_form(instance=question)
                    temp = {"form": form, "question": question, "option_class": "hide", "options": None}
                    if question.type == 2:
                        temp["option_class"] = ""
                        def create_option(que):
                            option_list = models.Option.objects.filter(question=que)
                            for option in option_list:
                                form = forms.Option_form(instance=option)
                                yield {"form": form, "option": option}
                        temp["options"] = create_option(question)
                    yield temp

        return render(request, "edit_questionnaire.html",
                      {"questionform_list": create_question(), "naire": questionnaire})
    else:
        question_list=json.loads(request.POST.get("question_list"))
        print(question_list)
        for i in question_list:
            print(i["title"])
            id=i.get("question_id")
            type=i.get("type")
            title=i.get("title")
            if i.get("question_id"):
                print("1111111")
                question_obj = models.Question.objects.filter(id=id)
                question_obj.update(type=type,title=title)
            else:
                print()
                question_obj=models.Question.objects.create(type=type,title=title,questionnaire_id=naire_id)
                # print(question_obj)
            # print(question_obj)
            option_list=i.get("option")
            if option_list:
                for j in option_list:
                    if j.get("option_id"):
                        option_obj = models.Option.objects.filter(id=j.get("option_id"))
                        option_obj.update(title=j.get("title"),value=j.get("value"))
                    else:
                        models.Option.objects.create(title=j.get("title"),value=j.get("value"),question=question_obj.first())
        return HttpResponse("111")

    # [{'question_id': '1', 'title': '爱根6不6', 'type': '2',
    #   'option': [{'title': '6', 'value': '9'}, {'title': '不6', 'value': '1'}]},
    #  {'question_id': '2', 'title': '给爱根打个分', 'type': '1', 'option': None},
    #  {'question_id': '3', 'title': '给爱根评个价', 'type': '3', 'option': None}]
    # {'question_id': 'null', 'title': '啊啊啊', 'type': '1', 'option': None}

# Create your views here.
