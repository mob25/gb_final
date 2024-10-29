from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=CASCADE, related_name='follower',
        verbose_name='Пользователь')
    author = models.ForeignKey(
        User, on_delete=CASCADE, related_name='following',
        verbose_name='Автор')

    def __str__(self):
        return f"{self.user}, {self.author}"

    class Meta:
        ordering = ['-id']
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='unique_user_author')]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
