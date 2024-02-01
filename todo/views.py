from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, ListView

from .forms import TodoForm
from .models import Todo


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "todo/index.html"
    context_object_name = "list"
    ordering = ["-date"]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forms"] = TodoForm()
        context["title"] = "TODO LIST"
        return context

    def post(self, request, *args, **kwargs):
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = self.request.user
            todo.save()
            return redirect("todo:list")
        else:
            messages.error(request, "Invalid form submission.")
            return redirect("todo:list")


class TodoDeleteView(LoginRequiredMixin, DeleteView):  # type: ignore
    model = Todo
    success_url = reverse_lazy("todo:list")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo.user != self.request.user:
            raise Http404("You do not have permission to delete this todo.")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model, pk=self.kwargs["pk"], user=self.request.user
        )
