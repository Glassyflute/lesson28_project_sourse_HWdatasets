from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200, null=True)
    lat = models.FloatField(max_length=50)
    lng = models.FloatField(max_length=50)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return self.name


class AdUser(models.Model):
    ROLES = [
        ("member", "Участник"),
        ("moderator", "Модератор"),
        ("admin", "Админ")
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, null=True)
    username = models.SlugField(max_length=30)
    password = models.SlugField(max_length=30)
    role = models.CharField(max_length=15, choices=ROLES, default="member")
    age = models.PositiveIntegerField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    # user may have several ads?
    # ads_by_user = models.ManyToManyField(Ad) --не видит Ad, он ниже. взять ads_by_user как annotate

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Ad(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=1000, null=True)
    logo = models.ImageField(upload_to='logos/', null=True)
    is_published = models.BooleanField(default=False)
    author_id = models.ForeignKey(AdUser, on_delete=models.CASCADE, null=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category)
    # category_id in table Ads
    # no location === annotate???

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name

