from django.db import models

# Create your models here.ç

class SpreadsheetSheet(models.Model):
    """Модель для хранения листов spreadsheet"""
    key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    data = models.JSONField(default=list)  # Двумерный массив данных
    rows = models.IntegerField(default=20)
    columns = models.IntegerField(default=10)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title
    
class Item(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    price = models.FloatField()
    

