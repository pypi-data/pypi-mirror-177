from banyanclient.paths.v2_service_tunnel_id.get import ApiForget
from banyanclient.paths.v2_service_tunnel_id.put import ApiForput
from banyanclient.paths.v2_service_tunnel_id.delete import ApiFordelete


class V2ServiceTunnelId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
