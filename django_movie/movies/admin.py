from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from movies.models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    """Модифицированное поле ввода"""
    description = forms.CharField(
        label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    """Добавление отзывов в раздел фильма"""
    model = Review
    # 1 дополнительное поле ввода нового отзыва
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotInline(admin.StackedInline):
    """Добавление кадров из фильма в раздел фильма"""
    model = MovieShot
    extra = 1

    readonly_fields = ('get_image',)

    # вывод миниатюры фотографии в списке
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="140">')
    # имя столбика с картинками
    get_image.short_description = 'Изображениe'


@ admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильм"""
    # порядок столбцов
    list_display = ('id', 'title', 'category', 'url', 'draft')
    # ссылка на страницу редактирования
    list_display_links = ('title',)
    # фильтрация по полям
    list_filter = ('category', 'year')
    # поиск по полям (важно указаь поле соединённой модели)
    search_fields = ('title', 'category__name')
    # подключение связанных с фильмом моделей
    inlines = [MovieShotInline, ReviewInline]
    # дублирование кнопок сохранения/удаления вверху страницы
    save_on_top = True
    # сохранение с копированием
    save_as = True
    # позволить редактировать поле в списке
    list_editable = ('draft',)

    # custom actions
    actions = ['publish', 'unpublish']

    # подключение модифицированного поля ввода
    form = MovieAdminForm

    # вывод миниатюры фотографии в списке
    readonly_fields = ('get_poster',)
    # группирование полей ввода
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': (('get_poster', 'description', 'poster'))
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Съемочная группа', {
            'classes': ('collapse',),
            'fields': (('actors', 'director', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_the_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )
    # получение постера к фильму

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} height="240">')
    # имя столбика с картинками
    get_poster.short_description = 'Изображениe'

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей было обновлено"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей было обновлено"
        self.message_user(request, f"{message_bit}")

    publish.short_description = 'Опубликовать'
    publish.allow_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allow_permissions = ('change',)


@ admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('id', 'name', 'email', 'parent', 'movie')
    list_display_links = ('name',)
    # запрет редактирования полей
    readonly_fields = ('name', 'email')


@admin.register(FilmCrew)
class FilmCrewAdmin(admin.ModelAdmin):
    """Съемочная группа"""
    list_display = ('id', 'name', 'age', 'get_image')
    list_display_links = ('name',)
    readonly_fields = ('get_image',)

    # вывод миниатюры фотографии в списке
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="50">')
    # имя столбика с картинками
    get_image.short_description = 'Изображениe'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('id', 'name')
    list_display_links = ('name',)


@admin.register(MovieShot)
class MovieShotAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('id', 'title', 'movie', 'get_image')
    list_display_links = ('title',)

    readonly_fields = ('get_image',)

    # вывод миниатюры фотографии в списке
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="50">')
    # имя столбика с картинками
    get_image.short_description = 'Изображениe'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг фильма"""
    list_display = ('id', 'ip', 'rate', 'movie')
    list_display_links = ('ip',)


# переименовывание заголовка и имени админской страницы
admin.site.site_title = "Django movies"
admin.site.site_header = "Django movies"
