'''
Created on Mar 25, 2022

@author: Siro

'''

import json
from atwork.atframework.tools.log.config import logger
from atwork.atframework.web.common.maps.resource_maps import ResourceMaps

class ApiResponseChecking(object):
    rm = ResourceMaps()

    """
    Check response for registration

    {
    "success": true,
    "t": "bb13cf8e15fd435a91e1b41562dfcb51"
    }

    """

    def check_response_registration(self, response_data):
        # json_data = json.dumps(response_data)
        families_dic = json.loads(response_data)

        logger.info(families_dic)

        registration_key_list = []
        registration_value_list = []
        for i, j in families_dic.items():
            registration_key_list.append(i)
            registration_value_list.append(j)
        # families key should be games
        for k in range(len(registration_key_list)):
            if registration_key_list[k] == "success":
                result = (registration_value_list[k])
                return result
        return False

    """
    Check response for login
    """
    def check_response_login(self, response_data):
        # json_data = json.dumps(response_data)
        families_login_dic = json.loads(response_data)

        logger.info(families_login_dic)

        login_key_list = []
        login_value_list = []
        for i, j in families_login_dic.items():
            login_key_list.append(i)
            login_value_list.append(j)
        # families key should be games
        for k in range(len(login_key_list)):
            if login_key_list[k] == "success":
                result = (login_value_list[k])
                return result
        return False

    """
    Check response for logout
    """
    def check_response_logout(self, response_data):
        # json_data = json.dumps(response_data)
        families_logout_dic = json.loads(response_data)

        logger.info(families_logout_dic)

        logout_key_list = []
        logout_value_list = []
        for i, j in families_logout_dic.items():
            logout_key_list.append(i)
            logout_value_list.append(j)
        # families key should be games
        for k in range(len(logout_key_list)):
            if logout_key_list[k] == "success":
                result = (logout_value_list[k])
                return result
        return False

    """
    Check response for games/family/favorites
    """

    def check_response_game_family_favorites(self, response_data):
        # json_data = json.dumps(response_data)
        families_dic = json.loads(response_data)

        families_key_list = []
        families_value_list = []
        for i, j in families_dic.items():
            families_key_list.append(i)
            families_value_list.append(j)
        # families key should be games
        assert families_key_list[0] == 'games'

        # print(key_list)
        family = families_value_list[0][0]

        family_key_list = []
        for k in family:
            family_key_list.append(k)
        logger.info(family_key_list)

        list_string = ['familyId', 'name', 'status', 'provider', 'translations']
        string_set = set(family_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    """
    Check response for /positioning
    """

    def check_response_positioning_group(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)
        positionings_key_list = []
        positionings_value_list = []
        for i, j in positioning_dic.items():
            positionings_key_list.append(i)
            positionings_value_list.append(j)
        # group's key should be Jackpots
        assert positionings_value_list[0] == 'Jackpots'

        logger.info(positionings_key_list)
        list_string = ['name', 'friendlyName', 'slug', 'tags', 'classifyName', 'classifyId', 'type', 'status', 'families',
                       'count', 'size', 'currentPage', 'pageCount']
        string_set = set(positionings_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    """
    Check response for /positioning/{group}
    """

    def check_response_positioning_not_logged_in(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)

        positioning_keys_list = []
        positioning_values_list = []
        for i, j in positioning_dic.items():
            positioning_keys_list.append(i)
            positioning_values_list.append(j)
        # positioning key should be positioning
        assert positioning_keys_list[0] == 'positioning'

        # print(positioning)
        positioning = positioning_values_list[0][0]
        assert positioning.get("name") == 'automation group'

        positioning_key_list = []
        for k in positioning:
            positioning_key_list.append(k)

        print(positioning_key_list)
        list_string = ['name', 'friendlyName', 'slug', 'tags', 'classifyName', 'classifyId', 'type', 'status', 'order', 'families', 'count', 'size', 'currentPage', 'pageCount']
        string_set = set(positioning_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_positioning_logged_in(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)
        positioning_keys_list = []
        positioning_values_list = []
        for i, j in positioning_dic.items():
            positioning_keys_list.append(i)
            positioning_values_list.append(j)
        # positioning key should be positioning
        assert positioning_keys_list[0] == 'positioning'

        # print(positioning)
        positioning = positioning_values_list[0][0]
        assert positioning.get("name") == 'Taiwan'

        positioning_key_list = []
        for k in positioning:
            positioning_key_list.append(k)

        print(positioning_key_list)
        list_string = ['name', 'friendlyName', 'slug', 'tags', 'classifyName', 'classifyId', 'type', 'status', 'order', 'families', 'count', 'size', 'currentPage', 'pageCount']
        string_set = set(positioning_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_groups_not_logged_in(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)

        positioning_keys_list = []
        positioning_values_list = []
        for i, j in positioning_dic.items():
            positioning_keys_list.append(i)
            positioning_values_list.append(j)
        # positioning key should be positioning
        assert positioning_keys_list[0] == 'groups'

        # print(positioning)
        positioning = positioning_values_list[0][0]
        assert positioning.get("name") == 'automation group'

        positioning_key_list = []
        for k in positioning:
            positioning_key_list.append(k)

        print(positioning_key_list)
        list_string = ['name', 'friendlyName', 'slug', 'tags', 'classifyName', 'classifyId', 'type', 'status', 'order', 'families', 'count', 'size', 'currentPage', 'pageCount']
        string_set = set(positioning_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_groups_logged_in(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)

        positioning_keys_list = []
        positioning_values_list = []
        for i, j in positioning_dic.items():
            positioning_keys_list.append(i)
            positioning_values_list.append(j)
        # positioning key should be positioning
        assert positioning_keys_list[0] == 'groups'

        # print(positioning)
        positioning = positioning_values_list[0][0]
        assert positioning.get("name") == 'Taiwan'

        positioning_key_list = []
        for k in positioning:
            positioning_key_list.append(k)

        print(positioning_key_list)
        list_string = ['name', 'friendlyName', 'slug', 'tags', 'classifyName', 'classifyId', 'type', 'status', 'order', 'families', 'count', 'size', 'currentPage', 'pageCount']
        string_set = set(positioning_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_positioning_friendly_name_provider(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)
        positioning_keys_list = []
        positioning_values_list = []
        for i, j in positioning_dic.items():
            positioning_keys_list.append(i)
            positioning_values_list.append(j)
        # positioning friendly name should be [2]
        friendly_name = positioning_values_list[2]
        assert friendly_name == 'Book Of Dead'

        list_string = ['position', 'familyId', 'familyName', 'provider', 'providerName', 'tags', 'status', 'translations', 'games']
        string_set = set(positioning_keys_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    """
    Check response for /games/family/favorites
    """
    def check_response_games_family_favorites(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        games_values_list = []
        for i, j in games_dic.items():
            games_keys_list.append(i)
            games_values_list.append(j)
        assert games_keys_list[0] == 'games'

        game_family_id = []
        for game_dic in games_values_list[0]:
            game_family_id.append(game_dic.get("familyId"))

        print(game_family_id)
        list_string = [75559, 73609, 70021, 63911, 57957, 57931, 41343, 30163, 18801, 12015, 5307, 2187]
        string_set = set(game_family_id)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    """
    Check response for /games/family/favorites?text=hello
    """
    def check_response_games_family_favorites_text(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)

        for game_dic in games_dic['games']:
            game_family_id = game_dic['familyId']

        assert game_family_id == 30163
        return True

    """
    Check response for /games/families/recent?limit=50
    """
    def check_response_games_family_recent(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        game_family_recent = []
        for game_dic in games_dic:
            game_family_recent.append(game_dic["familyId"])

        list_string = [71659, 71061, 57957, 59387, 12015, 43137, 55903, 6529, 52861, 54447, 10975, 21505, 3955, 57931,
                       41343, 61649, 14537, 45919, 76495, 71503, 47037, 54707, 5307]
        string_set = set(game_family_recent)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    """
    Check response for /games/favourites
    """
    def check_response_games_favourites(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        game_family_recent = []
        for game_dic in games_dic.values():
            for game_id in game_dic:
                game_family_recent.append(game_id["gameId"])

        list_string = [55465, 55595, 55609, 55610, 55621, 60015, 60037, 60045, 60267, 60405, 60427, 60536, 60542,
                       60561, 60567, 60573, 60574, 60579, 162658, 170368, 170386, 510051, 700009, 700031, 800001,
                       800035]
        string_set = set(game_family_recent)
        result = all([word in game_family_recent for word in list_string])
        assert result
        return True

    def check_response_games_favourites_if_existed(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        game_family_recent = []
        for game_dic in games_dic.values():
            for game_id in game_dic:
                game_family_recent.append(game_id["gameId"])

        list_string = [161033]
        string_set = set(game_family_recent)
        result = all([word in game_family_recent for word in list_string])
        if result == False:
            return True
        else:
            return False

    def check_response_games_post_status(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_family_status = []
        for game_family_status in games_dic.keys():
            games_family_status.append(game_family_status)

        list_string = ['success']
        result = all([word in games_family_status for word in list_string])
        assert result
        return True
    
    def check_response_games_family_favorites_if_existed(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        games_values_list = []
        for i, j in games_dic.items():
            games_keys_list.append(i)
            games_values_list.append(j)
        assert games_keys_list[0] == 'games'

        game_family_id = []
        for game_dic in games_values_list[0]:
            game_family_id.append(game_dic.get("familyId"))

        list_string_new_add = [75585]
        string_set = set(game_family_id)
        result = all([word in string_set for word in list_string_new_add])
        if result == False:
            return True
        else:
            return False

    def check_response_games_real_name(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)
        print(games_keys_list)
        assert games_keys_list[0] == 'url'
        return True

    def check_response_games_demo_name(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)
        assert games_keys_list[0] == 'url'
        game_id = games_dic.get('gameId')
        list_string = int(60721)
        if game_id == list_string:
            return True
        else:
            return False

    def check_response_token_real_name(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)
        assert games_keys_list[0] == 'token'
        return True

    def check_response_game_playing(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)
        assert games_keys_list[0] == 'success'
        return True

    def check_response_family_launch_id(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)
        assert games_keys_list[0] == 'url'
        return True

    def check_response_games_groups(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)

        assert games_keys_list[0] == 'groups'
        return True

    def check_response_games_menu(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)
        assert games_keys_list[0] == 'menu'
        return True

    def check_response_games_name(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        games_values_list = []
        game = []
        gamekey = []

        for i,j in games_dic.items():
            games_keys_list.append(i)
            games_values_list.append(j)
        assert games_keys_list[0] == 'games'

        for game_dic in games_values_list[0]:
            game.append(game_dic)

        for key in game[0].keys():
            gamekey.append(key)

        assert gamekey[0] == 'name'
        return True

    def check_response_games_group_blacklist(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        games_values_list = []
        game_key = []

        for i,j in games_dic.items():
            games_keys_list.append(i)
            games_values_list.append(j)
        assert games_keys_list[0] == 'games'

        for game in games_values_list[0][0].keys():
            game_key.append(game)

        list_string = ['gameConfig', 'blockedCountries', 'excludedCountries']
        string_set = set(game_key)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_games_providerId(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)

        list_string = ['count', 'size', 'currentPage', 'pageCount', 'games']
        string_set = set(games_keys_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_player_rtp(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)

        list_string = ['today', 'lastMonth', 'lifeTime']
        string_set = set(games_keys_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_jackpots(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_list = json.loads(response_data)
        positionings_key_list = []
        for i in positioning_list[0]:
            positionings_key_list.append(i)

        list_string = ['name', 'friendlyName', 'gameId', 'provider', 'supplier', 'gameFamilyId', 'ratio',
                       'gameDisabled', 'promoMoneyEnabled', 'hideDemoUrl', 'newGame', 'freeSpins', 'jackpotGame']
        string_set = set(positionings_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_total_jackpots(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_list = json.loads(response_data)
        if positioning_list != []:
            positionings_key_list = []
            for i in positioning_list[0]:
               positionings_key_list.append(i)
               list_string = ['amount', 'currency', 'createdTime', 'provider']
               string_set = set(positionings_key_list)
               result = all([word in string_set for word in list_string])
               assert result
               return True
        else:
            list_string = []
            string_set = set(positioning_list)
            result = all([word in string_set for word in list_string])
            assert result
            return True

    def check_response_slug_provider(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)
        positionings_key_list = []
        for i in positioning_dic:
            positionings_key_list.append(i)

        list_string = ['position', 'familyId', 'familyName', 'provider', 'providerName', 'tags', 'status',
                       'translations', 'games']
        string_set = set(positionings_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_positioning_all(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)
        positioning_keys_list = []
        positioning_values_list = []
        for i, j in positioning_dic.items():
            positioning_keys_list.append(i)
            positioning_values_list.append(j)
        # positioning key should be positioning
        assert positioning_keys_list[0] == 'positioning'

        # print(positioning)
        positioning = positioning_values_list[0][0]
        assert positioning.get("name") == 'test11111'

        positioning_key_list = []
        for k in positioning:
            positioning_key_list.append(k)

        print(positioning_key_list)
        list_string = ['name', 'friendlyName', 'slug', 'tags', 'classifyName', 'classifyId', 'type', 'status',
                       'order', 'families', 'count', 'size', 'currentPage', 'pageCount']
        string_set = set(positioning_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_game_providers(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_list = json.loads(response_data)
        positionings_key_list = []
        for i in positioning_list[0]:
            positionings_key_list.append(i)

        list_string = ['providerId', 'name']
        string_set = set(positionings_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_game_winners(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_list = json.loads(response_data)
        if positioning_list != []:
            positionings_key_list = []
            for i in positioning_list[0]:
               positionings_key_list.append(i)
               list_string = ['productId', 'name', 'provider', 'nickName', 'createdTime', 'amount', 'currency', 'country']
               string_set = set(positionings_key_list)
               result = all([word in string_set for word in list_string])
               assert result
               return True
        else:
            list_string = []
            string_set = set(positioning_list)
            result = all([word in string_set for word in list_string])
            assert result
            return True

    def check_response_player_balance(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_list = json.loads(response_data)
        positionings_key_list = []
        for i in positioning_list:
            positionings_key_list.append(i)

        list_string = ['currency', 'balance', 'cash', 'promo', 'rebate', 'rebatePoints', 'savingCash', 'cashBack',
                       'availableWithdrawal', 'statusPoints', 'awardPoints', 'currentTurnover', 'totalTurnover',
                       'bonusDeduction', 'firstDepositDone', 'playerTimeExpired', 'realityCheckReached', 'jackpotWin']
        string_set = set(positionings_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_player_affiliate_get(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)
        assert games_keys_list[0] == 'success'
        return True

    def check_response_player_affiliate_post(self, response_data):
        # json_data = json.dumps(response_data)
        games_dic = json.loads(response_data)
        games_keys_list = []
        for i in games_dic.keys():
            games_keys_list.append(i)

        list_string = ['success']
        string_set = set(games_keys_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    def check_response_get_voucher(self, response_json):
        logger.info(response_json)
        voucher_id = str(response_json["vouchers"][0]["voucherId"])
        if voucher_id != '':
            return True
        return False

    def check_response_claim_player_voucher(self, response_json):
        logger.info(response_json)
        claim_result = response_json["success"]
        if claim_result is True:
            return True
        return False

    def check_response_cancel_player_voucher(self, response_json):
        logger.info(response_json)
        cancel_result = response_json["success"]
        if cancel_result is True:
            return True
        return False

    def check_response_delete_player_voucher(self, response_json):
        logger.info(response_json)
        delete_result = response_json["success"]
        if delete_result is True:
            return True
        return False
