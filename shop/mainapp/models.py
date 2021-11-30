from PIL import Image

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()


# Берет url продукта. Аналог получения абсолютного url
def get_product_url(obj, viewname):
    # .meta скрытый элемент
    ct_model = obj.__class__.meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


##### Вывод сообщения об ошибке
class MinResolutionExceptionError(Exception):
    pass
class MaxResolutionExceptionError(Exception):
    pass
#####

class LatestProductsManager:
    @staticmethod
    def get_product_for_main_page(*args, **kwargs):
        with_respect = kwargs.get('with_respect')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            # Вызываем ее род класс, условно objects
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            # extend - расширение в список ((добавление))
            products.extend(model_products)

        if with_respect:
            ct_model = ContentType.objects.filter(model=with_respect)
            if ct_model.exists():
                if with_respect in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.starstwith
                        (with_respect), reverse=True
                    )
        return products



# Иимтируем поведение стандартной модели
class LatestProducts:
    objects = LatestProductsManager()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    min_resolution = (400, 400)
    max_resolution = (3000, 3000)

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория',on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    warranty = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Гарантия')

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)

        min_height, min_width = self.min_resolution
        max_height, max_width = self.max_resolution
        if img.width < min_width or img.height < min_height:
            raise MinResolutionExceptionError('Меньше минимального разрешения: {} x {}'.format(*self.min_resolution))
        elif img.width > max_width or img.height > max_height:
            raise MaxResolutionExceptionError('Больше максимального разрешения: {} x {}'.format(*self.max_resolution))
        print(img.width, img.height)

        return image


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель',on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина',on_delete=models.CASCADE, related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {}".format(self.product.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец',on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Notebook(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolut_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='Максимальный объем памяти')
    main_cam = models.CharField(max_length=255, verbose_name='Главная камера')
    front_cam = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolut_url(self):
        return get_product_url(self, 'product_detail')

'''
class SmartWatch(Product):
    size = models.CharField(max_length=255, verbose_name='Размер дисплея')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    glass_material = models.CharField(max_length=255, verbose_name='Материал стекла')
    belt_material = models.CharField(max_length=255, verbose_name='Материал ремня')


    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)
        
'''