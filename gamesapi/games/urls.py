from django.conf.urls import url
from games import views

urlpatterns = [
    # url(r'^games/$', views.game_list),
    # url(r'^games/(?P<pk>[0-9]+)/$', views.game_detail),
    url(r'^game-categories/$', views.GameCategoryViewSet.as_view(), name=views.GameCategoryViewSet.name),
    url(r'^game-categories/(?P<pk>[0-9]+)/$', views.GameCategoryDetailViewSet.as_view(), name=views.GameCategoryDetailViewSet.name),
    url(r'^games/$', views.GameViewSet.as_view(), name=views.GameViewSet.name),
    url(r'^games/(?P<pk>[0-9]+)/$', views.GameDetailViewSet.as_view(), name=views.GameDetailViewSet.name),
    url(r'^players/$', views.PlayerViewSet.as_view(), name=views.PlayerViewSet.name),
    url(r'^players/(?P<pk>[0-9]+)/$', views.PlayerDetailViewSet.as_view(), name=views.PlayerDetailViewSet.name),
    url(r'^player-score/$', views.PlayerScoreViewSet.as_view(), name=views.PlayerScoreViewSet.name),
    url(r'^player-score/(?P<pk>[0-9]+)/$', views.PlayerScoreDetailViewSet.as_view(), name=views.PlayerScoreDetailViewSet.name),
    url(r'^users/$', views.UserViewSet.as_view(), name=views.UserViewSet.name),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailViewSet.as_view(), name=views.UserDetailViewSet.name),
    url(r'^article-types/$', views.ArticleTypeViewSet.as_view(), name=views.ArticleTypeViewSet.name),
    url(r'^articles/$', views.ArticleViewSet.as_view(), name=views.ArticleViewSet.name),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailViewSet.as_view(), name=views.UserDetailViewSet.name),
    url(r'^$', views.ApiRoot.as_view(), name=views.ApiRoot.name)
]
