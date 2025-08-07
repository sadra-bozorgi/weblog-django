from django.urls import path
from .import views

app_name = 'maqale'

urlpatterns=[
    path('maqale/',views.post_list,name='maqale'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('comment/like/<int:comment_id>/', views.like_comment, name='like_comment'),
]