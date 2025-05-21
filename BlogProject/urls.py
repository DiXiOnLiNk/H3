from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views  # Імпорт для login/logout

# Swagger імпорти
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger конфігурація
schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="API документація до блогу",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# View-функція для редіректу з головної сторінки
def redirect_to_docs(request):
    return redirect('/swagger/')

urlpatterns = [
    path('', redirect_to_docs),
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # ✅ Додано logout
]
