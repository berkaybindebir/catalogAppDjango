from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.product_list, name='list'), #index route
    url(r'^detail/(?P<slug>[\w-]+)/$', views.product_detail, name='detail'), #detail route
    url(r'^create/', views.product_create, name='create'), #create route
    url(r'^detail/(?P<slug>[\w-]+)/edit/$', views.product_update, name='update'), #update route
    url(r'^detail/(?P<slug>[\w-]+)/delete/$', views.product_delete, name='delete'), #delete route
    url(r'^category/(?P<slug>.+)/$', views.category_details, name='category'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
