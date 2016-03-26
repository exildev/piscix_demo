from django.shortcuts import  redirect, render, HttpResponse
# Create your views here.
from supra import views as supra
from forms import MantenimientoForm, ReporteForm, ReparacionForm, LoginForm
import models

def index(request):
    return redirect('/dashboard/')
#end def

class ImagenRInline(supra.SupraInlineFormView):
    base_model = models.Reporte
    inline_model = models.ImagenR
#end class

class ReporteSupra(supra.SupraFormView):
    model = models.Reporte
    form_class = ReporteForm
    inlines = [ImagenRInline]
    template_name = 'cliente/form.html'
#end class

class ImagenMInline(supra.SupraInlineFormView):
    base_model = models.Mantenimiento
    inline_model = models.ImagenM
#end class

class MantenimientoSupra(supra.SupraFormView):
    model = models.Mantenimiento
    form_class = MantenimientoForm
    inlines = [ImagenMInline]
    template_name = 'cliente/form.html'
#end class

class ImagenREInline(supra.SupraInlineFormView):
    base_model = models.Reparacion
    inline_model = models.ImagenRE
#end class

class ReparacionSupra(supra.SupraFormView):
    model = models.Reparacion
    form_class = ReparacionForm
    inlines = [ImagenREInline]
    template_name = 'cliente/form.html'
#end class

class ReporteList(supra.SupraListView):
    model = models.Reporte
    list_display =  [
        'nombre','tipo__nombre','reporta__first_name','reporta__last_name',
        'descripcion', 'fecha']
    search_fields = ['cliente__id','reporta__id','nombre']
#end class

def cliente_info(request, id):
    cliente = models.Cliente.objects.filter(id=id).first()
    if cliente:
        reparacion = models.Reparacion.objects.filter(cliente=cliente)
        reporte = models.Reporte.objects.filter(cliente=cliente)
        mantenimiento = models.Mantenimiento.objects.filter(cliente=cliente)
        return render(request, 'cliente/cliente.html',
                      {'cliente':cliente, 'reparacion':reparacion,
                       'reporte':reporte, 'mantenimiento':mantenimiento})
    #end if
    return render(request, 'cliente/cliente.html',
                  {'cliente':None, 'reparacion':None,
                   'reporte':None, 'mantenimiento':None})
#end def

def loginC(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(username=username, password=password)
            if usuario is not None and usuario.is_active:
                login(request, usuario)
                return HttpResponse(status=200)
			#end if
            return HttpResponse({"error":"el usuario no esta activo"},status=400, content_type='application/json')
		#end if
        errors = form.errors.items()
        return HttpResponse(simplejson.dumps(dict(errors)),status=400, content_type='application/json')
	#end if
    return HttpResponse(status=403)
#end def

def logoutC(request):
	logout(request)
	return 200
#end def
