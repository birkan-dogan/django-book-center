# Book-Center
> Database tablolarımızı oluşturalım
- in models.py
```python
from django.db import models

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length = 250)
    author = models.CharField(max_length = 250)
    description = models.TextField(blank = True, null = True)
    published_date = models.DateField()

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f" {self.name} - {self.author} "


```
> PositiveIntegerField() için validators kullanıyoruz. Validators için `MinValueValidator` ve `MaxValueValidator` validatorlarını import ediyoruz.
```python
from django.contrib.auth.models import User
from django.core.validators import(
    MinValueValidator,
    MaxValueValidator
)  # for rating fields

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = "comments")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)],
    )

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f" {self.rating}"
```
## GenericAPI Views and Mixins
> CRUD işlemlerlerinde benzer kodları tekrar tekrar yazmanın önüne geçmek için Django'nun bize sunduğu birtakım metodları kullanabiliriz.  
Django_Rest_Framework, APIView class'ından türetilen ve APIView class'ının kabiliyetlerine yenilerini de ekleyen GenericAPIView class'ına ve bazı mixinslere sahip. (GenericAPIView, APIView'ın instance'ı)
### Attributes of GenericAPIView
>The following attributes control the basic view behavior.
- `queryset` - The queryset that should be used for returning objects from this view. Typically, you must either set this attribute, or override the `get_queryset()` method. If you are overriding a view method, it is important that you call get_queryset() instead of accessing this property directly, as queryset will get evaluated once, and those results will be cached for all subsequent requests.  
- `serializer_class` - The serializer class that should be used for validating and deserializing input, and for serializing output. Typically, you must either set this attribute, or override the `get_serializer_class()` method.
 
- **lookup_field** - The model field that should be used for performing object lookup of individual model instances. Defaults to 'pk'. Note that when using hyperlinked APIs you'll need to ensure that both the API views and the serializer classes set the lookup fields if you need to use a custom value.
lookup_url_kwarg - The URL keyword argument that should be used for object lookup. The URL conf should include a keyword argument corresponding to this value. If unset this defaults to using the same value as lookup_field.

> GenericAPIView'a birtakım yetenekler katmak için Mixins methodlarını kullanabiliriz.
- ListModelMixin
- CreateModelMixin
- RetrieveModelMixin
- UpdateModelMixin
- DestroyModelMixin

> - in views.py
```python
from rest_framework.generics import GenericAPIView
from ..models import Book, Comment
from .serializers import CommentSerializer, BookSerializer

from rest_framework.mixins import ListModelMixin, CreateModelMixin

"""
we import `ListModelMixin` from mixins to get list of all books
we import `CreateModelMixin` from mixins to create a new Book instance

"""

class BookListCreateAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # to list all Book instances
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # to create a new Book instance
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

## Concrete Views
> Bir concrete view, GenericAPIView ve ilgili mixinlerin birleşmesinden oluşur.  
ex.) **RetrieveUpdateAPIView**, GenericAPIView ile (RetrieveModelMixin ve UpdateModelMixin'in) birlikte kullanılmasıyla elde edilir.

- List ve create işlemleri yapabilen bir concreteView örneği:
```python
from ..models import Book, Comment
from .serializers import CommentSerializer, BookSerializer

from rest_framework import generics

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

```

> Concrete Views sayesinde primary_key belirtmeden id özelinde retrieve/update/delete işlemleri yapabiliriz.
```python

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


```
- urls.py file'ına da detay sayfası için path eklemeliyiz.
```python
urlpatterns = [
    path("books/", BookListCreateAPIView.as_view(), name = "book-list"),
    path("books/<int:pk>",BookDetailAPIView.as_view(), name = "book-detail"),
]
```

### overwrite the methods of concreteView
> ConcreteView'lar birçok işlemi arka planda kendisi hallettiğinden bazı durumlarda concreteview'ın kullandığı methodları override edebiliriz.  
ex.) bir comment oluştururken model'imizde belirttiğimiz üzere comment bir book ile ilişkili olmalı
```python
# in models.py/Comment
book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = "comments")

