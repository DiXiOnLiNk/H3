from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

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

# Шляхи
urlpatterns = [
    path('', redirect_to_docs),  # головна → swagger
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),  # підключення URL з додатку blog
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
