import typing_extensions

from openapi_client.apis.tags import TagValues
from openapi_client.apis.tags.access_tier_api import AccessTierApi
from openapi_client.apis.tags.registered_service_api import RegisteredServiceApi
from openapi_client.apis.tags.api_key_api import ApiKeyApi
from openapi_client.apis.tags.audit_log_api import AuditLogApi
from openapi_client.apis.tags.bundle_api import BundleApi
from openapi_client.apis.tags.cloud_resource_api import CloudResourceApi
from openapi_client.apis.tags.cloud_resource_service_api import CloudResourceServiceApi
from openapi_client.apis.tags.device_api import DeviceApi
from openapi_client.apis.tags.enduser_api import EnduserApi
from openapi_client.apis.tags.security_role_api import SecurityRoleApi
from openapi_client.apis.tags.event_api import EventApi
from openapi_client.apis.tags.saasapp_api import SaasappApi
from openapi_client.apis.tags.satellite_api import SatelliteApi
from openapi_client.apis.tags.service_tunnel_api import ServiceTunnelApi
from openapi_client.apis.tags.security_policy_api import SecurityPolicyApi

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
