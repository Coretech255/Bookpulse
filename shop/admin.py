from django.contrib import admin
from .models import Product, Category, Rating

class ProductAdmin(admin.ModelAdmin):
    # Customize how the user model is displayed on the admin dashboard
    list_display = ('title', 'authors', 'isbn', 'price', 'publication_date')
    search_fields = ('title', 'authors', 'isbn', 'publication_date')
    filter_horizontal = ()
    list_filter = ('publication_date',)
    fieldsets = ()
    ordering = ('title',)  # Specify a valid field for ordering, such as 'email'

# Register the Product model with the custom admin class
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Category, CategoryAdmin)
# Add a verbose name for the Category model
Category._meta.verbose_name = "Book Category"
Category._meta.verbose_name_plural = "Book Categories"

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'timestamp')
    list_filter = ('timestamp',)

admin.site.register(Rating, RatingAdmin)
