from decimal import Decimal
from django.db import IntegrityError

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag


def filter_tag(request):
    tags = request.GET.get('tags', 'bld')
    recipe_list = Recipe.objects.filter(tags__slug__in=tags).distinct()
    return recipe_list, tags


def get_tag(tags):
    tag_dict = {
        'Завтрак': 'breakfast',
        'Обед': 'lunch',
        'Ужин': 'dinner',
    }
    return [tag_dict[item] for item in tags]


def save_recipe(request, form):
    try:
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        tags = form.cleaned_data['tag']
        for tag in tags:
            Tag.objects.create(recipe=recipe, title=tag)

        objs = []

        for key, value in form.data.items():
            print(key, value)
            if 'nameIngredient' in key:
                title = value
            elif 'valueIngredient' in key:
                amount = Decimal(value.replace(',', '.'))
            elif 'unitsIngredient' in key:
                dimension = value
                ing = Ingredient.objects.get(
                    title=title, dimension=dimension
                )
                objs.append(
                    IngredientAmount(
                        ingredient=ing, recipe=recipe, amount=amount
                    )
                )
        IngredientAmount.objects.bulk_create(objs)
        return None
    except IntegrityError:
        return 400
