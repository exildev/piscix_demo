# encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from inventario import models as inv
from django.contrib.auth.models import User
# Create your models here.


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.TextField(max_length=400)
    telefono = models.IntegerField()
    fecha = models.DateField("Fecha de nacimiento")
    piscina = models.ForeignKey(inv.Activo, verbose_name="Piscina adquirida")

    def __unicode__(self):
        return u"%s %s" % (self.nombre, self.apellidos)
    # end def

    def _nombre(self):
        return """<a href="#" id="%(id)d" class="cliente">%(nombre)s</a>""" % {'id': self.pk, 'nombre': self.nombre}
    #end def

    _nombre.allow_tags = True
# end class


class Piscinero(User):
    estado = (('Soltero', 'Soltero'),
              ('Casado', 'Casado'),
              ('Divorciado', 'Divorciado'),
              ('En una relación', 'En una relación'))
    identificacion = models.CharField(max_length=100)
    fecha = models.DateField("Fecha de nacimiento")
    direccion = models.TextField(max_length=400)
    telefono = models.IntegerField()
    padre = models.CharField(max_length=200)
    madre = models.CharField(max_length=200)
    estado_civil = models.CharField(max_length=100, choices=estado)

    class Meta:
        verbose_name = "Piscinero"
        verbose_name_plural = "Piscineros"
# end class


class TipoReporte(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Tipo de reporte"
        verbose_name_plural = "Tipos de reporte"
    # end class

    def __unicode__(self):
        return u"%s" % self.nombre
    # end def
# end class


class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoReporte, verbose_name="Tipo de novedad")
    cliente = models.ForeignKey(Cliente)
    reporta = models.ForeignKey(Piscinero)
    descripcion = models.TextField(max_length=400)
    fecha = models.DateTimeField(
        verbose_name="Fecha de reporte", auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.nombre
    # end def
# end class


class ImagenR(models.Model):
    imagen = models.ImageField(upload_to="repotes")
    reporte = models.ForeignKey(Reporte)

    class Meta:
        verbose_name = "Imagen de reporte"
        verbose_name_plural = "Imagenes de reporte"
    # end class
# end class


class Mantenimiento(models.Model):
    nombre = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente)
    piscinero = models.ForeignKey(Piscinero)
    fecha = models.DateTimeField(
        verbose_name="Fecha de reporte", auto_now_add=True)
    descripcion = models.TextField(max_length=400)

    def __unicode__(self):
        return u"%s" % self.nombre
    # end def
# end class


class ImagenM(models.Model):
    imagen = models.ImageField(upload_to="mantenimiento")
    mantenimiento = models.ForeignKey(Mantenimiento)

    class Meta:
        verbose_name = "Imagen de mantenimiento"
        verbose_name_plural = "Imagenes de mantenimientos"
    # end class
# end class


class Reparacion(models.Model):
    nombre = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente)
    piscinero = models.ForeignKey(Piscinero)
    fecha = models.DateTimeField(
        verbose_name="Fecha de reporte", auto_now_add=True)
    descripcion = models.TextField(max_length=400)

    class Meta:
        verbose_name = "Reparación"
        verbose_name_plural = "Reparaciones"
    # end class

    def __unicode__(self):
        return u"%s" % self.nombre
    # end def
# end class


class ImagenRE(models.Model):
    imagen = models.ImageField(upload_to="reparacion")
    reparacion = models.ForeignKey(Reparacion)

    class Meta:
        verbose_name = "Imagen de reparación"
        verbose_name_plural = "Imagenes de reparaciones"
    # end class
# end class
