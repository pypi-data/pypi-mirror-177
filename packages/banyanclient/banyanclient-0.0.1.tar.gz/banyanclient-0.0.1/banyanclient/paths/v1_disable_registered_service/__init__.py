# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from banyanclient.paths.v1_disable_registered_service import Api

from banyanclient.paths import PathValues

path = PathValues.V1_DISABLE_REGISTERED_SERVICE