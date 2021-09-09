from django.db import models
from django_mysql.models import ListTextField
from django.contrib.auth.models import User

class Users(User):
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    # username = models.CharField(max_length=30,unique = True)
    # password = models.CharField(max_length=30)
    avatar = models.CharField(max_length=30)
    # active = models.BooleanField(default=False)
    token = models.UUIDField(null=True)
    contacts_id = ListTextField(
                base_field = models.IntegerField(),
                size=1000)
    gps_id = ListTextField(
                base_field = models.IntegerField(),
                size=1000)




    def get_fullname(self):
        return self.first_name + ' ' + self.last_name




class Messages(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='receiver')
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0) # 0:nothing  1: send   2: recieve   3: seen

    def __str__(self):
        return self.text

class Gp(models.Model):
    name = models.CharField(max_length=30)
    members = ListTextField(
                base_field = models.IntegerField(),
                size=1000)
    admin = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='admin')

    def __str__(self):
        return self.name


class Gp_messages(models.Model):
    gp = models.ForeignKey(Gp,on_delete=models.CASCADE,related_name='gp')
    text = models.TextField()
    sender = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='sendergp')
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0) # 0:nothing  1: send   2: recieve  3: seen
