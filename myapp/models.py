from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

class MyProfile(models.Model):
    user = models.OneToOneField("auth.User")
    date_of_birth = models.DateField(null=True)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='uploads/', default='uploads\gallery\Berlin, Germany.jpg')

    def __str__(self):
        return self.user.username

    def necessary_permmisin(self):
        User.user_permissions.clear()
        User.user_permissions.all()
        pass
