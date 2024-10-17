import uuid

from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Model, Brand, Group, CustomUser, GlobalApiKey, Client
from .permissions import  require_api_key, IsAuthenticatedAndEnabled
from .serializers import RegisterSerializer, ModelSerializer, MarqueSerializer, GroupeSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.http import HttpResponseForbidden, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import GlobalApiKey
def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser, login_url='/login/')
def manage_api_key(request):
    raw_key = None
    message = None

    if request.method == 'POST':
        name = request.POST.get('name')

        if 'send_email' in request.POST:
            raw_key = GlobalApiKey.generate_raw_key()
            hashed_key = GlobalApiKey.hash_key(raw_key)

            new_api_key = GlobalApiKey.objects.create(
                key=hashed_key,
                name=name,
                is_active=True
            )

            send_mail(
                'Votre Clé API',
                f'Voici votre clé API : {raw_key}\n Pour {name}  \n Utilisez-la pour accéder aux services.',
                'charles.agostinelli26@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
            message = f"La clé API brute a été envoyée à {request.user.email}."

    return render(request, '../templates/manage_api_key.html', {'message': message})
@require_api_key
def protected_api_view(request):
    data = {
        'message': 'Vous avez accédé à une API protégée avec une clé API valide.'
    }
    return JsonResponse(data)
class APIDocumentationView(TemplateView):
    template_name = "../templates/documentation.html"
@login_required
@user_passes_test(is_superuser, login_url='/login/')
def manage_users(request):
    users = CustomUser.objects.filter(enabled=0)
    models = Model.objects.all()
    brands = Brand.objects.all()
    groups = Group.objects.all()

    return render(request, '../templates/manage_users.html', {
        'users': users,
        'models': models,
        'brands': brands,
        'groups': groups
    })

class CreateClientView(APIView):
    permission_classes = [IsAuthenticatedAndEnabled]

    def post(self, request):
        client_id = request.data.get('client_id')
        email = request.data.get('email')
        api_key = request.data.get('api_key')
        count = request.data.get('count', 1000)
        uuid = request.data.get('uuid')

        if Client.objects.filter(client_id=client_id).exists():
            return Response({"error": "Client déjà enregistré"}, status=status.HTTP_400_BAD_REQUEST)

        new_client = Client(client_id=client_id, email=email, api_key=api_key, count=count, uuid=uuid)
        new_client.save()

        return Response({
            "message": "Client créé avec succès",
            "client_id": new_client.client_id,
            "email": new_client.email,
            "api_key": new_client.api_key,
            "count": new_client.count,
            "uuid": new_client.uuid

        }, status=status.HTTP_201_CREATED)
@login_required
@user_passes_test(is_superuser, login_url='/login/')
def accept_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.enabled = 1
    user.save()
    return redirect('manage_users')
class ProtectedView(APIView):
    permission_classes = [IsAuthenticatedAndEnabled]

    def get(self, request):
        return Response({"message": "Vous êtes authentifié et pouvez accéder à cette vue."}, status=200)

class CustomLoginView(FormView):
    template_name = '../templates/registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('manage_users')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(self.request, user)
                return redirect(self.get_success_url())
            else:
                return HttpResponseForbidden("Accès refusé. Vous n'avez pas les droits d'administrateur.")
        else:
            messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect.")
            return self.form_invalid(form)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetClientCountByUUIDView(APIView):
    permission_classes = [IsAuthenticatedAndEnabled]
    def get(self, request, uuid):
        client = get_object_or_404(Client, uuid=uuid)

        return Response({'count': client.count}, status=status.HTTP_200_OK)


class DeleteClientByUUIDView(APIView):

    def delete(self, request, uuid):
        # Cherche le client par son UUID
        client = get_object_or_404(Client, uuid=uuid)

        # Supprime le client
        client.delete()

        # Renvoie une réponse avec un statut HTTP 200
        return Response({'message': 'Client supprimé avec succès.'}, status=status.HTTP_200_OK)

###############Model###############

class ModelCreateView(generics.CreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticatedAndEnabled]

class ModelUpdateView(generics.UpdateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticatedAndEnabled]

class ModelListView(generics.ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticatedAndEnabled]  # Utilisation correcte de la permission
class ModelDeleteView(generics.DestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticatedAndEnabled]

###############Marque###############
class MarqueCreateView(generics.CreateAPIView):
        queryset = Brand.objects.all()
        serializer_class = MarqueSerializer
        permission_classes = [IsAuthenticatedAndEnabled]

class MarqueUpdateView(generics.UpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = MarqueSerializer
    permission_classes = [IsAuthenticatedAndEnabled]

class MarqueListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = MarqueSerializer
    permission_classes = [IsAuthenticatedAndEnabled]

class MarqueDeleteView(generics.DestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = MarqueSerializer
    permission_classes = [IsAuthenticatedAndEnabled]

###############Groupe###############
class GroupeCreateView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticatedAndEnabled]

class GroupeUpdateView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticatedAndEnabled]


class GroupeListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticatedAndEnabled]

class GroupeDeleteView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticatedAndEnabled]