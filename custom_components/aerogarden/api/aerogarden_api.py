import base64
import logging
from turtle import update
import urllib
import aiohttp

from .const import DEFAULT_HOST, LOGIN_URL, STATUS_URL, UPDATE_URL
from .exceptions import *

_LOGGER = logging.getLogger(__name__)

class AerogardenApi:
    def __init__(self, session: aiohttp.ClientSession, username: str, password: str, host:str=None):
        self._session = session
        self._username = urllib.parse.quote(username)
        self._password = urllib.parse.quote(password)
        self._host = host if host else DEFAULT_HOST
        self._userid = None
        self._data = None

        self.gardens = []

        self._headers = {
            "User-Agent": "HA-Aerogarden/0.1",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    @property
    def is_logged_in(self):
        return True if self._userid else False

    @property
    def gardens(self):
        return self._data.keys()

    def garden_name(self, macaddr):
        multi_garden = self.garden_property(macaddr, "chooseGarden")
        if not multi_garden:
            return self.garden_property(macaddr, "plantedName")
        multi_garden_label = "left" if multi_garden == 0 else "right"
        return self.garden_property(macaddr, "plantedName") + "_" + multi_garden_label

    def garden_property(self, macaddr, field):
        if macaddr not in self._data:
            return None
        if field not in self._data[macaddr]:
            return None

        return self._data[macaddr].get(field, None)

    async def login(self):
        post_data = "mail=" + self._username + "&userPwd=" + self._password
        url = self._host + LOGIN_URL

        try:
            async with self._session.post(url, data=post_data, headers=self._headers) as r:
                response = await r.json()

                userid = response["code"]
                if userid > 0:
                    self._userid = str(userid)
                else:
                    raise AerogardenServerError(f"Login call returned unexpected response {response}")
        except AerogardenException as ex:
            _LOGGER.exception("Error communicating with Aerogarden API", exc_info=ex)
            raise
        except Exception as ex:
            _LOGGER.exception("Error communicating with Aerogarden API", exc_info=ex)
            raise AerogardenAuthFailedError

    async def update(self):
        data = {}
        if not self.is_logged_in:
            return

        url = self._host + STATUS_URL
        post_data = "userID=" + self._userid

        try:
            async with self._session.post(url, data=post_data, headers=self._headers) as r:
                garden_data = await r.json()

                if "Message" in garden_data:
                    raise AerogardenServerError(f"Could not update Aerogarden information: {garden_data['Message']}")
                
                for garden in garden_data:
                    if "plantedName" in garden:
                        garden["plantedName"] = base64.b64decode(garden["plantedName"]).decode(
                            "utf-8"
                        )  

                # Seems to be for multigarden config, untested, adapted from
                # https://github.com/JeremyKennedy/homeassistant-aerogarden/commit/5854477c35103d724b86490b90e286b5d74f6660
                id = garden.get("configID", None)
                garden_mac = garden["airGuid"] + "-" + ("" if id is None else str(id))
                data[garden_mac] = garden

                _LOGGER.debug("Updating data {}".format(data))
                self._data = data
                self.gardens = self._data.keys()
        except AerogardenException as ex:
            _LOGGER.exception("Error communicating with Aerogarden API", exc_info=ex)
            raise
        except Exception as ex:
            _LOGGER.exception("Error communicating with Aerogarden API", exc_info=ex)
            raise AerogardenAuthFailedError

    async def light_toggle(self, macaddr):
        """light_toggle:
        Toggles between Bright, Dimmed, and Off.
        I couldn't find any way to set a specific state, it just cycles between the three.
        """

        if not self.is_logged_in:
            return

        if macaddr not in self._data:
            return None

        post_data = {
            "airGuid": macaddr,
            "chooseGarden": self.garden_property(macaddr, "chooseGarden"),
            "userID": self._userid,
            "plantConfig": '{ "lightTemp" : %d }'
            % (self.garden_property(macaddr, "lightTemp"))
            # TODO: Light Temp may not matter, check.
        }
        url = self._host + UPDATE_URL
        _LOGGER.debug(f"Sending POST data to toggle light: {post_data}")

        try:
            async with self._session.post(url, data=post_data, headers=self._headers) as r:
                response = await r.json()

                if "code" not in response or response["code"] != 1:
                    raise AerogardenServerError(f"Toggle light call returned unexpected response {response}")
        except AerogardenException as ex:
            _LOGGER.exception("Error communicating with Aerogarden API", exc_info=ex)
            raise
        except Exception as ex:
            _LOGGER.exception("Error communicating with Aerogarden API", exc_info=ex)
            raise AerogardenAuthFailedError

        #force an update after making a change
        await update()
