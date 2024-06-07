from django import forms
from .models import Category, Husband, Women
from django.core.validators import MinLengthValidator, MaxLengthValidator, ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'йцукенгшщзхъфывапролджэёячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮ1234567890- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутвовать только русские символы, дефис и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):  # forms.Form
    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }

        labels = {'slug': 'URL'}
    # title = forms.CharField(max_length=255,
    #                         label='Заголовок',
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         min_length=5,
    #                         error_messages={
    #                             'min_length': 'Слишком короткий заголовок',
    #                             'required': 'Без заголовка никак'
    #                         },)
    #                         # validators=[
    #                         #     RussianValidator(),
    #                         # ])
    slug = forms.SlugField(max_length=255,
                           required=False,
                           label='URL',
                           validators=[
                               MinLengthValidator(5, message='Минимум 5 символов'),
                               MaxLengthValidator(100, message='Максимум 100 символов'),
                           ],
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Будет сгенерировано'}
                               )
                           )
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    # is_published = forms.BooleanField(required=False, label='Видимость', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label='Не замужем', required=False, label='Муж')

    # def clean_title(self):  # Валидатор для одного поля певрое слово clean второе поле
    #     title = self.cleaned_data['title']
    #     ALLOWED_CHARS = 'йцукенгшщзхъфывапролджэёячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮ1234567890- '
    #
    #     if not (set(title) <= set(ALLOWED_CHARS)):
    #         raise ValidationError('Должны присутвовать только русские символы, дефис и пробел')

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")

