from django.shortcuts import render
from product.models import *
from user import models
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import F, Func, Value, Avg
from datetime import datetime

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
    return render(request, "search_list.html", context=context)


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
        return makeListOrderbyKeyword("star")


def compareSearch(request):

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

