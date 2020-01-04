from django.db import models





# Create your models here.
class BookInfo(models.Model):
    title = models.CharField(max_length=20)
    pub_date = models.DateField()
    read = models.IntegerField(default=0)#阅读量
    comment = models.IntegerField(default=0)#评论量
    is_delete = models.BooleanField(default=False)#逻辑删除
    def __str__(self):
        return self.title

class HeroInfo(models.Model):
    name = models.CharField(max_length=20)
    gender = models.BooleanField()
    comment = models.CharField(max_length=100)
    is_delete = models.BooleanField(default=False)
    book = models.ForeignKey("BookInfo",on_delete=models.CASCADE)#在老版本中 on_delete=models.CASCADE是默认参数  新版本需添加此参数 不然会报错
    def __unicode__(self):
        return self.name