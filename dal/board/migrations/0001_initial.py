# Generated by Django 3.0.4 on 2020-03-22 04:03

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, verbose_name='제목')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='내용')),
                ('category', models.CharField(choices=[('notice', '공지사항'), ('event', '이벤트')], max_length=20, verbose_name='카테고리')),
                ('is_fixed', models.BooleanField(verbose_name='상단고정')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='조회수')),
            ],
            options={
                'verbose_name': '공지 게시판',
                'verbose_name_plural': '공지 게시판',
            },
        ),
        migrations.CreateModel(
            name='User_story_origin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='이미지1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='이미지2')),
                ('sort', models.CharField(choices=[('unread', '읽지않음'), ('read', '읽음'), ('editing', '제작중'), ('complete', '제작완료'), ('hold', '보류')], default='unread', max_length=20, verbose_name='분류')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '사연 원본',
                'verbose_name_plural': '사연 원본',
            },
        ),
        migrations.CreateModel(
            name='User_story',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mtype', models.CharField(max_length=10, verbose_name='M-Type')),
                ('title', models.CharField(max_length=200, verbose_name='제목')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='내용')),
                ('image', models.ImageField(upload_to='uploads/', verbose_name='썸네일')),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('likes', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('user_story_origin', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='board.User_story_origin', verbose_name='원본')),
            ],
            options={
                'verbose_name': '월경 이야기',
                'verbose_name_plural': '월경 이야기',
            },
        ),
    ]
