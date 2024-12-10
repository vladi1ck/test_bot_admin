from django.contrib.auth.models import User
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from catalog.models import Category, SubCategory, Product
from faq.models import FAQ


@receiver(post_migrate)
def create_initial_data(sender, **kwargs):

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(username='admin', password='admin')
        print("Суперпользователь 'admin' создан")
    admin_user = User.objects.filter(username='admin').first()

    if not Category.objects.exists():
        Category.objects.create(name='Женская одежда')
        Category.objects.create(name='Мужская одежда')
        Category.objects.create(name='Детская одежда')

    if not SubCategory.objects.exists():
        categories = Category.objects.all()
        for category in categories:
            SubCategory.objects.create(name='Рубашка', parent=category)
            SubCategory.objects.create(name='Джинсы', parent=category)
            SubCategory.objects.create(name='Брюки', parent=category)

    subcategory = SubCategory.objects.first()
    if not Product.objects.exists():

        Product.objects.create(
            name='Джинсы',
            description='Хорошие джинсы',
            image='media/jeans.png',
            price=100,
            category=subcategory,
            image_absolute_path='/app/jeans.png'
        )
    if not FAQ.objects.exists():
        FAQ.objects.create(
            name="Как зарегистрироваться?",
            answer= "Для регистрации перейдите на наш сайт и нажмите 'Регистрация'."
        )
        FAQ.objects.create(
            name="Как сбросить пароль?",
            answer="Чтобы сбросить пароль, используйте форму восстановления на сайте."
        )
        FAQ.objects.create(
            name= "Как связаться с поддержкой?",
            answer="Связаться с поддержкой можно по email: support@example.com."
        )
        FAQ.objects.create(
            name= "Где найти информацию о тарифах?",
            answer="Информация о тарифах доступна на странице 'Тарифы' на нашем сайте."
        )

@receiver(signal=post_save, sender=Product)
def create_image_absolute_path(instance, sender, **kwargs):
    if not hasattr(instance, '_image_absolute_path_updated'):
        if not instance.image_absolute_path:
            instance.image_absolute_path = f'/app/{instance.image}'
            instance._image_absolute_path_updated = True
            instance.save(update_fields=['image_absolute_path'])
