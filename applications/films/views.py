from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from applications.films.models import Like, Film, Rating, Comment
from applications.films.serializers import RatingSerializer, MovieSerializer, CommentsSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from applications.films.paginations import LargeResultsSetPagination


class FilmAPIView(viewsets.ModelViewSet):

    queryset = Film.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner', 'title']
    search_fields = ['title']
    ordering_fields = ['id']
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):

        try:
            user = request.user
            film_id = Film.objects.get(pk=pk)
        except Film.DoesNotExist:
            return Response('movie not found', status=404)

        like_obj, _ = Like.objects.get_or_create(owner=user, film_id=pk)

        like_obj.is_like = not like_obj.is_like
        like_obj.save()
        status = 'liked'

        if not like_obj.is_like:
            status = 'unliked'

        return Response({'status': status})

    @action(methods=['POST'], detail=True)
    def rating(self ,request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(owner=request.user, film_id=pk)
        rating_obj.rating = serializer.data['rating']
        rating_obj.save()
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

