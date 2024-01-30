import bcrypt, jwt
from typing import Optional
from .models import Member
from release_web_backend import settings

def get_member(id: int, password: str) -> Optional[Member]:
    members = Member.objects.filter(id=id)
    if members.count() == 0:
        return None
    
    member = members[0]
    if bcrypt.checkpw(password.encode('utf-8'), member.password):
        return member
    else:
        return None

def get_token(member: Member) -> str:
    token = {'id': member.id, 'password': member.password}
    return jwt.encode(token, settings.get_secret('JWT_KEY'))