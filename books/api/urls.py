from django.urls import path
from .views import BookListCreateAPIView, BookDetailAPIView, CommentCreateAPIView, CommentDetailAPIView

urlpatterns = [
    path("books/", BookListCreateAPIView.as_view(), name = "book-list"),
    path("books/<int:pk>",BookDetailAPIView.as_view(), name = "book-detail"),
    path("books/<int:book_pk>/comment", CommentCreateAPIView.as_view(), name = "comment"),
    path("comments/<int:pk>", CommentDetailAPIView.as_view(), name = "comments"),
]