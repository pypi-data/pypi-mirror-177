"""Module for communication with Knauer devices."""
import asyncio

from loguru import logger

from .knauer_finder import autodiscover_knauer
from flowchem.exceptions import InvalidConfiguration


class KnauerEthernetDevice:
    """Common base class for shared logic across Knauer pumps and valves."""

    TCP_PORT = 10001
    BUFFER_SIZE = 1024
    _id_counter = 0

    def __init__(self, ip_address, mac_address, **kwargs):
        """
        Knauer Ethernet Device - either pump or valve.

        If a MAC address is given, it is used to autodiscover the IP address.
        Otherwise, the IP address must be given.

        Note that for configuration files, the MAC address is preferred as it is static.

        Args:
            ip_address: device IP address (only 1 of either IP or MAC address is needed)
            mac_address: device MAC address (only 1 of either IP or MAC address is needed)
            name: name of device (optional)
        """
        super().__init__(**kwargs)

        # MAC address
        if mac_address:
            self.ip_address = self._ip_from_mac(mac_address)
        else:
            self.ip_address = ip_address

        # These will be set in initialize()
        self._reader: asyncio.StreamReader = None  # type: ignore
        self._writer: asyncio.StreamWriter = None  # type: ignore

        # Note: the pump requires "\n\r" as EOL, the valves "\r\n"! So this is set by the subclasses
        self.eol = b""

    def _ip_from_mac(self, mac_address: str) -> str:
        """Get IP from MAC."""
        # Autodiscover IP from MAC address
        available_devices = autodiscover_knauer()
        # IP if found, None otherwise
        ip_address = available_devices.get(mac_address)
        if ip_address is None:
            raise InvalidConfiguration(
                f"{self.__class__.__name__}:{self.name}\n"  # type: ignore
                f"Device with MAC address={mac_address} not found!\n"
                f"[Available: {available_devices}]"
            )
        return ip_address

    async def initialize(self):
        """Initialize connection."""
        # Future used to set shorter timeout than default
        future = asyncio.open_connection(host=self.ip_address, port=10001)
        try:
            self._reader, self._writer = await asyncio.wait_for(future, timeout=3)
        except OSError as connection_error:
            logger.exception(connection_error)
            raise InvalidConfiguration(
                f"Cannot open connection with device {self.__class__.__name__} at IP={self.ip_address}"
            ) from connection_error
        except asyncio.TimeoutError as timeout_error:
            logger.exception(timeout_error)
            raise InvalidConfiguration(
                f"No reply from device {self.__class__.__name__} at IP={self.ip_address}"
            ) from timeout_error

    async def _send_and_receive(self, message: str) -> str:
        self._writer.write(message.encode("ascii") + self.eol)
        await self._writer.drain()
        logger.debug(f"WRITE >>> '{message}' ")
        reply = await self._reader.readuntil(separator=b"\r")
        logger.debug(f"READ <<< '{reply.decode().strip()}' ")
        return reply.decode("ascii").strip()
