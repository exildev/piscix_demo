# encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from cuser.middleware import CuserMiddleware
from django.db.models import Sum, F, DecimalField
from inventario.widgets import MoneyInput


class Proveedor(models.Model):
    nombre = models.CharField(max_length=45)
    logo = models.ImageField(upload_to='logo', null=True, blank=True)
    fecha = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.nombre

    # end def

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Provedores"

    # end class

    def thumbnail(self):
        if self.logo:
            imagen = self.logo
        else:
            imagen = 'No-foto.png'
        # end if
        return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

    # end def
    thumbnail.allow_tags = True


# end class

class Fabricante(models.Model):
    nombre = models.CharField(max_length=45)
    logo = models.ImageField(upload_to='logo', null=True, blank=True)
    fecha = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.nombre

    # end def
    def thumbnail(self):
        if self.logo:
            imagen = self.logo
        else:
            imagen = 'No-foto.png'
        # end if
        return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

    # end def

    thumbnail.allow_tags = True


# end class

class Articulo(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(max_length=500)  # NO
    fabricante = models.ForeignKey(Fabricante)
    fecha_creacion = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(
        upload_to='articulos', null=True, blank=True)  # NO
    #tiempo_entrega = models.IntegerField('Tiempo de entrega(Dias)')
    activado = models.BooleanField(default=True)  # NO True
    precio = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        verbose_name = "Articulo Piscina"
        verbose_name_plural = "Articulos Piscinas"
    # end class

    def __unicode__(self):
        return self.nombre

    # end def

    def precio_(self):
        vals = str(self.precio).split('.')
        money = MoneyInput()
        value = money.intToStringWithCommas(
            int(vals[0])).replace(',', '.') + ',' + vals[1]
        return "$" + value

    # end def

    def thumbnail(self):
        if self.imagen:
            imagen = self.imagen
        else:
            imagen = 'No-foto.png'
        # end if
        return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

    # end def

    thumbnail.allow_tags = True


# end Class


class Bodega(models.Model):
    identi = models.CharField('Identificación', max_length=45)
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)

    @staticmethod
    def bodega_actual():
        user = CuserMiddleware.get_user()
        cuenta = Cuenta.objects.filter(pk=user.pk).first()
        if cuenta:
            return cuenta.bodega
        # end if
        return None

    # end def

    def precio_piscinas(self):
        activos = Activo.objects.filter(bodega=self).aggregate(
            total=Sum('articulo__precio'))
        if activos['total']:
            total = activos['total']
            vals = str(total).split('.')
            money = MoneyInput()
            value = money.intToStringWithCommas(
                int(vals[0])).replace(',', '.') + ',' + vals[1]
            return u"$ %s" % value
        # end if
        else:
            return u"$ %s" % 0
        # end if

    # end def

    def precio_insumos(self):
        agg = Sum(F('articulo__precio') * F('cantidad'))
        agg.output_field = DecimalField(max_digits=19, decimal_places=2)
        nserial = ActivoInsumo.objects.filter(bodega=self).aggregate(total=agg)
        if nserial['total']:
            total = nserial['total']
            vals = str(total).split('.')
            money = MoneyInput()
            value = money.intToStringWithCommas(
                int(vals[0])).replace(',', '.') + ',' + vals[1]
            return u"$ %s" % value
        else:
            return u"$ %d" % 0
        # end if

    # end def

    def precio_total(self):
        activos = Activo.objects.filter(bodega=self).aggregate(
            total=Sum('articulo__precio'))
        agg = Sum(F('articulo__precio') * F('cantidad'))

        agg.output_field = DecimalField(max_digits=19, decimal_places=2)
        nserial = ActivoInsumo.objects.filter(bodega=self).aggregate(total=agg)

        if activos['total']:
            total = activos['total']
        else:
            total = 0
        # end if
        if nserial['total']:
            total = total + nserial['total']
        # end if
        if total == 0:
            return total
        else:
            vals = str(total).split('.')
            money = MoneyInput()
            value = money.intToStringWithCommas(
                int(vals[0])).replace(',', '.') + ',' + vals[1]
            return value
        # end if

    # end def

    def capital_en_bodega(self):
        return u"$ %s" % (self.precio_total(),)

    # end def

    def __unicode__(self):
        return self.nombre

    # end def


# end calss


class Cuenta(User):
    bodega = models.ForeignKey(Bodega)

    class Meta:
        verbose_name = 'Cuenta de bodega'
        verbose_name_plural = "Cuentas de bodegas"
    # end class
# end class


