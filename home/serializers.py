from rest_framework import serializers
from .models import Movie,CastMember,Review,Favorite
from django.db.models import Avg
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field

class CastMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=CastMember
        fields='__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        fields='__all__'
    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Review rating must be between 1 and 10.")
        return value
        
class MovieSerializer(serializers.ModelSerializer):
    cast=CastMemberSerializer(many=True,read_only=True)
    reviews=ReviewSerializer(many=True,read_only=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model=Movie
        fields = [
                "id",
                "title",
                "poster_url",
                "plot",
                "release_date",
                "genre",
                "language",
                "runtime_minutes",
                "director",
                "rating",
                "trailer_url",
                "cast",
                "reviews",
                "average_rating",
            ]
    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 0 and 10.")
        return value
    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_average_rating(self, obj) -> float | None:
        average = obj.reviews.aggregate(average=Avg("rating"))["average"]
        if average is None:
            return None
        return round(float(average), 1)
    
User = get_user_model()
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8)
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data["username"],email=validated_data.get("email", ""),password=validated_data["password"])
        return user
    
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "user", "movie", "created_at"]
        read_only_fields = ["user", "created_at"]
    def validate_movie(self, value):
        user = self.context["request"].user
        if Favorite.objects.filter(user=user, movie=value).exists():
            raise serializers.ValidationError("This movie is already in your favorites.")
        return value