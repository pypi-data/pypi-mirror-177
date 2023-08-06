import typing_extensions

from banyanclient.apis.tags import TagValues
from banyanclient.apis.tags.access_tier_api import AccessTierApi
from banyanclient.apis.tags.registered_service_api import RegisteredServiceApi
from banyanclient.apis.tags.api_key_api import ApiKeyApi
from banyanclient.apis.tags.audit_log_api import AuditLogApi
from banyanclient.apis.tags.bundle_api import BundleApi
from banyanclient.apis.tags.cloud_resource_api import CloudResourceApi
from banyanclient.apis.tags.cloud_resource_service_api import CloudResourceServiceApi
from banyanclient.apis.tags.device_api import DeviceApi
from banyanclient.apis.tags.enduser_api import EnduserApi
from banyanclient.apis.tags.security_role_api import SecurityRoleApi
from banyanclient.apis.tags.event_api import EventApi
from banyanclient.apis.tags.saasapp_api import SaasappApi
from banyanclient.apis.tags.satellite_api import SatelliteApi
from banyanclient.apis.tags.service_tunnel_api import ServiceTunnelApi
from banyanclient.apis.tags.security_policy_api import SecurityPolicyApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ACCESS_TIER: AccessTierApi,
        TagValues.REGISTERED_SERVICE: RegisteredServiceApi,
        TagValues.API_KEY: ApiKeyApi,
        TagValues.AUDIT_LOG: AuditLogApi,
        TagValues.BUNDLE: BundleApi,
        TagValues.CLOUD_RESOURCE: CloudResourceApi,
        TagValues.CLOUD_RESOURCE_SERVICE: CloudResourceServiceApi,
        TagValues.DEVICE: DeviceApi,
        TagValues.ENDUSER: EnduserApi,
        TagValues.SECURITY_ROLE: SecurityRoleApi,
        TagValues.EVENT: EventApi,
        TagValues.SAASAPP: SaasappApi,
        TagValues.SATELLITE: SatelliteApi,
        TagValues.SERVICE_TUNNEL: ServiceTunnelApi,
        TagValues.SECURITY_POLICY: SecurityPolicyApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ACCESS_TIER: AccessTierApi,
        TagValues.REGISTERED_SERVICE: RegisteredServiceApi,
        TagValues.API_KEY: ApiKeyApi,
        TagValues.AUDIT_LOG: AuditLogApi,
        TagValues.BUNDLE: BundleApi,
        TagValues.CLOUD_RESOURCE: CloudResourceApi,
        TagValues.CLOUD_RESOURCE_SERVICE: CloudResourceServiceApi,
        TagValues.DEVICE: DeviceApi,
        TagValues.ENDUSER: EnduserApi,
        TagValues.SECURITY_ROLE: SecurityRoleApi,
        TagValues.EVENT: EventApi,
        TagValues.SAASAPP: SaasappApi,
        TagValues.SATELLITE: SatelliteApi,
        TagValues.SERVICE_TUNNEL: ServiceTunnelApi,
        TagValues.SECURITY_POLICY: SecurityPolicyApi,
    }
)
