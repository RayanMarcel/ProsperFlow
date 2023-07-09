import decimal
from django.db import models
from UserProfile.choices import ChoicesBancos, ChoicesTipoConta
from datetime import datetime
from django.db.models import Sum
from decimal import Decimal

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    token = models.CharField(max_length=50)

    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extract.models import Valores
        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month=datetime.now().month).aggregate(Sum('valor'))
        total_gasto = valores['valor__sum'] if valores['valor__sum'] else 0
        return round(total_gasto, 2)

    def calcula_percentual_gasto_por_categoria(self):
        
        try:
            percentual = (self.total_gasto() * 100) / self.valor_planejamento
            return round(percentual, 0)
        except:
            return 0

class Conta(models.Model):
    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=3, choices=ChoicesBancos.bancos)
    tipo = models.CharField(max_length=2, choices=ChoicesTipoConta.tipo)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    icone = models.ImageField(upload_to='icones')
    token = models.CharField(max_length=50)

    def __str__(self):
        return self.apelido
    
