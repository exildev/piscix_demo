from django.conf.urls import url
import views

urlpatterns = [
    url(r'add/reporte/',views.ReporteSupra.as_view(), name="add_reporte"),
    url(r'add/reparacion/',views.ReparacionSupra.as_view(), name="add_reparacion"),
    url(r'add/mantenimiento/',views.MantenimientoSupra.as_view(), name="add_mantenimiento"),
    url(r'list/reporte/',views.ReporteList.as_view(), name="list_reporte"),
    url(r'info/cliente/(?P<id>\d+)/',views.cliente_info, name="cliente_info"),
  #url(r'$', views.index, name="index"),
]
