from django.contrib import admin
from .models import SpreadsheetSheet, Item
# Register your models here.


@admin.register(SpreadsheetSheet)
class SpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('key', 'title',  'rows', 'columns', 'order' )

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'amount', 'price')


    # key = models.CharField(max_length=100, unique=True)
    # title = models.CharField(max_length=200)
    # data = models.JSONField(default=list)  # Хранит двумерный массив
    # rows = models.IntegerField(default=20)
    # columns = models.IntegerField(default=10)
    # order = models.IntegerField(default=0)