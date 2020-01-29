from django.shortcuts import render
from product.models import *
<<<<<<< HEAD
from user import models
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import F, Func, Value, Avg
from datetime import datetime
=======
from django.core.paginator import Paginator
from django.db.models import F, Func, Value, Avg, Q
>>>>>>> 0862f76261cb56993587e2162bd7d1c0c7e40e09

# Create your views here.


class ProductDetail(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context["now"] = Profile.birth_date
        return context


def search_list(request):
    products = Product.objects.all()

    if "q" in request.GET:
        query = request.GET.get("q")
        query = query.replace(" ", "")
        products = products.annotate(
            rename=Func(F("name"), Value(" "), Value(""), function="REPLACE")
        ).filter(rename__icontains=query)

    paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "products": products,
        "page_obj": page_obj,
    }
<<<<<<< HEAD
    return render(request, "search_list.html", context=context)


=======
    return render(request, 'search_list.html', context=context)
    
>>>>>>> 0862f76261cb56993587e2162bd7d1c0c7e40e09
def KeywordSearch(request):
    def makeListOrderbyKeyword(keyword):
        products = []
        temp = (
            Review.objects.values("product_id__id")
            .annotate(avgOrder=Avg(keyword))
            .order_by("-avgOrder")
        )
        for i in temp:
            products += Product.objects.filter(id=i["product_id__id"])
            print(i)
        paginator = Paginator(products, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "products": products,
            "page_obj": page_obj,
        }
        return render(request, "keyword_search.html", context=context)

    if request.GET.get("keyword") == "star":
        return makeListOrderbyKeyword("star")
    elif request.GET.get("keyword") == "absorbency":
        return makeListOrderbyKeyword("absorbency")
    elif request.GET.get("keyword") == "anti_odour":
        return makeListOrderbyKeyword("anti_odour")
    elif request.GET.get("keyword") == "comfort":
        return makeListOrderbyKeyword("comfort")
    elif request.GET.get("keyword") == "sensitivity":
        return makeListOrderbyKeyword("sensitivity")
    else:
<<<<<<< HEAD
        return makeListOrderbyKeyword("star")


=======
        return makeListOrderbyKeyword('star')
        
>>>>>>> 0862f76261cb56993587e2162bd7d1c0c7e40e09
def compareSearch(request):
    temp = None
    products = None
    page_obj = None
    first_page = True

<<<<<<< HEAD
    products1 = (
        Review.objects.values("product_id")
        .annotate(absorbency_avg=Avg("absorbency"))
        .values("product_id__name", "absorbency_avg")
        .filter(absorbency_avg__gt=3)
    )
    products2 = (
        Review.objects.values("product_id")
        .annotate(absorbency_avg=Avg("absorbency"))
        .filter(absorbency_avg__gt=3)
        .values("product_id", "product_id__name")
    )
    products3 = (
        Review.objects.annotate(absorbency_avg=Avg("absorbency"))
        .values("product_id__name", "absorbency_avg")
        .filter(absorbency_avg__gt=3)
    )

    context = {
        "products1": products1,
        "products2": products2,
        "products3": products3,
    }
    return render(request, "compare_search.html", context=context)


# def compareSearch(request):

#     if request.method == 'GET':

#         compareProduct = Product.objects.get(name = request.GET.get('q')) # 검색어
#         compareCondition = request.GET.getlist('compareCondition') # 검색조건

#         print(type(Review.objects.filter(product_id__id = compareProduct.id).aggregate(Avg('absorbency'))))

#         fieldAvgDictionary = {} # 비교하려는 제품 1개에 대한 값들
#         for condition in compareCondition:
#             if condition == 'price':
#                 fieldAvgDictionary['price'] = compareProduct.price
#             elif condition == 'nature_friendly':
#                 fieldAvgDictionary['nature_friendly'] = compareProduct.nature_friendly
#             else:
#                 Review.objects.filter(product_id__id = compareProduct.id).aggregate(Avg(condition))

#         print(fieldAvgDictionary)

#         products = Product.objects.all()
#         for condition, avgValue in fieldAvgDictionary.items():
#             if condition == 'price':
#                 products.filter(price__lt = avgValue)
#             elif condition == 'absorbency':
#                 temp = Review.objects

#         paginator = Paginator(products, 3)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         context = {
#             'products': products,
#             'page_obj': page_obj,
#         }
#         return render(request, 'compare_search.html', context=context)

#     else:
#         return render(request, 'compare_search.html', {})
=======
    if 'q' in request.GET:
        first_page = False
        # products는 Review objects를 product로 group by 한 후 평균 리뷰를 매칭
        products = Review.objects.values('product_id', 'product_id__category', \
        'product_id__image', 'product_id__hashtag__name', 'product_id__name', 'product_id__price', \
        'product_id__nature_friendly').annotate(Avg('absorbency'), Avg('anti_odour'), Avg('comfort'), \
        Avg('sensitivity'))

        query = request.GET.get('q')
        if query in products.values_list('product_id__name', flat=True):
            my_product = products.get(product_id__name=query)
        else:
            return render(request, 'compare_search.html', {'first_page':first_page})
        
        if 'low-priced' in request.GET: 
            products = products.filter(product_id__price__lt=my_product['product_id__price'])
        if 'nature-friendly' in request.GET:
            products = products.filter(product_id__nature_friendly__gt=my_product['product_id__nature_friendly'])
        if 'absorbent' in request.GET:
            products = products.filter(absorbency__gt=my_product['absorbency__avg'])
        if 'comfort' in request.GET:
            products = products.filter(comfort__gt=my_product['comfort__avg'])
        if 'anti-odour' in request.GET:
            products = products.filter(anti_odour__gt=my_product['anti_odour__avg'])
        if 'less-trouble' in request.GET:
            products = products.filter(sensitivity__gt=my_product['sensitivity__avg'])

        str_id = []
        for i in products:
            str_id += str(i['product_id'])
        temp = Product.objects.filter(id__in=str_id)

        paginator = Paginator(temp, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'products': temp,
        'page_obj': page_obj,
        'first_page': first_page,
    }

    return render(request, 'compare_search.html', context=context)


>>>>>>> 0862f76261cb56993587e2162bd7d1c0c7e40e09

