from django.urls import path

from .views import TodoDeleteView, TodoListView

app_name = "todo"

urlpatterns = [
    path("", TodoListView.as_view(), name="list"),
    path("del/<int:pk>/", TodoDeleteView.as_view(), name="del"),
]
