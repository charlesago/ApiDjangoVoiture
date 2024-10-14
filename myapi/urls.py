from django.urls import path
from . import views
from .views import RegisterView, ProtectedView, ModelCreateView, MarqueCreateView

urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('hello/', views.HelloWorld.as_view(), name='hello-world'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create/model', ModelCreateView.as_view(), name='model-create'),
    path('create/marque', MarqueCreateView.as_view(), name='marque-create'),
    path('create/groupe', MarqueCreateView.as_view(), name='marque-create'),

]
