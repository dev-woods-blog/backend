from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.post_list),
    path('posts/category/<int:categoryId>', views.post_list_by_category),
    path('posts/detail/<int:postId>', views.detail_post),
    path('new/post', views.create_post),
    path('posts/<int:postId>', views.update_delete_post),
    path('category/list', views.category_list),
    path('category', views.create_category),
    path('category/list/<int:categoryId>', views.update_delete_category)
]