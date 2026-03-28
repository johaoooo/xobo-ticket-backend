from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
from django.utils import timezone
import secrets
import hashlib
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    UpdateProfileSerializer, ChangePasswordSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)
from .models import User


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            user.email = request.data['email']
        if 'telephone' in request.data:
            user.telephone = request.data['telephone']
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        return Response(UserSerializer(user).data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current = request.data.get('current_password')
        new_pw  = request.data.get('new_password')

        if not current or not new_pw:
            return Response(
                {'error': 'Mot de passe actuel et nouveau requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not request.user.check_password(current):
            return Response(
                {'error': 'Mot de passe actuel incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(new_pw) < 6:
            return Response(
                {'error': 'Le mot de passe doit contenir au moins 6 caractères'},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.set_password(new_pw)
        request.user.save()
        return Response({'message': 'Mot de passe modifié avec succès.'})


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Si un compte existe avec cet email, vous recevrez un lien.'})

        token = secrets.token_urlsafe(32)
        user.reset_password_token = hashlib.sha256(token.encode()).hexdigest()
        user.reset_password_expires = timezone.now() + timezone.timedelta(hours=24)
        user.save()

        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        print(f"🔑 Reset URL: {reset_url}")

        try:
            from django.core.mail import send_mail
            send_mail(
                subject="🔑 Réinitialisation de votre mot de passe - Xobo Ticket",
                message=f"Réinitialisez votre mot de passe : {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"❌ Erreur email: {e}")

        return Response({'message': 'Si un compte existe avec cet email, vous recevrez un lien.'})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token        = request.data.get('token')
        new_password = request.data.get('new_password')
        confirm      = request.data.get('confirm_password')

        if not token or not new_password:
            return Response({'error': 'Token et nouveau mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm:
            return Response({'error': 'Les mots de passe ne correspondent pas'}, status=status.HTTP_400_BAD_REQUEST)
        if len(new_password) < 6:
            return Response({'error': 'Minimum 6 caractères'}, status=status.HTTP_400_BAD_REQUEST)

        hashed = hashlib.sha256(token.encode()).hexdigest()
        try:
            user = User.objects.get(
                reset_password_token=hashed,
                reset_password_expires__gt=timezone.now()
            )
        except User.DoesNotExist:
            return Response({'error': 'Lien invalide ou expiré'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.reset_password_token = None
        user.reset_password_expires = None
        user.save()
        return Response({'message': 'Mot de passe réinitialisé avec succès.'})


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Accès refusé'}, status=status.HTTP_403_FORBIDDEN)

        from stands.models import Stand
        data = []
        for user in User.objects.filter(role='user').order_by('-date_joined'):
            nb_stands  = Stand.objects.filter(user=user).count()
            nb_valides = Stand.objects.filter(user=user, statut='valide').count()
            nb_attente = Stand.objects.filter(user=user, statut='en_attente').count()
            data.append({
                'id':         user.id,
                'username':   user.username,
                'first_name': user.first_name,
                'last_name':  user.last_name,
                'email':      user.email,
                'avatar':     request.build_absolute_uri(user.avatar.url) if user.avatar else None,
                'date_joined': user.date_joined,
                'nb_stands':  nb_stands,
                'nb_valides': nb_valides,
                'nb_attente': nb_attente,
            })
        return Response(data)
