from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Film(models.Model):
    """
        Здесь мы создаем модельку Нашего фильма
    """

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts', verbose_name='Владелец'
    )

    title = models.CharField('Название', max_length=40,)
    description = models.TextField('Описание', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    update_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f'{self.title}'


class Like(models.Model):

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    movie = models.ForeignKey(
        Film, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} -> {self.movie.title}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} -> {self.post.title}'


class Rating(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(
        Film, on_delete=models.CASCADE, related_name='ratings')

    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ], blank=True, null=True)

    def __str__(self):
        return f'{self.owner} -> {self.movie.title}'
