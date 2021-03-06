# from django.shortcuts import render
#
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# # from rest_framework.renderers import JSONRenderer
# from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser
# from rest_framework import status
# from rest_framework.response import Response
#
# from games.models import Game
# from games.serializers import GameSerializer
#
# # class JSONResponse(HttpResponse):
# #
# #     def __init__(self, data, **kwargs):
# #         content = JSONRenderer().render(data)
# #         kwargs['content_type'] = 'application/json'
# #         super(JSONResponse, self).__init__(content, **kwargs)
#
#
# # @csrf_exempt
# @api_view(['GET', 'POST'])
# def game_list(request):
#     if request.method == 'GET':
#         games = Game.objects.all()
#         games_serializer = GameSerializer(games, many=True)
#         return Response(games_serializer.data)
#         # return JSONResponse(games_serializer.data)
#     elif request.method == 'POST':
#         # game_data = JSONParser().parse(request)
#         game_serializer = GameSerializer(data=request.data)
#         # game_serializer = GameSerializer(data=game_data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return Response(game_serializer.data, status=status.HTTP_201_CREATED)
#             # return JSONResponse(game_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         # return JSONResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # @csrf_exempt
# @api_view(['GET', 'PUT', 'POST'])
# def game_detail(request, pk):
#     try:
#         game = Game.objects.get(pk=pk)
#     except Game.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         game_serializer = GameSerializer(game)
#         return Response(game_serializer.data)
#         # return JSONResponse(game_serializer.data)
#     elif request.method == 'PUT':
#         # game_data = JSONParser().parse(request)
#         # game_serializer = GameSerializer(game, data=game_data)
#         game_serializer = GameSerializer(game, data=request.data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return Response(game_serializer.data)
#             # return JSONResponse(game_serializer.data)
#         return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         # return JSONResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         game.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

import django_filters
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle

from games.models import Player, PlayerScore, GameCategory, Game, Article, ArticleType
from games.permissions import IsOwnerOrReadOnly
from games.serializers import PlayerSerializer, PlayerScoreSerializer, \
    GameCategorySerializer, GameSerializer, \
    UserSerializer, ArticleSerializer, ArticleTypeSerializer
from rest_framework import filters
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter, FilterSet


from haystack.forms import FacetedSearchForm as BaseFacetedSearchForm
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView



class UserViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetailViewSet(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class GameCategoryViewSet(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle, )
    filter_fields = ('name', )
    search_fields = ('^name', )
    ordering_fields = ('name', )


class GameCategoryDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)


class GameViewSet(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    filter_fields = ('name', 'game_category', 'release_date', 'played', 'owner')
    search_fields = ('^name',)
    ordering_fields = ('name', 'release_date',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GameDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class PlayerViewSet(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'
    filter_fields = ('name', 'gender')
    search_fields = ('^name',)
    ordering_fields = ('name',)


class PlayerDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreFilter(django_filters.FilterSet):
    min_score = django_filters.NumberFilter(field_name='score', lookup_expr='gte')
    max_score = django_filters.NumberFilter(field_name='score', lookup_expr='lte')
    from_score_date = django_filters.DateTimeFilter(field_name='score_date', lookup_expr='gte')
    to_score_date = django_filters.DateTimeFilter(field_name='score_date', lookup_expr='lte')
    player_name = django_filters.AllValuesFilter(field_name='player__name')
    game_name = django_filters.AllValuesFilter(field_name='game__name')

    class Meta:
        model = PlayerScore
        fields = [
            'score', 'min_score', 'max_score', 'from_score_date',
            'to_score_date', 'player_name', 'game_name'
        ]


class PlayerScoreViewSet(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'
    filter_class = PlayerScoreFilter
    ordering_fields = ('score', 'score_date', )


class PlayerScoreDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


class ArticleViewSet(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    name = 'article-list'
    # filter_class = PlayerScoreFilter


class ArticleTypeViewSet(generics.ListCreateAPIView):
    queryset = ArticleType.objects.all()
    serializer_class = ArticleTypeSerializer
    name = 'article-types'
    # filter_class = PlayerScoreFilter


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'players': reverse(PlayerViewSet.name, request=request),
            'game-categories': reverse(GameCategoryViewSet.name, request=request),
            'games': reverse(GameViewSet.name, request=request),
            'scores': reverse(PlayerScoreViewSet.name, request=request),
            'users': reverse(UserViewSet.name, request=request),
            'article-types': reverse(ArticleTypeViewSet.name, request=request),
            'articles': reverse(ArticleViewSet.name, request=request)
        })



class FacetedSearchForm(BaseFacetedSearchForm):
    def __init__(self, *args, **kwargs):
        self.selected_facets = kwargs.pop("selected_facets", [])
        super(FacetedSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        sqs = self.searchqueryset
        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

        if self.load_all:
            sqs = sqs.load_all()

        return sqs


class FacetedSearchView(BaseFacetedSearchView):
    template_name = 'search/search.html'
    facet_fields = []
    form_class = FacetedSearchForm
