from banyanclient.paths.v2_api_key.get import ApiForget
from banyanclient.paths.v2_api_key.post import ApiForpost


class V2ApiKey(
    ApiForget,
    ApiForpost,
):
    pass
