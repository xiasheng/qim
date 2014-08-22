
from im.views.common import *
from im.models.models import User
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import random, hashlib
from im.views.zmqsender import AddUser2Group
from im.views.file import SaveFile

def generateXmppAccount(phonenum):
    return phonenum + '@d-connected.com'

def generateSecretKey():
    return RandomStr(128)

def generateSessionId(phonenum):
    return RandomStr()
    
def checkSessionId(sid):
    return True

def checkVerify(verify):
    return True
    
def checkPhoneNum(phonenum):
    p = re.compile(r'((^13[0-9]|15[0|3|6|7|8|9]|18[8|9])\d{8}$)')
    if phonenum and p.match(phonenum):
        return True
    raise MyException(info='illegal phonenum')


def checkRegisterSign(phonenum, nonce, token):
    if token == hashlib.md5(phonenum + nonce).hexdigest():
        return True

    raise MyException(info='token error')



def checkAuthSign(phonenum, nonce, token, secretkey):
    if token == hashlib.md5(phonenum + nonce + secretkey).hexdigest():
        return True

    raise MyException(info='token error')
    


def RequireAuth(view):
    def new_view(request, *args, **kwargs):

        try:
            phonenum = request.REQUEST.get('phonenum')
            nonce = request.REQUEST.get('nonce')
            token = request.REQUEST.get('token')

            user = User.objects.get(phonenum=phonenum)

            checkAuthSign(phonenum, nonce, token, user.secretkey)

            request.META['USER'] = user
            return view(request, *args, **kwargs)

        except:
            return ErrorResponse(E_AUTH)

    return new_view  

   
def ExternalAuth(request):
    try:
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = User.objects.get(phonenum=name)
        
        if password == hashlib.md5(name + user.secretkey).hexdigest():
            return HttpResponse("success", status=200)
    except:
        pass

    return HttpResponse('failed', status=400)    
    

def Register1(request):
    ret = {}

    try:
        phonenum = request.POST.get('phonenum')
        nonce = request.POST.get('nonce')
        token = request.POST.get('token')

        checkRegisterSign(phonenum, nonce, token)

        ret['sid'] = generateSessionId(phonenum)
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)
        

def Register2(request):
    ret = {}

    try:
        phonenum = request.POST.get('phonenum')
        nonce = request.POST.get('nonce')
        sid = request.POST.get('sid')
        verify = request.POST.get('verify')
        token = request.POST.get('token')

        checkRegisterSign(phonenum, nonce, token)
        checkSessionId(sid)
        checkVerify(verify)

        try:
            user = User.objects.get(phonenum=phonenum)
        except ObjectDoesNotExist:
            user = User.objects.create(phonenum=phonenum, secretkey=generateSecretKey(), xmpp_account=generateXmppAccount(phonenum))
            AddUser2Group(phonenum, 'test')
 
        ret['user'] = user.toJSON()
        ret['user']['secretkey'] = user.secretkey

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)        


def GetFriends(request):
    ret = {}
    try:
        users = User.objects.filter(is_enable=True)
        ret['users'] = []
        for u in users:
            ret['users'].append(u.toJSON())
    except:
        pass

    return SuccessResponse(ret)  


def UpdateProfile(request):
    ret = {}

    try:
        user = request.META['USER']
        
        user.nickname = request.POST.get('nickname', user.nickname)
        user.gender = request.POST.get('gender', user.gender)
        file = request.FILES.get('file', None)       
        if file:
            (path, user.avatar) = SaveFile(file, 'ProfileAvatar')

        user.save()
        ret['profile'] = user.toJSON()
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)   


def GetProfile(request):
    ret = {}

    try:
        user = request.META['USER']
        ret['profile'] = user.toJSON()
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)



def CreateTestUsers(request):
    ret = {}
    ret['users'] = []

    try:

        num = int(request.POST.get('num', 8))
        
        pre = '1380000000'

        for i in range(num):
            phonenum = pre + str(i+1)
            user = User.objects.create(phonenum=phonenum, secretkey=generateSecretKey(), xmpp_account=generateXmppAccount(phonenum), is_test=True)
            ret['users'].append(user.toJSON())

        return SuccessResponse(ret)
    except IOError:
        return ErrorResponse(E_SYSTEM)

def DeleteTestUsers(request):
    ret = {}

    try:
        users = User.objects.filter(is_test=True)

        for user in users:
            user.delete()
    except:
        pass

    return SuccessResponse(ret)


def ShowAllUser(request):
    ret = {}
    try:
        count = User.objects.all().count()
        users = User.objects.all()
        ret['count'] = count
        ret['users'] = []
        for u in users:
            ret['users'].append(u.toJSON())
    except:
        pass

    return SuccessResponse(ret)

