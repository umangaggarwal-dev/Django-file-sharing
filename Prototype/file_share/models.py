from __future__ import unicode_literals
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import uuid
import datetime
from django.template import loader
from django.core.mail import send_mail
import os
from django.conf import settings

DEFAULT_FOLDERS = ['Documents','Images','Voices']

class Folder(MPTTModel):
    name = models.CharField(max_length = 100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

    @receiver(post_save, sender=User)
    def create_user_folders(sender, instance, created, **kwargs):
            #user = tenantUser.objects.get(pk = instance)
            #user = User.objects.get(pk = instance)
            if created:
                root = "root%s" % str(instance.email).replace('.', '_')
                dir_path = "/home/umang/mera_project/Prototype/file_share/static/file_share/uploads/%s/" % root
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                    root_folder = Folder(name=root, user=instance)
                    root_folder.save()
                    for folder in DEFAULT_FOLDERS:
                        f = Folder(name=folder, parent=root_folder, user=instance)
                        f.save()
#def get_dest(instance, filename):
#    return 


class File(models.Model):
    file = models.FileField()
    folder = models.ForeignKey(Folder, on_delete = models.CASCADE)
    #key = models.TextField()


class newFile(models.Model):
    filename = models.TextField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    shared_key = models.TextField(null = True, blank=True)
    @property
    def relative_path(self):
        return os.path.relpath(self.path, settings.MEDIA_ROOT)

class PasswordChangeRequest(models.Model):
    ID = models.CharField(max_length = 36, unique=True, default=uuid.uuid4)
    time = models.DateField(default = datetime.date.today)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)

@receiver(post_save, sender=PasswordChangeRequest)
def change_password_mail(sender, instance, created, **kwargs):
    user = str(instance.UserId.username)
    key = str(instance.ID)
    subject = "Reset password confirmation mail"
    message = "Click on the link"
    from_email = 'umangaggarwal31@gmail.com'
    to = [str(instance.UserId.email)]
    html_message = loader.render_to_string(
        "file_share/forgot_password_mail.html",
        {
            'username': user,
            'key': key
        }

    )
    send_mail(subject, message, from_email, to, fail_silently=True, html_message=html_message)


class Trust(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='source')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')