from django.test import TestCase, Client
from django.urls import reverse
#from django.contrib.auth.models import User
from user.models import CustomUser
from shop.models import Product, Rating, Interaction
from shop.views import ProductListView, ProductDetailView, register_interaction, recommend_books_view
from django.http import JsonResponse
import pandas as pd
from surprise import SVDpp, Dataset, Reader
import json

# Test whether the index view renders successfully
class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('shop:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')
        self.assertIn('cart', response.context)

class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(title="Test Product", author="Author", 
                                              isbn="1234567890", price="10.00", publication_date="1999")

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')
        self.assertIn('products', response.context)

    def test_product_search_list_view(self):
        response = self.client.get(reverse('shop:product_search_list') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/search_results.html')
        self.assertIn('products', response.context)
        self.assertQuerysetEqual(response.context['products'], [self.product])

class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')
        self.product = Product.objects.create(title="Test Product", author="Author", 
                                              isbn="1234567890", price="10.00", publication_date="1999")

    def test_product_detail_view(self):
        self.client.login(email='testuser@example.com', password='12345')
        response = self.client.get(reverse('shop:product_detail', kwargs={'isbn': self.product.isbn}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        self.assertIn('product', response.context)
        self.assertIn('recommended_books', response.context)

class RegisterInteractionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')
        self.product = Product.objects.create(title="Test Product", author="Author", 
                                              isbn="1234567890", price="10.00", publication_date="1999")
        self.client.login(email='testuser@example.com', password='12345')

    def test_register_interaction_like(self):
        response = self.client.post(reverse('shop:register_interaction', kwargs={'isbn': self.product.isbn}),
                                    {'like': 'true'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')

        interaction = Interaction.objects.get(user=self.user, product=self.product)
        self.assertTrue(interaction.liked)

class RecommendBooksViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')
        self.product = Product.objects.create(title="Test Product", author="Author", 
                                              isbn="1234567890", price="10.00", publication_date="1999")
        Rating.objects.create(user=self.user, product=self.product, rating=5)

    def test_recommend_books_view(self):
        self.client.login(email='testuser@example.com', password='12345')
        response = self.client.get(reverse('shop:recommend_books', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/recommendations.html')
        self.assertIn('recommended_books', response.context)

class RecommendationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')
        self.product1 = Product.objects.create(title="Test Product 1", author="Author", 
                                               isbn="1234567890", price="10.00", publication_date="1999")
        self.product2 = Product.objects.create(title="Test Product 2", author="Author", 
                                               isbn="0987654321", price="10.00", publication_date="1999")
        Rating.objects.create(user=self.user, product=self.product1, rating=5)

    def test_get_top_n_recommendations(self):
        ratings = Rating.objects.all().values('user_id', 'product_id', 'rating')
        df = pd.DataFrame(list(ratings))

        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['user_id', 'product_id', 'rating']], reader)
        
        algo = SVDpp()
        trainset = data.build_full_trainset()
        algo.fit(trainset)
        
        view = ProductDetailView()
        top_n_books = view.get_top_n_recommendations(algo, self.user.id, df)
        self.assertIn(self.product2.id, top_n_books)

class ProductDetailPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')
        self.product = Product.objects.create(title="Test Product", author="Author", 
                                              isbn="1234567890", price="10.00", publication_date="1999")
        self.client.login(email='testuser@example.com', password='12345')

    def test_post_review(self):
        response = self.client.post(reverse('shop:product_detail', kwargs={'isbn': self.product.isbn}),
                                    {'rating': 5, 'review': 'Great product!'})
        self.assertRedirects(response, reverse('shop:product_detail', kwargs={'isbn': self.product.isbn}))
        rating = Rating.objects.get(user=self.user, product=self.product)
        self.assertEqual(rating.rating, 5)

class LoadDataTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')
        self.product = Product.objects.create(title="Test Product", author="Author", 
                                              isbn="1234567890", price="10.00", publication_date="1999")
        Rating.objects.create(user=self.user, product=self.product, rating=5)

    def test_load_data(self):
        view = ProductDetailView()
        data, df = view.load_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

