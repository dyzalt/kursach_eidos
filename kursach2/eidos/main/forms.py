from .models import Articles
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, ClearableFileInput

class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'text', 'date', 'image']

        widgets= {
            'title': TextInput(attrs={
                'class': 'form-control form-control-top',
                'placeholder': 'Article name'
            }),
            'text': Textarea(attrs={
                'class': 'form-control form-control-text',
                'placeholder': 'Article text'
            }),
            'date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Date'
            }),
            'image': ClearableFileInput(attrs={
                'class': 'custom-image-input',
                'type': 'file',
                'placeholder': 'Image',
                'accept': 'image/*'
            })
        }