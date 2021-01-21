from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    message = forms.CharField(
        label = False,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Message'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = False

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Title'
        })

    class Meta:
        model = Post
        fields = (
            'title',
            'message',
            'author',
        )
        exclude = ('author',)
