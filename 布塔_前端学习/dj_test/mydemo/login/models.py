from django.db import models

# Create your models here.
#python manage.py makemigrations /migrate
class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]#元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
        verbose_name = "用户"
        verbose_name_plural = "用户"

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)#与User表字段 一对一关系
    c_time = models.DateTimeField(auto_now_add=True)# 为添加时的时间，更新对象时不会有变动

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        # db_table = 'xxx' 设置表名为xxx 不设置就默认生成app名字_类型   ( login_ConfirmString)
        ordering = ["-c_time"]#
        verbose_name = "确认码"#给模型类指定一个直观可读的信息xxx
        verbose_name_plural = "确认码"#设置verbose_name的复数
        #app_label = 'xxx'#定义模型类属于哪一个应用

# class Meta:
#     ordering = ["-c_time"]
#     verbose_name = "用户"
#     verbose_name_plural = "用户"