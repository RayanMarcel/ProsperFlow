from django.db import models
from UserProfile.choices import ChoicesBancos, ChoicesTipoConta

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)
    token = models.CharField(max_length=50)

    def __str__(self):
        return self.categoria

class Conta(models.Model):
    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=3, choices=ChoicesBancos.bancos)
    tipo = models.CharField(max_length=2, choices=ChoicesTipoConta.tipo)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    icone = models.ImageField(upload_to='icones')
    token = models.CharField(max_length=50)

    def __str__(self):
        return self.apelido
    
