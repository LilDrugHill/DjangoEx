from django.urls import path, re_path, register_converter
from women import views
from women import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    # path('cats/<int:cat_id>', views.categories),
    # path('cats/<slug:cat_slug>', views.categories_by_slug),
    # #re_path(r"^archive/(?P<year>[0-9]{4}"), # При успешной регулярке отдает сайт иначе 404, заккомент тк функионал теперь в отдельном классе
    # path('archive/<year4:year>', views.archive)
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('category/<slug:cat_slug>', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.TagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>', views.UpdatePage.as_view(), name='tag'),

]















