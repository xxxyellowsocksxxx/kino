from django import forms

from movies.models import Review


class ReviewForm(forms.ModelForm):
    """ Форма отзыва """

    class Meta:
        model = Review
        fields = ('name', 'email', 'text')
