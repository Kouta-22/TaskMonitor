from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import deletar_registro
from django.views.generic import RedirectView




urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),  
    path('logout/', views.logout_view, name='logout'),
    path('deletar/<int:registro_id>/', deletar_registro, name='deletar_registro'),
    path('atualizar_registro/<int:registro_id>/', views.atualizar_registro, name='atualizar_registro'),
    path('gerenciamento_registros/', views.gerenciamento_registros, name='gerenciamento_registros'),
    path('favicon.ico', views.ignore_favicon, name='ignore_favicon'),
    path('<str:tipo_sala>/', views.registrar_sala, name='registrar_sala'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
