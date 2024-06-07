import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator

from .models import Women, Category, TagPost, UploadFile
from .forms import AddPostForm, UploadFileForm
from .utils import DataMixin

# Create your views here.
# def index(request):
#     # t = render_to_string('women/index.html')  тоже что и возврат ниже
#     # return HttpResponse(t)
#     posts = Women.published.all().select_related('cat')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', data)


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WomenHome, self).get_context_data()

        return self.get_mixin_context(context, **kwargs)


def handle_uploaded_file(f):
    file_name = f"uploads/{f.name}"
    i = 1
    while os.path.isfile(file_name):
        name, format = f.name.split('.')
        name += f'({i})'
        file_name = f'uploads/{".".join((name, format))}'
        i += 1
    with open(file_name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    contact_list = Women.published.all().order_by('pk')
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'title': 'О сайте',
        'page_obj': page_obj,
    }

    return render(request, 'women/about.html', data)


def categories(request, cat_id):
    return HttpResponse(f'<h1>Категории<p> {cat_id}</p></h1>')


def categories_by_slug(request, cat_slug):
    return HttpResponse(f'Категории {cat_slug}')


def archive(request, year):
    return HttpResponse(f'Архив по годам: {year}')


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'women/post.html', data)


class ShowPost(DataMixin, DetailView):
    # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title, cat_selected=context['post'].cat.pk)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             #
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'title': 'Добавление статьи',
#         'menu': menu,
#         'form': form,
#     }
#
#     return render(request, 'women/add_page.html', data)

# class AddPage(View):
#
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'title': 'Добавление статьи',
#             'menu': menu,
#             'form': form,
#         }
#         return render(request, 'women/add_page.html', data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             #
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#         data = {
#             'title': 'Добавление статьи',
#             'menu': menu,
#             'form': form,
#         }
#         return render(request, 'women/add_page.html', data)


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    # model = Women
    # fields = '__all__'
    template_name = 'women/add_page.html'
    title_page = 'Добавление статьи'

    def get_context_data(self, **kwargs):
        context = super(AddPage, self).get_context_data(**kwargs)
        return self.get_mixin_context(context, cat_selected=None)

    # def form_valid(self, form): Для класса formview, createview автоматически создает запись
    #     form.save()
    #     return super(AddPage, self).form_valid()


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'cat', 'is_published', 'husband', 'tags', 'photo']
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование страницы'

    def get_context_data(self, **kwargs):
        context = super(UpdatePage, self).get_context_data()
        return self.get_mixin_context(context, title='Редактирование страницы')

def login(request):
    return HttpResponse('Войти')


def contact(request):
    return HttpResponse('Контакты')

#
# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'women/index.html', data)


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # При пустом списке посты 404

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Тег: {tag.tag}',
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'  # Переменная содержащая кверисет
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тэг - ' + tag.tag)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
