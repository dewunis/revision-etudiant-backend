from django.db import models
from user.models import User
from django.utils.translation import gettext as _

class PasswordResetCode(models.Model):
    class Meta :
        verbose_name = _('Code de réinitialisation')
        verbose_name_plural = _('Codes de réinitialisation')
    
    code = models.CharField(max_length=6,null=False,blank=False,)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=False)
    expiration_date = models.DateTimeField(verbose_name=_('Date d\'expiration'),)
    
    def __str__(self):
        return self.code
