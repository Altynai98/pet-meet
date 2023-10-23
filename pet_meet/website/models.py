from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        ordering = ('created_at',)

    username = None
    email = models.EmailField(null=False, unique=True)  # we dont want to have 2 users with the same email (unique=True)
    # password = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=60, null=False)
    address_street = models.CharField(max_length=100, null=True)
    address_city = models.CharField(max_length=100, null=True)
    address_country = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(null=True)
    bio = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)  # when a record will be created, current time will be assigned
    updated_at = models.DateTimeField(auto_now=True, null=True)  # when a record is updated, current time will be assigned

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
  

class Group(models.Model):
    class Meta:
        ordering = ('created_at',)

    name = models.CharField(max_length=80, null=False)
    city = models.CharField(max_length=80, null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    creator = models.ForeignKey(User, related_name='created_groups', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    class Meta:
        ordering = ('created_at',)

    title = models.CharField(max_length=80, null=False)
    location = models.CharField(max_length=100, null=False)
    time = models.DateTimeField(null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    group = models.ForeignKey(Group, related_name='meetings', on_delete=models.CASCADE, null=False)
    creator = models.ForeignKey(User, related_name='created_meetings', on_delete=models.CASCADE, null=False)
    attendees = models.ManyToManyField(User, related_name='attending_meetings')

    def __str__(self):
        return f'{self.title} {self.location} {self.time}'


class Post(models.Model):
    class Meta:
        ordering = ('created_at',)

    title = models.CharField(max_length=80, null=False)
    text = models.TextField(null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, null=False)
    group = models.ForeignKey(Group, related_name='posts', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'"{self.title}" - {self.user}'


class Comment(models.Model):
    class Meta:
        ordering = ('created_at',)

    text = models.TextField(null=False)
    rating = models.CharField(
        max_length=1,
        choices=(
            ('1', '1'), 
            ('2', '2'), 
            ('3', '3'), 
            ('4', '4'), 
            ('5', '5')
        ),
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text
    

class Animal(models.Model):
    class Meta:
        ordering = ('created_at',)

    name = models.CharField(max_length=50, null=False)
    breed = models.CharField(max_length=80, null=True)
    type = models.CharField(
        max_length=3,
        choices=(
            ('dog', 'dog'),
            ('cat', 'cat')
        ),
        null=False
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    user = models.ForeignKey(User, related_name='animals', on_delete=models.CASCADE, null=False)



