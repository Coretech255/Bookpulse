from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from django.shortcuts import render

# Create your views here.

def IndexView(request):
    pass
    return render(request,'shop/index.html')


# ListView - Display a list of objects
class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

# DetailView - Display details of a single object
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['related_products'] = Product.objects.exclude(id=self.object.id)[:5]  # Exclude the current product and select some other products
        return context


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

