from django.conf.urls import url

from .import views


urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/ para buscar por numero de paginas agregando specifics para agregar una notiacion de busqueda
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^videos/$',views.video, name='videos'),
    url(r'^encuestas/$',views.encuesta, name='encuestas'),
    url(r'^videodeta/(?P<video_id>[0-9]+)/$', views.videodeta, name='videodeta'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^crear/', views.crear, name='crear'),
    url(r'^login/',views.login_view,name='login'),
    url(r'^logout/',views.logout_view,name='logout'),
    url(r'^search/', views.search,name='busqueda'),
    url(r'^registro/',views.register_view,name='registro'),



]