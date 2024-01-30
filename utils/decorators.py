import json
from typing import Callable
from django.http import HttpRequest, HttpResponse

from members.models import Member
from .auth import get_member_from_token

def need_login(func: Callable[[HttpRequest, Member, dict], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    
    def wrapper(request: HttpRequest) -> HttpResponse:
        data = json.loads(request.body) if request.body != b'' else {}
        member = get_member_from_token(request.COOKIES['token']) if 'token' in request.COOKIES else None
        if member == None:
            return HttpResponse(status=401)
        
        return func(request, member, data)

    return wrapper