<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> main
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
    path('partners', views.get_partners, name='partners')
    # ^ api для запроса списка партёнров
                ЧИТАТЬ ОПИСАНИЕ НИЖЕ
-----------------------------------------------------------------
Статические запросы: "они ссылаются на html с их страницой"
    '', - основная страница
    'admin', - админка
    'history_page', - страница с историческими линиями
-----------------------------------------------------------------
API для того, чтобы получить json'ки данного сегмента:
    'history_page/get',
    'news',
    'partners'
Данный сегмент апишек возвращает json'ки вида:
[
    {
        title: "lkfkv",
        desc: "mlcmwlmw",
        url: "https//"
    },
    {
        title: "lkfkv",
        desc: "mlcmwlmw",
        url: "https//"
    }
]
Смотри подробней в json_api/media/jsons
------------------------------------------------------------------
API для добавления информации в соответствующий json:
    'api/post_news'
    'api/post_history_line'
    'api/post_partners'
записывают в json отправленные данные, пример отправки на js смотри в файле admin.html - func sumbitData(formData)
------------------------------------------------------------------
<<<<<<< HEAD
=======
=======
для новостей fetch('/api/get_news') ->
{
    title: "Literaly that Russia",
    description: "Russia is the best country",
    img_path: "media/uploads/image.png"
}
>>>>>>> back
>>>>>>> main
