from django.urls import path
from . import views
from .views import registro
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('contacto/', views.contacto, name='contacto'),
    path('sobre-mi/', views.sobre_mi, name='sobre_mi'),
    path('terminos/', views.terminos, name='terminos'),
    path('precios/', views.precios, name='precios'),
    path('precios-simple/', views.precios_simple, name='precios_simple'),
    path('registro/', registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('opciones-categorias/', views.opciones_categorias, name='opciones_categorias'),
    path('opciones-estilos/', views.opciones_estilos, name='opciones_estilos'),
    path('opcionessolicitudes/', views.opcionessolicitudes, name='opcionessolicitudes'),
    path('agregar-categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('modificar-categoria/', views.modificar_categoria, name='modificar_categoria'),
    path('eliminar-categoria/', views.eliminar_categoria, name='eliminar_categoria'),
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('portafolio/', views.portafolio, name='portafolio'), 
    path('portafolio-simple/', views.portafolio_simple, name='portafolio_simple'),
    path('administrar-dibujos/', views.administrar_dibujos, name='administrar_dibujos'),
    path('formulario/', views.formulario, name='formulario'),
    path('eliminar-categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('get_categoria/<int:categoria_id>/', views.get_categoria, name='get_categoria'),
    path('eliminar-dibujo/<int:dibujo_id>/', views.eliminar_dibujo, name='eliminar_dibujo'),
    path('logout/', views.logout_view, name='logout'),
    path('miperfil/', views.mi_perfil, name='mi_perfil'),
    path('mis_solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('login/', views.login_view, name='login'),
    path('eliminar_solicitud/<int:solicitud_id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
    path('eliminar_solicitud1/<int:solicitud_id>/', views.eliminar_solicitud1, name='eliminar_solicitud1'),
    path('actualizar_solicitud/', views.actualizar_solicitud, name='actualizar_solicitud'), 
    path('obtener_correo_usuario/', views.obtener_correo_usuario, name='obtener_correo_usuario'),
    path('descargar_referencia/<int:solicitud_id>/', views.descargar_referencia, name='descargar_referencia'),

]
