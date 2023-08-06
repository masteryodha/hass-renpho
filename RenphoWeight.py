import requests

import json
import time
import datetime
from homeassistant.const import MASS_KILOGRAMS, MASS_POUNDS
from .types import Measurements
#from aiohttp import ClientSession

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode

import logging

_LOGGER = logging.getLogger(__name__)

class RenphoWeight():
    def __init__ (self, email, password, public_key, session, unit_of_measurements = MASS_KILOGRAMS):
        self.email = email
        self.password = password
        self.session = session
        self.public_key = public_key
        self.session_key = None
        self.user_id = None
        self.account_name = None

        if unit_of_measurements != MASS_KILOGRAMS : 
            self.unit_of_measurements = MASS_POUNDS
        else:
            self.unit_of_measurements = MASS_KILOGRAMS

    async def _async_auth(self):
        
        try:
            key = RSA.importKey(self.public_key)
            cipher = PKCS1_v1_5.new(key)
            newPassword = b64encode(cipher.encrypt(bytes(self.password, "utf-8")))
            
            data = {
                'secure_flag': 1,
                'email': self.email,
                'password': newPassword.decode('utf-8')
            }
               
            url = 'https://renpho.qnclouds.com/api/v3/users/sign_in.json?app_id=Renpho'
            resp = await self.session.post(url, data=data)
            data = await resp.json(content_type=None)
            
            #TODO : Tester le retour et gérer l'erreur
            self.session_key = data['terminal_user_session_key']
            self.user_id = data['id']
            self.account_name = data['account_name']
            _LOGGER.debug('RENPHO WEIGHT - session_key = {}'.format(self.session_key))
            _LOGGER.debug('RENPHO WEIGHT - account_name = {}'.format(self.account_name))
            _LOGGER.debug('RENPHO WEIGHT - user_id = {}'.format(self.user_id))
        except Exception as e:
            _LOGGER.error('RENPHO WEIGHT - Erreur on authentication : {}'.format(e))
            

    async def _async_getMeasurements(self):
        
        try: 
            #Todo retourner une entité Measurements à la place du json direct.
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=30)
            week_ago = int(time.mktime(week_ago.timetuple()))

            url = 'https://renpho.qnclouds.com/api/v2/measurements/list.json?user_id=' + str(self.user_id) + '&last_at=' + str(week_ago) + '&locale=en&app_id=Renpho&terminal_user_session_key=' + str(self.session_key)
            resp = await self.session.get(url)
            data = await resp.json(content_type=None)
            _LOGGER.debug('RENPHO WEIGHT - Got Measurements successfully')
                        
            if (len(data['last_ary']) == 0): 
              _LOGGER.info('RENPHO WEIGHT - No measurements in the last 30 days')
              return Measurements(weight = 0, 
                                created_at = datetime.datetime.now(),
                                bodyfat = 0,
                                water = 0,
                                bmr = 0,
                                bodyage = 0,
                                bone = 0,
                                subfat = 0,
                                visfat = 0,
                                bmi = 0,
                                sinew = 0,
                                protein = 0,
                                fat_free_weight = 0,
                                muscle = 0,
                                user_id = self.user_id,
                                account_name = self.account_name,
                                unit_of_measurements = self.unit_of_measurements)
            
            parsed_data = data['last_ary'][0]
            _LOGGER.info('RENPHO WEIGHT - Got Measurements successfully')
            
            #Return the first of the last measurements on the renpho API.  Should be the latest for the main user.
            return Measurements(weight = parsed_data['weight'], 
                                created_at = parsed_data['created_at'],
                                bodyfat = parsed_data['bodyfat'],
                                water = parsed_data['water'],
                                bmr = parsed_data['bmr'],
                                bodyage = parsed_data['bodyage'],
                                bone = parsed_data['bone'],
                                subfat = parsed_data['subfat'],
                                visfat = parsed_data['visfat'],
                                bmi = parsed_data['bmi'],
                                sinew = parsed_data['sinew'],
                                protein = parsed_data['protein'],
                                fat_free_weight = parsed_data['fat_free_weight'],
                                muscle = parsed_data['muscle'],
                                user_id = self.user_id,
                                account_name = self.account_name,
                                unit_of_measurements = self.unit_of_measurements
                                )
        except Exception as e:
            _LOGGER.error('RENPHO WEIGHT - Erreur when getting measurements : {}'.format(e))
            
    async def async_getInfo(self):
        await self._async_auth()
        return await self._async_getMeasurements()
        