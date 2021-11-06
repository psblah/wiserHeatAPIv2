from .device import _WiserDevice, _WiserBattery
from .helpers import _to_wiser_temp, _from_wiser_temp
from .rest_controller import _WiserRestController
from .const import (
    WISERROOMSTAT
)

import inspect
import logging

_LOGGER = logging.getLogger(__name__)


class _WiserRoomStat(_WiserDevice):
    """Class representing a Wiser Room Stat device"""

    def __init__(self, data, device_type_data):
        super().__init__(data)
        self._data = data
        self._device_type_data = device_type_data
        self._device_lock_enabled = data.get("DeviceLockEnabled", False)
        self._indentify_active = data.get("IdentifyActive", False)

    def _send_command(self, cmd: dict):
        """
        Send control command to the room stat
        param cmd: json command structure
        return: boolen - true = success, false = failed
        """
        rest = _WiserRestController()
        result = rest._send_command(WISERROOMSTAT.format(self.id), cmd)
        if result:
            _LOGGER.info(
                "Wiser room stat - {} command successful".format(
                    inspect.stack()[1].function
                )
            )
        return result

    @property
    def battery(self):
        """Get the battery information for the room stat"""
        return _WiserBattery(self._data)

    @property
    def current_humidity(self) -> int:
        """Get the current humidity reading of the room stat"""
        return self._device_type_data.get("MeasuredHumidity", 0)

    @property
    def current_target_temperature(self) -> float:
        """Get the room stat current target temperature setting"""
        return _from_wiser_temp(self._device_type_data.get("SetPoint", 0))

    @property
    def current_temperature(self) -> float:
        """Get the current temperature measured by the room stat"""
        return _from_wiser_temp(self._device_type_data.get("MeasuredTemperature", 0))

    @property
    def device_lock_enabled(self) -> bool:
        """Get or set room stat device lock"""
        return self._device_lock_enabled

    @device_lock_enabled.setter
    def device_lock_enabled(self, enable: bool):
        """
        Set the device lock setting on the room stat
        param enabled: turn on or off
        """
        return self._send_command({"DeviceLockEnabled": enable})

    @property
    def identify(self) -> bool:
        """Get or set if the room stat identify function is enabled"""
        return self._indentify_active

    @identify.setter
    def identify(self, enable: bool = False):
        """
        Set the identify function setting on the room stat
        param enabled: turn on or off
        """
        if self._send_command({"Identify": enable}):
            self._indentify_active = enable