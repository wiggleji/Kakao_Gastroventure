from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Restaurant(models.Model):
    # TODO: 음식점 이미지 추가? 카카오 맵에서 가져오고 없을 경우 default 이미지 사용
    # PK - 음식점 id

    # 음식점명
    name = models.CharField(max_length=128, blank=False, null=False)
    # kakao_id (Unique)
    kakao_id = models.IntegerField(unique=True)
    # kakao_url (Unique)
    kakao_url = models.URLField(default="http://place.map.kakao.com/")
    # 음식점 주소 (Unique)
    address = models.CharField(default="", max_length=256)
    # 음식점 도로명 주소 (Unique)
    road_address = models.CharField(default="", max_length=256)
    # 음식점 전화번호
    telephone = models.CharField(default="", max_length=256)
    # 평균 평점
    average_rates = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0),
                    MaxValueValidator(5.0)])
    # 평가 댓글 수
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} {self.kakao_url}"


class Review(models.Model):
    # PK - 리뷰 id

    # FK - 음식점 id
    restaurant = models.ForeignKey(
        'Restaurant',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    # 작성자명
    writer = models.CharField(max_length=128, null=True, blank=True)
    # 작성날짜
    date = models.DateField()
    # 평점
    rate = models.FloatField(
        validators=[MinValueValidator(0.0),
                    MaxValueValidator(5.0)])
    # 리뷰 내용
    content = models.CharField(max_length=256, null=True, blank=True)


class License(models.Model):
    # PK - 정보 id

    # FK - 음식점 id
    restaurant = models.ForeignKey(
        'Restaurant',
        related_name='license',
        on_delete=models.CASCADE
    )
    # 변경일자
    update_date = models.DateField(blank=False, null=False)
    # 변경 전 내용
    before_data = models.CharField(max_length=256)
    # 변경 후 내용
    after_data = models.CharField(max_length=256)
    # 변경사유
    reason = models.CharField(max_length=256)
