from django import forms

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    """Класс форма для создания новых рецептов."""
    TAG_CHOICES = (
        ('Завтрак', 'orange'),
        ('Обед', 'green'),
        ('Ужин', 'purple'),
    )

    title = forms.CharField(max_length=256)
    tag = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=TAG_CHOICES,
    )
    print(tag)
    duration = forms.IntegerField(min_value=1)
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form__textarea'})
    )
    image = forms.ImageField()

    class Meta:
        model = Recipe
        fields = ('title', 'tag', 'duration', 'text', 'image')
