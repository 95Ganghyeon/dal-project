from django.shortcuts import render
from product.models import *
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import F, Func, Value, Avg

# Create your views here.
def ProductDetail(request):
    product = Product.objects.get(id=1)
    review = Review.objects.get()
    # review = Review.objects.select_related('user_id').get(id=1)
    context={
        'product': product,
        # 'review': review,
    }
    return render(request, 'product_detail.html', context=context)

def search_list(request):
    products = Product.objects.all()

    if 'q' in request.GET:
        query = request.GET.get('q')
        query = query.replace(" ", "")
        products = products.annotate(rename=Func(F('name'), Value(' '), Value(''), function='REPLACE')).filter(rename__icontains=query)
        
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products': products,
        'page_obj': page_obj,
    }
    return render(request, 'search_list.html', context=context)

    
    
def KeywordSearch(request):
    
    products = Review.objects.values_list('product_id__image','product_id__hashtag','product_id__name','product_id__category','star').annotate(avgStar=Avg('star')).order_by('-avgStar')
    
    
    
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products': products,
        'page_obj': page_obj,
    }
    return render(request, 'keyword_search.html', context=context)


def compareSearch(request):
    products = None
    page_obj = None
    first_page = True
    products = Product.objects.select_related().all()
    for product in products:
        print(product.name)
    if 'q' in request.GET:
        first_page = False
        query = request.GET.get('q')
        # my_product = Product.objects.get(name=query)
        # products = Product.objects.filter(price__lt=my_product.price)
        
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
    context = {
        'products': products,
        'page_obj': page_obj,
        'first_page': first_page,
    }
    return render(request, 'compare_search.html', context=context)








# class SearchList(generic.ListView):
#     model = Product
#     template_name = 'search_list.html'
#     paginate_by = 6
#     context_object_name = 'products'
    
#     def get_queryset(self):
#         try:
#             search = self.request.GET.get('q')
#         except KeyError:
#             search = None
    
#         if search:
#             product_list = Product.objects.filter(name__icontains=search)
#         else:
#             product_list = Product.objects.all()
#         return product_list





 
    # joined_ProductReview = Review.objects.select_related('product_id')
    # products = Product.objects.values_list('id', 'image', 'hashtag', 'name', 'category', Avg('review__star'))
    # products = Review.objects.values_list('product_id__id', 'product_id__category', 'star').annotate(avgStar=Avg('star')).order_by('-avgStar')
    # products = joined_ProductReview.values('product_id').annotate(avgStar=Avg('star')).order_by('-avgStar')
    
    # if request.GET.get('keyword') == 'general':
    #     products = Review.objects.values('product_id').annotate(avgStar=Avg('star')).order_by('-avgStar')
    #     # products = joined_ProductReview.values('product_id').annotate(avgStar=Avg('star')).order_by('-avgStar')
    # elif request.GET.get('keyword') == 'absorbency':
    #     products = Review.objects.values('product_id').annotate(avgAbsorbency=Avg('absorbency')).order_by('-absorbency')
    #     # products = joined_ProductReview.values('product_id').annotate(avgAbsorbency=Avg('absorbency')).order_by('-absorbency')
    # elif request.GET.get('keyword') == 'anti_odour':
    #     products = Review.objects.values('product_id').annotate(avgAnti_odour=Avg('anti_odour')).order_by('-anti_odour')    
    #     # products = joined_ProductReview.values('product_id').annotate(avgAnti_odour=Avg('anti_odour')).order_by('-anti_odour')    
    # elif request.GET.get('keyword') == 'comfort':
    #     products = Review.objects.values('product_id').annotate(avgComfort=Avg('comfort')).order_by('-comfort')
    #     # products = joined_ProductReview.values('product_id').annotate(avgComfort=Avg('comfort')).order_by('-comfort')
    # elif request.GET.get('keyword') == 'sensitivity':
    #     products = Review.objects.values('product_id').annotate(avgSensitivity=Avg('sensitivity')).order_by('-sensitivity')
    #     # products = joined_ProductReview.values('product_id').annotate(avgSensitivity=Avg('sensitivity')).order_by('-sensitivity')

    # products = Review.objects.all()