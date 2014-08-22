
import os, hashlib
from im.views.common import *


ADDR_SERVER = '54.255.173.40/f'

SIZE_SMALL_IMAGE = 60
UPLOAD_FILE_PATH = '/var/www/im/im/upload'

STATUS_IMAGE_PATH = UPLOAD_FILE_PATH + '/s/i/'
STATUS_AUDIO_PATH = UPLOAD_FILE_PATH + '/s/a/'

MESSAGE_IMAGE_PATH = UPLOAD_FILE_PATH + '/m/i/'
MESSAGE_AUDIO_PATH = UPLOAD_FILE_PATH + '/m/a/'

PROFILE_AVATAR_PATH = UPLOAD_FILE_PATH + '/p/a/'
PROFILE_PHOTO_PATH  = UPLOAD_FILE_PATH + '/p/p/'

OTHER_PATH = UPLOAD_FILE_PATH + '/o/'

def GetFileExtension(file):
    ext = ''
    if '.' in file.name:
        ext = file.name.split('.')[-1]
    return ext


FILE_PATH = {
    'StatusImage'  : STATUS_IMAGE_PATH,
    'StatusAudio'  : STATUS_AUDIO_PATH,
    'MessageImage' : MESSAGE_IMAGE_PATH,
    'MessageAudio' : MESSAGE_AUDIO_PATH,
    'ProfileAvatar': PROFILE_AVATAR_PATH,
    'ProfilePhoto' : PROFILE_PHOTO_PATH,
}

def GetFilePathByType(type):
    if type in FILE_PATH:
        path = FILE_PATH[type]
    else:
        path = OTHER_PATH    

    return path

def SaveFile(file, type):
    ext = GetFileExtension(file)
    path = GetFilePathByType(type)

    content = file.read()
    fid = hashlib.md5(content).hexdigest()
    if ext:
        fid = fid + '.' + ext

    fullpath = os.path.join(path, fid)
    f = open(fullpath, 'w+')
    f.write(content)
    f.close()

    url = 'http://' + ADDR_SERVER + path[len(UPLOAD_FILE_PATH):] + fid
    if type in ["StatusImage", "MessageImage", "ProfilePhoto"]:
        os.system('convert %s -resize %d %s' %(fullpath, SIZE_SMALL_IMAGE, os.path.join(path, "tb_" + fid)))

    return (fullpath,url)


def DeleteFile(filepath):
    try:
        os.remove(filepath)
        ext = filepath.split('.')[-1]
        if ext in ['jpg', 'jpeg', 'png']:
            tb = os.path.join(os.path.dirname(filepath), 'tb_' + os.path.basename(filepath))
            os.remove(tb)
    except:
        pass 


def UploadMessageFile(request):
    ret = {}

    try:
        file = request.FILES.get('file')
        ext = GetFileExtension(file)
        
        if ext in ['jpg', 'jpeg', 'png']:
            (path,url) = SaveFile(file, "MessageImage")
        elif ext in ['pcm', 'aud']:
            (path,url) = SaveFile(file, "MessageAudio")
        else:
            (path,url) = ('', '')

        ret['url'] = url
        
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)
