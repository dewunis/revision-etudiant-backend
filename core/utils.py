import os,uuid
import magic
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.conf import settings

def validate_foreign_key(model,key,message,data):
    value = data.get(key)
    if value:
        try:
            if not model.objects.filter(pk=value).exists():
                return message
        except:
            return message
        
def get_media_absolute_url(request):
    base_url = settings.MEDIA_URL
    return request.build_absolute_uri(base_url)
        
def get_unique_filename(filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return unique_filename
        
def validate_image_extension(value):
    allowed_extensions = ['jpg', 'jpeg', 'png']
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in allowed_extensions:
        raise ValidationError(_('Extension de fichier invalide. Veuillez télécharger un fichier image valide.'))
    
def validate_latex_file(value):
    allowed_extensions = ['tex',]
    ext = os.path.splitext(value.name)[1][1:].lower()

    if ext not in allowed_extensions:
        raise ValidationError(_('Le fichier doit avoir l\'extension .tex.'))
