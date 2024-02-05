import re
from rest_framework import serializers
from django.utils.translation import gettext as _

def validate_password(value):
    if len(value) < 6:
        raise serializers.ValidationError(_('Doit contenir au moins 6 caractères.'))
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise serializers.ValidationError(_('Doit contenir au moins un symbole.'))