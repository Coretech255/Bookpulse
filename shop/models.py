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
    author = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=20, unique=True)
    publication_date = models.IntegerField()
    cover_photo_url = models.URLField(null=True, blank=True)
    digital_book = models.FileField(upload_to='books/', null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='products')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    

class Interaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    clicks = models.IntegerField(default=0)
    time_spent = models.FloatField(default=0.0)
    added_to_cart = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.title} - Interaction"
    
    def calculate_interaction_value(self):
        if self.liked:
            return 7.0
        elif self.added_to_cart:
            return 10.0
        else:
            return min(self.clicks * 3 + self.time_spent * 2 / 60, 5.0)



class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, to_field='isbn', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    review = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    #class Meta:
    #    unique_together = ('user', 'product', 'rating')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.product.title} - {self.rating}"

    def update_rating(self, rating_value):
        self.rating = min(round(rating_value, 1), 10.0)
        self.save()


    #@classmethod
    #def update_or_create_rating(cls, user, product):
        #rating, created = cls.objects.get_or_create(user=user, product=product)
        #rating.calculate_interaction_rating()
        #return rating

