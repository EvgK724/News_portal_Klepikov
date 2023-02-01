import django_filters
from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post


class PostFilter(FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок',
    )


    type = django_filters.ChoiceFilter(
        field_name='category_type',
        label='Тип',
        empty_label='Выбрать',
        choices=Post.CATEGORY_CHOICES,
    )

    added_after = DateTimeFilter(
        field_name='date_create',
        lookup_expr='gt',
        label='Дата публикации с:',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )
