import json, jwt
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .auth import get_member, get_token

@csrf_exempt
def login(request: HttpRequest):
    data = json.loads(request.body)
    id = data['id']
    password = data['password']

    member = get_member(id, password)
    if member == None:
        return JsonResponse({'success': False})
    
    response = JsonResponse({'success': True})
    response.set_cookie('token', get_token(member))
    return response