import re
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from study.models import Level,Cursus,Formation,SchoolSystem
from core.utils import validate_foreign_key
from core.settings import COUNTRIES_ONLY
from django.core.exceptions import ObjectDoesNotExist


def validate_password(value):
    if len(value) < 6:
        raise serializers.ValidationError(_('Doit contenir au moins 6 caractères.'))
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise serializers.ValidationError(_('Doit contenir au moins un symbole.'))

def validate_foreign_keys(data):
    from .models import Avatar
    errors = {}
    finaly_errors = {}
    
    errors['level_id'] = validate_foreign_key(Level,message="Niveau non trouvé.",data=data,key='level_id')
    errors['avatar_id'] = validate_foreign_key(Avatar,message="Avatar non trouvé.",data=data,key='avatar_id')
    errors['cursus_id'] = validate_foreign_key(Cursus,message="Cursus non trouvé.",data=data,key='cursus_id')
    errors['formation_id'] = validate_foreign_key(Formation,message="Formation non trouvé.",data=data,key='formation_id')
    errors['user_id'] = validate_foreign_key(get_user_model(),message="Utilisateur non trouvé.",data=data,key='user_id')
    errors['school_system_id'] = validate_foreign_key(SchoolSystem,message="Système scolaire non trouvé.",data=data,key='school_system_id')
    
    for error in errors :
        if errors[error] is not None :
            finaly_errors[error] = errors[error]
        
    return finaly_errors
        

def validate_name(value):
    if value and len(value) < 2:
        raise serializers.ValidationError("Doit contenir au moins 2 caractères.")
    
    if value and re.search(r'[0-9]', value):
        raise serializers.ValidationError("Doit pas contenir de chiffre.")
    
def validate_country(value):
    if value not in COUNTRIES_ONLY :
        raise serializers.ValidationError("Pays non pris en charge.")
    
    
def vaildate_formation_choice(data):
    formation_id = data.get('formation_id')
    cursus_id = data.get('cursus_id')
    try :
        cursus = Cursus.objects.get(pk=cursus_id)    
    except Exception:
        raise serializers.ValidationError({"cursus_id": _("Cursus non trouvé.")})
     
    if formation_id :
        try :
            formation = Formation.objects.get(pk=formation_id)
        except Exception :
            raise serializers.ValidationError({"formation_id": _("Formation non trouvé.")})
    
        # Vérifier si la formation appartient au cursus spécifié
        if int(formation.cursus_id) != int(cursus_id) :
            raise serializers.ValidationError({"formation_id": _(f"Cette formation n'appartient pas a ce cursus : {cursus.name}.")})
    else :
        # Si aucune formation n'est fournie mais que le cursus doit posseder une formation. 
        formations = Formation.objects.filter(cursus=cursus)
        if formations :
            raise serializers.ValidationError({"formation_id": _(f"Vous devez spécifier une formation pour ce cursus : {cursus.name}.")})