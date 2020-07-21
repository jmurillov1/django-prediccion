from django.contrib import admin
from apiAnalisis.models import Libro
from apiAnalisis.models import Cliente
from apiAnalisis.models import Grafica
# Register your models here.
admin.site.register(Libro)
admin.site.register(Cliente)
admin.site.register(Grafica)