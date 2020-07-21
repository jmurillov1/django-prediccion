from django.db import models
from django.urls import reverse

class Autenticacion():
		
	def sign_in_with_email_and_password(email="remihuro@hotmail.com",passw=""):
		print('passw:'+passw)
		if passw=="12345678":
			return True
		else:
			return False

