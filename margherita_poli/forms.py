from django import forms
from .models import Painting, Post


class PaintingForm(forms.ModelForm):
    class Meta:
        model = Painting
        fields = [
            'section',
            'title', 'description',
            'title_en', 'description_en',
            'image',
            'status', 'price', 'custom_price_text',
            'order',
        ]
        
        labels = {
            'section': 'Collezione',
            'title': 'Titolo del dipinto',
            'description': 'Descrizione',
            'title_en': 'Titolo (EN)',
            'description_en': 'Descrizione (EN)',
            'image': 'Immagine',
            'status': 'Stato',
            'price': 'Prezzo (€)',
            'custom_price_text': 'Testo personalizzato',
            'order': 'Ordine',
        }

        widgets = {
            'section': forms.Select(attrs={'class': 'field-input'}),
            
            'title': forms.TextInput(attrs={'class': 'field-input'}),
            'description': forms.Textarea(attrs={'class': 'field-input', 'rows': 4}),
            
            'title_en': forms.TextInput(attrs={'class': 'field-input'}),
            'description_en': forms.Textarea(attrs={'class': 'field-input', 'rows': 4}),
            
            'image': forms.ClearableFileInput(attrs={'class': 'field-input'}),
            
            'status': forms.Select(attrs={'class': 'field-input'}),
            'price': forms.NumberInput(attrs={'class': 'field-input', 'placeholder': '0.00'}),
            'custom_price_text': forms.TextInput(attrs={'class': 'field-input'}),
            
            'order': forms.NumberInput(attrs={'class': 'field-input'}),
        }
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titolo_it', 'titolo_en', 'contenuto_it', 'contenuto_en']
        widgets = {
            'titolo_it': forms.TextInput(attrs={'placeholder': 'Titolo in italiano'}),
            'titolo_en': forms.TextInput(attrs={'placeholder': 'Titolo in inglese'}),
            'contenuto_it': forms.Textarea(attrs={'placeholder': 'Contenuto in italiano'}),
            'contenuto_en': forms.Textarea(attrs={'placeholder': 'Contenuto in inglese'}),
        }