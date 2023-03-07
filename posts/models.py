from django.db import models

class Category(models.Model):
    parentId = models.IntegerField()
    name = models.CharField(max_length=255)

class Post(models.Model):
    categoryId = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField()
    thumbnail_image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

