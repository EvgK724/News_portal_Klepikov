from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    post_category = forms.ModelChoiceField(
        label='Категория',
        empty_label='Выбрать',
        queryset=Category.objects.all(),
    )

    author = forms.ModelChoiceField(
        label="Автор",
        empty_label='Выбрать',
        queryset=Author.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category_type',
            'author',
        ]
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'category_type': 'Тип',
            'author': 'Автор',
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if text == title:
            raise ValidationError(
                "Описание не должно быть идентично названию"
            )

        return cleaned_data


