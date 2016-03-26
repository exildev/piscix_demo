from django.http import HttpResponse
import json as simplejson

def check_login(funcion):
	def check(request,*args, **kwargs):
		if request.user.is_authenticated():
			return funcion(request,*args, **kwargs)
			#end if
		return HttpResponse(simplejson.dumps({'status':400, 'errors':['Debes iniciar sesion para continuar con la operacion']}), content_type= "application/json")
	#end def
	return check
#end def
