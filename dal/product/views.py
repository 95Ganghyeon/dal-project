from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import F, Func, Value, Avg, Q
from django.views import generic
from product.models import *

# Create your views here.


class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context["now"] = Profile.birth_date
        return context


def NormalSearch(request):
    product_list = Product.objects.all()
    query = request.GET.get('q')
    if query:
        query = query.replace(" ", "")
        product_list = product_list.annotate(rename=Func(F('name'), Value(' '), Value(''), function='REPLACE')).filter(rename__icontains=query)
        
    paginator = Paginator(product_list, 3)
    page = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    context = {
        'product_list': product_list,
        'page_obj': page_obj,        
    }
    return render(request, 'normal_search.html', context=context)


def KeywordSearch(request):
    def makeListOrderbyKeyword(keyword):
        """
        html radio에서 사용자가 체크한 항목에 맞는 기준으로 Product를 정렬하여, 그 데이터를 바탕으로 랜더링 해주는 함수임
        """
        product_list = []
        review_list = Review.objects.values('product_id__id').annotate(avgOrder = Avg(keyword)).order_by('-avgOrder')
        for review in review_list:
            product_list += Product.objects.filter(id=review['product_id__id'])            
        
        paginator = Paginator(product_list, 3)
        page = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context = {
            'product_list': product_list,
            'page_obj': page_obj,
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
        return makeListOrderbyKeyword('star')


def compareSearch(request):
    
    def updateReviewSummary():
        """
        이게 ReviewSummary 테이블을 UPDATE 하는 함수인데, 이걸 2-3일에 한번 하는 작업으로 바꿔야 함
        """
        entireTable = ReviewSummary.objects.all()
        for record in entireTable:
            productReviews = Review.objects.filter(product__id=record.product.id)
            if productReviews:
                record.absorbency_avg = Review.objects.filter(product__id=record.product.id).aggregate(avg=Avg('absorbency'))['avg']
                record.anti_odour_avg = Review.objects.filter(product__id=record.product.id).aggregate(avg=Avg('anti_odour'))['avg']
                record.comfort_avg = Review.objects.filter(product__id=record.product.id).aggregate(avg=Avg('comfort'))['avg']
                record.sensitivity_avg = Review.objects.filter(product__id=record.product.id).aggregate(avg=Avg('sensitivity'))['avg']
                record.save()
            else:
                pass # 리뷰가 아직 입력되지 않은 경우에는 None type을 aggregate해봐야  None type이 나옴. ReviewSummary의 필드값은 모두 Float type이어야 함.

    
    updateReviewSummary() # 우선 코드 동작을 보기 위해 임시로 넣어놓았음

    
    ReviewSummary_list = ReviewSummary.objects.all()

    query = request.GET.get('q')    
    if query:        
        criterionProduct = Product.objects.get(name__icontains=query)
        criterionReviewSummary = ReviewSummary.objects.get(product__id=criterionProduct.id)
    else:
        return render(request, 'compare_search.html') # 검색어가 없으면 그냥 초기화면 랜더링

    compareCondition = request.GET.getlist('compareCondition')
    for condition in compareCondition:
        if condition == 'price':
            ReviewSummary_list = ReviewSummary_list.filter(product__price__lt=criterionProduct.price)            
        if condition == 'nature_friendly':
            ReviewSummary_list = ReviewSummary_list.filter(product__nature_friendly__gt=criterionProduct.nature_friendly)
        if condition == 'absorbency':            
            ReviewSummary_list = ReviewSummary_list.filter(absorbency_avg__gt=criterionReviewSummary.absorbency_avg)            
        if condition == 'comfort':
            ReviewSummary_list = ReviewSummary_list.filter(comfort_avg__gt=criterionReviewSummary.comfort_avg)
        if condition == 'anti_odour':
            ReviewSummary_list = ReviewSummary_list.filter(anti_odour_avg__gt=criterionReviewSummary.anti_odour_avg)
        if condition == 'sensitivity':
            ReviewSummary_list = ReviewSummary_list.filter(sensitivity_avg__gt=criterionReviewSummary.sensitivity_avg)
    
    product_list = []
    for reviewsummary in ReviewSummary_list:
        product_list += Product.objects.filter(id=reviewsummary.product.id)
    
    print(product_list)
    
    paginator = Paginator(product_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'product_list': product_list,
        'page_obj': page_obj,
    }

    return render(request, "compare_search.html", context=context)

