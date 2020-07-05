from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Restaurant(models.Model):
    # PK - 음식점 id

    # 음식점명
    name = models.CharField()
    # kakao_id
    kakao_id = models.IntegerField()
    # 음식점 주소
    address = models.CharField()
    # 음식점 전화번호
    telephone = models.CharField()
    # 평균 평점
    average_rates = models.FloatField(
        validators=[MinValueValidator(0.0),
                    MaxValueValidator(5.0)])
    # 리뷰수? -> DRF nested


class Review(models.Model):
    # PK - 리뷰 id

    # FK - 음식점 id
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE
    )
    # 작성자명
    writer = models.CharField()
    # 작성날짜
    date = models.DateField()
    # 평점
    rate = models.FloatField(
        validators=[MinValueValidator(0.0),
                    MaxValueValidator(5.0)])


class License(models.Model):
    # PK - 정보 id

    # FK - 음식점 id
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE
    )
    # 변경일자
    update_date = models.DateField()
    # 변경 전 내용
    before_data = models.CharField()
    # 변경 후 내용
    after_data = models.CharField()
    # 변경사유
    reason = models.CharField()
