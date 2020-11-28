from django.contrib import admin
from .models import site_views
# Register your models here.

class site_viewsAdmin(admin.ModelAdmin):
    list_display = ('page','views')

    def page(self,obj):
        return obj.page_name.upper()

    def views(self, obj):
        return obj.page_views

    def get_queryset(self, request):
        qset = super(site_viewsAdmin, self).get_queryset(request)
        qset = qset.order_by('-page_views')
        return qset

admin.site.register(site_views, site_viewsAdmin)
