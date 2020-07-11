import math
import json

from bs4 import BeautifulSoup as bs

from requests_html import HTMLSession

from gastroventure.settings import KAKAO_API_KEY

session = HTMLSession()


def search_by_keyword(keyword):
    """
    식당명으로 식당 목록 반환
    Kakao: https://developers.kakao.com/tool/rest-api/open/v2/local/search/keyword.json/get
    :param keyword: 식당명
    :return: 단순 식당 목록 [JSON]
    """
    api_url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {KAKAO_API_KEY}"
    }
    params = {
        "size": 15,
        "sort": "accuracy",
        "category_group_code": "FD6",  # 음식점 코드 (카페 코드: CE7)
        "query": keyword
    }

    # JSON 형태로 목록 반환
    places = session.request(
        method="GET",
        url=api_url,
        headers=headers,
        params=params).json()

    return places


def list_with_rate(rsts):
    """
    식당 목록 (리뷰 평점 평균 포함)
    :param rsts: 간단 식당목록
    :return: 세부 식당목록 [JSON]
    """
    restaurant_list = []
    for rst in rsts["documents"]:
        # 검색 목록 식당 조회
        rst_id = rst["place_url"].split('/')[-1]
        rst_info = session.get(
            f"https://place.map.kakao.com/main/v/{rst_id}").json()

        # 리뷰수(댓글 수): comntcnt
        # 리뷰 총합 / 리뷰 수
        score_sum = rst_info["basicInfo"]["feedback"]["scoresum"]
        score_count = rst_info["basicInfo"]["feedback"]["scorecnt"]
        comment_count = rst_info["basicInfo"]["feedback"]["comntcnt"]

        try:
            # 평균 평점
            rst_rate = round(score_sum / score_count, 1)
        except ZeroDivisionError:
            # 평점이 없을 경우 ZeroDivisionError
            rst_rate = 0
        rst["scoreavg"] = rst_rate
        rst["comment_count"] = comment_count
        restaurant_list.append(rst)

    return restaurant_list


def reviews(rst):
    # TODO: Django Restaurant 모델 필드로 불러와서 가져오기
    """
    식당 전체 리뷰 목록 조회
    :param rst: 식당
    :return: 전체 리뷰 목록 [JSON]
    """
    rst_id = rst.kakao_id
    # 댓글 페이지 수 = 댓글 수 / 5
    comment_page_size = math.ceil(rst.comment_count / 5)

    review_list = []
    for i in range(1, comment_page_size + 1):
        rst_reviews = session.get(
            f"https://place.map.kakao.com/commentlist/v/{rst_id}/{i}").json()
        review_list += rst_reviews["comment"]["list"]

    return review_list


def gov_license(keyword):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://www.foodsafetykorea.go.kr',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoCompany.do?menu_grp=MENU_NEW04&menu_no=2813',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = [
        ('menu_no', '2813'),
        ('menu_no', '2813'),
        ('menu_grp', 'MENU_NEW04'),
        ('menu_grp', 'MENU_NEW04'),
        ('copyUrl',
         'http://www.foodsafetykorea.go.kr:80/portal/specialinfo/searchInfoCompany.do?menu_grp=MENU_NEW04&menu_no=2813'),
        ('s_mode', '1'),
        ('s_opt', 'all'),
        ('s_sido_cd', 'all'),
        ('s_bsn_nm', keyword),
        ('s_opt1', 'N'),
        ('s_opt2', 'N'),
        ('s_opt3', 'N'),
        ('s_opt4', 'I'),
        ('s_keyword', ''),
        ('s_opt5', 'N'),
        ('s_opt5_sdt', ''),
        ('s_opt5_edt', ''),
        ('s_opt6', '1'),
        ('s_opt7', 'N'),
        ('s_induty_cd', 'all'),
        ('s_order_by', 'reg_dt'),
        ('s_list_cnt', '10'),
        ('s_page_num', '1'),
        ('s_food_truck_yn', ''),
        ('s_na_yn', ''),
        ('s_halal_yn', ''),
        ('s_prsdnt_nm', ''),
        ('s_dsp_reason', ''),
        ('s_induty_cd_dsp', ''),
        ('s_tx_id', '2'),
        ('chk_sido', 'all'),
        ('chk_sido', 'all'),
        ('bsn_nm', keyword),
        ('opt4', 'I'),
        ('opt4', 'I'),
        ('keyword', ''),
        ('keyword', ''),
        ('opt6_1', '1'),
        ('upjongOne', 'all'),
        ('prsdnt_nm', ''),
        ('opt6_2', '1'),
    ]

    response = session.post(
        'http://www.foodsafetykorea.go.kr/ajax/portal/specialinfo/searchBsnList.do',
        headers=headers,
        data=data,
        verify=False
    )
    return response.json()['bsnList'].json()


if __name__ == '__main__':
    keyword = "오향가"
    restaurants = search_by_keyword(keyword)
    rsts_rate = list_with_rate(restaurants)
    review = reviews(rsts_rate[0])
    print(review)
    # rsts_list = gov_license(keyword)
    # print(rsts_list)
