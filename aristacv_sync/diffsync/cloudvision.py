"""DiffSync adapter for Arista CloudVision."""
from diffsync import DiffSync

import aristacv_sync.diffsync.cvutils as cvutils

from .models import Device, UserTag


class CloudVision(DiffSync):
    """DiffSync adapter implementation for CloudVision user-defined device tags."""

    device = Device
    tag = UserTag

    top_level = ["device"]

    type = "CloudVision"

    nb = None

    def load(self):
        devices = cvutils.get_devices()
        for dev in devices:
            self.device = Device(name=dev["hostname"], device_id=dev["device_id"])
            self.add(self.device)
            dev_tags = cvutils.get_device_tags(device_id=dev["device_id"])
            for tag in dev_tags:
                if tag["type"] == "CREATOR_TYPE_USER":
                    self.tag = UserTag(name=tag["label"], device_name=dev["hostname"], value=tag["value"])
                    self.add(self.tag)
                    self.device.add_child(self.tag)
