# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from banyanclient.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    ACCESS_TIER = "access_tier"
    REGISTERED_SERVICE = "registered_service"
    API_KEY = "api_key"
    AUDIT_LOG = "audit_log"
    BUNDLE = "bundle"
    CLOUD_RESOURCE = "cloud_resource"
    CLOUD_RESOURCE_SERVICE = "cloud_resource_service"
    DEVICE = "device"
    ENDUSER = "enduser"
    SECURITY_ROLE = "security_role"
    EVENT = "event"
    SAASAPP = "saasapp"
    SATELLITE = "satellite"
    SERVICE_TUNNEL = "service_tunnel"
    SECURITY_POLICY = "security_policy"
