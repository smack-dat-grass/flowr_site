from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:tool_id>/', views.tool, name='tool'),
    # path('<int:tool_id>/sso_lookup/<str:sso>/', views.sso_lookup, name='sso_lookup'),
    # path('<int:tool_id>/user_training_update', utm_views.user_training_update, name='user_training_update'),

]

