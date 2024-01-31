from datetime import date
from typing import Callable
from django.http import Http404, HttpRequest, JsonResponse

from .models import Book, BookRecord
from members.models import Member
from utils.decorators import need_login
from utils.image_loader import load_image

@need_login
def list_book(request: HttpRequest, member: Member, data: dict):
    
    get_info: Callable[[Book], dict] = \
        lambda book: {
            'name': book.name,
            'id': book.id,
            'author': book.author,
            'publisher': book.publisher,
            'image': '',
            'available': book.available,
            'tags': [str(tag) for tag in book.tags.all()],
        }
    
    return JsonResponse({'books': [get_info(b) for b in Book.objects.all()]})


@need_login
def get_image(request: HttpRequest, member: Member, data: dict):

    id = data['id']
    if not Book.objects.filter(id=id).exists():
        return Http404()
    
    book = Book.objects.get(id=id)
    return JsonResponse({'image': load_image(f'book/{book.id}.jpg')})


@need_login
def borrow(request: HttpRequest, member: Member, data: dict):

    id = data['id']
    if not Book.objects.filter(id=id).exists():
        return JsonResponse({'success': False, 'error': '책을 찾을 수 없습니다.'}, status=404)
    
    book = Book.objects.get(id=id)
    if not book.available:
        return JsonResponse({'success': False, 'error': '책이 이미 대출중입니다.'}, status=403)
    
    book.available = False
    record = BookRecord(borrower=member, book=book, start_date=date.today())
    record.save()
    
    return JsonResponse({'success': True})