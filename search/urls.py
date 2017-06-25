from django.conf.urls import url

from search import views

urlpatterns = [
    url(r'^import_db/$', views.import_db),
    url(r'import_index/$', views.import_index),
    url(r'^run/$', views.search)
]