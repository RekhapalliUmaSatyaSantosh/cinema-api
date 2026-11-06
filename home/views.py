from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import viewsets,filters
from .models import Movie,Review,CastMember,Favorite
from .serializers import MovieSerializer,ReviewSerializer,CastMemberSerializer,FavoriteSerializer
from .permissions import IsAdminOrReadOnly,ReviewPermission
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated 

# Create your views here.
class MoviesViewsSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend,]
    permission_classes=[IsAdminOrReadOnly]
    search_fields = ["title", "director", "language", "plot"]
    ordering_fields = ["title", "rating", "release_date"]
    ordering = ["title"]    
    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.query_params.get("genre")
        language = self.request.query_params.get("language")
        if genre:
            genres = [
                item.strip()
                for item in genre.split(",")
                if item.strip()
            ]
            if genres:
                table = Movie._meta.db_table
                placeholders = ", ".join(["%s"] * len(genres))
                sql = (
                    f"EXISTS ("
                    f"SELECT 1 FROM json_each({table}.genre) "
                    f"WHERE json_each.value IN ({placeholders})"
                    f")"
                )
                queryset = queryset.extra(
                    where=[sql],
                    params=genres,
                )
        if language:
            queryset = queryset.filter(language__iexact=language)
        return queryset


class CastViewSet(viewsets.ModelViewSet):
    queryset=CastMember.objects.all()
    serializer_class=CastMemberSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermission]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user,reviewer_name=self.request.user.username)
        
    def update_movie_rating(self, movie):
        from django.db.models import Avg
        average = movie.reviews.aggregate(average=Avg("rating"))["average"]
        if average is not None:
            movie.rating = round(average, 1) if average is not None else 0
            movie.save(update_fields=["rating"])
            
    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user,reviewer_name=self.request.user.username)
        self.update_movie_rating(review.movie)
    
    def perform_update(self, serializer):
        review = serializer.save()
        self.update_movie_rating(review.movie)
    
    def perform_destroy(self, instance):
        movie = instance.movie
        instance.delete()
        self.update_movie_rating(movie)
        
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all() 
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options"]
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)