from PIL import Image

from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *

# ValidationError - вывод сообщение об ошибке с пояснением
# mark_safe - для изменения шрифта в NotebookAdminForm
#
#  Используется для узнавания ширины и высоты картинки



# Минимальное разрешение изображение для вставки в товар
class NotebookAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['image'].help_text = mark_safe('<span style="color:#000080; font-size: '
                '15px;">  Загрузите изображение более высокого ' \
                'качества. Например {} x {}'.format(*Product.min_resolution
            )
        )

# Вывод параметров картинки
    def clean_image(self):

        image = self.cleaned_data['image']
        # imp - загруженная картинка
        img = Image.open(image)
        min_height, min_width = Product.min_resolution
        max_height, max_width = Product.max_resolution

        # проверка на макс резол
        if img.width < min_width or img.height < min_height:
            raise ValidationError('Меньше минимального разрешения: {} x {}'.format(*Product.min_resolution))
        elif img.width > max_width or img.height > max_height:
            raise ValidationError('Больше максимального разрешения: {} x {}'.format(*Product.max_resolution))

        print(img.width, img.height)
        return image



# Отключение выбора типа предмета как смартфон
class NotebookAdmin(admin.ModelAdmin):
    form = NotebookAdminForm
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




# Отключение выбора типа предмета как ноутбук
class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(NotebookProduct, NotebookAdmin)
admin.site.register(SmartphoneProduct, SmartphoneAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
#admin.site.register(SmartWatch)