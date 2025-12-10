from django.urls import path
from api import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.my_page, name='page'),
    # ^ основная страница
    path('admin', views.admin, name='admin'),
    # ^ админка
    path('history_page', views.history_page, name='history_page'), 
    # ^ просто страница, где будут собраны все исторические линии 
    path('history_page/get', views.get_history_lines, name='load_history_page'), 
    # ^ api для подгрузки из history_lines.json
    path('news', views.get_news, name='news'),
    # ^ api для подгрузки всех новостей из news.json на главную страницу
    path('api/post_news', views.post_news, name='post_news'),
    # ^ api для записи новостей в news.json
    path('api/post_history_line', views.post_history_line, name='post_history_line'),
    # ^  api для добавления в history_lines.json
    path('api/post_partners', views.post_partner, name='post_partners'),
    # ^ api для добавления в партнёры
    path('partners', views.get_partners, name='partners'),
    # ^ api для запроса списка партёнров
    path('api/post_team_member', views.post_team_member, name='huila'),
    # ^  api для добавления в список команды
    path('team_page/get', views.get_team, name='team'),
    # ^ api для запроса команды
    path('team_page', views.team_page, name='team_page'),
    # ^ страница с командой
    path('contacts_page', views.contacts_page, name='contacts'),
    # ^ страница с контактами
    path('news_page', views.news_page, name='news_page'),
    
    path('api/login/', views.login_view, name='login'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

