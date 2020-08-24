import datetime
import dateutil.parser
from difflib import SequenceMatcher

from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from service.models import Restaurant, Review, License
from service.serializers import RestaurantSerializer, ReviewSerializer, LicenseSerializer

from kakao.api import search_by_keyword, list_with_rate, reviews
from safe_food.api import gov_license, get_owner_history_text_list


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
                # 음식점 목록이 없을 경우
                # TODO: Kakao API 요청
                kakao_restaurants = list_with_rate(search_by_keyword(keyword=filter_name))
                for rst in kakao_restaurants:
                    name = rst['place_name']
                    if name[-1] == "점":
                        # 체인음식점 키워드 예외처리
                        name_keyword = name.split(" ")[0]
                    else:
                        name_keyword = name
                    kakao_id = rst['id']
                    kakao_url = rst['place_url']
                    kakao_image_url = rst['kakao_image_url']
                    address = rst['address_name']
                    road_address = rst['road_address_name']
                    telephone = rst['phone']
                    average_rates = rst['scoreavg']
                    comment_count = rst['comment_count']

                    # 모델 생성
                    Restaurant.objects.create(
                        name=name,
                        name_keyword=name_keyword,
                        kakao_id=kakao_id,
                        kakao_url=kakao_url,
                        kakao_image_url=kakao_image_url,
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
        # TODO: 식품안전나라 식당 내역 조회 후 모델 생성
        rst_license = License.objects.filter(restaurant=restaurant)
        if len(rst_license) == 0:
            gov_rsts_list = gov_license(restaurant.name_keyword)
            for rst in gov_rsts_list:
                # 음식점 도로명주소와 식품안전나라 주소 비교
                # #TODO: 유사도로 비교
                compare_ratio = SequenceMatcher(None,
                                                restaurant.road_address,
                                                rst["SITE_ADDR"]).ratio()
                if compare_ratio > 0.50:
                    # 주소 유사도 50% 넘을 경우 내역 생성
                    gov_rst_id = rst["BSN_LCNS_LEDG_NO"]
                    rst_history = get_owner_history_text_list(gov_rst_id)
                    create_history_model_from_gov(restaurant, rst_history)

        restaurant_reviews = Review.objects.filter(restaurant=restaurant)
        if len(restaurant_reviews) == 0:
            # Kakao 리뷰 가져와 모델 생성
            # TODO: 예외처리
            kakao_reviews = reviews(rst=restaurant)
            create_review_model_from_kakao(restaurant, kakao_reviews)

        serialzer = RestaurantSerializer(restaurant)
        return Response(serialzer.data)


def create_history_model_from_gov(restaurant, rst_history):
    """
    TODO: Django Model 생성 코드
    TODO: 모델 일괄 생성으로 코드 업데이트 필요
    식품안전나라 인허가 변경사항으로 모델 생성
    :param restaurant: 음식점 model PK
    :param rst_history: 식품업체 인허가 변경정보 목록 [text]
    :return: True/False
    """
    for index in range(0, len(rst_history), 4):
        change_date = rst_history[index]
        update_date = datetime.datetime.strptime(change_date, '%Y -%m -%d')
        before_data = rst_history[index + 1]
        after_data = rst_history[index + 2]
        reason = rst_history[index + 3]

        License.objects.create(
            restaurant=restaurant,
            update_date=update_date,
            before_data=before_data,
            after_data=after_data,
            reason=reason
        )


def create_review_model_from_kakao(restaurant, reviews):
    # TODO: 예외처리
    # TODO: 모델 일괄 생성으로 코드 업데이트 필요
    for review in reviews:
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
    return True


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class LicenseViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
