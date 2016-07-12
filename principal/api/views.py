from rest_framework.generics import ListAPIView, RetrieveAPIView

from principal.models import Post
from .serializers import PostSerializer,PostDetailSerializer

class PostListAPIView(ListAPIView):
	queryset=Post.objects.all()
	serializer_class=PostSerializer




class PostDetailAPIView(RetrieveAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer




class PostUpdateAPIView(RetrieveAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer


class PostDeleteAPIView(RetrieveAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer
