import dateutil.parser

from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from service.models import Restaurant, Review, License
from service.serializers import RestaurantSerializer, ReviewSerializer, LicenseSerializer

from kakao.api import search_by_keyword, list_with_rate, reviews


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def list(self, request, *args, **kwargs):
        # TODO: 목록이 없으면 Kakao API 요청 후 모델 생성, 다시 목록 가져오기

        # 음식점명 필터링
        filter_name = self.request.query_params.get('name')
        if filter_name:
            queryset = Restaurant.objects.filter(name__icontains=filter_name)

            if len(queryset) == 0:
                # TODO: Kakao API 요청
                kakao_restaurants = list_with_rate(search_by_keyword(keyword=filter_name))
                for rst in kakao_restaurants:
                    name = rst['place_name']
                    kakao_id = rst['id']
                    kakao_url = rst['place_url']
                    address = rst['address_name']
                    road_address = rst['road_address_name']
                    telephone = rst['phone']
                    average_rates = rst['scoreavg']
                    comment_count = rst['comment_count']
                    # 모델 생성
                    Restaurant.objects.create(
                        name=name,
                        kakao_id=kakao_id,
                        kakao_url=kakao_url,
                        address=address,
                        road_address=road_address,
                        telephone=telephone,
                        average_rates=average_rates,
                        comment_count=comment_count
                    )
                queryset = Restaurant.objects.filter(name__icontains=filter_name)
        else:
            queryset = Restaurant.objects.all()

        serialzer = self.get_serializer(queryset, many=True)
        return Response(serialzer.data)

    def retrieve(self, request, *args, **kwargs):
        # TODO: 리뷰, 인허가 내역이 없으면 Kakao API, 식품안전나라 요청 후 모델 생성, 다시 가져오기
        rst_queryset = Restaurant.objects.all()

        restaurant = get_object_or_404(rst_queryset, pk=kwargs.get("pk"))
        restaurant_reviews = Review.objects.filter(restaurant=restaurant)
        if len(restaurant_reviews) == 0:
            # TODO: Kakao API 요청
            kakao_reviews = reviews(rst=restaurant)
            for review in kakao_reviews:
                writer = review.get('username')
                date = dateutil.parser.parse(review.get('date'))
                rate = review.get('point')
                content = review.get('contents')

                # 모델 생성
                Review.objects.create(
                    restaurant=restaurant,
                    writer=writer,
                    date=date,
                    rate=rate,
                    content=content
                )

        serialzer = RestaurantSerializer(restaurant)
        return Response(serialzer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class LicenseViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
