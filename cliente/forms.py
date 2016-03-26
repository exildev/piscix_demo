# encoding:utf-8
from django import forms
from cliente import models as cli
from inventario import models as inv
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import get_connection, EmailMultiAlternatives
from cuser.middleware import CuserMiddleware
from django.contrib.auth.models import User
from django_select2.forms import Select2Widget


class CalendarWidget(forms.DateInput):

  class Media:
    css = {
        'all': ('datepicker/css/datepicker.css',)
    }
    js = ('datepicker/js/bootstrap-datepicker.js', 'cliente/js/date.js')
  # end class
# end class


class ClienteForm(forms.ModelForm):

  class Meta:
    model = cli.Cliente
    exclude = ()
  # end class

  def __init__(self, *args, **kwargs):
    super(ClienteForm, self).__init__(*args, **kwargs)
    self.fields['fecha'].widget = CalendarWidget(
        attrs={'class': 'date'}, format="%d/%m/%Y")
    self.fields['fecha'].input_formats = ('%Y/%m/%d', '%d/%m/%Y')
    if self.instance.pk == None:
      user = CuserMiddleware.get_user()
      cuenta = inv.Cuenta.objects.filter(pk=user.pk).first()
      if cuenta:
        self.fields['piscina'].queryset = inv.Activo.objects.filter(
            vendido=False, bodega=cuenta.bodega)
      else:
        self.fields['piscina'].queryset = inv.Activo.objects.filter(
            vendido=False)
      # end if
  # end def

  def clean(self):
    if self.instance.pk == None:
      user = CuserMiddleware.get_user()
      cuenta = inv.Cuenta.objects.filter(pk=user.pk).first()
      if cuenta:
        self.instance.creado_por = cuenta
        return super(ClienteForm, self).clean()
      else:
        raise forms.ValidationError(
            "Necesita tener una cuenta de bodega para registrar un cliente")
      # end if
    # end if
  # end def

  def save(self, commit=True):
    cliente = super(ClienteForm, self).save(commit)
    piscina = inv.Activo.objects.filter(id=cliente.piscina.id).first()
    piscina.bodega = None
    piscina.vendido = True
    piscina.save()
    mensaje = u"Cliente: %s %s Ubicación:%s" % (
        cliente.nombre, cliente.apellidos, cliente.direccion)
    inv.TrazabilidadActivo(activo=piscina, mensage=mensaje).save()
    return cliente
  # end def
# end class


class PiscineroForm(UserCreationForm):

  def __init__(self, *args, **kwargs):
    super(PiscineroForm, self).__init__(*args, **kwargs)
    self.fields['fecha'].widget = CalendarWidget(
        attrs={'class': 'date'}, format="%d/%m/%Y")
    self.fields['fecha'].input_formats = ('%Y/%m/%d', '%d/%m/%Y')

  class Meta:
    model = cli.Piscinero
    exclude = (
        'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', 'password'
    )
  # end class
# end class


class ReporteForm(forms.ModelForm):

  class Meta:
    model = cli.Reporte
    exclude = ()
    widgets = {
        'cliente': Select2Widget,
        'reporta': Select2Widget,
        'tipo': Select2Widget
    }
  # end class

  def save(self, commit=True):
    reporte = super(ReporteForm, self).save(commit)
    admin = User.objects.values_list(
        'email', flat=True).filter(is_superuser=True)
    username = User.objects.filter(is_superuser=True).first()
    subject, from_email, to = reporte.nombre, 'mariobarrpach@gmail.com', admin
    text_content = u'Estimad(a) %s' % username.username
    html_content = u'Reporte realizado por: %s %s a el cliente: %s %s .<br>Información del reporte: %s' % (
        reporte.reporta.first_name, reporte.reporta.last_name, reporte.cliente.nombre,
        reporte.cliente.apellidos, reporte.descripcion)
    print to
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return reporte
  # end def
# end class


class MantenimientoForm(forms.ModelForm):

  class Meta:
    model = cli.Mantenimiento
    exclude = ()
    widgets = {
        'cliente': Select2Widget,
        'piscinero': Select2Widget,
    }
  # end class

  def save(self, commit=True):
    man = super(MantenimientoForm, self).save(commit)
    admin = User.objects.values_list(
        'email', flat=True).filter(is_superuser=True)
    username = User.objects.filter(is_superuser=True).first()
    subject, from_email, to = man.nombre, 'mariobarrpach@gmail.com', admin
    text_content = u'Estimad(a) %s' % username.username
    html_content = u'Mantenimiento realizado por: %s %s a el cliente: %s %s .<br>Información del mantenimiento: %s' % (
        man.piscinero.first_name, man.piscinero.last_name, man.cliente.nombre,
        man.cliente.apellidos, man.descripcion)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return man
  # end def
