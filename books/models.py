from django.db import models
from django.contrib.auth.models import User
from django.core.validators import(
    MinValueValidator,
    MaxValueValidator
)  # for rating fields

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length = 250)
    author = models.CharField(max_length = 250)
    description = models.TextField(blank = True, null = True)
    published_date = models.DateField()

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f" {self.name} - {self.author} "

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = "comments")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)],
    )

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f" {self.rating}"