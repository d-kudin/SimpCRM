from django.db import models


class Record(models.Model):
	utworzono = models.DateTimeField(auto_now_add=True)
	imie = models.CharField(max_length=50)
	nazwisko =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	nr_telefonu = models.CharField(max_length=15)
	adres =  models.CharField(max_length=100)
	miasto =  models.CharField(max_length=50)
	wojewodztwo =  models.CharField(max_length=50)
	kod_pocztowy =  models.CharField(max_length=20)

	def __str__(self):
		return(f"{self.imie} {self.nazwisko}")