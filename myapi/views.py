from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Model, Brand, Group, CustomUser
from .permissions import IsEnabled
from .serializers import RegisterSerializer, ModelSerializer, MarqueSerializer, GroupeSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.http import HttpResponseForbidden

def is_superuser(user):
    return user.is_superuser


class APIDocumentationView(TemplateView):
    template_name = "../templates/documentation.html"
@login_required
@user_passes_test(is_superuser, login_url='/login/')
def manage_users(request):
    users = CustomUser.objects.filter(enabled=0)
    return render(request, '../templates/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_superuser, login_url='/login/')
def accept_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.enabled = 1
    user.save()
    return redirect('manage_users')
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

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

###############Model###############

class ModelCreateView(generics.CreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated, IsEnabled]

class ModelUpdateView(generics.UpdateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated, IsEnabled]

class ModelListView(generics.ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated, IsEnabled]

class ModelDeleteView(generics.DestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated, IsEnabled]

###############Marque###############
class MarqueCreateView(generics.CreateAPIView):
        queryset = Brand.objects.all()
        serializer_class = MarqueSerializer
        permission_classes = [IsAuthenticated, IsEnabled]

class MarqueUpdateView(generics.UpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = MarqueSerializer
    permission_classes = [IsAuthenticated, IsEnabled]

class MarqueListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = MarqueSerializer
    permission_classes = [IsAuthenticated, IsEnabled]

class MarqueDeleteView(generics.DestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = MarqueSerializer
    permission_classes = [IsAuthenticated, IsEnabled]

###############Groupe###############
class GroupeCreateView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticated, IsEnabled]

class GroupeUpdateView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticated, IsEnabled]


class GroupeListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticated, IsEnabled]

class GroupeDeleteView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticated, IsEnabled]