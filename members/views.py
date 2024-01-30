import json, jwt
from typing import Callable
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Member
from .auth import encrypt_password, get_member, get_member_from_token, get_token
from release_web_backend.image_loader import load_image, save_image

def need_login(func: Callable[[HttpRequest, Member, dict], HttpResponse]):
    
    def wrapper(request: HttpRequest) -> HttpResponse:
        data = json.loads(request.body)
        member = get_member_from_token(request.COOKIES['token'])
        if member == None:
            return HttpResponse(status=401)
        func(request, member, data)

    return wrapper

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


@need_login
def get_profile(request: HttpRequest, member: Member, data: dict):

    return JsonResponse({
        'name': member.name,
        'id': member.id,
        'phone': member.phone,
        'email': member.email,
        'state': member.state,
        'role': member.role,
        'message': member.message,
        'image': load_image(f'member/{member.id}.jpg'),
    })


@csrf_exempt
@need_login
def edit_profile(request: HttpRequest, member: Member, data: dict):
    
    if 'phone' in data:
        member.phone = data['phone']
    if 'email' in data:
        member.email = data['email']
    if 'message' in data:
        member.message = data['message']
    if 'image' in data:
        save_image(f'member/{member.id}.jpg', data['image'])
    
    member.save()
    return JsonResponse({'success': True})


@csrf_exempt
@need_login
def edit_password(request: HttpRequest, member: Member, data: dict):
    
    if get_member(member.id, data['oldPassword']) == None:
        return JsonResponse({'success': False, 'error': '잘못된 비밀번호입니다.'})
    
    member.password = encrypt_password(data['newPassword'])
    member.save()
    return JsonResponse({'success': True})


@csrf_exempt
@need_login
def logout(request: HttpRequest, member: Member, data: dict):

    response = JsonResponse({'success': True})
    response.delete_cookie('token')
    return response
    
    