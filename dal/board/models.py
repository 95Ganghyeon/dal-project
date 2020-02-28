from django.db import models
from user.models import User
from django.urls import reverse
from django.utils.translation import gettext as _
from ckeditor_uploader.fields import RichTextUploadingField

# 공지사항
class Notice(models.Model):
    CATEGORY = (
        ("notice", "공지사항"),
        ("event", "이벤트"),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(_("제목"), max_length=200)
    content = RichTextUploadingField(_("내용"))
    category = models.CharField(_("카테고리"), max_length=20, choices=CATEGORY)
    is_fixed = models.BooleanField(_("상단고정"))
    created_at = models.DateTimeField(_("작성일"), auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("notice-detail", kwargs={"pk": self.id})

    class Meta:
        verbose_name = _("공지 게시판")
        verbose_name_plural = _("공지 게시판")

# 사연 원본(admin에서만 볼 수 있음)
class User_story_origin(models.Model):
    SORT = (
        ("unread", "읽지않음"),
        ("read", "읽음"),
        ("editing", "제작중"),
        ("complete", "제작완료"),
        ("hold", "보류"),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='stories', on_delete=models.PROTECT)
    title = models.CharField(_("제목"), max_length=200)
    content = models.TextField(_("내용"))
    image1 = models.ImageField(_("이미지1"), upload_to='uploads/', null=True, blank=True)
    image2 = models.ImageField(_("이미지2"), upload_to='uploads/', null=True, blank=True)
    sort = models.CharField(_("분류"), max_length=20, choices=SORT, default=SORT[0][0])
    created_at = models.DateTimeField(_("작성일"), auto_now_add=True)

    class Meta:
        verbose_name = _("사연 원본")
        verbose_name_plural = _("사연 원본")

# 사연 편집본(contents 게시판에 게시됨)
class User_story(models.Model):
    id = models.AutoField(primary_key=True)
    user_story_origin = models.OneToOneField("User_story_origin", verbose_name=_("원본"), on_delete=models.PROTECT)
    title = models.CharField(_("제목"), max_length=200)
    content = RichTextUploadingField(_("내용"))
    image = models.ImageField(_("썸네일"), upload_to='uploads/')
    hits = models.PositiveIntegerField(_("조회수"), default=0)
    likes = models.ManyToManyField(User, related_name='likes')
    created_at = models.DateTimeField(_("작성일"), auto_now_add=True)

    def get_total_likes(self):
        return self.likes.count()
    get_total_likes.short_description = "좋아요"
    
    total_likes = property(get_total_likes)
    
    def get_absolute_url(self):
        return reverse("user-story-detail", kwargs={"pk": self.id})
    
    class Meta:
        verbose_name = _("월경 이야기")
        verbose_name_plural = _("월경 이야기")