from django.db import models
from user.models import CustomUser



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    author_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author, related_name='authors')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=20)
    publication_date = models.IntegerField()
    cover_photo = models.ImageField()
    digital_book = models.FileField(upload_to='books/', null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    review = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.title} - {self.rating}"
