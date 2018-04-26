from django.conf.urls import url
from twitter_app import views

urlpatterns = [
                url(r'^main_page/$', views.main_page, name='Main'),
                 url(r'^dashboard/$', views.dashboard, name='ins_action' ),
            ]
