from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from cart.forms import CartAddProductForm
from .forms import RatingForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Product, Rating
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

# DetailView - Display details of a single object
class ProductDetailView(DetailView):
    model = Product
    cart_product_form = CartAddProductForm()
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    
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

