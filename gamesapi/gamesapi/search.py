#
# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl import *
# from elasticsearch.helpers import bulk
# from elasticsearch import Elasticsearch
# from games import models
#
# connections.create_connection()
#
# class GameIndex(DocType):
#     owner = Integer()
#     created = Date()
#     name = Text()
#     release_date = Date()
#
#     class Meta:
#         index = 'game-index'
#
#
# def bulk_indexing():
#     GameIndex.init()
#     es = Elasticsearch()
#     bulk(client=es, actions=(
#         b.indexing() for b in models.Game.objects.all().iterator()
#     ))
