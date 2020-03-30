#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/29 0021 下午 19:40
# @Author  : xiaozhi！
# @FileName: pdd_api
# @Software: PyCharm


import time
import hashlib
import requests
from urllib.parse import urlencode


class PddApi:
    host = "https://gw-api.pinduoduo.com/api/router?"
    headers = {
        "accept": "application/json"
    }

    def __init__(self, id=None, token=None, secret=None):
        """
        初始化
        """
        self.client_id = id
        self.secret = secret
        self.access_token = token
        self.data_type = "JSON"

    def sign_md5(self, params):
        """
        对拼接好的字符串进行md5签名
        """
        hl = hashlib.md5()
        hl.update(params.encode(encoding='utf-8'))
        return hl.hexdigest().upper()

    def splice_str(self):
        """
        升序排序请求参数，连接字符串，并在首尾加上client_secret
        """
        self.timestamp = f"{time.time()}".split(".")[0]
        pdd_dict = self.__dict__.copy()
        secret = self.secret
        del pdd_dict["secret"]
        reverse_list = sorted([(k, str(v)) for k, v in pdd_dict.items()], key=lambda x:x[0])
        reverse_list.insert(0, ("", secret))
        reverse_list.append(("", secret))
        reverse_list_str = list(map(lambda x: "".join(x), reverse_list))
        params = "".join(reverse_list_str)
        return params, pdd_dict

    def urlencode_data(self, params, pdd_dict):
        pdd_dict["sign"] = self.sign_md5(params)
        result = urlencode(pdd_dict)
        url = f"{self.host}{result}"
        return url

    def pdd_order_list_get(self, **kwargs):
        """
        获取订单列表
        kwargs: order_status=None, refund_status=None, start_confirm_at=None, end_confirm_at=None,
                           page=None, page_size=None
        """
        res_type = "pdd.order.list.get"
        self.type = res_type
        for k, v in kwargs.items():
            setattr(self, k, v)
        params, pdd_dict = self.splice_str()

        url = self.urlencode_data(params, pdd_dict)
        return self.response_json(url=url)

    def pdd_order_information_get(self, order_sn=None):
        """
        获取订单详情
        """
        res_type = "pdd.order.information.get"
        self.order_sn = order_sn
        self.type = res_type
        params, pdd_dict = self.splice_str()
        url = self.urlencode_data(params, pdd_dict)
        return self.response_json(url=url)

    def pdd_order_status_get(self, order_sns=None):
        """
        订单状态
        """
        res_type = "pdd.order.status.get"
        self.order_sns = order_sns
        self.type = res_type
        params, pdd_dict = self.splice_str()
        url = self.urlencode_data(params, pdd_dict)
        return self.response_json(url=url)

    def pdd_erp_order_sync(self, **kwargs):
        """
        erp打单信息同步,
        kwargs: order_sn=None, order_state=None, waybill_no=None, logistics_id=None
        """
        res_type = "pdd.erp.order.sync"
        self.type = res_type
        for k, v in kwargs.items():
            setattr(self, k, v)
        params, pdd_dict = self.splice_str()
        url = self.urlencode_data(params, pdd_dict)
        return self.response_json(url=url)

    def pdd_order_number_list_increment_get(self, **kwargs):
        """
        订单增量接口
        kwargs: is_lucky_flag=None, order_state=None, start_updated_at=None, end_updated_at=None,page_size=None,
        page=None, refund_status=None
        """
        res_type = "pdd.order.number.list.increment.get"
        self.type = res_type
        for k, v in kwargs.items():
            setattr(self, k, v)
        params, pdd_dict = self.splice_str()
        url = self.urlencode_data(params, pdd_dict)
        return self.response_json(url=url)

    def response_json(self, url):
        res = requests.post(url=url, headers=self.headers)
        return res.json()
