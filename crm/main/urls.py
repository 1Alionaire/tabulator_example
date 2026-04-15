from django.urls import path
from . import views

urlpatterns = [
    path('spreadsheet/', views.spreadsheet_view, name='spreadsheet'),
    path('api/sheets/', views.sheets_api, name='sheets_api'),
    path('api/sheets/save/', views.save_sheet_api, name='save_sheet'),
    path('api/sheets/save-all/', views.save_all_sheets_api, name='save_all_sheets'),
]
