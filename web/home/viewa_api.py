import json
from django.http import JsonResponse

def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['user_location'] = {
            'lat': data['location']['lat'],
            'lng': data['location']['lng']
        }
        return JsonResponse({'message': 'Lokalizacja zapisana pomyślnie!'})
    return JsonResponse({'error': 'Nieprawidłowe żądanie.'}, status=400)
