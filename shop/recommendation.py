import pandas as pd
from .models import Rating

def fetch_dataset():
    ratings = Rating.objects.all()
    rating_data = [
        (rating.user_id, rating.product.isbn, rating.rating) 
        for rating in ratings]
    
    return rating_data

