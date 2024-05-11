from django.contrib import admin
from .models import Product, Category, Rating, Author

class ProductAdmin(admin.ModelAdmin):
    # Customize how the user model is displayed on the admin dashboard
    list_display = ('title', 'isbn', 'price', 'publication_date')
    search_fields = ('title', 'author', 'isbn', 'publication_date')
    filter_horizontal = ()
    list_filter = ('author', 'publication_date',)
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

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')

admin.site.register(Author, AuthorAdmin)
# Add a verbose name for the Author model
Author._meta.verbose_name = "Book Author"
Author._meta.verbose_name_plural = "Book Authors"

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'timestamp')
    list_filter = ('timestamp',)

admin.site.register(Rating, RatingAdmin)
