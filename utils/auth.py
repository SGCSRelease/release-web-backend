import bcrypt, jwt
from typing import Optional
from ..members.models import Member
from release_web_backend import settings

JWT_KEY = settings.get_secret('JWT_KEY')

def get_member(id: int, password: str) -> Optional[Member]:
    members = Member.objects.filter(id=id)
    if members.count() == 0:
        return None
    
    member = members[0]
    if bcrypt.checkpw(password.encode('utf-8'), member.password):
        return member
    else:
        return None

def get_member_from_token(token: str) -> Optional[Member]:
    payload = jwt.decode(token, JWT_KEY)
    return get_member(payload['id'], payload['password'])

def get_token(member: Member) -> str:
    token = {'id': member.id, 'password': member.password}
    return jwt.encode(token, JWT_KEY)

def encrypt_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())