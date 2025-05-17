import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import stream_manager

@csrf_exempt
def add_stream(request):
    # Handle preflight CORS request
    if request.method == 'OPTIONS':
        response = JsonResponse({'detail': 'OK'})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    url = data.get('url')
    if not url:
        return JsonResponse({'error': 'No URL provided'}, status=400)

    # Create a new stream entry
    stream_id = stream_manager.add_stream(url)
    response = JsonResponse({'id': stream_id}, status=201)
    response["Access-Control-Allow-Origin"] = "*"
    return response
