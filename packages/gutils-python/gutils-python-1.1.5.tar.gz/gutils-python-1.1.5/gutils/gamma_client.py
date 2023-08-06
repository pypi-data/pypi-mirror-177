import requests
from gutils.misc import retry
from gutils.config.settings import GAMMA_USER, GAMMA_PASSWORD


class GammaClient:
    def __init__(self, gamma_user=GAMMA_USER, gamma_pwd=GAMMA_PASSWORD):
        self.__host_header = 'https://api-restricted.stg-myteksi.com/api/frontend/v1/'
        self.__headers = {'referer': 'https://gamma.stg-myteksi.com/',
                          'origin': 'https://gamma.stg-myteksi.com',
                          'x-requested-with': 'XMLHttpRequest ',
                          'X-Api-Source': 'gamma-int-api',
                          'content-type': 'application/json',
                          'cache-control': 'no-cache',
                          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
                          'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                          'accept': 'application/json, text/plain, */*',
                          'accept-encoding': 'gzip, deflate, br',
                          }
        self.__token = self.login(gamma_user, gamma_pwd)
        self.__headers.update({'Authorization': self.__token,
                               'cookie': 'authorization=%s;' % self.__token})

    def login(self, gamma_user, gamma_pwd):
        url = '{}auth/jumpcloud_login'.format(self.__host_header)
        payload = {
            'username': gamma_user,
            'password': gamma_pwd,
            'app_id': 'gamma',
        }
        response = requests.post(url, json=payload, headers=self.__headers)
        if response.text:
            return response.json()['access_token']
        else:
            raise Exception('Failed to login Gamma')

    @retry(retries=5, duration=2)
    def get_pax_tac(self, pax_id):
        url = '{}passengers/{}/request_tac'.format(self.__host_header, pax_id)
        response = requests.get(url, headers=self.__headers)
        try:
            tac = response.json()['tac']
            if tac:
                return tac
        except:
            pass
        else:
            raise Exception("=====Tried 5 times, Fail to get the pax {} tac======".format(pax_id))

    def get_pax_id_by_phone_number(self, phone_number):
        url = '{}passengers/search?page=1&sort=email+asc'.format(self.__host_header)
        data = {'phone_number': {'eq': phone_number}}
        response = requests.post(url, headers=self.__headers, json=data)
        try:
            id = response.json()['results'][0]['id']
            if id:
                return str(id)
        except:
            pass
        else:
            raise Exception("=====Fail to get the pax id======")

    @retry(retries=5, duration=2)
    def get_new_pax_tac(self, phone_number):
        url = '{}passengers/lookup_otp'.format(self.__host_header)
        data = {"phone_number": phone_number}
        response = requests.post(url, headers=self.__headers, json=data)
        try:
            tac = response.json()['otp']
            if tac:
                return tac
        except:
            pass
        else:
            raise Exception("=====Tried 5 times, Fail to get the pax tac======")

    def get_pax_balance(self, pax_id):
        url = '{}passengers/{}'.format(self.__host_header, pax_id)
        response = requests.get(url, headers=self.__headers)
        if response.text:
            return response.json()['result']['credit_balance'][0]['balance']
        else:
            raise Exception("GPC balance is 0")

    def get_pax_name(self, pax_id):
        url = '{}passengers/{}'.format(self.__host_header, pax_id)
        response = requests.get(url, headers=self.__headers)
        if response.text:
            return response.json()['result']['name']
        else:
            raise Exception('Failed to get the pax {} name'.format(pax_id))

    def get_pax_email(self, pax_id):
        url = '{}passengers/{}/edit'.format(self.__host_header, pax_id)
        response = requests.get(url, headers=self.__headers)
        if response.text:
            return response.json()['fields']['email']['value']
        else:
            raise Exception('Failed to get the pax {} email'.format(pax_id))

    def check_pax_ban(self, pax_id):
        url = '{}passengers/{}'.format(self.__host_header, pax_id)
        response = requests.get(url, headers=self.__headers)
        return response.json()['result']['banned']


if __name__ == '__main__':
    gc = GammaClient()
    print(gc.get_pax_tac('93858071'))
    print(gc.get_pax_name('93858071'))
    print(gc.get_pax_email('93858071'))
