# existing imports
from django.urls import path
from django.conf.urls import url
from apiAnalisis import views

urlpatterns = [
    #Autenticación
    url(r'^$',views.Autenticacion.singIn),
    url(r'^postsign/',views.Autenticacion.postsign),

    #Clientes
    path('clientes/', views.ListCliente.as_view()),
    path('clientes/<int:pk>/', views.DetailCliente.as_view()),
    path('clientesFiltroDinamico/', views.ClientesAPIView.as_view()),
    path('clientesporcedula/', views.CedulaClientesAPIView.as_view()),
    path('clientesportipo/', views.TipoClientesAPIView.as_view()),
    path('predecir/',views.Clasificacion.predecirTipoCliente),
    path('enviarSolicitud/',views.Clasificacion.guardar),
    path('verDiagrama/',views.Clasificacion.enviarDiagrama),

    #Búsqueda de Clientes por DNI
    path('mostrarInterfazBuscar/', views.Clasificacion.mostrarInterfazBuscar),
    path('buscarCliente/', views.Clasificacion.buscarCliente),

    #Predicción
    url(r'^mostrarInterfazPredecir/',views.Clasificacion.mostrarInterfazPredecir),
    url(r'^predecirTipoCliente/',views.Clasificacion.predecirTipoCliente),
    
    
    #Interfaz con estilo
    url(r'^mostrarInterfazPredecirConEstilo/',views.Clasificacion.mostrarInterfazPredecirConEstilo),
    
    #Otros
    path('libros/', views.ListLibro.as_view()),
    path('libros/<int:pk>/', views.DetailLibro.as_view()),
    path('graficas/', views.ListGrafica.as_view()),
    path('graficas/<int:pk>/', views.DetailGrafica.as_view()),
]