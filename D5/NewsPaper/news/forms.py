from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['author',  'head', 'text', 'post_category']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        head = cleaned_data.get("head")

        if head == text:
            raise ValidationError(
                "Текст не должен быть идентичен заголовку."
            )

        return cleaned_data