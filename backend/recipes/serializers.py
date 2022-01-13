from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Favorite, ShoppingCart, Recipe, \
    CountOfIngredient
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = CountOfIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time',
        )

    def get_ingredients(self, obj):
        queryset = CountOfIngredient.objects.filter(recipe=obj)
        return RecipeIngredientReadSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = CountOfIngredient
        fields = ('id', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = RecipeIngredientWriteSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            CountOfIngredient.objects.create(
                recipe=recipe, ingredient=ingredient['id'],
                amount=ingredient['amount'])

    def create_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.tags.clear()
        tags = validated_data.get('tags')
        self.create_tags(tags, instance)
        CountOfIngredient.objects.filter(recipe=instance).all().delete()
        ingredients = validated_data.get('ingredients')
        self.create_ingredients(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(
            instance, context=context).data


class RepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipes')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RepresentationSerializer(
            instance.recipe, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RepresentationSerializer(
            instance.recipe, context=context).data
