from uuid import uuid4
from pytils.translit import slugify


menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]


def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


class DataMixin:
    title_page = None
    extra_context = {}
    cat_selected = None
    paginate_by = 3

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        # if 'menu' not in self.extra_context:
        #     self.extra_context['menu'] = menu

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    def get_mixin_context(self, context,  **kwargs):
        context['cat_selected'] = self.cat_selected
        context.update(kwargs)
        return context
