

from django.db import models
import time

def Now():
    return int(time.time())

class Demo(models.Model):
    user_id = models.IntegerField(primary_key=True)
    dev_id = models.CharField(max_length=128)
    mac = models.CharField(max_length=32)
    token = models.CharField(max_length=128)
    password = models.CharField(max_length=128, null=True)
    nickname = models.CharField(max_length=64, default='')
    type = models.CharField(max_length=32, null=True)
    is_test = models.BooleanField(default=False)
    is_enable = models.BooleanField(default=True)
    time_created = models.IntegerField(default=Now)
    
    def toJSON(self):
        r = {}
        r['id'] = str(self.user_id)
        r['mac'] = self.mac
        r['token'] = self.token
        r['nickName'] = self.nickname
        return r


class User(models.Model):
    phonenum = models.CharField(max_length=16)
    secretkey = models.CharField(max_length=128)
    xmpp_account = models.CharField(max_length=128)
    is_test = models.BooleanField(default=False)
    is_enable = models.BooleanField(default=True)
    nickname = models.CharField(max_length=64, default='')
    gender = models.CharField(max_length=16, default='')
    avatar = models.CharField(max_length=128, default='')
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['phonenum'] = self.phonenum
        r['xmpp_account'] = self.xmpp_account
        r['nickname'] = self.nickname
        r['gender'] = self.gender
        r['avatar'] = self.avatar
        return r 
