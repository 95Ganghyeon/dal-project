from django.db import models
from django.urls import reverse
from user.models import Profile, User

# from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)  # 등록된 시간
    updated = models.DateTimeField(auto_now=True)  # 업데이트된 시간

    class Meta:
        abstract = True


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    content = RichTextUploadingField()


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True)
    best_review_fk = models.OneToOneField(
        "Review", on_delete=models.SET_NULL, null=True, blank=True
    )
    size = models.PositiveIntegerField()
    category = models.CharField(
        max_length=30
    )  # 같은 회사의 생리대라고 하더라도 [팬티라인, 소, 중, 대, ...]의 카테고리가 있음
    one_line = models.CharField(max_length=100)
    brand_fk = models.ForeignKey("Brand", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    hashtag_fk = models.ManyToManyField("Hashtag")
    price = models.PositiveIntegerField()
    price_per_piece = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def search_string(self):
        return self.name.replace(" ", "")

    def get_absolute_url(self):
        return reverse("product:ProductDetail", args=[str(self.id)])

    def get_price_per_piece(self):
        return self.price // self.count

    def save(self, *args, **kwargs):
        self.price_per_piece = self.get_price_per_piece()
        super(Product, self).save(*args, **kwargs)


class ProductIngredient(models.Model):
    """
    점수 반영 비율: 표지층(cover_layer) 30% // 흡수층(absorbent_layer) 60% // 기타(etc) 10%
    """

    RANGE_ONE_TO_FIVE = (
        (0, "0점"),
        (10, "10점"),
        (20, "20점"),
        (30, "30점"),
        (40, "40점"),
    )

    product_fk = models.OneToOneField("Product", on_delete=models.CASCADE)
    cover_layer_string = models.TextField(null=True)
    cover_layer_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(40)],
        choices=RANGE_ONE_TO_FIVE,
        default=None,
    )
    absorbent_layer_string = models.TextField(null=True)
    absorbent_layer_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(40)],
        choices=RANGE_ONE_TO_FIVE,
        default=None,
    )
    etc_string = models.TextField(null=True)
    etc_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(40)],
        choices=RANGE_ONE_TO_FIVE,
        default=None,
    )

    nature_friendly_score = models.FloatField(editable=False)

    def get_nature_friendly_score(self):
        if "팬티라이너" in self.product_fk.category:
            return (
                (self.cover_layer_score / 40) * 45
                + (self.absorbent_layer_score / 40) * 45
                + (self.etc_score / 40) * 10
            )
        else:
            return (
                (self.cover_layer_score / 40) * 30
                + (self.absorbent_layer_score / 40) * 60
                + (self.etc_score / 40) * 10
            )

    def save(self, *args, **kwargs):
        self.nature_friendly_score = self.get_nature_friendly_score()
        super(ProductIngredient, self).save(*args, **kwargs)


class Review(TimeStampedModel):

    # form.py 에서 1~5까지 radio 선택지를 주기 위해서 필요함
    RANGE_ONE_TO_FIVE = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    id = models.AutoField(primary_key=True)
    image = models.ImageField(blank=True)
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    product_fk = models.ForeignKey("Product", on_delete=models.CASCADE)
    content = models.TextField()  # 설명란
    m_type = models.CharField(max_length=4)  # 유저의 mtype
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None,
    )  # 종합평점
    absorbency = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None,
    )  # 흡수력
    anti_odour = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None,
    )  # 탈취성
    sensitivity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None,
    )  # 피부친화도
    comfort = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None,
    )  # 촉감/착용감

    def __str__(self):
        return self.user_fk.username + "의 리뷰"

    def score_str(self):
        if self.score == 1:
            return "최악"
        elif self.score == 2:
            return "별로"
        elif self.score == 3:
            return "나름"
        elif self.score == 4:
            return "오오"
        elif self.score == 5:
            return "대박"

    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"pk": self.id})


class Hashtag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
