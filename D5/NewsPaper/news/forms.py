from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

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


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user