import requests
# from requests.auth import HTTPBasicAuth
# import json

from atwork.atframework.web.common.maps.resource_maps import ResourceMaps
from atwork.atframework.tools.log.config import logger
from atwork.atframework.web.utils.utils import Utils


class BillfoldAPI:
    utils = Utils()
    rm = ResourceMaps()

    def registerByPayload(self, password, email='', user_name='', nick_name='', phone_number='', device='desktop'):
        logger.info('[AtLog] ----- API for registration by payload')
        url = self.rm.SITE_PREFIX + self.rm.REGISTER_URL
        password = str(password)
        email = str(email)
        user_name = str(user_name)
        nick_name = str(nick_name)
        phone_number = str(phone_number)
        payload = {}
        if email != '' and user_name == '' and nick_name == '' and phone_number == '':
            payload = {'email': email,
                       'policyChecked': 'true',
                       'password': password}
        elif user_name != '' and email == '' and nick_name == '' and phone_number == '':
            payload = {'userName': user_name,
                       'policyChecked': 'true',
                       'password': password}
        elif nick_name != '' and email == '' and user_name == '' and phone_number == '':
            payload = {'nickName': nick_name,
                       'policyChecked': 'true',
                       'password': password}
        elif phone_number != '' and email == '' and nick_name == '' and user_name == '':
            payload = {'phoneNumber': phone_number,
                       'policyChecked': 'true',
                       'password': password}
        else:
            assert "registration data error!!"
        response = requests.post(url, headers=self.utils.get_header(device), data=payload)
        return response

    def registerByParams(self, password, email='', user_name='', nick_name='', phone_number='', device='desktop'):
        logger.info('[AtLog] ----- API for registration by Params')
        url = self.rm.SITE_PREFIX + self.rm.REGISTER_URL
        password = str(password)
        email = str(email)
        user_name = str(user_name)
        nick_name = str(nick_name)
        phone_number = str(phone_number)
        if password == "":
            password = self.rm.TEST_PASSWORD_FOR_API
        if email != '' and user_name == '' and nick_name == '' and phone_number == '':
            url = url + "?email=" + email + "&" + "password=" + password + "?policyChecked=true"
        elif user_name != '' and email == '' and nick_name == '' and phone_number == '':
            url = url + "?userName=" + user_name + "&" + "password=" + password + "?policyChecked=true"
        elif nick_name != '' and email == '' and user_name == '' and phone_number == '':
            url = url + "?nickName=" + nick_name + "&" + "password=" + password + "?policyChecked=true"
        elif phone_number != '' and email == '' and nick_name == '' and user_name == '':
            url = url + "?phoneNumber=" + phone_number + "&" + "password=" + password + "?policyChecked=true"
        else:
            assert "registration data error!!"
        response = requests.post(url, headers=self.utils.get_header(device))
        if response.status_code != 200:
            logger.error("status code is " + str(response.status_code))
            assert False
        return response

    def loginByParams(self, password='', email='', user_name='', nick_name='', phone_number='', device='desktop'):
        logger.info('[AtLog] ----- API for login by params')
        url = self.rm.SITE_PREFIX + self.rm.LOGIN_URL
        if password == "":
            password = self.rm.TEST_PASSWORD_FOR_API
        if email != "":
            url = url + "?email=" + email + "&" + "password=" + password
        elif user_name != "":
            url = url + "?userName=" + user_name + "&" + "password=" + password
        elif nick_name != "":
            url = url + "?nickName=" + nick_name + "&" + "password=" + password
        elif phone_number != "":
            url = url + "?phoneNumber=" + phone_number + "&" + "password=" + password
        else:
            url = url + "?email=" + self.rm.TEST_USEREMAIL_FOR_API + "&" + "password=" + password

        response = requests.post(url, headers=self.utils.get_header(device))
        logger.info("JSESSIONID is " + response.cookies.get('JSESSIONID'))
        # print(response.cookies)
        return response

    def loginByPayload(self, payload=None, device='desktop'):
        logger.info('[AtLog] ----- API for login by payload')
        url = self.rm.SITE_PREFIX + self.rm.LOGIN_URL
        payload = {'email': self.rm.TEST_USEREMAIL_FOR_API,
                   'grant_type': 'password',
                   'password': self.rm.TEST_PASSWORD_FOR_API}
        response = requests.post(url, headers=self.utils.get_header(device), data=payload)
        logger.info("JSESSIONID is " + response.cookies.get('JSESSIONID'))
        # print(response.cookies.values()[0])
        return response

    def loginByParamsCashio(self, password='', email='', user_name='', nick_name='', phone_number='', device='desktop'):
        logger.info('[AtLog] ----- API for login by params cashio')
        url = self.rm.SITE_PREFIX + self.rm.CASHIO_LOGIN_URL
        if password == "":
            password = self.rm.TEST_PASSWORD_FOR_API
        if email != "":
            url = url + "?email=" + email + "&" + "password=" + password
        elif user_name != "":
            url = url + "?userName=" + user_name + "&" + "password=" + password
        elif nick_name != "":
            url = url + "?nickName=" + nick_name + "&" + "password=" + password
        elif phone_number != "":
            url = url + "?phoneNumber=" + phone_number + "&" + "password=" + password
        else:
            url = url + "?email=" + self.rm.TEST_USEREMAIL_FOR_API + "&" + "password=" + password
        response = requests.post(url, headers=self.utils.get_header(device))
        logger.info("JSESSIONID is " + response.cookies.get('JSESSIONID'))
        # print(response.cookies)
        return response

    def loginByPayloadCashio(self, payload=None, device='desktop'):
        logger.info('[AtLog] ----- API for login by payload')
        url = self.rm.SITE_PREFIX + self.rm.CASHIO_LOGIN_URL
        payload = {'email': self.rm.TEST_USEREMAIL_FOR_API,
                   'grant_type': 'password',
                   'password': self.rm.TEST_PASSWORD_FOR_API}
        response = requests.post(url, headers=self.utils.get_header(device), data=payload)
        logger.info("JSESSIONID is " + response.cookies.get('JSESSIONID'))
        # print(response.cookies.values()[0])
        return response

    def logout(self, payload=None, device='desktop'):
        logger.info('[AtLog] ----- API for logout')
        url = self.rm.SITE_PREFIX + self.rm.LOGOUT_URL
        response = requests.post(url, headers=self.utils.get_header(device), data=payload)
        return response

    def game_family_favorites(self, cookie='', payload=None, params='', device='desktop'):
        logger.info('[AtLog] ----- API for games/family/favorites?text={text}')
        url = self.rm.SITE_PREFIX + self.rm.FAMILY_FAVORITES_URL + "?text=" + params
        response = requests.get(url, headers=self.utils.get_header(device, cookie), data=payload)
        return response

    def positioning(self, cookie='', payload=None, text='', size='', mobile='false', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /positioning?&size={size}')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_URL + "?size=20000"
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def positioning_mobile_true(self, cookie='', payload=None, text='', size='', mobile='true',
                                user_agent_env='mobile'):
        logger.info('[AtLog] ----- API for /positioning?mobile={mobile}')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_URL + "?mobile=" + mobile
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def positioning_mobile_false(self, cookie='', payload=None, text='', size='', mobile='false',
                                 user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /positioning?mobile={mobile}')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_URL + "?mobile=" + mobile
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def positioning_group(self, cookie='', payload=None, text='', page='', size='', mobile='',
                          user_agent_env='desktop'):
        logger.info(
            '[AtLog] ----- API for /positioning/{group}?mobile={mobile}&text={searchtext}&page={page}&size={size}')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_URL + "/" + self.rm.FAMILY_GROUP_NAME
        if text != '':
            url = url + "&text=" + text
        if page != '':
            url = url + "&page=" + page
        if size != '':
            url = url + "&size=" + size
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def positioning_groups(self, cookie='', payload=None, text='', page='', size='', mobile='',
                           user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /positioning/groups')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_URL + "/" + "groups"
        if text != '':
            url = url + "&text=" + text
        if page != '':
            url = url + "&page=" + page
        if size != '':
            url = url + "&size=" + size
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def positioning_group_mobile_true(self, cookie='', payload=None, text='', page='', size='', mobile='true',
                                      user_agent_env='mobile'):
        logger.info(
            '[AtLog] ----- API for /positioning/{group}?mobile={mobile}&text={searchtext}&page={page}&size={size}')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_URL + "/" + self.rm.FAMILY_GROUP_NAME + "?mobile=" + mobile
        if text != '':
            url = url + "&text=" + text
        if page != '':
            url = url + "&page=" + page
        if size != '':
            url = url + "&size=" + size
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def positioning_group_mobile_false(self, cookie='', payload=None, text='', page='', size='', mobile='false',
                                       user_agent_env='desktop'):
        logger.info(
            '[AtLog] ----- API for /positioning/{group}?mobile={mobile}&text={searchtext}&page={page}&size={size}')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_URL + "/" + self.rm.FAMILY_GROUP_NAME + "?mobile=" + mobile
        if text != '':
            url = url + "&text=" + text
        if page != '':
            url = url + "&page=" + page
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def positioning_friendlyName_provider(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                                          mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /positioning/{friendlyName}/{provider}?mobile={mobile}')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_GROUP_URL + self.rm.FRIENDLY_NAME + self.rm.PROVIDER + "?mobile=" + mobile
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_family_favorites(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                               mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/family/favorites')
        url = self.rm.SITE_PREFIX + self.rm.FAMILY_FAVORITES_URL
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_family_recent(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                            mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/families/recent?limit=50')
        url = self.rm.SITE_PREFIX + self.rm.GAME_RECENT_URL + "?" + "limit=50"
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_favourites(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                         mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/favourites')
        url = self.rm.SITE_PREFIX + self.rm.GAME_FAVOURITES_URL
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_real_name(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                        mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /game/real/{name}')
        url = self.rm.SITE_PREFIX + self.rm.GAME_REAL_NAME + "60002"
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_demo_name(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                        mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /game/demo/{name}')
        url = self.rm.SITE_PREFIX + self.rm.GAME_DEMO_NAME + self.rm.GAME_DEMO_ID
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_token_real_name(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                              mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /game/token/real/{name}')
        url = self.rm.SITE_PREFIX + self.rm.GAME_TOKEN_REAL_NAME + self.rm.GAME_DEMO_ID
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def game_playing(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                     mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /game/playing')
        url = self.rm.SITE_PREFIX + self.rm.GAME_PLAYING
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def family_token_real_id(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                             mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /family/token/real/{id}')
        url = self.rm.SITE_PREFIX + self.rm.FAMILY_TOKEN_REAL_ID + self.rm.FAMILY_ID
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def family_real_launch_id(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                              mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /family/real/launch/{id}')
        url = self.rm.SITE_PREFIX + self.rm.FAMILY_REAL_LAUNCH_ID + self.rm.FAMILY_ID
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def family_demo_launch_id(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                              mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /family/demo/launch/{id}')
        url = self.rm.SITE_PREFIX + self.rm.FAMILY_DEMO_LAUNCH_ID + self.rm.FAMILY_ID
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_favourites_add(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                             mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/favourites/add?gameId=161033')
        url = self.rm.SITE_PREFIX + self.rm.GAME_FAVOURITES_URL + "/add?gameId=" + self.rm.GAME_ID
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.post(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_favourites_delete(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                                mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/favourites/remove?gameId=161033')
        url = self.rm.SITE_PREFIX + self.rm.GAME_FAVOURITES_URL + "/remove?gameId=" + self.rm.GAME_ID
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.post(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_family_add_favorites(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                                   mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/family/favorites?familyId=75585')
        url = self.rm.SITE_PREFIX + self.rm.FAMILY_FAVORITES_URL + "?familyId=" + self.rm.FAMILY_ID
        if text != '':
            url = url + "&text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.post(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_family_favorites_delete(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                                      mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/family/favorites?familyId=75585')
        url = self.rm.SITE_PREFIX + self.rm.FAMILY_FAVORITES_URL + "?familyId=" + self.rm.FAMILY_ID
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.delete(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_groups(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                     mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /groups')
        url = self.rm.SITE_PREFIX + self.rm.GAMES_GROUPS
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_menu(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                   mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /groups')
        url = self.rm.SITE_PREFIX + self.rm.GAMES_MENU
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_group(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                    mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/{group}')
        url = self.rm.SITE_PREFIX + self.rm.GAMES + "/Slots"
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_allmobileanddesktop_recentgames(self, cookie='', payload=None, text='', friendlyName='', provider='',
                                              size='',
                                              mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/allMobileAndDesktop/recentGames')
        url = self.rm.SITE_PREFIX + self.rm.GAMES_ALLMOBILE_AND_DESKTOP_RECENTGAMES
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_group_blacklist(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                              mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /games/{group}/blacklist')
        url = self.rm.SITE_PREFIX + self.rm.GAMES_GROUPS_BLACKLIST
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def games_providerId(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                         mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /{providerId}/games')
        url = self.rm.SITE_PREFIX + self.rm.GAME_PROVIDER_ID
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def game_rate(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                  mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /rate/game?gameId=161033&rating=2')
        url = self.rm.SITE_PREFIX + self.rm.GAME_RATE + "?gameId=" + self.rm.GAME_ID + "&rating=2"
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.post(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def player_rtp(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                   mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /player/rtp')
        url = self.rm.SITE_PREFIX + self.rm.PLAYER_RTP
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def jackpots(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                 mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /jackpots?currency=EUR')
        url = self.rm.SITE_PREFIX + self.rm.JACKPOTS + "?currency=" + self.rm.CURRENCY
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def total_jackpots(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                       mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /totalJackpots?currency=EUR')
        url = self.rm.SITE_PREFIX + self.rm.TOTAL_JACKPOTS + "?currency=" + self.rm.CURRENCY
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def positioning_slug_provider(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                                  mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /positioning/what-a-hoot/1')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_GROUP_URL + self.rm.SLUG_PROVIDER
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def positioning_all(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                        mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /positioning/all')
        url = self.rm.SITE_PREFIX + self.rm.POSITIONING_URL + "/all"
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def game_providers(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                       mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /game/providers')
        url = self.rm.SITE_PREFIX + self.rm.GAME_PROVIDERS
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def game_winners(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                     mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /winners')
        url = self.rm.SITE_PREFIX + self.rm.GAME_WINNERS
        if text != '':
            url = url + "?text=" + text
        if size != '':
            url = url + "&size=" + size
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def player_balance(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                       mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for /player/balance')
        url = self.rm.SITE_PREFIX + self.rm.PLAYER_BALANCE
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def player_affiliate_get(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                             mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for get /player/affiliate')
        url = self.rm.SITE_PREFIX + self.rm.PLAYER_AFFILIATE
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def player_my_affiliate_get(self, cookie='', payload=None, text='', friendlyName='', provider='', size='',
                                mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for get /player/myAffiliate')
        url = self.rm.SITE_PREFIX + self.rm.PLAYER_MY_AFFILIATE
        print(url)
        response = requests.get(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def player_my_affiliate_post(self, cookie='', payload=None, myAffiliateToken='', btag='',
                                 myAffiliateId='', mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for post /player/myAffiliate')
        url = self.rm.SITE_PREFIX + self.rm.PLAYER_MY_AFFILIATE
        myAffiliateToken = 'some-myaffiliate-id'
        myAffiliateId = 'some-myaffiliate-id'
        btag = 'some-myaffiliate-id'
        if myAffiliateToken != '':
            url = url + "?myAffiliateToken=" + myAffiliateToken
        if myAffiliateId != '':
            url = url + "&myAffiliateId=" + myAffiliateId
        if btag != '':
            url = url + "&btag=" + btag
        print(url)
        response = requests.post(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def player_affiliate_post(self, cookie='', payload=None, myAffiliateToken='', btag='',
                              myAffiliateId='', mobile='', user_agent_env='desktop'):
        logger.info('[AtLog] ----- API for post /player/affiliate')
        url = self.rm.SITE_PREFIX + self.rm.PLAYER_AFFILIATE
        myAffiliateToken = 'some-affiliate-id'
        myAffiliateId = 'some-affiliate-id'
        btag = 'some-affiliate-id'
        if myAffiliateToken != '':
            url = url + "?myAffiliateToken=" + myAffiliateToken
        if myAffiliateId != '':
            url = url + "&myAffiliateId=" + myAffiliateId
        if btag != '':
            url = url + "&btag=" + btag
        print(url)
        response = requests.post(url, headers=self.utils.get_header(user_agent_env, cookie), data=payload)
        return response

    def get_player_vouchers(self, cookie='', page='', size='', status='', start_time='', end_time='', device='desktop'):
        logger.info('[AtLog] ----- API for registration by Params')
        url = self.rm.SITE_PREFIX + self.rm.PALYER_VOUCHER_URL
        if page != "" or size != "" or status != "" or start_time != "" or end_time != "":
            url = url + "&"
            if page != "":
                url = url + "?page=" + page
            if size != "":
                url = url + "?size=" + size
            if status != "":
                url = url + "?status=" + status
            if start_time != "":
                url = url + "?startTime=" + start_time
            if end_time != "":
                url = url + "?endTime=" + end_time
        else:
            logger.info("[AtLog] ----- no parameter insert-----")
        response = requests.get(url, headers=self.utils.get_header(device, cookie))
        if response.status_code != 200:
            logger.error("status code is " + str(response.status_code))
            assert False
        return response

    def claim_player_voucher(self, voucher_id, cookie='', device='desktop'):
        logger.info('[AtLog] ----- API for claim voucher')
        url = self.rm.SITE_PREFIX + self.rm.CLAIM_PLAYER_VOUCHER_URL + str(voucher_id)
        response = requests.post(url, headers=self.utils.get_header(device, cookie))
        if response.status_code != 200:
            logger.error("status code is " + str(response.status_code))
            assert False
        return response

    def cancel_player_voucher(self, voucher_id, cookie='', device='desktop'):
        logger.info('[AtLog] ----- API for cancel voucher')
        url = self.rm.SITE_PREFIX + self.rm.CANCEL_PLAYER_VOUCHER_URL + str(voucher_id)
        response = requests.post(url, headers=self.utils.get_header(device, cookie))
        if response.status_code != 200:
            logger.error("status code is " + str(response.status_code))
            assert False
        return response

    def delete_player_voucher(self, voucher_id, cookie='', device='desktop'):
        logger.info('[AtLog] ----- API for delete voucher')
        url = self.rm.SITE_PREFIX + self.rm.DELETE_PLAYER_VOUCHER_URL + str(voucher_id)
        response = requests.post(url, headers=self.utils.get_header(device, cookie))
        if response.status_code != 200:
            logger.error("status code is " + str(response.status_code))
            assert False
        return response