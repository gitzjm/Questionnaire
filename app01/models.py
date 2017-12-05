from django.db import models


class Userinfo(models.Model):
    """
    教师表
    """
    user = models.CharField(verbose_name="用户名", max_length=32)
    pwd = models.CharField(verbose_name="密码", max_length=32)
    emali = models.EmailField()

    def __str__(self):
        return self.user


class Classlist(models.Model):
    """
    班级表
    """
    title = models.CharField(verbose_name="班级名", max_length=32)

    def __str__(self):
        return self.title


class Student(models.Model):
    """
    学生表
    """
    user = models.CharField(verbose_name="用户名", max_length=32)
    pwd = models.CharField(verbose_name="密码", max_length=32)
    cls = models.ForeignKey(verbose_name="所属班级", to=Classlist)

    def __str__(self):
        return self.user


class Quesrionnaire(models.Model):
    """
    问卷表
    """
    title = models.CharField(verbose_name="问卷标题", max_length=128)
    create_time = models.DateTimeField(auto_now_add=True)
    cls = models.ForeignKey(verbose_name="调查班级", to=Classlist)

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    问题表
    """
    title = models.CharField(verbose_name="问题", max_length=128)
    que_types = (
        (1, "评分"),
        (2, "单选"),
        (3, "评价"),
    )
    type = models.IntegerField(verbose_name="问题类型", choices=que_types)
    questionnaire = models.ForeignKey(to=Quesrionnaire)

    def __str__(self):
        return self.title


class Option(models.Model):
    """
    问题选项表
    """
    title = models.CharField(verbose_name="选项名", max_length=256)
    value = models.CharField(max_length=256)
    question = models.ForeignKey(to=Question)

    def __str__(self):
        return self.title


class Answer(models.Model):
    """
    答案表
    """
    user = models.ForeignKey(to=Student)
    question = models.ForeignKey(to=Question)
    questionnaire = models.ForeignKey(to=Quesrionnaire)
    create_time = models.DateTimeField(auto_now_add=True)
    val = models.IntegerField(null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)  # Create your models here.
