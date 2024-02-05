from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings

from .models import PasswordResetCode
from user.models import User

from .serializers import (
    PasswordResetCreateCodeSerializer,
    PasswordResetConfirmCodeSerializer,
    PasswordResetSerializer
)

class PasswordResetApiView(APIView):
    """
    Vue API pour gérer les demandes de réinitialisation de mot de passe.

    Cette vue permet aux utilisateurs de réinitialiser leur mot de passe en fournissant un code valide.

    Méthodes :
    - post : Gère les demandes de réinitialisation de mot de passe.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Gère les requêtes POST pour réinitialiser les mots de passe utilisateur.

        Paramètres :
        - request : L'objet de requête HTTP.
        - args : Arguments positionnels supplémentaires.
        - kwargs : Arguments de mot-clé supplémentaires.

        Retourne :
        - Response : Une réponse JSON indiquant le résultat de la demande de réinitialisation de mot de passe.
        """
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        password = request.data.get('password')
        code = request.data.get('code')

        # Vérifie si le code de réinitialisation est valide et non expiré
        try:
            password_reset_code = PasswordResetCode.objects.get(code=code, expiration_date__gte=timezone.now())
        except PasswordResetCode.DoesNotExist:
            return Response({'message': 'Code de réinitialisation invalide ou expiré',}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, email=email)
        except Http404:
            return Response({'message': 'Compte avec cette adresse email non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.save()
        password_reset_code.delete()

        return Response({'message': 'Mot de passe réinitialisé avec succès.'})


password_reset_api_view = PasswordResetApiView.as_view()


class PasswordResetConfirmCodeApiView(APIView):
    """
    Vue API pour confirmer la validité d'un code de réinitialisation de mot de passe.

    Cette vue permet aux utilisateurs de confirmer si un code de réinitialisation fourni est valide.

    Méthodes :
    - post : Gère les requêtes POST pour confirmer les codes de réinitialisation.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Gère les requêtes POST pour confirmer la validité des codes de réinitialisation.

        Paramètres :
        - request : L'objet de requête HTTP.
        - args : Arguments positionnels supplémentaires.
        - kwargs : Arguments de mot-clé supplémentaires.

        Retourne :
        - Response : Une réponse JSON indiquant le résultat de la confirmation du code.
        """
        serializer = PasswordResetConfirmCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = request.data.get('code')

        # Vérifie si le code de réinitialisation est valide et non expiré
        try:
            PasswordResetCode.objects.get(code=code, expiration_date__gte=timezone.now())
        except PasswordResetCode.DoesNotExist:
            return Response({'code': 'Code invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Code de réinitialisation valide.'})


password_reset_confirm_code_api_view = PasswordResetConfirmCodeApiView.as_view()


class PasswordResetCodeCreateApiView(APIView):
    """
    Vue API pour créer et envoyer des codes de réinitialisation de mot de passe.

    Cette vue permet aux utilisateurs de demander un code de réinitialisation de mot de passe, qui est ensuite envoyé à leur adresse e-mail.

    Méthodes :
    - post : Gère les requêtes POST pour créer et envoyer des codes de réinitialisation.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Gère les requêtes POST pour créer et envoyer des codes de réinitialisation.

        Paramètres :
        - request : L'objet de requête HTTP.
        - args : Arguments positionnels supplémentaires.
        - kwargs : Arguments de mot-clé supplémentaires.

        Retourne :
        - Response : Une réponse JSON indiquant le résultat du processus de création et d'envoi de code.
        """
        serializer = PasswordResetCreateCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')

        try:
            user = get_object_or_404(User, email=email)
        except Http404:
            return Response({'message': 'Compte avec cette adresse email non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        expiration_date = timezone.now() + timezone.timedelta(minutes=15)
        code = get_random_string(length=6, allowed_chars='012GXPMBGAR3456GHPTI789')

        # Supprime tous les anciens codes de réinitialisation de mot de passe pour l'utilisateur
        try:
            old_password_reset_code = PasswordResetCode.objects.get(user=user)
            old_password_reset_code.delete()
        except PasswordResetCode.DoesNotExist:
            pass  # Pas besoin de supprimer s'il n'existe pas
        
        PasswordResetCode.objects.create(user=user, code=code, expiration_date=expiration_date)

        send_mail(
            'Code de réinitialisation de mot de passe',
            f'Le code pour réinitialiser votre mot de passe est : {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True,
        )

        return Response({'message': 'Renseigner le code reçu par email pour retrouver votre mot de passe.'})


password_reset_create_code_api_view = PasswordResetCodeCreateApiView.as_view()
