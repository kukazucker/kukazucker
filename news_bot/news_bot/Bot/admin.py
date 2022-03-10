from django.contrib import admin

from Bot.models import News
from Bot.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'user_id', 'first_name', 'last_name', 'username' ) 

@admin.register(News)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'channel', 'profile', 'news_text', 'news_file', 'created_at' ) 
