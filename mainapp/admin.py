from django.contrib import admin
from django.contrib import messages 
from django.utils.html import format_html
from .models import User, Request, Review

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'fio', 'phone', 'email')
    search_fields = ('username', 'fio', 'phone')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transport', 'start_date', 'status_display', 'payment_method')
    list_filter = ('status', 'transport', 'payment_method')
    search_fields = ('user__fio', 'user__username') 
    ordering = ('-created_at',)
    list_per_page = 10 
    
    def status_display(self, obj):
        colors = {0: '#6C757D', 1: '#4CCFE0', 2: '#28A745'}
        return format_html(
            '<b style="color: {};">{}</b>',
            colors.get(obj.status, '#000'),
            obj.get_status_display()
        )
    status_display.short_description = 'Статус'

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            messages.success(request, f'Статус заявки №{obj.id} успешно изменен на "{obj.get_status_display()}"!')
        super().save_model(request, obj, form, change)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'created_at')
    list_filter = ('created_at',)