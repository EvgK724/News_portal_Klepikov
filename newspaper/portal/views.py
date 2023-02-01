from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy


class PostsList(ListView):
    model = Post
    ordering = '-date_create'
    template_name = 'posts.html'
    context_object_name = 'posts_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['filterset'] = self.filterset
        # context['is_author'] = self.request.user.groups.filter(name='authors')
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post_detail'


class PostSearch(ListView):
    form_class = PostForm
    model = Post
    ordering = '-date_create'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('portal.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.category_type = 'NW'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('portal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('portal.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('portal.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        return super().form_valid(form)


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('portal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    success_url = reverse_lazy('posts_list')


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('portal.delete_post',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('posts_list')


class AuthorCreateView(LoginRequiredMixin):
    model = Author
    fields = ['author']

    def form_valid(self, form):
        form.instance.author_user = self.request.user
        return super().form_valid(form)

# @login_required
# def upgrade_user(self, request):
#     user = request.user
#     authors = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         authors.user_set.add(user)
#         if not hasattr(user, 'author'):
#             Author.objects.create(author_user=User.objects.get(pk=user.id))
#     return redirect('/')


