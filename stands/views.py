from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from .models import Stand, Validation
from .serializers import StandSerializer, StandListSerializer, ValidateStandSerializer
from src.services.email_service import EmailService

class StandViewSet(viewsets.ModelViewSet):
    queryset = Stand.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return StandListSerializer
        return StandSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='validate')
    def validate_stand(self, request, pk=None):
        stand = self.get_object()
        serializer = ValidateStandSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.user.role != 'admin':
            return Response(
                {'error': 'Seul un administrateur peut valider les stands'},
                status=status.HTTP_403_FORBIDDEN
            )

        if stand.statut != 'en_attente':
            return Response(
                {'error': f'Ce stand est déjà {stand.statut}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        temp_password = serializer.validated_data['validation_password']
        comment = serializer.validated_data.get('comment', '')

        stand.temp_password = make_password(temp_password)
        stand.validation_comment = comment
        stand.save()

        try:
            EmailService.send_temp_password_email(stand, temp_password)
        except Exception as e:
            print(f"Erreur email: {e}")

        return Response({
            'message': 'Stand prêt à être activé ! Un email a été envoyé au propriétaire.',
            'stand': StandSerializer(stand).data
        })

    @action(detail=True, methods=['post'], url_path='activate', permission_classes=[AllowAny])
    def activate_stand(self, request, pk=None):
        stand = self.get_object()
        password = request.data.get('password')

        if not password:
            return Response(
                {'error': 'Mot de passe requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not stand.temp_password:
            return Response(
                {'error': "Ce stand n'a pas encore été validé par l'administrateur"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, stand.temp_password):
            return Response(
                {'error': 'Mot de passe incorrect'},
                status=status.HTTP_403_FORBIDDEN
            )

        stand.statut = 'valide'
        stand.password = stand.temp_password
        stand.temp_password = None
        stand.save()

        Validation.objects.create(
            stand=stand,
            valide_par=request.user,
            password_validation=password
        )

        return Response({
            'message': 'Stand activé avec succès !',
            'stand': StandSerializer(stand).data
        })

    @action(detail=False, methods=['get'], url_path='stats')
    def get_stats(self, request):
        total = Stand.objects.count()
        valides = Stand.objects.filter(statut='valide').count()
        attente = Stand.objects.filter(statut='en_attente').count()

        return Response({
            'total': total,
            'valides': valides,
            'attente': attente
        })
