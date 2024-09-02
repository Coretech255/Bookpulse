import logging
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, Rating, Interaction
from .resources import RatingResource

logger = logging.getLogger(__name__)

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
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
     list_display = ('name', 'description',)
admin.site.register(Category, CategoryAdmin)

class RatingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = RatingResource
    list_display = ('get_user_full_name', 'get_product_isbn', 'rating', 'timestamp')
    list_filter = ('timestamp',)

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_user_full_name.short_description = 'User'

    def get_product_isbn(self, obj):
        return obj.product.isbn
    get_product_isbn.short_description = 'Product ISBN'
    #list_display = ('user', 'product', 'rating', 'timestamp')
    #list_filter = ('timestamp',)

    def before_import_row(self, row, **kwargs):
        logger.info(f"Processing row with Product ISBN: {row['product_isbn']}")
        if not Product.objects.filter(isbn=row['product_isbn']).exists():
            logger.error(f"Product with ISBN {row['product_isbn']} does not exist.")

admin.site.register(Rating, RatingAdmin)

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'liked', 'clicks',  'added_to_cart', 'timestamp')
    list_filter = ('timestamp',)

admin.site.register(Interaction, InteractionAdmin)
