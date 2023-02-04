# Generated by Django 4.1.5 on 2023-02-01 03:14

import blog.custom_field
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', blog.custom_field.UnsignedAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', help_text='게시글 제목 입니다.', max_length=255, verbose_name='제목')),
                ('slug', models.SlugField(default='', max_length=200, unique=True)),
                ('summary', models.CharField(default='', help_text='게시글 요약글 입니다.', max_length=255, verbose_name='요약')),
                ('is_published', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[(0, 'Trash'), (1, 'Publish'), (2, 'Future'), (3, 'Draft'), (4, 'Pending'), (5, 'Private'), (6, 'Auto Draft')], default=3, help_text='게시글 상태 : publish (발행, 공개), draft (임시)', verbose_name='상태')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='발행일시')),
            ],
            options={
                'db_table': 'articles',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', blog.custom_field.UnsignedAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255, verbose_name='섹션 명칭')),
                ('slug', models.SlugField(default='', max_length=200, unique=True)),
                ('description', models.CharField(default='', max_length=255, verbose_name='섹션 요약 설명')),
                ('logical_path', models.CharField(default='', max_length=255)),
                ('order', models.IntegerField(default=0, verbose_name='정렬 순')),
                ('depth', models.IntegerField(default=0, verbose_name='깊이')),
                ('count', models.IntegerField(default=0, editable=False, verbose_name='글 수')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'section',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', blog.custom_field.UnsignedAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255)),
                ('slug', models.CharField(default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='ArticleContent',
            fields=[
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='blog.article')),
                ('markdown', models.TextField(blank=True, default='', verbose_name='마크 다운')),
                ('output', models.TextField(blank=True, default='', verbose_name='HTML 아웃풋')),
            ],
            options={
                'db_table': 'article_content',
            },
        ),
        migrations.CreateModel(
            name='SectionArticle',
            fields=[
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='blog.article')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'section_article_rel',
            },
        ),
        migrations.CreateModel(
            name='TagArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name_cached', models.CharField(default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.tag')),
            ],
            options={
                'db_table': 'tag_article_rel',
            },
        ),
        migrations.AddField(
            model_name='tag',
            name='articles',
            field=models.ManyToManyField(related_name='tag', through='blog.TagArticle', to='blog.article'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['-published_at'], name='articles_publish_aa799f_idx'),
        ),
        migrations.AddField(
            model_name='sectionarticle',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.section', verbose_name='섹션 카테고리'),
        ),
        migrations.AddIndex(
            model_name='sectionarticle',
            index=models.Index(fields=['section_id'], name='section_art_section_5f99a2_idx'),
        ),
    ]
