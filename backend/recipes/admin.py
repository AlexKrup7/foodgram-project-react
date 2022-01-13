from django.contrib.admin import ModelAdmin, register

from .models import CountOfIngredient, Favorite, Ingredient, Recipe, Tag


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color',)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    list_filter = ('name',)
    search_fields = ('name',)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'added_in_favorites')
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('added_in_favorites',)

    def added_in_favorites(self, obj):
        return obj.favorites.count()


@register(CountOfIngredient)
class CountOfIngredientAdmin(ModelAdmin):
    list_display = (
        'id', 'recipe', 'ingredient', 'amount'
    )


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
