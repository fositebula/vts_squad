from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
import views


urlpatterns = [
    url('^$', views.index, name='index'),
    url('^submit/$', views.job_submit, name='submit'),
    url('^job_info/$', views.job_info, name='job_info')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)