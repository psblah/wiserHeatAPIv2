from .device import _WiserDevice, _WiserBattery
from .helpers import _from_wiser_temp
from .rest_controller import _WiserRestController
from .const import (
    WISERSMARTVALVE
)

import inspect
import logging

_LOGGER = logging.getLogger(__name__)

class _WiserSmartValve(_WiserDevice):
    """Class representing a Wiser Smart Valve device"""

    def __init__(self, data: dict, device_type_data: dict):
        super().__init__(data)
        self._data = data
        self._device_type_data = device_type_data

        self._device_lock_enabled = data.get("DeviceLockEnabled", False)
        self._indentify_active = data.get("IdentifyActive", False)

    def _send_command(self, cmd: dict):
        """
        Send control command to the smart valve
        param cmd: json command structure
        return: boolen - true = success, false = failed
        """
        rest = _WiserRestController()
        result = rest._send_command(WISERSMARTVALVE.format(self.id), cmd)
        if result:
            _LOGGER.info(
                "Wiser smart valve - {} command successful".format(
                    inspect.stack()[1].function
                )
            )
        return result

    @property
    def battery(self):
        """Get battery information for smart valve"""
        return _WiserBattery(self._data)

    @property
    def device_lock_enabled(self) -> bool:
        """Get or set smart valve device lock"""
        return self._device_lock_enabled

    @device_lock_enabled.setter
    def device_lock_enabled(self, enable: bool):
        if self._send_command({"DeviceLockEnabled": enable}):
            self._device_lock_enabled = enable

    @property
    def current_target_temperature(self) -> float:
        """Get the smart valve current target temperature setting"""
        return _from_wiser_temp(self._device_type_data.get("SetPoint"))

    @property
    def current_temperature(self) -> float:
        """Get the current temperature measured by the smart valve"""
        return _from_wiser_temp(self._device_type_data.get("MeasuredTemperature"))

    @property
    def identify(self) -> bool:
        """Get or set if the smart valve identify function is enabled"""
        return self._indentify_active

    @identify.setter
    def identify(self, enable: bool = False):
        if self._send_command({"Identify": enable}):
            self._indentify_active = enable

    @property
    def mounting_orientation(self) -> str:
        """Get the mouting orientation of the smart valve"""
        return self._device_type_data.get("MountingOrientation")

    @property
    def percentage_demand(self) -> int:
        """Get the current percentage demand of the smart valve"""
        return self._device_type_data.get("PercentageDemand")