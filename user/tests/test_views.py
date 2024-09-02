from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from user.forms import CustomUserCreationForm, UpdateUserForm

UserModel = get_user_model()

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='testuser@example.com', password='Testpass123')
        self.client.login(email='testuser@example.com', password='Testpass123')

    def test_register_view_get(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_form.html')
    
    def test_register_view_post_valid(self):
        response = self.client.post(reverse('user:register'), {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'NewPass123',
            'password2': 'NewPass123',
        })

        # Check if the form is valid
        #form = response.context['form']
        #if form and form.errors:
        #    print("Form errors:", form.errors)

        self.assertRedirects(response, reverse('user:login'))
        self.assertEqual(UserModel.objects.count(), 2)
        self.assertTrue(UserModel.objects.filter(email='newuser@example.com').exists())
            # Check the success message
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Account created successfully. You can now log in.')
    
    def test_register_view_post_invalid_email(self):
        response = self.client.post(reverse('user:register'), {
            'email': 'testuser@example.com',
            'password1': 'NewPass123',
            'password2': 'NewPass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('registration_form'))
        self.assertEqual('Email is already in use.')
    

    
    def test_login_view_get(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_form.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('user:login'), {
            'email': 'testuser@example.com',
            'password': 'Testpass123',
        })
        self.assertRedirects(response, reverse('shop:index'))
    
    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('user:login'), {
            'email': 'testuser@example.com',
            'password': 'WrongPassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_form.html')
        self.assertContains(response, 'Invalid email or password')

    def test_profile_view_get(self):
        self.client.login(email='testuser@example.com', password='Testpass123')
        response = self.client.get(reverse('user:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_post_valid(self):
        self.client.login(email='testuser@example.com', password='Testpass123')
        response = self.client.post(reverse('user:profile'), {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'testuser@example.com',
        }, follow=True)
        
        # Print the redirected URL to debug
        print(response.redirect_chain)

        # Check the final response after following the redirect
        self.assertEqual(response.status_code, 200)

        #self.assertRedirects(response, reverse('user:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual('Your profile is updated successfully')

    def test_logout_view(self):
        response = self.client.get(reverse('user:logout'))
        self.assertRedirects(response, reverse('shop:index'))
        self.assertNotIn('_auth_user_id', self.client.session)
