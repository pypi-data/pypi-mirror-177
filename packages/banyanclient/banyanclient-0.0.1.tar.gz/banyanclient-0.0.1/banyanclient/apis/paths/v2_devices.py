from banyanclient.paths.v2_devices.get import ApiForget
from banyanclient.paths.v2_devices.delete import ApiFordelete


class V2Devices(
    ApiForget,
    ApiFordelete,
):
    pass
