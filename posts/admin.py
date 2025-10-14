from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'price', 'created_at', 'views_count']
    list_filter = ['status', 'category', 'created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'views_count']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'author', 'category', 'status')
        }),
        ('Дополнительная информация', {
            'fields': ('price', 'contact_phone', 'contact_email', 'image')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at', 'views_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    list_editable = ['is_active']
    ordering = ['-created_at']
