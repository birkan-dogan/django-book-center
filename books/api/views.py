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