from django.shortcuts import render
from product.models import *
from django.views import generic


# Create your views here.

def product_details(request):
    product = Product.objects.get(id=1)
    review = Review.objects.get(id=1)
    # review = Review.objects.select_related('user_id').get(id=1)
    context={
        'product': product,
        'review': review,
    }
    return render(request, 'product_detail.html', context=context)
    
# class product_details(generic.DetailView):
#     model = Product
#     template_name = 'product_details.html'
    
    


class search_list(generic.ListView):
    model = Product
    template_name = 'search_list.html'
    paginate_by = 6
    
    def get_queryset(self):
        return Product.objects.filter(name = 'Test')
    
    # def get_context_data()
    
    




