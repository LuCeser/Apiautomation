# coding:utf-8
import requests

from util.handle_log import run_log as logger


class BaseRequest:

    @staticmethod
    def send_get(url, data, header=None, cookie=None):
        """
        Requests发送Get请求
        :param url：请求地址
        :param data：Get请求参数
        :param cookie：cookie参数
        :param header：header参数
        """
        response = requests.get(url=url, params=data, cookies=cookie, headers=header)
        return response

    @staticmethod
    def send_post(url, data, header=None, cookie=None):
        """
        Requests发送Post请求
        :param url：请求地址
        :param data：Post请求参数
        :param data：Post请求参数
        :param cookie：cookie参数
        :param header：header参数
        """
        response = requests.post(url=url, json=data, cookies=cookie, headers=header)
        return response

    @staticmethod
    def send_put(url, data, header=None, cookie=None):
        """
        Requests发送Put请求
        :param url：请求地址
        :param data：Put请求参数
        :param data：Put请求参数
        :param cookie：cookie参数
        :param header：header参数
        """
        response = requests.put(url=url, json=data, cookies=cookie, headers=header)
        return response

    @staticmethod
    def send_patch(url, data, header=None, cookie=None):
        """
        Requests发送Patch请求
        :param url：请求地址
        :param data：Patch请求参数
        :param data：Patch请求参数
        :param cookie：cookie参数
        :param header：header参数
        """
        response = requests.patch(url=url, json=data, cookies=cookie, headers=header)
        return response

    def run_main(self, method, url, data, header, cookie=None):
        try:
            result = ''
            if method.upper() == 'GET':
                result = self.send_get(url, data, header, cookie)
            elif method.upper() == 'POST':
                result = self.send_post(url, data['body'], header, cookie)
            elif method.upper() == 'PUT':
                result = self.send_put(url, data['body'], header, cookie)
            elif method.upper() == 'PATCH':
                result = self.send_patch(url, data['body'], header, cookie)

            return result
        except Exception as e:
            logger.exception('请求主函数调用失败：{}'.format(e))


# 实例
baseRequest = BaseRequest()
