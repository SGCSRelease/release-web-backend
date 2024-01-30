from django.db import models
from django.contrib.auth.models import AbstractUser

class State:
    ENROLLED = 0
    ABSENCE = 1
    GRADUATED = 2
    choices = (
        (ENROLLED, '재학'),
        (ABSENCE, '휴학'),
        (GRADUATED, '졸업'),
    )

class Role:
    choices = (
        (0, '학회원'),
        (1, '임원'),
        (2, '학회장'),
    )
    

class Member(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)
    password = models.BinaryField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    state = models.IntegerField(choices=State.choices)
    role = models.IntegerField(choices=Role.choices)