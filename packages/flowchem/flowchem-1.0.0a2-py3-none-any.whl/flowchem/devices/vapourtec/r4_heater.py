""" Control module for the Vapourtec R4 heater """
from __future__ import annotations

import time
from collections import namedtuple
from collections.abc import Iterable

import aioserial
import pint
from loguru import logger

from flowchem import ureg
from flowchem.components.technical.temperature_control import TempRange
from flowchem.devices.flowchem_device import DeviceInfo
from flowchem.devices.flowchem_device import FlowchemDevice
from flowchem.devices.vapourtec.r4_heater_channel_control import R4HeaterChannelControl
from flowchem.exceptions import InvalidConfiguration
from flowchem.people import *

try:
    from flowchem_vapourtec import VapourtecR4Commands

    HAS_VAPOURTEC_COMMANDS = True
except ImportError:
    HAS_VAPOURTEC_COMMANDS = False


class R4Heater(FlowchemDevice):
    """R4 reactor heater control class."""

    DEFAULT_CONFIG = {
        "timeout": 0.1,
        "baudrate": 19200,
        "parity": aioserial.PARITY_NONE,
        "stopbits": aioserial.STOPBITS_ONE,
        "bytesize": aioserial.EIGHTBITS,
    }

    ChannelStatus = namedtuple("ChannelStatus", "state, temperature")

    def __init__(
        self,
        name: str = "",
        min_temp: float | list[float] = -100,
        max_temp: float | list[float] = 250,
        **config,
    ):
        super().__init__(name)
        # Set min and max temp for all 4 channels
        if not isinstance(min_temp, Iterable):
            min_temp = [min_temp] * 4
        if not isinstance(max_temp, Iterable):
            max_temp = [max_temp] * 4
        assert len(min_temp) == len(max_temp) == 4
        self._min_t = min_temp
        self._max_t = max_temp

        if not HAS_VAPOURTEC_COMMANDS:
            raise InvalidConfiguration(
                "You tried to use a Vapourtec device but the relevant commands are missing!\n"
                "Unfortunately, we cannot publish those as they were provided under NDA.\n"
                "Contact Vapourtec for further assistance."
            )

        self.cmd = VapourtecR4Commands()

        # Merge default settings, including serial, with provided ones.
        configuration = R4Heater.DEFAULT_CONFIG | config
        try:
            self._serial = aioserial.AioSerial(**configuration)
        except aioserial.SerialException as ex:
            raise InvalidConfiguration(
                f"Cannot connect to the R4Heater on the port <{config.get('port')}>"
            ) from ex

        self.metadata = DeviceInfo(
            authors=[dario, jakob, wei_hsin],
            maintainers=[dario],
            manufacturer="Vapourtec",
            model="R4 reactor module",
        )

    async def initialize(self):
        """Ensure connection."""
        self.metadata.version = await self.version()
        logger.info(f"Connected with R4Heater version {self.metadata.version}")

    async def _write(self, command: str):
        """Writes a command to the pump"""
        cmd = command + "\r\n"
        await self._serial.write_async(cmd.encode("ascii"))
        logger.debug(f"Sent command: {repr(command)}")

    async def _read_reply(self) -> str:
        """Reads the pump reply from serial communication."""
        reply_string = await self._serial.readline_async()
        logger.debug(f"Reply received: {reply_string.decode('ascii').rstrip()}")
        return reply_string.decode("ascii")

    async def write_and_read_reply(self, command: str) -> str:
        """Sends a command to the pump, read the replies and returns it, optionally parsed."""
        self._serial.reset_input_buffer()
        await self._write(command)
        logger.debug(f"Command {command} sent to R4!")
        response = await self._read_reply()

        if not response:
            raise InvalidConfiguration("No response received from heating module!")

        logger.debug(f"Reply received: {response}")
        return response.rstrip()

    async def version(self):
        """Get firmware version."""
        return await self.write_and_read_reply(self.cmd.VERSION)

    async def set_temperature(self, channel, temperature: pint.Quantity):
        """Set temperature to channel."""
        cmd = self.cmd.SET_TEMPERATURE.format(
            channel=channel, temperature_in_C=round(temperature.m_as("°C"))
        )
        await self.write_and_read_reply(cmd)
        # Set temperature implies channel on
        await self.power_on(channel)
        # Verify it is not unplugged
        status = await self.get_status(channel)
        if status.state == "U":
            logger.error(
                f"TARGET CHANNEL {channel} UNPLUGGED! (Note: numbering starts at 0)"
            )

    async def get_status(self, channel) -> ChannelStatus:
        """Get status from channel."""
        # This command is a bit fragile for unknown reasons.
        failure = 0
        while True:
            try:
                raw_status = await self.write_and_read_reply(
                    self.cmd.GET_STATUS.format(channel=channel)
                )
                return R4Heater.ChannelStatus(raw_status[:1], raw_status[1:])
            except InvalidConfiguration as ex:
                failure += 1
                # Allows 3 failures cause the R4 is choosy at times...
                if failure > 3:
                    raise ex
                else:
                    continue

    async def get_temperature(self, channel):
        """Get temperature (in Celsius) from channel."""
        state = await self.get_status(channel)
        return None if state.temperature == "281.2" else state.temperature

    async def power_on(self, channel):
        """Turn on channel."""
        await self.write_and_read_reply(self.cmd.POWER_ON.format(channel=channel))

    async def power_off(self, channel):
        """Turn off channel."""
        await self.write_and_read_reply(self.cmd.POWER_OFF.format(channel=channel))

    def components(self):
        temp_limits = {
            ch_num: TempRange(min=ureg.Quantity(t[0]), max=ureg.Quantity(t[1]))
            for ch_num, t in enumerate(zip(self._min_t, self._max_t))
        }
        return [
            R4HeaterChannelControl(f"reactor{n+1}", self, n, temp_limits[n])
            for n in range(4)
        ]


if __name__ == "__main__":
    import asyncio

    heat = R4Heater(port="COM1")

    async def main(heat):
        """test function"""
        await heat.initialize()
        # Get reactors
        r1, r2, r3, r4 = heat.components()

        await r1.set_temperature("30 °C")
        print(f"Temperature is {await r1.get_temperature()}")

    asyncio.run(main(heat))
