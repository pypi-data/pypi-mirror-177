"""
Guardian API websocket utilities.
"""
import os
import json
import asyncio
import logging
import requests
import websockets
from dotenv import load_dotenv
from dataclasses import dataclass, asdict
import socket
import sys

from .config import settings

load_dotenv()


class GuardianAPI:
    """Main Guardian API client."""

    def __init__(self, debug: bool = True) -> None:
        self.ws_identifier = settings.WS_IDENTIFIER
        self.rest_api_get_url = settings.REST_API_URL_GET
        self.rest_api_login_url = settings.REST_API_LOGIN

        self.debug: bool = debug

        self.ping_timeout: int = 10
        self.retry_time: int = 5

        self.first_message_check = True
        self.final_message_check = False

        self.SENTINEL = object()

    def unpack_from_queue(self, package):
        """Unpack data from the queue filled with BLE data

        Args:
            package (dict): _description_

        Returns:
            _type_: _description_
        """
        return (
            package["timestamp"],
            package["device_id"],
            package["data"],
            package["stop"],
        )

    async def connect_ws_api(
        self,
        data_queue: asyncio.Queue,
        deviceID: str = "deviceMockID",
        recordingID: str = "dummy_recID",
    ) -> None:
        """_summary_

        Args:
            data_queue (asyncio.Queue): Data queue from the BLE client
        """

        def log_first_message():
            if self.debug:
                logging.info("[API]: First package sent")
                logging.info(
                    "[API]: data_model.stop = %s",
                    data_model.stop,
                )
                logging.info(
                    "[API]: data_model.deviceID = %s",
                    data_model.deviceID,
                )
                logging.info(
                    "[API]: data_model.recordingID = %s",
                    data_model.recordingID,
                )
                logging.info(
                    "[API]: First package receipt: %s",
                    package_receipt,
                )

        def log_final_message():
            logging.info("[API]: Last package sent")
            logging.info(
                "[API]: data_model.stop = %s",
                data_model.stop,
            )
            logging.info(
                "[API]: data_model.deviceID = %s",
                data_model.deviceID,
            )
            logging.info(
                "[API]: data_model.recordingID = %s",
                data_model.recordingID,
            )
            logging.info(
                "[API]: Last package receipt: %s",
                package_receipt,
            )
            logging.info("[API]: Cloud connection sucesfully terminated")
            logging.info("[API]: Breaking inner loop of API client")

        async def unpack_and_load_data():
            """Get data from the queue and pack it into a dataclass"""
            package = await data_queue.get()
            (
                device_timestamp,
                device_id,
                data,
                stop,
            ) = self.unpack_from_queue(package)

            if data is not None:
                data_model.deviceTimestamp = device_timestamp
                data_model.deviceID = device_id
                data_model.payload = data
                data_model.stop = stop

        async def unpack_and_load_data_termination():
            """Get data from the queue and pack it into a dataclass"""
            package = await data_queue.get()
            (
                device_timestamp,
                device_id,
                _,
                _,
            ) = self.unpack_from_queue(package)

            if self.debug:
                logging.info("[API]: Terminating cloud connection")
            data_model.deviceTimestamp = device_timestamp
            data_model.deviceID = device_id
            data_model.payload = "STOP_CANCELLED"
            data_model.stop = True

        self.first_message_check = True
        self.final_message_check = False

        # init data model
        data_model = GuardianDataModel("", deviceID, recordingID, "", False)

        while True:

            if self.final_message_check:
                if self.debug:
                    logging.info("[API]: Final message received, closing websocket")
                await asyncio.sleep(5)
                break

            if self.debug:
                logging.info("[API]: Connecting to WS API...")

            websocket_resource_url = (
                f"wss://{self.ws_identifier}.execute-api.eu-central-1.amazonaws.com/v1"
            )

            try:
                async with websockets.connect(websocket_resource_url) as websocket:
                    # log the websocket resource url
                    self.first_message_check = True
                    if self.debug:
                        logging.info(
                            f"[API]: Connected to websocket resource url: {websocket_resource_url}"
                        )
                        logging.info("[API]: Sending data to the cloud")
                    while True:
                        try:
                            # forward data to the cloud
                            await unpack_and_load_data()

                            #print("Sending to the cloud ", asdict(data_model))
                            await websocket.send(json.dumps(asdict(data_model)))
                            package_receipt = await websocket.recv()

                            if self.first_message_check:
                                self.first_message_check = False
                                if self.debug:
                                    log_first_message()

                            if data_model.stop:
                                if self.debug:
                                    log_final_message()
                                self.final_message_check = True
                                break

                        except (
                            asyncio.TimeoutError,
                            websockets.exceptions.ConnectionClosed,
                        ) as error:
                            if self.debug:
                                logging.error(
                                    "[API]: Error in sending data to the cloud: %s",
                                    error,
                                )
                            try:
                                if self.debug:
                                    logging.info(
                                        "[API]: ws client connection closed or asyncio Timeout"
                                    )
                                pong = await websocket.ping()
                                await asyncio.wait_for(pong, timeout=self.ping_timeout)
                                if self.debug:
                                    logging.info(
                                        "[API]: Ping successful, connection alive and continue.."
                                    )
                                print("Try to ping websocket successful")
                                continue
                            except:
                                if self.debug:
                                    logging.error(
                                        f"[API]: Ping failed, connection closed, trying to reconnect in {self.retry_time} seconds"
                                    )
                                    logging.error("[API]: Ping failed - will retry...")
                                await asyncio.sleep(self.ping_timeout)
                                break

                        except asyncio.CancelledError:
                            async with websockets.connect(
                                websocket_resource_url
                            ) as websocket:
                                if self.debug:
                                    logging.info(
                                        "[API]: Re-establishing cloud connection in exeption"
                                    )
                                    logging.info(
                                        "[API]: Fetching last package from queue"
                                    )
                                await unpack_and_load_data_termination()

                                #print("Sending to the cloud ", asdict(data_model))
                                await websocket.send(json.dumps(asdict(data_model)))
                                package_receipt = await websocket.recv()
                                
                                if self.debug:
                                    log_final_message()
                                self.final_message_check = True
                                break

            except socket.gaierror:
                logging.info(
                    "[API]: Socket error - retrying connection in {} sec (Ctrl-C to quit)".format(
                        self.retry_time
                    )
                )
                logging.info(
                    "[API]: Websocket connection error - trying to reconnect again..."
                )
                await asyncio.sleep(self.retry_time)
                continue

            except ConnectionRefusedError:
                logging.error(
                    "Cannot connect to API endpoint. Please check the URL and try again."
                )
                logging.error(
                    "Retrying connection in {} seconds".format(self.retry_time)
                )
                await asyncio.sleep(self.retry_time)
                continue

            # TODO: receive response from websocket and handle it, later with bidirectional streaming

    def get_recordings_info_all(self, device_id: str = "mock-device-0") -> None:
        recordings_url = f"{self.rest_api_login_url}recordings"
        print(recordings_url)
        with requests.Session() as session:
            r = session.get(recordings_url, auth=(device_id, ""))
            if r.status_code == 200:
                print("Recording list retrieved successfully")
                # print the list of recordings pretty
                print(json.dumps(r.json(), indent=4, sort_keys=True))
                return r.json
            else:
                print("Loading recording list failed")

    def get_recording_info_by_id(
        self, device_id: str, recording_id: str = "recordingId-0"
    ) -> None:
        recordings_url = f"{self.rest_api_login_url}recordings/{recording_id}"

        with requests.Session() as session:
            r = session.get(recordings_url, auth=(device_id, ""))
            if r.status_code == 200:
                print("Recording ID file found")
                print(r.json())
                return r.json
            else:
                print("Recording not found")
                print(r.status_code)
                print(r.json())

    def download_recording_by_id(
        self, device_id: str, recording_id: str = "recordingId-0"
    ) -> None:

        recordings_folder_name = "recordings"
        recording_subfolder_name = recording_id
        # combine the folder name and subfolder name
        folder_path = os.path.join(recordings_folder_name, recording_subfolder_name)
        # create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # create subfolde
        recording_types = ["eeg", "imu"]        

        for data_type in recording_types:
            with requests.Session() as session:

                record_url = f"{self.rest_api_login_url}recordings/{recording_id}/download/{data_type}"
                r = session.get(record_url, auth=(device_id, ""))
                if r.status_code == 200:
                    print(f"Recording ID file found, downloading {data_type} data")
                    print(r.json())
                    # get url from response
                    url = r.json()["downloadUrl"]
                    r = session.get(url)
                    filename = f"{recording_id}_{data_type}.csv"
                    # combine folder name and filename
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "wb") as f:
                        # giving a name and saving it in any required format
                        # opening the file in write mode
                        f.write(r.content)

                    print("Downloading complete for recording ID: ", recording_id)
                else:
                    print("Data download failed")
                    print(r.status_code)
                    print(r.json())


@dataclass
class GuardianDataModel:
    """Data model for Guardian data"""

    deviceTimestamp: str
    deviceID: str
    recordingID: str
    payload: str  # This is a base64 encoded bytearray as a string
    stop: bool
