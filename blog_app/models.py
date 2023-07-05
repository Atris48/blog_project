from django.db import models
from account_app.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=505)
    title_site = models.CharField(max_length=80)
    site_meta = models.CharField(max_length=500)
    short_description = models.TextField()
    description = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='image')
    published = models.BooleanField(default=False)
    view = models.IntegerField(default=0)
    slug = models.SlugField()

    def __str__(self):
        return self.title
