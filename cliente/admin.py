from django.contrib import admin
from cliente import models as cli
from cliente.forms import ( ClienteForm, PiscineroForm, ReporteForm,
                           ReparacionForm, MantenimientoForm)
from import_export.admin import ExportMixin
from import_export import resources

# Register your models here.


class ClienteResource(resources.ModelResource):

    class Meta:
        model = cli.Cliente
        fields = (
            'nombre', 'apellidos', 'piscina', 'email,', 'direccion', 'telefono', 'fecha'
        )
        export_oder = fields
    # end class
# end class


class ClienteAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('_nombre', 'apellidos', 'piscina',
                    'email', 'direccion', 'telefono', 'fecha')
    search_fields = ('nombre', 'apellidos', 'direccion', 'email')
    list_filter = ('piscina', 'fecha')
    form = ClienteForm
    fields = ('nombre','apellidos','fecha','direccion','telefono','email','piscina')
    resource_class = ClienteResource

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('piscina',)
        return self.readonly_fields
    # end def

    class Media:
        js = ('cliente/js/cliente.js',)
        css = {
            'all':('cliente/css/style.css',)
        }
    #end class
# end class


class PiscineroResource(resources.ModelResource):

    class Meta:
        model = cli.Piscinero
        fields = (
            'username', 'first_name', 'last_name', 'email', 'identificacion', 'direccion', 'telefono', 'fecha', 'padre', 'madre', 'estado_civil', 'date_joined', 'last_login')
        export_order = (
            'username', 'first_name', 'last_name', 'email', 'identificacion', 'direccion', 'telefono', 'fecha', 'padre', 'madre', 'estado_civil', 'date_joined', 'last_login')
    # end class
# end class

class PiscineroAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'identificacion', 'direccion',
                    'telefono', 'fecha', 'padre', 'madre', 'estado_civil', 'date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name',
                     'email', 'identificacion', 'telefono')
    form = PiscineroForm
    fields = (
        'first_name', 'last_name','fecha','username',  'email', 'identificacion', 'direccion',
        'telefono', 'padre', 'madre', 'estado_civil','password1','password2'
    )
    resource_class = PiscineroResource
# end class


class ImagenRStacked(admin.StackedInline):
    model = cli.ImagenR
# end class


class ReporteResource(resources.ModelResource):

    class Meta:
        model = cli.Reporte
        fields = (
            'nombre', 'descripcion', 'tipo__nombre', 'cliente__nombre', 'cliente__apellidos',
            'reporta__first_name', 'reporta__last_name', 'fecha'
        )
        export_order = fields
    # end class
# end class


class ReporteAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'tipo',
                    'cliente', 'reporta', 'fecha')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('tipo', 'cliente', 'reporta', 'fecha')
    inlines = (ImagenRStacked,)
    resource_class = ReporteResource
    form = ReporteForm
# end class


class ImagenMStacked(admin.StackedInline):
    model = cli.ImagenM
# end class


class MantenimientoResource(resources.ModelResource):

    class Meta:
        model = cli.Mantenimiento
        fields = (
            'nombre', 'cliente__nombre', 'cliente__apellidos', 'piscinero__first_name',
            'piscinero__last_name', 'descripcion', 'fecha'
        )
        export_order = fields
    # end class
# end class


class MantenimientoAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'piscinero', 'descripcion', 'fecha')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('cliente', 'piscinero', 'fecha')
    inlines = (ImagenMStacked,)
    resource_class = MantenimientoResource
    form = MantenimientoForm
# end class


class ImagenREStacked(admin.StackedInline):
    model = cli.ImagenRE
# end class


class ReparacionResource(resources.ModelResource):

    class Meta:
        model = cli.Reparacion
        fields = (
            'nombre', 'cliente__nombre', 'cliente__apellidos', 'piscinero__first_name',
            'piscinero__last_name', 'descripcion', 'fecha'
        )
        export_order = fields
    # end class
# end class


class ReparacionAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'piscinero', 'descripcion', 'fecha')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('cliente', 'piscinero', 'fecha')
    inlines = (ImagenREStacked,)
    resource_class = ReparacionResource
    form = ReparacionForm
# end class

admin.site.register(cli.Cliente, ClienteAdmin)
admin.site.register(cli.Piscinero, PiscineroAdmin)
admin.site.register(cli.TipoReporte)
admin.site.register(cli.Reporte, ReporteAdmin)
admin.site.register(cli.Mantenimiento, MantenimientoAdmin)
admin.site.register(cli.Reparacion, ReparacionAdmin)
