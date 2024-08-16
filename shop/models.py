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
    likes = models.BooleanField(default=False)
    clicks = models.IntegerField(default=0)
    time_spent = models.FloatField(default=0.0)
    add_to_cart = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} - Interaction"



class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    isbn = models.ForeignKey(Product, to_field='isbn', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    review = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'isbn')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.isbn.title} - {self.rating}"

    def calculate_interaction_rating(self):
        interactions = Interaction.objects.filter(user=self.user, product=self.product)

        rating = 0
        if self.rating.exists():
            self.save()
        elif interactions.exists():
            for interaction in interactions:
                if interaction.likes:
                    rating += 4.0
                if interaction.clicks > 0:
                    rating += 3.0
                if interaction.time_spent > 0:
                    rating += interaction.time_spent / 60
                if interaction.review:
                    rating += 2.5
                if interaction.purchased:
                    rating += 5.0
                if interaction.add_to_cart:
                    rating += 4.5
            
            # Ensure the rating does not exceed 5.0
            self.rating = min(round(rating, 2), 5.0)
            self.save()

    @classmethod
    def update_or_create_rating(cls, user, product):
        rating, created = cls.objects.get_or_create(user=user, product=product)
        rating.calculate_interaction_rating()
        return rating

