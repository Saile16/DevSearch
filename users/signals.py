# ----USANDO SIGNALS ----
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile


# @receiver(post_save,sender=Profile)
# def profileUpdated(sender,instance,created,**kwargs):
#     print('Profile saved!!')
#     print('Instance:',instance)
#     print('Created:',created)
#     print('Kwargs:',kwargs)
#     print('Sender',sender)

# def deleteUser(sender,instance,**kwargs):
#     print('User deleted!!')
#     print('Instance:',instance)
#     print('Kwargs:',kwargs)
#     print('Sender',sender)

# post_save.connect(profileUpdated,sender=Profile)
# post_delete.connect(deleteUser,sender=Profile)

#de esta manera estamos usando los signals para un profile al momento de crear el user
def createProfile(sender,instance,created,**kwargs):
    print('Profile signla trigerred')
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

def updateUser(sender,instance,created,**kwargs):
    profile=instance
    user=profile.user

    if created == False:
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()

#de sta manera eliminamos el User ligador al profile
def deleteProfile(sender,instance,**kwargs):
    print('Profile deleted signal triggered')
    user=instance.user
    user.delete()

post_save.connect(createProfile,sender=User)
post_save.connect(updateUser,sender=Profile)
post_delete.connect(deleteProfile,sender=Profile)