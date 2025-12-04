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


def my_page(request):
    return render(request, 'index.html')
def admin(request):
    return render(request, 'admin.html')
def history_page(request):
    return render(request, 'history_page.html')

@csrf_exempt
def get_partners(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.BASE_DIR,'media','jsons', 'partners.json')
        news = read_json(filepath)
        return JsonResponse(news, safe=False)

@csrf_exempt
def get_news(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.BASE_DIR,'media','jsons', 'news.json')
        news = read_json(filepath)
        return JsonResponse(news, safe=False)
    
@csrf_exempt
def get_history_lines(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.BASE_DIR,'media','jsons', 'history_lines.json')
        history_line = read_json(filepath)
        return JsonResponse(history_line, safe=False)

@csrf_exempt
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
            upload_to = 'uploads'
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

@csrf_exempt
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
            upload_to = 'uploads'
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

@csrf_exempt
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
            upload_to = 'uploads'
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
        filepath = os.path.join(settings.BASE_DIR,'media','jsons', 'history_lines.json')
        # Сохраняем в JSON (твоя функция)
        add_item_to_json(data, filepath)

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# @csrf_exempt
# def post(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print(data)
#         asyncio.run(add_item_to_json(data))
#         return JsonResponse("OK")
#     if request.method == 'GET':
#         return
#     return JsonResponse({"error": "POST only"}, status=405)
# @csrf_exempt
# def get_news(request):
#     if request.method == 'GET':
#         try:
#             data = read_json('news.json')
#             print(data)
#             return JsonResponse(data, safe=False)  # ← safe=False для списков!
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
# @csrf_exempt
# def upload_image(request):
#     if 'image' not in request.FILES:
#         return JsonResponse({'error': 'No image provided'}, status=400)
    
#     image_file = request.FILES['image']
#     instance = UploadedImage.objects.create(image=image_file)
    
#     return instance.image.url
# @csrf_exempt
# def get_images(request):
#     if request.method =='GET':
#     # Путь к папке с изображениями (например, 'media/uploads/')
#         media_root = settings.MEDIA_ROOT
#         folder_path = os.path.join(media_root, 'uploads')


#         # Проверяем, существует ли папка
#         if not os.path.exists(folder_path):
#             return JsonResponse({'error': 'Folder does not exist'}, status=404)

#         # Расширения изображений
#         image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

#         # Собираем все изображения
#         images = []
#         for filename in os.listdir(folder_path):
#             if filename.lower().endswith(image_extensions):
#                 file_path = os.path.join('uploads', filename)  # относительный путь
#                 images.append({
#                     'filename': filename,
#                     'url': f"{settings.MEDIA_URL}{file_path}",  # например: /media/uploads/photo.jpg
#                 })

#         return JsonResponse({'images': images})