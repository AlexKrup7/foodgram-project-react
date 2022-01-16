from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, ForeignKey, ImageField,
                              ManyToManyField, Model, PositiveIntegerField,
                              SlugField, TextField, UniqueConstraint)

User = get_user_model()

COOKING_TIME_MIN_ERROR = (
    'Время приготовления не может быть меньше одной минуты!'
)
INGREDIENT_MIN_AMOUNT_ERROR = (
    'Количество ингредиентов не может быть меньше {min_value}!'
)


class Tag(Model):
    name = CharField('Название', max_length=200, unique=True)
    color = CharField('Цвет в HEX', max_length=7, unique=True)
    slug = SlugField('Слаг', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Ingredient(Model):
    name = CharField('Название', max_length=200)
    measurement_unit = CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Recipe(Model):
    name = CharField('Название', max_length=200)
    text = TextField('Описание')
    ingredients = ManyToManyField(
        Ingredient,
        through='CountOfIngredient',
        verbose_name='Ингредиенты'
    )
    tags = ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    image = ImageField('Картинка', upload_to='recipes/')

    cooking_time = PositiveIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(
            1,
            message=COOKING_TIME_MIN_ERROR,
        ),)
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.name})'


class CountOfIngredient(Model):
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        verbose_name='Ингредиент',
    )
    amount = PositiveIntegerField(
        'Количество',
        validators=(MinValueValidator(
            1,
            message=INGREDIENT_MIN_AMOUNT_ERROR.format(
                min_value=1
            )
        ),)
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_ingredient_amount',
            ),
        )


class Favorite(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_recipe',
            ),
        )


class ShoppingCart(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        )
