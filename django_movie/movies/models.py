from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class FilmCrew(models.Model):
    """ Съемочная группа """
    name = models.CharField('Имя', max_length=50)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='crew/')

    class Meta:
        verbose_name = "Съемочная группа"
        verbose_name_plural = "Съемочная группа"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """ Жанр """
    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Genre_detail", kwargs={"pk": self.pk})


class Movie(models.Model):
    """ Фильм """
    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата выхода', default=2010)
    country = models.CharField('Страна', max_length=50)
    director = models.ManyToManyField(
        FilmCrew, verbose_name='Режиссер', related_name='film_director'
    )
    actors = models.ManyToManyField(
        FilmCrew, verbose_name='Актеры', related_name='film_actors'
    )
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world_premiere = models.DateField('Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField(
        'Бюджет', default=0, help_text="Указать сумму в долларах"
    )
    fees_in_usa = models.PositiveIntegerField(
        'Сборы в США', default=0, help_text="Указать сумму в долларах"
    )
    fees_in_the_world = models.PositiveIntegerField(
        'Сборы в мире', default=0, help_text="Указать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    # получение отзыва о фильме без родительских записей
    def get_review(self):
        return self.review_set.filter(parent__isnull=True)


class MovieShot(models.Model):
    """ Кадры из фильма """
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("MovieShots_detail", kwargs={"pk": self.pk})


class Rating(models.Model):
    """ Рейтинг """
    RATE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    ip = models.CharField('IP адрес', max_length=16)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Rating_detail", kwargs={"pk": self.pk})


class Review(models.Model):
    """ Отзыв """
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Текст', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Review_detail", kwargs={"pk": self.pk})
