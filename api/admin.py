from django.contrib import admin
from django.utils.safestring import mark_safe

from api.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_urls')

    def image_show(self, obj):
        return mark_safe('<img src="{url}" style="height:80px; object-fit: contain;" />'.format(url=obj.image.url))

    def image_urls(self, obj):
        def get_url(img):
            if not img: return '-'
            return img.url
        return get_url(obj.image)
