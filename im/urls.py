
from django.conf.urls import patterns, include, url

from views.user import Register1, Register2, RequireAuth, GetFriends, ExternalAuth, UpdateProfile, GetProfile
from views.user import CreateTestUsers, DeleteTestUsers, ShowAllUser
from views.file import UploadMessageFile

urlpatterns = patterns('',

    url(r'^register/s1/$', Register1),
    url(r'^register/s2/$', Register2),
    url(r'^auth/external/$', ExternalAuth),
    url(r'^friends/show/$', RequireAuth(GetFriends)),

    url(r'^profile/update/$', RequireAuth(UpdateProfile)),
    url(r'^profile/show/$', RequireAuth(GetProfile)),

    url(r'^file/upload/$', RequireAuth(UploadMessageFile)),


    url(r'^test/user/create/$', CreateTestUsers),
    url(r'^test/user/delete/$', DeleteTestUsers),
    url(r'^test/user/show/$', ShowAllUser),

)

