from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv"
    ]
    inlines = [
        OrderInline,
    ]
    list_display = "id", "name", "description_short", "price", "archived"
    list_display_links = "id", "name"
    ordering = "description",
    search_fields = "name", "description"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("collapse", "wide")
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": ("Extra options, options for delete product",)
        })
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return f"{obj.description[:48]}..."


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]

    list_display = "id", "delivery_adress", "promocode", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.prefetch_related("products").select_related("user")

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username