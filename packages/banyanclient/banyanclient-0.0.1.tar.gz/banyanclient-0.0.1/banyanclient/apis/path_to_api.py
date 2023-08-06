import typing_extensions

from banyanclient.paths import PathValues
from banyanclient.apis.paths.v1_enable_registered_service import V1EnableRegisteredService
from banyanclient.apis.paths.v1_services_stats import V1ServicesStats
from banyanclient.apis.paths.v1_service_connection_test import V1ServiceConnectionTest
from banyanclient.apis.paths.v1_insert_registered_service import V1InsertRegisteredService
from banyanclient.apis.paths.v2_access_tier_id_registered_services import V2AccessTierIdRegisteredServices
from banyanclient.apis.paths.v1_registered_services import V1RegisteredServices
from banyanclient.apis.paths.v1_delete_registered_service import V1DeleteRegisteredService
from banyanclient.apis.paths.v1_disable_registered_service import V1DisableRegisteredService
from banyanclient.apis.paths.v2_bundle_bundle_id import V2BundleBundleId
from banyanclient.apis.paths.v2_bundle import V2Bundle
from banyanclient.apis.paths.v2_bundle_bundle_id_service import V2BundleBundleIdService
from banyanclient.apis.paths.v2_bundle_bundle_id_service_service_id import V2BundleBundleIdServiceServiceId
from banyanclient.apis.paths.v2_service_tunnel import V2ServiceTunnel
from banyanclient.apis.paths.service_tunnel_id_security_policy_policy_id import ServiceTunnelIdSecurityPolicyPolicyId
from banyanclient.apis.paths.service_tunnel_id_security_policy import ServiceTunnelIdSecurityPolicy
from banyanclient.apis.paths.v2_service_tunnel_id import V2ServiceTunnelId
from banyanclient.apis.paths.v1_insert_saasapp import V1InsertSaasapp
from banyanclient.apis.paths.v1_policy_policy_id_attachment import V1PolicyPolicyIDAttachment
from banyanclient.apis.paths.v1_security_policies import V1SecurityPolicies
from banyanclient.apis.paths.v1_security_attach_policies import V1SecurityAttachPolicies
from banyanclient.apis.paths.v1_policies_stats import V1PoliciesStats
from banyanclient.apis.paths.v1_policy_attachment_attached_to_type_attached_to_id import V1PolicyAttachmentAttachedToTypeAttachedToID
from banyanclient.apis.paths.v1_policy_attachment_attached_to_type import V1PolicyAttachmentAttachedToType
from banyanclient.apis.paths.v1_delete_security_policy import V1DeleteSecurityPolicy
from banyanclient.apis.paths.v1_insert_security_attach_policy import V1InsertSecurityAttachPolicy
from banyanclient.apis.paths.v1_policy_attachment import V1PolicyAttachment
from banyanclient.apis.paths.v1_delete_security_attach_policy import V1DeleteSecurityAttachPolicy
from banyanclient.apis.paths.v1_insert_security_policy import V1InsertSecurityPolicy
from banyanclient.apis.paths.v1_securityroles_stats import V1SecurityrolesStats
from banyanclient.apis.paths.v1_disable_security_role import V1DisableSecurityRole
from banyanclient.apis.paths.v1_insert_security_role import V1InsertSecurityRole
from banyanclient.apis.paths.v1_enable_security_role import V1EnableSecurityRole
from banyanclient.apis.paths.v1_security_roles_enduser_devices import V1SecurityRolesEnduserDevices
from banyanclient.apis.paths.v1_delete_security_role import V1DeleteSecurityRole
from banyanclient.apis.paths.v1_security_roles import V1SecurityRoles
from banyanclient.apis.paths.v1_unregistered_device_endusers_csv import V1UnregisteredDeviceEndusersCsv
from banyanclient.apis.paths.v1_endusers_stats import V1EndusersStats
from banyanclient.apis.paths.v2_endusers import V2Endusers
from banyanclient.apis.paths.v1_mdm_insert_devices import V1MdmInsertDevices
from banyanclient.apis.paths.v2_enduser_groups import V2EnduserGroups
from banyanclient.apis.paths.v1_endusers import V1Endusers
from banyanclient.apis.paths.v1_enduser_devices_data import V1EnduserDevicesData
from banyanclient.apis.paths.v2_enduser import V2Enduser
from banyanclient.apis.paths.v1_endusers_csv import V1EndusersCsv
from banyanclient.apis.paths.v2_enduser_id import V2EnduserId
from banyanclient.apis.paths.v1_delete_device import V1DeleteDevice
from banyanclient.apis.paths.v1_send_device_notification import V1SendDeviceNotification
from banyanclient.apis.paths.v2_devices_csv import V2DevicesCsv
from banyanclient.apis.paths.v2_devices import V2Devices
from banyanclient.apis.paths.v1_enduser_devices import V1EnduserDevices
from banyanclient.apis.paths.v1_mdm_device_info import V1MdmDeviceInfo
from banyanclient.apis.paths.v1_device_id_token import V1DeviceIdToken
from banyanclient.apis.paths.v1_mdm_update_device import V1MdmUpdateDevice
from banyanclient.apis.paths.v1_devices_stats import V1DevicesStats
from banyanclient.apis.paths.v1_devices import V1Devices
from banyanclient.apis.paths.v1_events import V1Events
from banyanclient.apis.paths.v2_event_daily_counts import V2EventDailyCounts
from banyanclient.apis.paths.v1_event_types import V1EventTypes
from banyanclient.apis.paths.v1_events_feed import V1EventsFeed
from banyanclient.apis.paths.v1_events_count import V1EventsCount
from banyanclient.apis.paths.v1_audit_logs import V1AuditLogs
from banyanclient.apis.paths.v2_access_tier_id import V2AccessTierId
from banyanclient.apis.paths.v1_access_tiers_stats import V1AccessTiersStats
from banyanclient.apis.paths.v2_access_tier import V2AccessTier
from banyanclient.apis.paths.v1_one_click_support_bundle import V1OneClickSupportBundle
from banyanclient.apis.paths.v1_service_hostname_mapping import V1ServiceHostnameMapping
from banyanclient.apis.paths.v2_access_tier_access_tier_id_tunnel_config_tunnel_config_id import V2AccessTierAccessTierIdTunnelConfigTunnelConfigId
from banyanclient.apis.paths.v2_satellite import V2Satellite
from banyanclient.apis.paths.v2_satellite_id import V2SatelliteId
from banyanclient.apis.paths.v2_connector_stats import V2ConnectorStats
from banyanclient.apis.paths.v2_cloud_resource_id import V2CloudResourceId
from banyanclient.apis.paths.v2_cloud_resource_service_id import V2CloudResourceServiceId
from banyanclient.apis.paths.v2_cloud_resource_service import V2CloudResourceService
from banyanclient.apis.paths.v2_api_key_id import V2ApiKeyId
from banyanclient.apis.paths.v2_api_key_scope import V2ApiKeyScope
from banyanclient.apis.paths.v2_api_key import V2ApiKey

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V1_ENABLE_REGISTERED_SERVICE: V1EnableRegisteredService,
        PathValues.V1_SERVICES_STATS: V1ServicesStats,
        PathValues.V1_SERVICE_CONNECTION_TEST: V1ServiceConnectionTest,
        PathValues.V1_INSERT_REGISTERED_SERVICE: V1InsertRegisteredService,
        PathValues.V2_ACCESS_TIER_ID_REGISTERED_SERVICES: V2AccessTierIdRegisteredServices,
        PathValues.V1_REGISTERED_SERVICES: V1RegisteredServices,
        PathValues.V1_DELETE_REGISTERED_SERVICE: V1DeleteRegisteredService,
        PathValues.V1_DISABLE_REGISTERED_SERVICE: V1DisableRegisteredService,
        PathValues.V2_BUNDLE_BUNDLE_ID: V2BundleBundleId,
        PathValues.V2_BUNDLE: V2Bundle,
        PathValues.V2_BUNDLE_BUNDLE_ID_SERVICE: V2BundleBundleIdService,
        PathValues.V2_BUNDLE_BUNDLE_ID_SERVICE_SERVICE_ID: V2BundleBundleIdServiceServiceId,
        PathValues.V2_SERVICE_TUNNEL: V2ServiceTunnel,
        PathValues.SERVICE_TUNNEL_ID_SECURITY_POLICY_POLICY_ID: ServiceTunnelIdSecurityPolicyPolicyId,
        PathValues.SERVICE_TUNNEL_ID_SECURITY_POLICY: ServiceTunnelIdSecurityPolicy,
        PathValues.V2_SERVICE_TUNNEL_ID: V2ServiceTunnelId,
        PathValues.V1_INSERT_SAASAPP: V1InsertSaasapp,
        PathValues.V1_POLICY_POLICY_ID_ATTACHMENT: V1PolicyPolicyIDAttachment,
        PathValues.V1_SECURITY_POLICIES: V1SecurityPolicies,
        PathValues.V1_SECURITY_ATTACH_POLICIES: V1SecurityAttachPolicies,
        PathValues.V1_POLICIES_STATS: V1PoliciesStats,
        PathValues.V1_POLICY_ATTACHMENT_ATTACHED_TO_TYPE_ATTACHED_TO_ID: V1PolicyAttachmentAttachedToTypeAttachedToID,
        PathValues.V1_POLICY_ATTACHMENT_ATTACHED_TO_TYPE: V1PolicyAttachmentAttachedToType,
        PathValues.V1_DELETE_SECURITY_POLICY: V1DeleteSecurityPolicy,
        PathValues.V1_INSERT_SECURITY_ATTACH_POLICY: V1InsertSecurityAttachPolicy,
        PathValues.V1_POLICY_ATTACHMENT: V1PolicyAttachment,
        PathValues.V1_DELETE_SECURITY_ATTACH_POLICY: V1DeleteSecurityAttachPolicy,
        PathValues.V1_INSERT_SECURITY_POLICY: V1InsertSecurityPolicy,
        PathValues.V1_SECURITYROLES_STATS: V1SecurityrolesStats,
        PathValues.V1_DISABLE_SECURITY_ROLE: V1DisableSecurityRole,
        PathValues.V1_INSERT_SECURITY_ROLE: V1InsertSecurityRole,
        PathValues.V1_ENABLE_SECURITY_ROLE: V1EnableSecurityRole,
        PathValues.V1_SECURITY_ROLES_ENDUSER_DEVICES: V1SecurityRolesEnduserDevices,
        PathValues.V1_DELETE_SECURITY_ROLE: V1DeleteSecurityRole,
        PathValues.V1_SECURITY_ROLES: V1SecurityRoles,
        PathValues.V1_UNREGISTERED_DEVICE_ENDUSERS_CSV: V1UnregisteredDeviceEndusersCsv,
        PathValues.V1_ENDUSERS_STATS: V1EndusersStats,
        PathValues.V2_ENDUSERS: V2Endusers,
        PathValues.V1_MDM_INSERT_DEVICES: V1MdmInsertDevices,
        PathValues.V2_ENDUSER_GROUPS: V2EnduserGroups,
        PathValues.V1_ENDUSERS: V1Endusers,
        PathValues.V1_ENDUSER_DEVICES_DATA: V1EnduserDevicesData,
        PathValues.V2_ENDUSER: V2Enduser,
        PathValues.V1_ENDUSERS_CSV: V1EndusersCsv,
        PathValues.V2_ENDUSER_ID: V2EnduserId,
        PathValues.V1_DELETE_DEVICE: V1DeleteDevice,
        PathValues.V1_SEND_DEVICE_NOTIFICATION: V1SendDeviceNotification,
        PathValues.V2_DEVICES_CSV: V2DevicesCsv,
        PathValues.V2_DEVICES: V2Devices,
        PathValues.V1_ENDUSER_DEVICES: V1EnduserDevices,
        PathValues.V1_MDM_DEVICE_INFO: V1MdmDeviceInfo,
        PathValues.V1_DEVICE_ID_TOKEN: V1DeviceIdToken,
        PathValues.V1_MDM_UPDATE_DEVICE: V1MdmUpdateDevice,
        PathValues.V1_DEVICES_STATS: V1DevicesStats,
        PathValues.V1_DEVICES: V1Devices,
        PathValues.V1_EVENTS: V1Events,
        PathValues.V2_EVENT_DAILY_COUNTS: V2EventDailyCounts,
        PathValues.V1_EVENT_TYPES: V1EventTypes,
        PathValues.V1_EVENTS_FEED: V1EventsFeed,
        PathValues.V1_EVENTS_COUNT: V1EventsCount,
        PathValues.V1_AUDIT_LOGS: V1AuditLogs,
        PathValues.V2_ACCESS_TIER_ID: V2AccessTierId,
        PathValues.V1_ACCESS_TIERS_STATS: V1AccessTiersStats,
        PathValues.V2_ACCESS_TIER: V2AccessTier,
        PathValues.V1_ONE_CLICK_SUPPORT_BUNDLE: V1OneClickSupportBundle,
        PathValues.V1_SERVICE_HOSTNAME_MAPPING: V1ServiceHostnameMapping,
        PathValues.V2_ACCESS_TIER_ACCESS_TIER_ID_TUNNEL_CONFIG_TUNNEL_CONFIG_ID: V2AccessTierAccessTierIdTunnelConfigTunnelConfigId,
        PathValues.V2_SATELLITE: V2Satellite,
        PathValues.V2_SATELLITE_ID: V2SatelliteId,
        PathValues.V2_CONNECTOR_STATS: V2ConnectorStats,
        PathValues.V2_CLOUD_RESOURCE_ID: V2CloudResourceId,
        PathValues.V2_CLOUD_RESOURCE_SERVICE_ID: V2CloudResourceServiceId,
        PathValues.V2_CLOUD_RESOURCE_SERVICE: V2CloudResourceService,
        PathValues.V2_API_KEY_ID: V2ApiKeyId,
        PathValues.V2_API_KEY_SCOPE: V2ApiKeyScope,
        PathValues.V2_API_KEY: V2ApiKey,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V1_ENABLE_REGISTERED_SERVICE: V1EnableRegisteredService,
        PathValues.V1_SERVICES_STATS: V1ServicesStats,
        PathValues.V1_SERVICE_CONNECTION_TEST: V1ServiceConnectionTest,
        PathValues.V1_INSERT_REGISTERED_SERVICE: V1InsertRegisteredService,
        PathValues.V2_ACCESS_TIER_ID_REGISTERED_SERVICES: V2AccessTierIdRegisteredServices,
        PathValues.V1_REGISTERED_SERVICES: V1RegisteredServices,
        PathValues.V1_DELETE_REGISTERED_SERVICE: V1DeleteRegisteredService,
        PathValues.V1_DISABLE_REGISTERED_SERVICE: V1DisableRegisteredService,
        PathValues.V2_BUNDLE_BUNDLE_ID: V2BundleBundleId,
        PathValues.V2_BUNDLE: V2Bundle,
        PathValues.V2_BUNDLE_BUNDLE_ID_SERVICE: V2BundleBundleIdService,
        PathValues.V2_BUNDLE_BUNDLE_ID_SERVICE_SERVICE_ID: V2BundleBundleIdServiceServiceId,
        PathValues.V2_SERVICE_TUNNEL: V2ServiceTunnel,
        PathValues.SERVICE_TUNNEL_ID_SECURITY_POLICY_POLICY_ID: ServiceTunnelIdSecurityPolicyPolicyId,
        PathValues.SERVICE_TUNNEL_ID_SECURITY_POLICY: ServiceTunnelIdSecurityPolicy,
        PathValues.V2_SERVICE_TUNNEL_ID: V2ServiceTunnelId,
        PathValues.V1_INSERT_SAASAPP: V1InsertSaasapp,
        PathValues.V1_POLICY_POLICY_ID_ATTACHMENT: V1PolicyPolicyIDAttachment,
        PathValues.V1_SECURITY_POLICIES: V1SecurityPolicies,
        PathValues.V1_SECURITY_ATTACH_POLICIES: V1SecurityAttachPolicies,
        PathValues.V1_POLICIES_STATS: V1PoliciesStats,
        PathValues.V1_POLICY_ATTACHMENT_ATTACHED_TO_TYPE_ATTACHED_TO_ID: V1PolicyAttachmentAttachedToTypeAttachedToID,
        PathValues.V1_POLICY_ATTACHMENT_ATTACHED_TO_TYPE: V1PolicyAttachmentAttachedToType,
        PathValues.V1_DELETE_SECURITY_POLICY: V1DeleteSecurityPolicy,
        PathValues.V1_INSERT_SECURITY_ATTACH_POLICY: V1InsertSecurityAttachPolicy,
        PathValues.V1_POLICY_ATTACHMENT: V1PolicyAttachment,
        PathValues.V1_DELETE_SECURITY_ATTACH_POLICY: V1DeleteSecurityAttachPolicy,
        PathValues.V1_INSERT_SECURITY_POLICY: V1InsertSecurityPolicy,
        PathValues.V1_SECURITYROLES_STATS: V1SecurityrolesStats,
        PathValues.V1_DISABLE_SECURITY_ROLE: V1DisableSecurityRole,
        PathValues.V1_INSERT_SECURITY_ROLE: V1InsertSecurityRole,
        PathValues.V1_ENABLE_SECURITY_ROLE: V1EnableSecurityRole,
        PathValues.V1_SECURITY_ROLES_ENDUSER_DEVICES: V1SecurityRolesEnduserDevices,
        PathValues.V1_DELETE_SECURITY_ROLE: V1DeleteSecurityRole,
        PathValues.V1_SECURITY_ROLES: V1SecurityRoles,
        PathValues.V1_UNREGISTERED_DEVICE_ENDUSERS_CSV: V1UnregisteredDeviceEndusersCsv,
        PathValues.V1_ENDUSERS_STATS: V1EndusersStats,
        PathValues.V2_ENDUSERS: V2Endusers,
        PathValues.V1_MDM_INSERT_DEVICES: V1MdmInsertDevices,
        PathValues.V2_ENDUSER_GROUPS: V2EnduserGroups,
        PathValues.V1_ENDUSERS: V1Endusers,
        PathValues.V1_ENDUSER_DEVICES_DATA: V1EnduserDevicesData,
        PathValues.V2_ENDUSER: V2Enduser,
        PathValues.V1_ENDUSERS_CSV: V1EndusersCsv,
        PathValues.V2_ENDUSER_ID: V2EnduserId,
        PathValues.V1_DELETE_DEVICE: V1DeleteDevice,
        PathValues.V1_SEND_DEVICE_NOTIFICATION: V1SendDeviceNotification,
        PathValues.V2_DEVICES_CSV: V2DevicesCsv,
        PathValues.V2_DEVICES: V2Devices,
        PathValues.V1_ENDUSER_DEVICES: V1EnduserDevices,
        PathValues.V1_MDM_DEVICE_INFO: V1MdmDeviceInfo,
        PathValues.V1_DEVICE_ID_TOKEN: V1DeviceIdToken,
        PathValues.V1_MDM_UPDATE_DEVICE: V1MdmUpdateDevice,
        PathValues.V1_DEVICES_STATS: V1DevicesStats,
        PathValues.V1_DEVICES: V1Devices,
        PathValues.V1_EVENTS: V1Events,
        PathValues.V2_EVENT_DAILY_COUNTS: V2EventDailyCounts,
        PathValues.V1_EVENT_TYPES: V1EventTypes,
        PathValues.V1_EVENTS_FEED: V1EventsFeed,
        PathValues.V1_EVENTS_COUNT: V1EventsCount,
        PathValues.V1_AUDIT_LOGS: V1AuditLogs,
        PathValues.V2_ACCESS_TIER_ID: V2AccessTierId,
        PathValues.V1_ACCESS_TIERS_STATS: V1AccessTiersStats,
        PathValues.V2_ACCESS_TIER: V2AccessTier,
        PathValues.V1_ONE_CLICK_SUPPORT_BUNDLE: V1OneClickSupportBundle,
        PathValues.V1_SERVICE_HOSTNAME_MAPPING: V1ServiceHostnameMapping,
        PathValues.V2_ACCESS_TIER_ACCESS_TIER_ID_TUNNEL_CONFIG_TUNNEL_CONFIG_ID: V2AccessTierAccessTierIdTunnelConfigTunnelConfigId,
        PathValues.V2_SATELLITE: V2Satellite,
        PathValues.V2_SATELLITE_ID: V2SatelliteId,
        PathValues.V2_CONNECTOR_STATS: V2ConnectorStats,
        PathValues.V2_CLOUD_RESOURCE_ID: V2CloudResourceId,
        PathValues.V2_CLOUD_RESOURCE_SERVICE_ID: V2CloudResourceServiceId,
        PathValues.V2_CLOUD_RESOURCE_SERVICE: V2CloudResourceService,
        PathValues.V2_API_KEY_ID: V2ApiKeyId,
        PathValues.V2_API_KEY_SCOPE: V2ApiKeyScope,
        PathValues.V2_API_KEY: V2ApiKey,
    }
)