class Central(models.Model):
    bodega = models.ForeignKey(Bodega)

    class Meta:
        verbose_name = 'Central'
        verbose_name_plural = "Centrales"

    # end class

    def __unicode__(self):
        return u"Central %s" % (self.bodega.nombre,)

    # end def


# end class


class ArticuloInsumo(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(max_length=500)  # NO
    fabricante = models.ForeignKey(Fabricante)
    activado = models.BooleanField(default=True)  # NO True
    imagen = models.ImageField(
        upload_to='articulos', null=True, blank=True)  # NO
    precio = models.DecimalField(max_digits=19, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Articulo Insumo"
        verbose_name_plural = "Aticulos de Insumos"

    # end class

    def __unicode__(self):
        return self.nombre

    # end def

    def thumbnail(self):
        if self.imagen:
            imagen = self.imagen
        else:
            imagen = 'No-foto.png'
        # end if
        return '<img src="/media/%s" width=50px heigth=50px/>' % (imagen)

    # end def

    thumbnail.allow_tags = True


# end class

class ActivoInsumo(models.Model):
    articulo = models.ForeignKey(ArticuloInsumo)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    serial = models.CharField(max_length=60)
    activado = models.BooleanField(default=True)
    vendido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"

    # end class

    def __unicode__(self):
        return self.articulo.nombre

    # end def

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        cuenta = Cuenta.objects.filter(pk=user.pk).first()
        if cuenta:
            self.bodega = cuenta.bodega
            super(ActivoInsumo, self).save(*args, **kwargs)
        # end if
    # end def

# end class


class LogInsumo(models.Model):
    activo = models.ForeignKey(ActivoInsumo)
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad = models.IntegerField()
    bodega = models.ForeignKey(Bodega)

    class Meta:
        verbose_name = 'Log de Insumo'
        verbose_name_plural = 'Logs de insumos'
    # end class


# end class

class LogPiscina(models.Model):
    articulo = models.ForeignKey(Articulo)
    fecha = models.DateTimeField(auto_now=True)
    cantidad = models.IntegerField()
    bodega = models.ForeignKey(Bodega, null=True)

    class Meta:
        verbose_name = 'Log piscina'
        verbose_name_plural = "Logs de piscinas"
    # end class


# end class


class TipoActivo(models.Model):
    nombre = models.CharField(max_length=200)
    #marker = models.ImageField(upload_to='marker', verbose_name="Marcador", blank=True, null=True)
    #marker_2 = models.ImageField(upload_to='marker2', verbose_name="Marcador seleccionado", blank=True, null=True)

    class Meta:
        verbose_name = 'Tipo de piscina'
        verbose_name_plural = "Tipos de piscinas"
    # end class

    def __unicode__(self):
        return "%s" % (self.nombre,)
    # end def
# end class


class Activo(models.Model):
    articulo = models.ForeignKey(Articulo)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    serial = models.CharField(max_length=60)
    activado = models.BooleanField(default=True)
    vendido = models.BooleanField(default=False)
    medidas = models.TextField(max_length=400)
    tipo = models.ForeignKey(TipoActivo)

    def __unicode__(self):
        if self.bodega:
            bodega = self.bodega.nombre
        else:
            bodega = "Fuera de Bodega"
        # end if
        return u'%s - %s' % (unicode(self.articulo), bodega)
    # end def

    class Meta:
        verbose_name = "Piscina"
        verbose_name_plural = "Piscinas"
    # end class

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        cuenta = Cuenta.objects.filter(pk=user.pk).first()
        if cuenta:
            self.bodega = cuenta.bodega
            super(Activo, self).save(*args, **kwargs)
        # end if
    # end def
# end class


class Custodio(models.Model):
    identi = models.CharField('Identificación', max_length=45)
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    correo = models.CharField(max_length=45)

    def __unicode__(self):
        return self.nombre
    # end def
# end class


class ActaRequisicion(models.Model):
    central = models.ForeignKey(Central)
    bodega = models.ForeignKey(Bodega)
    fecha = models.DateTimeField(auto_now=True)
    descripcion = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'Acta de requisición'
        verbose_name_plural = "Actas de requisición"
    # end class
# end class


class RequisicionArticulo(models.Model):
    acta = models.ForeignKey(ActaRequisicion)
    articulo = models.ForeignKey(Articulo)
    cantidad = models.IntegerField()

    class Meta:
        verbose_name = 'Requisición de piscina'
        verbose_name_plural = 'Requesiciones de piscina'
    # end class
# end class


class RequisicionInsumo(models.Model):
    acta = models.ForeignKey(ActaRequisicion)
    activo = models.ForeignKey(ArticuloInsumo, verbose_name="Articulo")
    cantidad = models.IntegerField()

    class Meta:
        verbose_name = 'Requisición de insumo'
        verbose_name_plural = "Requisiciones de insumos"
    # end class
# end class


class ActaSalida(models.Model):
    activos = models.ManyToManyField(Activo, blank=True)
    fecha = models.DateTimeField(auto_now=True)
    custodio = models.ForeignKey(Custodio)
    salida = models.ForeignKey(Bodega, related_name='salida')
    destino = models.ForeignKey(Bodega, null=True, related_name='destino')
    archivo = models.FileField(
        'Acta', upload_to='actas_salida', null=True, blank=True)
    descripcion = models.TextField(max_length=500)
    creado_por = models.ForeignKey(Cuenta)

    class Meta:
        verbose_name = 'Acta de salida'
        verbose_name_plural = 'Actas de salidas'
    # end class

    def __unicode__(self):
        return 'Acta Salida: %s' % str(self.fecha)
    # end def

    def archivo_(self):
        if self.archivo:
            return "<a href='/media/%s'>Descargar</a>" % (self.archivo,)
        # end if
        return "Sin archivo"
    # end def

    archivo_.allow_tags = True

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        cuenta = Cuenta.objects.filter(pk=user.pk).first()
        if cuenta:
            self.creado_por = cuenta
            self.salida = cuenta.bodega
            super(ActaSalida, self).save(*args, **kwargs)
            self.activos.update(bodega=None)
        # end if
    # end def
# end class


@receiver(m2m_changed, sender=ActaSalida.activos.through)
def actaSalida_slot(sender, instance, action, **kwargs):
    """
    Automaticamente guarda cuando el activo es agregado al acta de salida
    """
    if action == 'post_add':
        instance.save()
        articulos = Articulo.objects.filter(
            activo__actasalida=instance).distinct('id')
        for a in articulos:
            cant = Activo.objects.filter(
                bodega=instance.salida, articulo=a).count()
            LogPiscina(articulo=a, cantidad=cant,
                       bodega=instance.salida).save()
        # end for
        for activo in instance.activos.all():
            TrazabilidadActivo(
                activo=activo, mensage='salida de bodega').save()
        # end for
    # end if
# end def


class SalidaInsumo(models.Model):
    activos = models.ManyToManyField(ActivoInsumo)
    fecha = models.DateTimeField(auto_now=True)
    custodio = models.ForeignKey(Custodio)
    salida = models.ForeignKey(Bodega, related_name="origen2")
    destino = models.ForeignKey(Bodega, null=True, related_name="destino2")
    archivo = models.FileField(
        'Acta', upload_to='actas_salida', null=True, blank=True)
    descripcion = models.TextField(max_length=500)
    creado_por = models.ForeignKey(Cuenta)

    class Meta:
        verbose_name = 'Salida de Insumo'
        verbose_name_plural = 'Salidas de Insumos'
    # end class

    def archivo_(self):
        if self.archivo:
            return "<a href='/media/%s'>Descargar</a>" % (self.archivo,)
        # end if
        return "Sin archivo"
    # end def

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        cuenta = Cuenta.objects.filter(pk=user.pk).first()
        if cuenta:
            self.creado_por = cuenta
            self.salida = cuenta.bodega
            super(SalidaInsumo, self).save(*args, **kwargs)
            self.activos.update(bodega=None)
        # end if
    # end def
# end class


@receiver(m2m_changed, sender=SalidaInsumo.activos.through)
def salidaInsumo_slot(sender, instance, action, **kwargs):
    """
    Automaticamente guarda cuando el activo es agregado al acta de salida
    """
    if action == 'post_add':
        instance.save()
        articulos = ArticuloInsumo.objects.filter(
            activo__salidainsumo=instance).distinct('id')
        for a in articulos:
            cant = ActivoInsumo.objects.filter(
                bodega=instance.salida, articulo=a).count()
            LogInsumo(articulo=a, cantidad=cant, bodega=instance.salida).save()
        # end for
        for activo in instance.activos.all():
            TrazabilidadInsumo(
                activo=activo, mensage='salida de bodega').save()
        # end for
    # end if
# end def


class ActaEntrada(models.Model):
    activos = models.ManyToManyField(Activo, blank=True)
    custodio = models.ForeignKey(Custodio)
    fecha = models.DateTimeField(auto_now_add=True)
    origen = models.ForeignKey(
        Bodega, null=True, blank=True, related_name='origen_')
    destino = models.ForeignKey(Bodega, related_name='destino_')
    imagen = models.ImageField(
        upload_to='actas_entrada', null=True, blank=True)
    descripcion = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'Acta de entrada'
        verbose_name_plural = 'Actas de entradas'
    # end class

    def thumbnail(self):
        if self.imagen:
            imagen = self.imagen
        else:
            imagen = 'No-foto.png'
        # end if
        return '<img src="/media/%s" width=50px heigth=50px/>' % imagen
    # end def

    thumbnail.allow_tags = True

    def __unicode__(self):
        return 'Acta Entrada: %s' % str(self.fecha)
    # end def

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        cuenta = Cuenta.objects.filter(pk=user.pk).first()
        if cuenta:
            self.destino = cuenta.bodega
            acta = super(ActaEntrada, self).save(*args, **kwargs)
            self.activos.update(bodega=self.destino)
            return acta
        # end if
    # end def
# end class


@receiver(m2m_changed, sender=ActaEntrada.activos.through)
def actaEntrada_slot(sender, instance, action, **kwargs):
    """
    Automaticamente guarda cuando el activo es agregado al acta de salida
    """
    if action == 'post_add':
        instance.save()
        articulos = Articulo.objects.filter(
            activo__actaentrada=instance).distinct('id')
        compra = Compra.objects.filter(pk=instance.pk).first()
        for a in articulos:
            cant = Activo.objects.filter(articulo=a).count()
            LogPiscina(articulo=a, cantidad=cant,
                       bodega=instance.destino).save()
        # end for
        for activo in instance.activos.all():
            TrazabilidadActivo(
                activo=activo, bodega=instance.destino, mensage='entrada de bodega').save()
        # end for
    # end if
# end def


class EntradaInsumo(models.Model):
    activos = models.ManyToManyField(ActivoInsumo)
    custodio = models.ForeignKey(Custodio)
    fecha = models.DateTimeField(auto_now_add=True)
    origen = models.ForeignKey(
        Bodega, null=True, blank=True, related_name='origen1')
    destino = models.ForeignKey(Bodega, related_name='destino1')
    imagen = models.ImageField(
        upload_to='actas_entrada', null=True, blank=True)
    descripcion = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'Entrada de Insumo'
        verbose_name_plural = 'Entradas de Insimos'
    # end class

    def thumbnail(self):
        if self.imagen:
            imagen = self.imagen
        else:
            imagen = 'No-foto.png'
        # end if
        return '<img src="/media/%s" width=50px heigth=50px/>' % imagen
    # end def

    thumbnail.allow_tags = True

    def __unicode__(self):
        return 'Acta Entrada: %s' % str(self.fecha)
    # end def

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        cuenta = Cuenta.objects.filter(pk=user.pk).first()
        if cuenta:
            self.destino = cuenta.bodega
            acta = super(EntradaInsumo, self).save(*args, **kwargs)
            self.activos.update(bodega=self.destino)
            return acta
        # end if
    # end def
# end class


@receiver(m2m_changed, sender=EntradaInsumo.activos.through)
def entradaInsumo_slot(sender, instance, action, **kwargs):
    """
    Automaticamente guarda cuando el activo es agregado al acta de salida
    """
    if action == 'post_add':
        instance.save()
        articulos = ArticuloInsumo.objects.filter(
            activo__entradainsumo=instance).distinct('id')
        compra = Compra.objects.filter(pk=instance.pk).first()
        for a in articulos:
            cant = ActivoInsumo.objects.filter(articulo=a).count()
            LogInsumo(articulo=a, cantidad=cant,
                      bodega=instance.destino).save()
        # end for
        for activo in instance.activos.all():
            TrazabilidadInsumo(
                activo=activo, bodega=instance.destino, mensage='entrada de bodega').save()
        # end for
    # end if
# end def


class Compra(ActaEntrada):
    creado_por = models.ForeignKey(Cuenta)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        cuenta = Cuenta.objects.filter(pk=user.pk).filterst()
        if cuenta:
            self.creado_por = cuenta
            super(Compra, self).save(*args, **kwargs)
        # end if
    # ens def
# end class


class TrazabilidadActivo(models.Model):
    activo = models.ForeignKey(Activo)
    fecha = models.DateTimeField(auto_now_add=True)
    bodega = models.ForeignKey(Bodega, null=True)
    mensage = models.CharField("Mensaje", max_length=150)
# end class


class TrazabilidadInsumo(models.Model):
    activo = models.ForeignKey(ActivoInsumo)
    fecha = models.DateTimeField(auto_now_add=True)
    bodega = models.ForeignKey(Bodega, null=True)
    mensage = models.CharField("Mensaje", max_length=150)
# end class
