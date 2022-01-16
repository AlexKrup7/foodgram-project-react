from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from backend.pagination import LimitPageNumberPagination
from backend.permissions import IsAuthorOrAdminOrReadOnly

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (CountOfIngredient, Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)


class IngredientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeSerializer

    @staticmethod
    def post_method_for_action(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_action(request=request, pk=pk,
                                           serializers=FavoriteSerializer)

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method_for_action(request=request, pk=pk,
                                           serializers=ShoppingCartSerializer)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_object = get_object_or_404(model, user=user, recipe=recipe)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = CountOfIngredient.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(total=Sum('amount'))
        shopping_list = 'список:\n'
        for number, ingredient in enumerate(ingredients, start=1):
            shopping_list += (
                f'{number} '
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["total"]} '
                f'{ingredient["ingredient__measurement_unit"]}\n')

        purchase_list = 'purchase_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (f'attachment;'
                                           f'filename={purchase_list}')
        return response
