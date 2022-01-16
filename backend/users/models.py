from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, CharField, EmailField, ForeignKey,
                              Model, UniqueConstraint)


class User(AbstractUser):
    email = EmailField('Почта', max_length=254, unique=True)
    username = CharField('Никнейм', max_length=150, unique=True, blank=True)
    first_name = CharField('Имя', max_length=150)
    last_name = CharField('Фамилия', max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    following = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            UniqueConstraint(
                fields=('user', 'following',),
                name='unique_subscribe',
            ),
        )
