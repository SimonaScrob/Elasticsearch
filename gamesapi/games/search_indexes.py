#
# from haystack import indexes
# from games.models import Game
#
#
# class GameIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     created = indexes.DateTimeField(model_attr='created')
#     name = indexes.CharField(model_attr='name')
#     release_date = indexes.DateTimeField(model_attr='release_date')
#     game_category = indexes.CharField(model_attr='game_category', faceted=True)
#     played = indexes.BooleanField(model_attr='played')
#
#     def get_model(self):
#         return Game
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.all()
