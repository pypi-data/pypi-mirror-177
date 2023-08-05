"""
Initialization of the IDUN Guardian Client
"""
import os
import asyncio
import logging
from datetime import datetime
from .igeb_bluetooth import GuardianBLE
from .igeb_api import GuardianAPI
from .igeb_utils import check_platform, check_valid_mac, check_valid_uuid
import uuid


class GuardianClient:
    """
    Class object for the communication between Guardian Earbuds and Cloud API
    """

    def __init__(
        self, address: str = "00000000-0000-0000-0000-000000000000", debug=True, debug_console=True
    ) -> None:
        self.is_connected = False
        self.debug = debug
        self.debug_to_console = debug_console
        if self.debug:
            if not os.path.exists("./logs"):
                os.makedirs("logs")
            datestr = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_filename = f"./logs/ble_info-{datestr}.log"
            # if directory does not exist, create it
            if not os.path.exists(os.path.dirname(log_filename)):
                os.makedirs(os.path.dirname(log_filename))
            log_handlers = [logging.FileHandler(log_filename)]

            if self.debug_to_console:
                log_handlers.append(logging.StreamHandler())
            logging.basicConfig(
                level=logging.INFO,
                datefmt="%d-%b-%y %H:%M:%S",
                format="%(asctime)s: %(name)s - %(levelname)s - %(message)s",
                handlers=log_handlers,
            )

        if address:
            if self.check_ble_address(address):
                self.guardian_ble = GuardianBLE(address, debug=self.debug)
                self.address = address
        else:
            logging.info("No BLE address provided, will search for device...")
            print("No BLE address provided, will search for device..")
            self.guardian_ble = GuardianBLE(debug=self.debug)

        self.guardian_api = GuardianAPI(debug=self.debug)

    def check_ble_address(self, address: str) -> bool:
        """Check if the BLE address is valid"""
        if (
            check_platform() == "Windows"
            or check_platform() == "Linux"
            and check_valid_mac(address)
        ):
            return True
        elif check_platform() == "Darwin" and check_valid_uuid(address):
            print("Platform detected: Darwin")
            print(f"UUID is valid for system Darwin: {address}")
            return True
        else:
            logging.error("Invalid BLE address")
            raise ValueError("Invalid BLE address")

    async def search_device(self):
        """Connect to the Guardian Earbuds

        Returns:
            is_connected: bool
        """

        self.address = await self.guardian_ble.search_device()
        self.is_connected = True
        if self.debug:
            await self.guardian_ble.get_service_and_char()

        return self.address

    async def search_device_auto(self):
        # TODO: search device and connect automatically, Andy knows this the best how to approach this problem, also need to change the BLE connection procedure using this and i see a lot of actual changes
        await self.guardian_ble.search_device()
        pass

    def disconnect(self):
        """Disconnect from the Guardian Earbuds"""

    async def get_device_address(self) -> str:
        """Get the MAC address of the Guardian Earbuds.
        It searches the MAC address of the device automatically. This
        address is used as the deviceID for cloud communication
        """

        # TODO: get the MAC address of the Guardian Earbuds

        device_address = await self.guardian_ble.get_device_mac()
        return device_address

    def start_stream(self):
        """Start streaming data from the Guardian Earbuds.
        Bidirectional websocket connection to the Guardian Cloud API.
        """
        pass

    async def stop_device(self):
        """Stop streaming data from the Guardian Earbuds"""
        await self.guardian_ble.stop_stream()

    async def start_recording(
        self,
        recording_timer: int = 36000,
        led_sleep: bool = False,
        experiment: str = "None provided",
    ):
        """
        Start recording data from the Guardian Earbuds.
        Unidirectional websocket connection to the Guardian Cloud API.
        """
        if self.debug:
            logging.info("CLIENT: Recording timer set to: %s seconds", recording_timer)
            logging.info("CLIENT: Start recording")

        print(f"CLIENT: Recording timer set to: {recording_timer} seconds")
        print("-----Recording starting------")

        data_queue: asyncio.Queue = asyncio.Queue(maxsize=86400)
        recording_id = str(
            uuid.uuid4()
        )  # the recordingID is a unique ID for each recording
        logging.info("[CLIENT] Recording ID: %s", recording_id)
        # log the experiment name in bold using the logging module
        logging.info("[CLIENT] Experiment description: %s", experiment)
        
        mac_id = await self.guardian_ble.get_device_mac()
        ble_client_task = self.guardian_ble.run_ble_record(
            data_queue, recording_timer, mac_id, led_sleep
        )
        api_consumer_task = self.guardian_api.connect_ws_api(
            data_queue, mac_id, recording_id
        )
        await asyncio.wait([ble_client_task, api_consumer_task])

        if self.debug:
            logging.info("CLIENT: Disconnect BLE and close websocket connection")

        print(f"-----Recording ID {recording_id}------")
        print(f"-----Device ID {mac_id}------")
        print("-----Recording stopped------")

    def stop_recording(self):
        """Stop recording data from the Guardian Earbuds"""

    async def start_impedance(
        self, impedance_display_time: int = 5, mains_freq_60hz: bool = False
    ):
        """
        Start recording data from the Guardian Earbuds.
        Unidirectional websocket connection to the Guardian Cloud API.
        """
        if self.debug:
            logging.info("CLIENT: Start recording")
        print("-----Impedance check started------")

        data_queue = asyncio.Queue()
        await data_queue.put(object())
        ble_client_task = self.guardian_ble.get_impedance_measurement(
            data_queue, impedance_display_time, mains_freq_60hz
        )
        # api_consumer_task = self.guardian_api.connect_ws_api(data_queue, self.address)
        await asyncio.wait([ble_client_task])

        if self.debug:
            logging.info("CLIENT: Disconnect BLE and close websocket connection")
        print("-----Impedance check stopped------")

    async def start_battery(self):
        """
        Start recording data from the Guardian Earbuds.
        Unidirectional websocket connection to the Guardian Cloud API.
        """
        print("-----Battery readout started------")
        if self.debug:
            logging.info("CLIENT: Start recording")

        ble_client_task = self.guardian_ble.read_battery_level()
        await asyncio.wait([ble_client_task])

        if self.debug:
            logging.info("CLIENT: Disconnect BLE and close websocket connection")
        print("-----Battery check stopped------")
