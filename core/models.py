# core/models.py

from django.db import models

class Sector(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class User(models.Model):
    user_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=10, default="Male")  # Added default

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user} - {self.company}"
