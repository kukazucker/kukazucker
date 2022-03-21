from django.db import models

class User(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_day = models.DateField(auto_now_add=False)
    balance = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'User',
        verbose_name_plural = 'Users'


class Product(models.Model):
    id = models.BigAutoField(
        auto_created=True, 
        primary_key=True, 
        serialize=False, 
        verbose_name='ID'
    )
    name = models.CharField(max_length=1000, unique=True)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return f'Product: {self.name}'

    class Meta:
        verbose_name = 'Product',
        verbose_name_plural = 'Products'


class RefLink(models.Model):
    id = models.BigAutoField(
        auto_created=True, 
        primary_key=True, 
        serialize=False, 
        verbose_name='ID'
    )
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=2000)
    link = models.URLField(editable=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ref Link: {self.name}'

    class Meta:
        verbose_name = 'Ref Link',
        verbose_name_plural = 'Ref Links'

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)

    def __str__(self):
        return f'Title: {self.title}'

    class Meta:
        verbose_name = 'Announcement',
        verbose_name_plural = 'Announcements'


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    amount = models.IntegerField()
    products = models.CharField(max_length=1000)
    status = models.CharField(max_length=100, default="created")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment: {self.user}'

    class Meta:
        verbose_name = 'Payment',
        verbose_name_plural = 'Payments'
