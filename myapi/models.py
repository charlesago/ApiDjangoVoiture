# myapi/models.py

from django.db import models


class Groupe(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
class Marque(models.Model):
    nom = models.CharField(max_length=100)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='marques')

    def __str__(self):
        return f"{self.nom} (Groupe: {self.groupe.nom})"
class Model(models.Model):
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name='models')
    nom = models.CharField(max_length=100)
    annee = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marque.nom} {self.nom} ({self.annee})"

