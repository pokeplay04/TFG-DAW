from django.urls import path

from . import api


urlpatterns= [
    path('', api.post_list, name='post_list'),
    path('api/', include('account.urls')),
    path('api/posts/', include('post.url')),
    path('admin/', admin.site.urls),
    

]