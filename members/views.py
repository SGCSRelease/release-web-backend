import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Member, Role
from utils.auth import encrypt_password, get_member, get_token
from utils.image_loader import load_image, save_image
from utils.decorators import need_login

@csrf_exempt
def login(request: HttpRequest) -> JsonResponse:

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
def get_profile(request: HttpRequest, member: Member, data: dict) -> JsonResponse:

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
def edit_profile(request: HttpRequest, member: Member, data: dict) -> JsonResponse:
    
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
def edit_password(request: HttpRequest, member: Member, data: dict) -> JsonResponse:
    
    if get_member(member.id, data['oldPassword']) == None:
        return JsonResponse({'success': False, 'error': '잘못된 비밀번호입니다.'})
    
    member.password = encrypt_password(data['newPassword'])
    member.save()

    response = JsonResponse({'success': True})
    response.set_cookie('token', get_token(member))
    return response


@csrf_exempt
@need_login
def logout(request: HttpRequest, member: Member, data: dict) -> JsonResponse:

    response = JsonResponse({'success': True})
    response.delete_cookie('token')
    return response
    
@need_login
def list_member(request: HttpRequest, member: Member, data: dict) -> JsonResponse:

    get_info = lambda member: {
        'name': member.name, 
        'image': load_image(f'member/{member.id}.jpg'),
        'message': member.message,
    }
    
    president = list(Member.objects.filter(role=Role.PRESIDENT).order_by('-name'))
    staff = list(Member.objects.filter(role=Role.STAFF).order_by('-name'))
    members = list(Member.objects.filter(role=Role.MEMBER).order_by('-name'))

    return JsonResponse({'members': [get_info(m) for m in president + staff + members]})
    