# end class


class ReparacionForm(forms.ModelForm):

  class Meta:
    model = cli.Reparacion
    exclude = ()
    widgets = {
        'cliente': Select2Widget,
        'piscinero': Select2Widget,
    }
  # end class

  def save(self, commit=True):
    man = super(ReparacionForm, self).save(commit)
    admin = User.objects.values_list(
        'email', flat=True).filter(is_superuser=True)
    username = User.objects.filter(is_superuser=True).first()
    subject, from_email, to = man.nombre, 'mariobarrpach@gmail.com', admin
    text_content = u'Estimad(a) %s' % username.username
    html_content = u'Reparación realizada por: %s %s a el cliente: %s %s .<br>Información de la reparación: %s' % (
        man.piscinero.first_name, man.piscinero.last_name, man.cliente.nombre,
        man.cliente.apellidos, man.descripcion)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return man
  # end def
# end class


class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput())
  password = forms.CharField(widget=forms.PasswordInput(render_value=False))
# end class


class UsuarioForm(forms.Form):
  username = forms.CharField(
      label="*Nombre de Usuario", widget=forms.TextInput())
  email = forms.EmailField(label="*Correo Electronico",
                           widget=forms.TextInput())
  password_one = forms.CharField(
      label="*Password", widget=forms.PasswordInput(render_value=False))
  password_two = forms.CharField(
      label="*Confirmar Password", widget=forms.PasswordInput(render_value=False))

  def clean_username(self):
    username = self.cleaned_data['username']
    try:
      u = User.objects.get(username=username)
    except User.DoesNotExist:
      return username
    raise forms.ValidationError('Este nombre de usuario ya existe')

  # end def

  def clean_email(self):
    email = self.cleaned_data['email']
    try:
      u = User.objects.get(email=email)
    except User.DoesNotExist:
      return email
    raise forms.ValidationError('Ya existe un usuario con este correo')

  # end def

  def clean_password_two(self):
    password_one = self.cleaned_data['password_one']
    password_two = self.cleaned_data['password_two']
    if password_one == password_two:
      pass
    else:
      raise forms.ValidationError('Las contraseñas no coinciden')
    # end if
  # end def

# end class


class RememberUserForm(forms.Form):
  mail = forms.EmailField(label="Email")

  def clean_mail(self):
    email = self.cleaned_data['mail']
    u = User.objects.filter(email=email)
    if not u:
      raise forms.ValidationError('No existe un usuario con ese email')
    return email
    # end if
  # end def
# end class


class NewPassForm(forms.Form):
  newPassword1 = forms.CharField(
      label="Nueva Contraseña", widget=forms.PasswordInput(render_value=False))
  newPassword2 = forms.CharField(label="Vuelve a escribir la contraseña nueva",
                                 widget=forms.PasswordInput(render_value=False))

  def clean_newPassword2(self):
    password1 = self.cleaned_data['newPassword1']
    password2 = self.cleaned_data['newPassword2']
    if password1 == password2:
      pass
    else:
      raise forms.ValidationError('Las contraseñas no coiciden')
    # end if
      # end def
# end class


class ChangePasswordForm(forms.Form):
  username = forms.CharField(label="Username")
  mail = forms.EmailField(label="Email")
  newPassword1 = forms.CharField(
      label="Nueva Contraseña", widget=forms.PasswordInput(render_value=False))
  newPassword2 = forms.CharField(label="Vuelve a escribir la contraseña nueva",
                                 widget=forms.PasswordInput(render_value=False))

  def clean_user(self):
    username = self.cleaned_data['username']
    u = User.objects.filter(username=username)
    if not u:
      raise forms.ValidationError('No existe un usuario con ese nombre')
    return username
    # end if
  # end def

  def clean_mail(self):
    mail = self.cleaned_data['mail']
    u = User.objects.filter(email=mail)
    if not u:
      raise forms.ValidationError('No existe un usuario con ese Email')
    return mail
    # end if
  # end def

  def clean_newPassword2(self):
    password1 = self.cleaned_data['newPassword1']
    password2 = self.cleaned_data['newPassword2']
    if password1 == password2:
      pass
    else:
      raise forms.ValidationError('Las contraseñas no coiciden')
    # end if
      # end def

# end class
