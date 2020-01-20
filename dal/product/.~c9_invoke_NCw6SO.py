from django.shortcuts import render
from product.models import *


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
    
def product_list(request):
    
    products = Product.object.all()
    return render(request, 'product_list.html', {'products':products})
    




