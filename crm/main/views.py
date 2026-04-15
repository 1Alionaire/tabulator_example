import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import SpreadsheetSheet, Item


def spreadsheet_view(request):
    """Страница со spreadsheet"""
    return render(request, 'main/index.html')


def sheets_api(request):
    """API: Получить все листы"""
    try:
        items = Item.objects.all()
        sheets = SpreadsheetSheet.objects.all()
        data = [
            {
                'key': sheet.key,
                'title': sheet.title,
                'data': sheet.data or [],
                'rows': sheet.rows,
                'columns': sheet.columns,
            }
            for sheet in sheets
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def save_sheet_api(request):
    """API: Сохранить один лист"""
    try:
        body = json.loads(request.body)
        key = body.get('key')
        data = body.get('data', [])
        
        if not key:
            return JsonResponse({'error': 'key is required'}, status=400)
        
        sheet, created = SpreadsheetSheet.objects.update_or_create(
            key=key,
            defaults={'data': data}
        )
        
        return JsonResponse({
            'status': 'ok', 
            'created': created,
            'key': key
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def save_all_sheets_api(request):
    """API: Сохранить все листы сразу"""
    try:
        sheets_data = json.loads(request.body)
        
        if not isinstance(sheets_data, list):
            return JsonResponse({'error': 'Expected array of sheets'}, status=400)
        
        saved_count = 0
        for sheet_data in sheets_data:
            key = sheet_data.get('key')
            if not key:
                continue
                
            SpreadsheetSheet.objects.update_or_create(
                key=key,
                defaults={
                    'title': sheet_data.get('title', key),
                    'data': sheet_data.get('data', []),
                    'rows': sheet_data.get('rows', 20),
                    'columns': sheet_data.get('columns', 10),
                }
            )
            saved_count += 1
        
        return JsonResponse({
            'status': 'ok', 
            'saved': saved_count
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_sheet_api(request, key):
    """API: Удалить лист"""
    try:
        deleted, _ = SpreadsheetSheet.objects.filter(key=key).delete()
        return JsonResponse({
            'status': 'ok',
            'deleted': deleted > 0
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