```
- Comment oluştururken, book ile comment nasıl eşleşecek? (yüzlerce kitap var)  
url'de endpoint'in içerisinde ilgili kitabın id'sini eklemeliyiz ve endpointimiz şu şekilde çalışmalı
**books/<`int:book_pk`>/comment/**
> Bunun için CreateAPIView'ın parent'larından CreateModelMixin'in içerisindeki `perform_create()` methodunu override ediyoruz.

> `perform_create()` methodunda serializer.save() komutu çalışıyor ve serializer kaydedilmeden önce biz hangi kitaba yorum yapıldıysa onu önce bulmalıyız ve sonra serializer save edilirken bulduğumuz kitabı kaydedilen object'e eklemeliyiz.

- in views.py
```python
class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        book_pk = self.kwargs.get("book_pk")
        # kitabımızın primary key parametresini `self.kwargs.get()` sayesinde çektik
        book = get_object_or_404(Book, pk = book_pk)
        serializer.save(book = book)
```
- in urls.py
```python
path("books/<int:book_pk>/comment", CommentCreateAPIView.as_view(), name = "comment"),
```

## Permissions
### Global Permissions
The default permission policy may be set globally, using the `DEFAULT_PERMISSION_CLASSES` setting.
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```
**IsAuthenticated** -> Sadece login olan kullanıcılara izin vermek istediğimizde kullanacağımız method  
**AllowAny** -> Default'u AllowAny'dir. AllowAny, herkese crud işlemleri için izin veren methodtur.  
**IsAdminUser**  
**IsAuthenticatedOrReadOnly**  

**doc**: https://www.django-rest-framework.org/api-guide/permissions/

### Local Permissions

- in permissions.py
```python
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class BasePermission(metaclass=BasePermissionMetaclass):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class AllowAny(BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """

    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

# permissions'lar boolean değer döndürür --> True or False
```
> Rest_framework'ün url'ini kullanarak browesableAPI üzerinden login/logout olabiliriz.
```python
# in main/urls.py
 path("api-auth/",include("rest_framework.urls")),

```
- in views.py
```python
from rest_framework import permissions

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # local permission
```

### Custom Permission
- in app/permissions.py
```python
from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)  # super() stands for IsAdminUser
        return bool(request.method in permissions.SAFE_METHODS or is_admin)


```

- in views.py
```python

from .permissions import IsAdminUserOrReadOnly  # custom permission

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]  # custom permission


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]  # custom permission


```

> Yorum yapan kullanıcıların **sadece kendi yorumları üzerinde** update ve delete işlemlerinin olması için bir permission yazalım ve 1 user 1 kitaba sadece 1 yorum yazabilsin istiyoruz.

```python
from rest_framework.exceptions import ValidationError  # to warn the user that can't comment second times

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        book_pk = self.kwargs.get("book_pk")
        # kitabımızın primary key parametresini `self.kwargs.get()` sayesinde çektik
        book = get_object_or_404(Book, pk = book_pk)
        user = self.request.user

        # 1 user 1 kitaba sadece 1 yorum yapabilir
        comments = Comment.objects.filter(book = book, user = user)
        if(comments.exists()):
            raise ValidationError("You can comment just one time for the same book")

        serializer.save(book = book, user = user)


```

> User sadece kendi yorumları üzerinde update, delete yetkilerine sahip olacak. Bunun için bizim önceki yorumlara erişmemiz ve yorumları yapan user ile login olmuş user'ı eşleştirmemiz lazım.
- in env/permission.py
```python
class BasePermission(metaclass=BasePermissionMetaclass):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

# BasePermission'ın methodlarından has_object_permission() methodunda objectimize erişebiliyoruz.
```
> BasePermission'dan inherit ederek oluşturacağımız custom permission'da has_object_permission() methodunu kullanarak obj.user'ımıza ulaşabiliriz ve kullanıcı durumuna göre permission'ımız True ya da False döner
- in app/permissions.py
```python

class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if(request.method in permissions.SAFE_METHODS):
            return True

        return request.user == obj.user


```
- in app/views.py
```python

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUserOrReadOnly]


```
