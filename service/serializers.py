from rest_framework import serializers

from service.models import Restaurant, Review, License


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # exclude = ["restaurant"]


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    license = LicenseSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'pk',
            'name',
            'name_keyword',
            'kakao_id',
            'kakao_url',
            'address',
            'road_address',
            'telephone',
            'average_rates',
            'comment_count',
            'license',
            'reviews'
        ]
