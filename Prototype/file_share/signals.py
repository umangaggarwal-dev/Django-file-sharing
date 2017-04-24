from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from .models import Folder

@receiver(post_save, sender=User)
def create_user_folders(sender, instance, created, **kwargs):
        #user = tenantUser.objects.get(pk = instance)
        #user = User.objects.get(pk = instance)
        if created:
            dir_path = "/home/umang/mera_project/Prototype/file_share/static/file_share/uploads/root%s/" % str(instance.email).replace('.', '_')
            #if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            root_folder = Folders(name='root', user=instance)
            root_folder.save()
            for folder in DEFAULT_FOLDERS:
                f = Folders(name=folder, parent=root_folder, user=instance)
                f.save()