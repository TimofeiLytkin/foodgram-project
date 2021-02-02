from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import RECIPES_ON_PAGE
from users.models import User

from recipes.forms import RecipeForm
from recipes.models import Recipe
from recipes.utils import filter_tag, get_tag, save_recipe


def index(request):
    recipe_list, tags = filter_tag(request)
    paginator = Paginator(recipe_list, RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'indexAuth.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
        },
    )


@login_required
def create_recipe(request):
    tags = []
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        response_code = save_recipe(request, form)
        if response_code == 400:
            return redirect('page_bad_request')
        return redirect('recipes')
    return render(request, 'formRecipe.html', {'form': form, 'tags': tags})


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'singlePage.html', {'recipe': recipe})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipe_list, tags = filter_tag(request)
    recipe_list = recipe_list.filter(author=author)
    paginator = Paginator(recipe_list, RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'authorRecipe.html',
        {
            'page': page,
            'paginator': paginator,
            'username': username,
            'tags': tags,
        },
    )


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_view', recipe_id=recipe_id)
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )
    if form.is_valid():
        recipe.ingredients.remove()
        recipe.quantity.all().delete()
        recipe.tags.all().delete()
        response_code = save_recipe(request, form)
        if response_code == 400:
            return redirect('page_bad_request')
        return redirect('recipe_view', recipe_id=recipe_id)
    tags_saved = recipe.tags.values_list('title', flat=True)
    form = RecipeForm(instance=recipe)
    form.fields['tag'].initial = list(tags_saved)
    tags = get_tag(tags_saved)
    return render(
        request,
        'formChangeRecipe.html',
        {'form': form, 'recipe': recipe, 'tags': tags},
    )


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', username=request.user.username)
    return redirect('recipes')


@login_required
def favorites(request):
    recipe_list, tags = filter_tag(request)
    recipe_list = recipe_list.filter(in_favorite__user=request.user)
    paginator = Paginator(recipe_list, RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorite.html',
        {'page': page, 'paginator': paginator, 'tags': tags},
    )


@login_required
def shopping_list(request):
    recipe_list, tags = filter_tag(request)
    recipe_list = recipe_list.filter(in_purchases__user=request.user)
    return render(
        request, 'shopList.html', {'recipe_list': recipe_list, 'tags': tags}
    )


@login_required
def subscriptions(request):
    authors = User.objects.filter(following__user=request.user)
    paginator = Paginator(authors, RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'myFollow.html', {'page': page, 'paginator': paginator}
    )


def get_ingredients(request):
    list = (
        Recipe.objects.filter(in_purchases__user=request.user)
        .order_by('ingredient__title')
        .values('ingredient__title', 'ingredient__dimension')
        .annotate(amount=Sum('quantity__amount'))
    )

    for ingredient in list:
        text = (
            f"{ingredient['ingredient__title'].capitalize()} "
            f"({ingredient['ingredient__dimension']}) \u2014 "
            f"{ingredient['amount']} \n"
        )

    filename = 'ingredients.txt'
    response = HttpResponse(text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
