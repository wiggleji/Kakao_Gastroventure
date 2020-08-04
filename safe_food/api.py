import math
import json

import requests
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession

session = HTMLSession()


def gov_license(keyword):
    """
    음식점명으로 식품안전나라 검색
    :param keyword: 음식점명 [text]
    :return: 음식점 목록 [list]
    """
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
    return response.json()['bsnList']


def get_owner_history_text_list(shop_id):
    """
    음식점 인허가 변경사항정보 조회
    :param shop_id: 식품안전나라 음식점 id [int]
    :return: 인허가 변경사항정보 목록 [text]
    """
    response = session.get(
        f'https://www.foodsafetykorea.go.kr/potalPopup/fooddanger/bsnInfoDetail.do?bsnLcnsLedgNo={shop_id}')
    owner_history = response.html.find(
        '#bsn_info > div.list-container > div.fcs_ddt > table:nth-of-type(2)',
        first=True)

    try:
        raw_text = owner_history.text.split(
            "변경사유\n"
        )[1]
        history_list = raw_text.split("\n")

    except Exception as e:
        print(e)
        return None
    return history_list


def make_model_by_history_list(rst_history):
    """
    TODO: Django Model 생성 코드
    식품안전나라 인허가 변경사항으로 모델 생성
    :param rst_history: 식품업체 인허가 변경정보 목록 [text]
    :return: True/False
    """
    for index in range(0, len(rst_history), 4):
        change_log = []
        change_date = rst_history[index]
        before = rst_history[index+1]
        after = rst_history[index+2]
        reason = rst_history[index+3]
        change_log.extend((
            change_date,
            before,
            after,
            reason
        ))
        print(change_log)


if __name__ == '__main__':
    keyword = "오향가"
    rsts_list = gov_license(keyword)
    print(rsts_list)
    print()
    # TODO: 카카오 주소와 동일한지 비교
    rst_history = get_owner_history_text_list(rsts_list[1]["BSN_LCNS_LEDG_NO"])
    print(rst_history)
    make_model_by_history_list(rst_history)
