from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Rating, Product, CustomUser

class RatingResource(resources.ModelResource):
    # Define the field for ForeignKey to Product
    product = fields.Field(
        column_name='isbn',  # CSV column name for the foreign key to Product
        attribute='product',  # Model attribute
        widget=ForeignKeyWidget(Product, 'isbn')  # Use ForeignKeyWidget with 'isbn' field
    )
    
    # Define the field for ForeignKey to CustomUser
    user = fields.Field(
        column_name='user_id',  # CSV column name for the foreign key to CustomUser
        attribute='user',  # Model attribute
        widget=ForeignKeyWidget(CustomUser, 'id')  # Use ForeignKeyWidget with 'email' field
    )

    class Meta:
        model = Rating
        fields = ('id', 'user', 'product', 'rating', 'review', 'timestamp')
        export_order = ('id', 'user', 'product', 'rating', 'review', 'timestamp')
