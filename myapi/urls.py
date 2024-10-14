from django.urls import path, include

from .views import RegisterView, ProtectedView, ModelListView, ModelCreateView, ModelUpdateView, ModelDeleteView, \
    MarqueListView, MarqueCreateView, MarqueUpdateView, MarqueDeleteView, GroupeListView, GroupeCreateView, \
    GroupeUpdateView, GroupeDeleteView, manage_users, accept_user, CustomLoginView, APIDocumentationView

urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('register', RegisterView.as_view(), name='register'),
    path('documentation', APIDocumentationView.as_view(), name='api-documentation'),


    path('login/', CustomLoginView.as_view(), name='login'),
    path('manage-users/', manage_users, name='manage_users'),
    path('accept-user/<int:user_id>', accept_user, name='accept_user'),

    path('models', ModelListView.as_view(), name='model-list'),
    path('create/model', ModelCreateView.as_view(), name='model-create'),
    path('update/model/<int:pk>', ModelUpdateView.as_view(), name='model-update'),
    path('delete/model/<int:pk>', ModelDeleteView.as_view(), name='model-delete'),

    path('marques', MarqueListView.as_view(), name='marque-list'),
    path('create/marque', MarqueCreateView.as_view(), name='marque-create'),
    path('update/marque/<int:pk>', MarqueUpdateView.as_view(), name='marque-update'),
    path('delete/marque/<int:pk>', MarqueDeleteView.as_view(), name='marque-delete'),

    path('groupes', GroupeListView.as_view(), name='groupe-list'),
    path('create/groupe', GroupeCreateView.as_view(), name='groupe-create'),
    path('update/groupe/<int:pk>', GroupeUpdateView.as_view(), name='groupe-update'),
    path('delete/groupe/<int:pk>', GroupeDeleteView.as_view(), name='groupe-delete'),

]
