from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from cart.forms import CartAddProductForm
from .forms import RatingForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Product, Interaction, Rating
from cart.cart import Cart
from django.shortcuts import render

# Create your views here.

def IndexView(request):
    cart = Cart(request)
    #print(cart)
    return render(request,'shop/index.html', {'cart': cart})


# ListView - Display a list of objects
class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Fetch the first 5 products (you can adjust the number as needed)
        return Product.objects.all()[:25]


# DetailView - Display details of a single object
class ProductDetailView(DetailView):
    model = Product
    cart_product_form = CartAddProductForm()
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        isbn = self.kwargs.get("isbn")
        return Product.objects.get(isbn=isbn)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add additional context data here
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        context['related_products'] = Product.objects.exclude(id=self.object.id)[:5]  # Exclude the current product and select some other products
        context['rating_form'] = RatingForm()
        context['ratings'] = Rating.objects.filter(product=self.object)
        return context


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = RatingForm(request.POST)
            product = self.get_object()
            if form.is_valid():
                rating = form.save(commit=False)
                rating.user = request.user
                rating.product = product
                rating.save()
                messages.success(request, "Your review has been submitted.")
            else:
                messages.error(request, "There was an error with your review.")
            return redirect('shop:product_detail', pk=product.pk)
        else:
            messages.error(request, "You need to be logged in to leave a review.")
            return redirect('user:login')

#Get Interaction
def register_interaction(request, isbn):
    product = get_object_or_404(Product, isbn=isbn)
    user = request.user

    interaction, created = Interaction.objects.get_or_create(user=user, product=product)
    rating_value = 0.0
    if 'like' in request.POST:
        interaction.liked = True
        rating_value = interaction.calculate_interaction_value()
    elif 'add_to_cart'in request.POST:
        interaction.added_to_cart = True
        rating_value = interaction.calculate_interaction_value()
    elif 'click' in request.POST:
        interaction.clicks += 1
        if 'time_spent' in request.POST:
            interaction.time_spent += float(request.POST['time_spent'])
            rating_value = interaction.calculate_interaction_value()

    interaction.save()

    # Update or create the rating
    rating, created = Rating.objects.get_or_create(user=user, product=product)
    rating.update_rating(rating_value)

    return JsonResponse({
        'status': 'success',
        'rating':rating.rating
    })
    
            


# UpdateView - Update an existing object
#class YourModelUpdateView(UpdateView):
#    model = YourModel
#    template_name = 'yourapp/yourmodel_form.html'
#    fields = '__all__'

# DeleteView - Delete an existing object
#class YourModelDeleteView(DeleteView):
#    model = YourModel
#    template_name = 'yourapp/yourmodel_confirm_delete.html'
#    success_url = reverse_lazy('yourmodel-list')  # Redirect to the list view after deletion

