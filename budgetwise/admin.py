from django.contrib import admin
from .models import Category, Transaction, Position

try:
    admin.site.unregister(Category)
except admin.sites.NotRegistered:
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'short_description')
    list_filter = ('parent',)
    search_fields = ('name',)
    fields = ('name', 'description', 'parent')
    def short_description(self, obj):
        text = obj.description or ''
        return text[:50] + '…' if len(text) > 50 else text
    short_description.short_description = 'Описание'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'category', 'type', 'created_at')
    list_filter = ('type', 'category')
    search_fields = ('user__username', 'category__name')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'category', 'name', 'quantity', 'price', 'sum')
    list_filter = ('category',)
    search_fields = ('name',)