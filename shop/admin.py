import logging
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, Rating, Author, Interaction

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


class RatingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'isbn', 'rating', 'timestamp')
    list_filter = ('timestamp',)

    def before_import_row(self, row, **kwargs):
        try:
            # Perform checks or transformations here
            if 'user' not in row or 'isbn' not in row:
                raise ValueError("Missing user or isbn in import data.")
        except Exception as e:
            logger.error(f"Error processing row {row}: {e}")

    def after_import_instance(self, instance, new, **kwargs):
        # Log the instance for debugging
        logger.debug(f"Processed instance: {instance}")

admin.site.register(Rating, RatingAdmin)

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'likes', 'clicks',  'add_to_cart', 'timestamp')
    list_filter = ('timestamp',)

admin.site.register(Interaction, InteractionAdmin)
