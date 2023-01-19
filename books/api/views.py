# from rest_framework.generics import GenericAPIView
# from ..models import Book, Comment
# from .serializers import CommentSerializer, BookSerializer

# from rest_framework.mixins import ListModelMixin, CreateModelMixin

# """
# we import `ListModelMixin` from mixins to get list of all books
# we import `CreateModelMixin` from mixins to create a new Book instance

# """

# class BookListCreateAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     # to list all Book instances
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     # to create a new Book instance
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

from ..models import Book, Comment
from .serializers import CommentSerializer, BookSerializer

from rest_framework import generics
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework import permissions
from .permissions import IsAdminUserOrReadOnly  # custom permission

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [permissions.IsAuthenticated] -->  local permission
    permission_classes = [IsAdminUserOrReadOnly]  # custom permission


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]  # custom permission

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        book_pk = self.kwargs.get("book_pk")
        # kitabımızın primary key parametresini `self.kwargs.get()` sayesinde çektik
        book = get_object_or_404(Book, pk = book_pk)
        serializer.save(book = book)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer