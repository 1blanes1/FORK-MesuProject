# views.py (без БД)
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from api.functions import *
from .models import UploadedImage
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import json
import os
from django.views.decorators.csrf import ensure_csrf_cookie


def my_page(request):
    return render(request, 'index2.html')
@ensure_csrf_cookie
def admin(request):
    return render(request, 'admin.html')
def history_page(request):
    return render(request, 'history_lines.html')
def team_page(request):
    return render(request, 'team.html')
def contacts_page(request):
    return render(request, 'contacts.html')
def news_page(request):
    return render(request, 'news.html')
def partners_page(request):
    return render(request, 'partners.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"error": "Неверный логин или пароль"}, status=401)
    return JsonResponse({"error": "Только POST"}, status=405)


def get_partners(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.BASE_DIR,'media', 'jsons', 'partners.json')
        news = read_json(filepath)
        return JsonResponse(news, safe=False)


def get_news(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.BASE_DIR,'media', 'jsons', 'news.json')
        news = read_json(filepath)
        return JsonResponse(news, safe=False)
    

def get_history_lines(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.BASE_DIR,'media', 'jsons', 'history_lines.json')
        history_line = read_json(filepath)
        return JsonResponse(history_line, safe=False)


def get_team(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.BASE_DIR,'media', 'jsons', 'team_member.json')
        team_member = read_json(filepath)
        return JsonResponse(team_member, safe=False)

@login_required
@require_http_methods(["DELETE"])
def delete_history_line(request):
    try:
        data = json.loads(request.body)
        title = data.get('title')
        print(title)
        delete_from_json_file('media/jsons/history_lines.json', title)
        return JsonResponse('ok', status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_http_methods(["DELETE"])
def delete_news(request):
    try:
        data = json.loads(request.body)
        title = data.get('title')
        print(title)
        delete_from_json_file('media/jsons/news.json', title)
        return JsonResponse('ok', status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_http_methods(["DELETE"])
def delete_partner(request):
    try:
        data = json.loads(request.body)
        title = data.get('title')
        print(title)
        delete_from_json_file('media/jsons/partners.json', title)
        return JsonResponse('ok', status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    pass

@login_required
@require_http_methods(["DELETE"])
def delete_team_member(request):
    try:
        data = json.loads(request.body)
        title = data.get('title')
        print(title)
        delete_from_json_file('media/jsons/team_member.json', title)
        return JsonResponse('ok', status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    pass


@login_required
@require_http_methods(["POST"])
def post_team_member(request):
    try:
        title = request.POST.get('title', '').strip()
        status = request.POST.get('status', '').strip()
        role = request.POST.get('role', '').strip()
        url = request.POST.get('url', '').strip()
        image = request.FILES.get('image')
        

        img_path = ""

        # Сохраняем изображение, если оно есть
        if image:
            # Формируем путь: uploads/имя_файла
            upload_to = 'uploads/team_member_img'
            full_path = os.path.join(upload_to, image.name)

            # Безопасность: избегаем перезаписи и путей вроде '../../etc/passwd'
            full_path = default_storage.get_available_name(full_path)

            # Сохраняем файл
            path = default_storage.save(full_path, ContentFile(image.read()))
            img_path = default_storage.url(path)  # Например: '/media/uploads/photo.jpg'
        # Подготавливаем данные
        data = {
            "title": title,
            "status": status,
            "role": role,
            "url": url,
            "img_path": img_path
        }
        filepath = os.path.join(settings.BASE_DIR,'media', 'jsons', 'team_member.json')
        # Сохраняем в JSON (твоя функция)
        add_item_to_json(data, filepath)

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def post_partner(request):
    try:
        title = request.POST.get('title', '').strip()
        url = request.POST.get('url', '').strip()
        image = request.FILES.get('image')
        

        img_path = ""

        # Сохраняем изображение, если оно есть
        if image:
            # Формируем путь: uploads/имя_файла
            upload_to = 'uploads/partner_img'
            full_path = os.path.join(upload_to, image.name)

            # Безопасность: избегаем перезаписи и путей вроде '../../etc/passwd'
            full_path = default_storage.get_available_name(full_path)

            # Сохраняем файл
            path = default_storage.save(full_path, ContentFile(image.read()))
            img_path = default_storage.url(path)  # Например: '/media/uploads/photo.jpg'
        # Подготавливаем данные
        data = {
            "title": title,
            "url": url,
            "img_path": img_path
        }
        filepath = os.path.join(settings.BASE_DIR,'media','jsons', 'partners.json')
        # Сохраняем в JSON (твоя функция)
        add_item_to_json(data, filepath)

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def post_news(request):
    try:
        title = request.POST.get('title', '').strip()
        desc = request.POST.get('desc', '').strip()
        url = request.POST.get('url', '').strip()
        image = request.FILES.get('image')
        

        img_path = ""

        # Сохраняем изображение, если оно есть
        if image:
            # Формируем путь: uploads/имя_файла
            upload_to = 'uploads/news_img'
            full_path = os.path.join(upload_to, image.name)

            # Безопасность: избегаем перезаписи и путей вроде '../../etc/passwd'
            full_path = default_storage.get_available_name(full_path)

            # Сохраняем файл
            path = default_storage.save(full_path, ContentFile(image.read()))
            img_path = default_storage.url(path)  # Например: '/media/uploads/photo.jpg'
        # Подготавливаем данные
        data = {
            "title": title,
            "desc": desc,
            "url": url,
            "img_path": img_path
        }
        filepath = os.path.join(settings.BASE_DIR,'media','jsons', 'news.json')
        # Сохраняем в JSON (твоя функция)
        add_item_to_json(data, filepath)

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_http_methods(["POST"])    
def post_history_line(request):
    try:
        title = request.POST.get('title', '').strip()
        desc = request.POST.get('desc', '').strip()
        url = request.POST.get('url', '').strip()
        image = request.FILES.get('image')
        

        img_path = ""

        # Сохраняем изображение, если оно есть
        if image:
            # Формируем путь: uploads/имя_файла
            upload_to = 'uploads/history_img'
            full_path = os.path.join(upload_to, image.name)

            # Безопасность: избегаем перезаписи и путей вроде '../../etc/passwd'
            full_path = default_storage.get_available_name(full_path)

            # Сохраняем файл
            path = default_storage.save(full_path, ContentFile(image.read()))
            img_path = default_storage.url(path)  # Например: '/media/uploads/photo.jpg'
            # real_img_path = "/media/img/" + image.name
        # Подготавливаем данные
        data = {
            "title": title,
            "desc": desc,
            "url": url,
            "img_path": img_path
        }
        filepath = os.path.join(settings.BASE_DIR,'media','jsons', 'history_lines.json')
        # Сохраняем в JSON (твоя функция)
        add_item_to_json(data, filepath)

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
