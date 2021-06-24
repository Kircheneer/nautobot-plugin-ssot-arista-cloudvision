"""DiffSync adapter for Arista CloudVision."""
from diffsync import DiffSync
import arista.tag.v1 as TAG
import nautobot_ssot_aristacv.diffsync.cvutils as cvutils

from .models import Device, CustomField


class CloudVision(DiffSync):
    """DiffSync adapter implementation for CloudVision user-defined device tags."""

    device = Device
    cf = CustomField

    top_level = ["device"]

    def load(self):
        devices = cvutils.get_devices()
        system_tags = cvutils.get_tags_by_type(TAG.models.CREATOR_TYPE_SYSTEM)
        for dev in devices:
            self.device = Device(name=dev["hostname"], device_id=dev["device_id"])
            self.add(self.device)
            dev_tags = [tag for tag in cvutils.get_device_tags(device_id=dev["device_id"]) if tag in system_tags]
            for tag in dev_tags:
                if any(tag["label"] in string for string in ["hostname", "serialnumber"]):
                    continue
                self.cf = CustomField(name=f"arista_{tag['label']}", value=tag["value"], device_name=dev["hostname"])
                self.add(self.cf)
                self.device.add_child(self.cf)