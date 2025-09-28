from django.urls import path
from api import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.my_page, name='page'),
    path('admin', views.admin, name='admin'),
    path('news', views.get_news, name='news'),
    path('api/post_news', views.post_news, name='post_news'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)