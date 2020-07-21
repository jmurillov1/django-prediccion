from django.db import models

#Modelo Grafica
class Grafica(models.Model):
    #https://mc.ai/integrar-modelo-de-red-neuronal-convolucional-en-django/
    # file will be uploaded to MEDIA_ROOT / uploads 
    imagen = models.ImageField(upload_to ='uploads/') 
    # or... 
    # file will be saved to MEDIA_ROOT / uploads / 2015 / 01 / 30 
    # upload = models.ImageField(upload_to ='uploads/% Y/% m/% d/')
    titulo = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return str(self.titulo)

# Modelo Libro
class Libro(models.Model):
    titulo=models.CharField(max_length=30)
    descripcion=models.TextField()
    def __str__(self):
        return str(self.titulo) + ':' + str(self.descripcion)

# Modelo Cliente
class Cliente(models.Model):
    #codigo=models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=10) #DNI 
    edad = models.IntegerField() #Edad
    tipoCliente = models.CharField(max_length=1, blank=True)
    def __str__(self):
        return str(self.cedula) + ':' +  str(self.edad) + ':' + str(self.tipoCliente)

#Modelo MAESTRO DETALLE
"""
class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
"""