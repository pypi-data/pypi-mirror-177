from banyanclient.paths.v2_cloud_resource_id.get import ApiForget
from banyanclient.paths.v2_cloud_resource_id.put import ApiForput
from banyanclient.paths.v2_cloud_resource_id.delete import ApiFordelete
from banyanclient.paths.v2_cloud_resource_id.patch import ApiForpatch


class V2CloudResourceId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
