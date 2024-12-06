# Generated by Django 5.1.3 on 2024-11-25 05:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('男性', '男性'), ('女性', '女性'), ('選択しない', '選択しない')], default='選択しない', max_length=10)),
                ('agency_or_group', models.CharField(blank=True, max_length=255, null=True)),
                ('job_title', models.CharField(max_length=255)),
                ('workhistory_text', models.TextField(blank=True, null=True)),
                ('awards_text', models.TextField(blank=True, null=True)),
                ('skills_text', models.TextField(blank=True, null=True)),
                ('portfolio_text', models.TextField(blank=True, null=True)),
                ('specialization_text', models.TextField(blank=True, null=True)),
                ('free_text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('artist', 'アーティスト'), ('creator', '製作者'), ('admin', '管理者')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]