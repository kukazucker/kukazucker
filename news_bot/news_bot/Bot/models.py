from pyexpat import model
from tabnanny import verbose
from django.db import models

class Profile( models.Model ):
    user_id = models.PositiveIntegerField( 
        verbose_name= 'User ID',
        unique=True
    )

    first_name = models.CharField( 
        verbose_name= 'First Name',
        max_length = 50
    )

    last_name = models.CharField( 
        verbose_name= 'Last Name',
        null=True,
        blank=True,
        max_length = 50
    )

    username = models.CharField( 
        verbose_name= 'Username',
        null=True,
        blank=True,
        max_length = 50
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class News( models.Model ):
    profile = models.ForeignKey(
        to='Bot.Profile',
        verbose_name='Profile',
        on_delete=models.PROTECT
    )

    channel = models.CharField(
        verbose_name= 'Channel',
        max_length=200
    )

    news_text = models.TextField(
        verbose_name= 'News Text',
        max_length=2000
    )

    news_file = models.FileField(
        blank=True,
        null=True,
        upload_to="files/%Y/%m/%d"
    )

    created_at = models.DateTimeField(
        verbose_name= 'Created at',
    )

    def __str__(self):
        return f'#{self.pk} {self.profile}'

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'




