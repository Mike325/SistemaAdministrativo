from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Usuario(models.Model):
    user = models.OneToOneField(User)
    codigo = models.CharField(max_length=9)
  #  rol = models.ForeignKey(Rol)

    def __unicode__(self):
        return self.user.username
        pass



#class Rol(models.Model):
 #   tipo = 
