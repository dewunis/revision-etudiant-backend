from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from study.models import Formation,Cursus,Level,SchoolSystem,Degree
from core.utils import get_unique_filename,validate_image_extension

from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
from password.validators import validate_password

# Modèle pour représenter l'avatar d'un étudiant
class Avatar(models.Model):
    class Meta :
        verbose_name = _('Avatar')
        verbose_name_plural = _('Avatars')
        
    avatar = models.FileField(upload_to='avatar/',null=True,blank=False,verbose_name=_('Avatar'),validators=[validate_image_extension],)

    def save(self, *args, **kwargs):
        if self.avatar:
            self.avatar.name = get_unique_filename(self.avatar.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.avatar}"
    
    @property
    def short_url(self):
        return self.avatar.url

# Modèle pour représenter un utilisateur personnalisé
class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')

    email = models.EmailField(unique=True, null=False, verbose_name=_('E-mail'))
    first_name = models.CharField(max_length=30, verbose_name=_('Prénom'))
    last_name = models.CharField(max_length=30, verbose_name=_('Nom'))
    password = models.TextField(null=False, validators=[validate_password], verbose_name=_('Mot de passe'))
    phone_number = PhoneNumberField(null=True,blank=True,verbose_name=_('Numéro de téléphone'),)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=False, verbose_name=_('Avatar'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date d\'inscription'),)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Modèle pour représenter le profil d'un étudiant
class Profil(models.Model):
    class Meta:
        verbose_name = _('Profil Étudiant')
        verbose_name_plural = _('Profils Étudiant')

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, blank=False, null=True, verbose_name=_('Niveau d\'étude'))
    cursus = models.ForeignKey(Cursus, on_delete=models.SET_NULL, blank=False, null=True)
    school_system = models.ForeignKey(SchoolSystem, on_delete=models.SET_NULL, blank=False, null=True, verbose_name=_('Système scolaire'))
    country = CountryField(verbose_name=_('Pays'),null=False,blank=False,default="TG")
    formation = models.ForeignKey(Formation, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Étudiant {self.user.last_name} {self.user.first_name} - {self.user.email}"
