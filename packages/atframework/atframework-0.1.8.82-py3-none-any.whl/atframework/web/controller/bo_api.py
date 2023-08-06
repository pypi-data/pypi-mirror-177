'''
Created on Nov 14, 2022

@author: Siro

'''
import json

import requests
# from requests.auth import HTTPBasicAuth
# import json

from atwork.atframework.web.common.maps.resource_maps import ResourceMaps
from atwork.atframework.tools.log.config import logger
from atwork.atframework.web.utils.utils import Utils


class BoAPI:
    utils = Utils()
    rm = ResourceMaps()

    def create_player_voucher(self, api_user_id, site_id, hash, userid, turnover_factor, amount, amount_type, type,
                              validity_duration, device='desktop'):
        logger.info('[AtLog] ----- API for create player voucher ----- ')
        url = self.rm.BO_API_SITE_PREFIX + self.rm.BO_API_VOUCHER_URL + "?apiUserId=" + api_user_id + "&siteId=" + site_id + "&hash=" + hash

        bonus = {
            "amount": int(amount),
            "amountType": amount_type,
            "type": type,
            "validityDuration": validity_duration
        }
        payload = json.dumps({
            "userId": int(userid),
            "turnoverFactor": int(turnover_factor),
            "bonus": bonus
        })

        response = requests.post(url, headers=self.utils.get_header(device), data=payload)
        if response.status_code != 200:
            logger.error("status code is " + str(response.status_code))
            assert False
        return response
