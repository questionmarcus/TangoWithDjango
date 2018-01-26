from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField(unique = True)

    def save(self, *args, ** kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # This is required as is links the profile to the main USER model in django
    user = models.OneToOneField(User)

    # Additional attributes here:
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __str__ method to output only the user name (cos thats all we need)
    def __str__(self):
        return self.user.username
