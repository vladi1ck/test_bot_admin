from django.contrib.auth.models import User
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from catalog.models import Category, SubCategory, Product


@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    print('CREATING DATA')

    # Создаем суперпользователя, если он не существует
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(username='admin', password='admin')
        print("Суперпользователь 'admin' создан")
    admin_user = User.objects.filter(username='admin').first()

    # Создаем категории, если их нет
    if not Category.objects.exists():
        Category.objects.create(name='Женская одежда')
        Category.objects.create(name='Мужская одежда')
        Category.objects.create(name='Детская одежда')

    # Создаем подкатегории, если их нет
    if not SubCategory.objects.exists():
        categories = Category.objects.all()
        for category in categories:
            SubCategory.objects.create(name='Рубашка', parent=category)
            SubCategory.objects.create(name='Джинсы', parent=category)
            SubCategory.objects.create(name='Брюки', parent=category)

    # Создаем продукт
    subcategory = SubCategory.objects.first()  # Или другой критерий выбора
    if not Product.objects.exists():  # Убедимся, что подкатегория существует

        Product.objects.create(
            name='Джинсы',
            description='Хорошие джинсы',
            image='media/jeans.png',
            price=100,
            category=subcategory,
            image_absolute_path='/app/jeans.png'
        )

@receiver(signal=post_save, sender=Product)
def create_image_absolute_path(instance, sender, **kwargs):
    if not hasattr(instance, '_image_absolute_path_updated'):
        # Если поле image_absolute_path не задано, то заполняем его
        if not instance.image_absolute_path:
            instance.image_absolute_path = f'/app/{instance.image}'
            # Устанавливаем флаг, чтобы предотвратить повторное обновление
            instance._image_absolute_path_updated = True
            instance.save(update_fields=['image_absolute_path'])
