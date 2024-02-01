from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "details"]

    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["placeholder"] = "Title"
        self.fields["details"].widget.attrs["placeholder"] = "Details"
