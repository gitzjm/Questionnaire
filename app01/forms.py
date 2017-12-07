from django.forms import ModelForm, fields, widgets
from app01 import models


class Quetsion_form(ModelForm):
    class Meta:
        model = models.Question
        fields = ['title', 'type']
        widgets = {
            "title": widgets.Textarea(attrs={
                "class": "form-control",
                "style":
                    "width:600px;"
                    "height:80px;"
                    "display:inline-block;"
                    "vertical-align:top"}),
            "type": widgets.Select(attrs={
                "class":"choice_question_type form-control",
                "style":"width:200px;"
                    "height:35px;"
                    "display:inline-block;"
            })
        }


class Option_form(ModelForm):
    class Meta:
        model = models.Option
        fields = ['title', 'value']
