from banyanclient.paths.v2_satellite_id.get import ApiForget
from banyanclient.paths.v2_satellite_id.put import ApiForput
from banyanclient.paths.v2_satellite_id.delete import ApiFordelete


class V2SatelliteId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
