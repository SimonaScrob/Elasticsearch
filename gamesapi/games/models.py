from django.db import models
# from gamesapi.search import GameIndex


class GameCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Game(models.Model):
    owner = models.ForeignKey('auth.User', related_name='games', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True)
    release_date = models.DateTimeField()
    game_category = models.ForeignKey(GameCategory, related_name='games', on_delete=models.CASCADE)
    played = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    # def indexing(self):
    #     obj = GameIndex(
    #         meta={'id': self.id},
    #         owner=self.owner,
    #         created=self.created,
    #         name=self.name,
    #         release_date=self.release_date
    #     )
    #     obj.save()
    #     return obj.to_dict(include_meta=True)


class Player(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, blank=False, default='')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=MALE)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class PlayerScore(models.Model):
    player = models.ForeignKey(Player, related_name='scores', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()
    score_date = models.DateTimeField()

    class Meta:
        ordering = ('-score',)


class ArticleType(models.Model):
    name = models.TextField(max_length=30)


class Article(models.Model):
    title = models.TextField(max_length=100)
    text = models.TextField()
    type = models.ForeignKey(ArticleType, related_name='articles',  on_delete=models.CASCADE)






