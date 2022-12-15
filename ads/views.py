import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView

from ads.models import Category, Ad, AdUser
from avito import settings


def root(request):
    return JsonResponse({
        "status": "ok"
    })


class CategoryListView(ListView):
    """
    Список категорий, с сортировкой по названию категории, с пагинатором и
    итоговой информацией
    """
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        categories = []
        for category in page_obj:
            categories.append(
                {
                    "id": category.id,
                    "name": category.name
                }
            )

        response = {
            "items": categories,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    """
    Детальная информация по выбранной категории
    """
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    """
    Создание новой категории
    """
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category_new = Category.objects.create(**category_data)

        return JsonResponse({
            "id": category_new.id,
            "name": category_new.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    """
    Обновление данных по категории
    """
    model = Category
    fields = ["name", "is_active"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"],
            is_active=category_data["is_active"],
        )

        return JsonResponse({
                    "id": category.id,
                    "name": category.name,
                    "is_active": category.is_active
                })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    """
    Удаление объявления
    """
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)







class AdListView(ListView):
    """
    Список всех объявлений, с сортировкой по цене объявления по убыванию, с пагинатором и
    итоговой информацией
    """
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("-name")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "price": ad.price,
                    "description": ad.description,
                    "logo": ad.logo,
                    "is_published": ad.is_published,
                    "author_id": ad.author_id,
                    "location_id": ad.location_id,
                    "categories": list(map(str, ad.categories.all()))
                }
            )

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    """
    Детальная информация по выбранному объявлению
    """
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "price": ad.price,
            "description": ad.description,
            "logo": ad.logo,
            "is_published": ad.is_published,
            "author_id": ad.author_id,
            "location_id": ad.location_id,
            "categories": list(map(str, ad.categories.all()))
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    """
    Создание нового объявления
    """
    model = Ad
    fields = ["name", "price", "description", "logo", "is_published", "author_id", "location_id", "categories"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        ad_new = Ad.objects.create(
            name=ad_data["name"],
            price=ad_data["price"],
            description=ad_data["description"],
            logo=ad_data["logo"],
            is_published=ad_data["is_published"],
            location_id=ad_data["location_id"]
        )

        ad_new.author_id = get_object_or_404(AdUser, pk=ad_data["author_id"])

        for category in ad_data["categories"]:
            category_obj, created = Category.objects.get_or_create(
                name=category,
                defaults={
                    "is_active": True
                }
            )
            ad_new.categories.add(category_obj)

        ad_new.save()

        return JsonResponse({
            "id": ad_new.id,
            "name": ad_new.name,
            "price": ad_new.price,
            "description": ad_new.description,
            "logo": ad_new.logo,
            "is_published": ad_new.is_published,
            "author_id": ad_new.author_id,
            "location_id": ad_new.location_id,
            "categories": list(map(str, ad_new.categories.all()))
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    """
    Обновление данных по выбранному объявлению
    """
    model = Ad
    fields = ["name", "price", "description", "is_published", "location_id", "categories"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        ad_upd = Ad.objects.create(
            name=ad_data["name"],
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            location_id=ad_data["location_id"]
        )

        ad_upd.author_id = get_object_or_404(AdUser, pk=ad_data["author_id"])

        for category in ad_data["categories"]:
            category_obj, created = Category.objects.get_or_create(
                name=category,
                defaults={
                    "is_active": True
                }
            )
            ad_upd.categories.add(category_obj)

        ad_upd.save()

        return JsonResponse({
                    "id": ad_upd.id,
                    "name": ad_upd.name,
                    "price": ad_upd.price,
                    "description": ad_upd.description,
                    "is_published": ad_upd.is_published,
                    "author_id": ad_upd.author_id,
                    "location_id": ad_upd.location_id,
                    "categories": list(map(str, ad_upd.categories.all()))
                })


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    """
    Добавление/обновление картинки в объявлении
    """
    model = Ad
    fields = ["name", "logo"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.logo = request.FILES["logo"]

        self.object.save()

        return JsonResponse({
                    "id": self.object.id,
                    "name": self.object.name,
                    "logo": self.object.logo.url if self.object.logo else None
                })


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    """
    Удаление объявления
    """
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)






class AdUserListView(ListView):
    """
    Список пользователей, с сортировкой по username, с пагинатором и
    итоговой информацией
    """
    model = AdUser

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("username")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ad_users = []
        for ad_user in page_obj:
            ad_users.append(
                {
                    "id": ad_user.id,
                    "first_name": ad_user.first_name,
                    "last_name": ad_user.last_name,
                    "username": ad_user.username,
                    "password": ad_user.password,
                    "role": ad_user.role,
                    "age": ad_user.age,
                    "location_id": ad_user.location_id
                }
            )

        # добавить сумму опубликованных объявл total_ads по каждому пользователю publ-true == annotate?
        response = {
            "items": ad_users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class AdUserDetailView(DetailView):
    """
    Детальная информация по выбранному пользователю
    """
    model = AdUser

    def get(self, request, *args, **kwargs):
        ad_user = self.get_object()

        return JsonResponse({
            "id": ad_user.id,
            "first_name": ad_user.first_name,
            "last_name": ad_user.last_name,
            "username": ad_user.username,
            "password": ad_user.password,
            "role": ad_user.role,
            "age": ad_user.age,
            "location_id": ad_user.location_id
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdUserCreateView(CreateView):
    """
    Создание нового пользователя
    """
    model = AdUser
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id"]

    def post(self, request, *args, **kwargs):
        ad_user_data = json.loads(request.body)
        ad_user_new = AdUser.objects.create(**ad_user_data)

        # location вводят текстом, после в виде ИД?

        return JsonResponse({
            "id": ad_user_new.id,
            "first_name": ad_user_new.first_name,
            "last_name": ad_user_new.last_name,
            "username": ad_user_new.username,
            "password": ad_user_new.password,
            "role": ad_user_new.role,
            "age": ad_user_new.age,
            "location_id": ad_user_new.location_id
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdUserUpdateView(UpdateView):
    """
    Обновление данных по пользователю
    """
    model = AdUser
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_user_data = json.loads(request.body)

        user_upd = AdUser.objects.create(
            first_name=ad_user_data["first_name"],
            last_name=ad_user_data["last_name"],
            role=ad_user_data["role"],
            age=ad_user_data["age"],
            location_id=ad_user_data["location_id"]
        )

        # location вводят текстом, после в виде ИД?

        user_upd.username = get_object_or_404(AdUser, pk=ad_user_data["username"])
        if user_upd.username:
            user_upd.password = ad_user_data["password"]

        return JsonResponse({
                    "id": user_upd.id,
                    "first_name": user_upd.first_name,
                    "last_name": user_upd.last_name,
                    "username": user_upd.username,
                    "password": user_upd.password,
                    "role": user_upd.role,
                    "age": user_upd.age,
                    "location_id": user_upd.location_id
                })


@method_decorator(csrf_exempt, name="dispatch")
class AdUserDeleteView(DeleteView):
    """
    Удаление пользователя
    """
    model = AdUser
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)



### select_relation ???? select_related(”user”) - foreign key