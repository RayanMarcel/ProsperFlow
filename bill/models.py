from django.db import models
from UserProfile.models import Categoria

class ContaPagar(models.Model):
    titulo = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    dia_pagamento = models.IntegerField()
    token = models.CharField(max_length=50)
    
    def __str__(self):
        return self.titulo

class ContaPaga(models.Model):
    conta = models.ForeignKey(ContaPagar, on_delete=models.DO_NOTHING)
    data_pagamento = models.DateField()
    token = models.CharField(max_length=50)