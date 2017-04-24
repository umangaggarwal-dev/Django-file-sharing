from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^drive/$', views.drive, name='drive'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^folders/(?P<folder>[\w\-]+)/$', views.folders, name='folders'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^share/$', views.share, name='share'),
    url(r'^validate_username/$', views.validate_username, name='validate_username'),
    url(r'^forgot_mail/$', views.forgot_mail, name='forgot_mail'),
    url(r'^forgot_mail_confirmation/$', views.forgot_mail_confirmation, name='confirm_password'),
    url(r'^addfriends/$', views.make_trust, name='addfriends'),
    url(r'^search_users/$', views.search_users, name='search_users'),
    url(r'^files/pdf/(?P<filename>\{w{40})/$', views.pdf_download),
]   