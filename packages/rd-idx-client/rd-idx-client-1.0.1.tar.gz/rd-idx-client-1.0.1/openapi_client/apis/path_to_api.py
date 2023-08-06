import typing_extensions

from openapi_client.paths import PathValues
from openapi_client.apis.paths.v1_user import V1User
from openapi_client.apis.paths.v1_order import V1Order
from openapi_client.apis.paths.v1_subscription_member_id import V1SubscriptionMemberId
from openapi_client.apis.paths.v1_activate_member_id_product_id import V1ActivateMemberIdProductId
from openapi_client.apis.paths.v1_cyberscan import V1Cyberscan
from openapi_client.apis.paths.v1_cyberscan_member_id import V1CyberscanMemberId
from openapi_client.apis.paths.v1_cyberscan_member_id_summary import V1CyberscanMemberIdSummary
from openapi_client.apis.paths.v1_cyberscan_member_id_data_type_hash_exposures import V1CyberscanMemberIdDataTypeHashExposures
from openapi_client.apis.paths.v1_cyberscan_member_id_data_type_hash import V1CyberscanMemberIdDataTypeHash
from openapi_client.apis.paths.v1_subscription_member_id_cancel import V1SubscriptionMemberIdCancel
from openapi_client.apis.paths.v1_subscription_member_id_deactivate import V1SubscriptionMemberIdDeactivate
from openapi_client.apis.paths.v1_member_member_id_locationcode import V1MemberMemberIdLocationcode

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V1_USER: V1User,
        PathValues.V1_ORDER: V1Order,
        PathValues.V1_SUBSCRIPTION_MEMBER_ID: V1SubscriptionMemberId,
        PathValues.V1_ACTIVATE_MEMBER_ID_PRODUCT_ID: V1ActivateMemberIdProductId,
        PathValues.V1_CYBERSCAN: V1Cyberscan,
        PathValues.V1_CYBERSCAN_MEMBER_ID: V1CyberscanMemberId,
        PathValues.V1_CYBERSCAN_MEMBER_ID_SUMMARY: V1CyberscanMemberIdSummary,
        PathValues.V1_CYBERSCAN_MEMBER_ID_DATA_TYPE_HASH_EXPOSURES: V1CyberscanMemberIdDataTypeHashExposures,
        PathValues.V1_CYBERSCAN_MEMBER_ID_DATA_TYPE_HASH: V1CyberscanMemberIdDataTypeHash,
        PathValues.V1_SUBSCRIPTION_MEMBER_ID_CANCEL: V1SubscriptionMemberIdCancel,
        PathValues.V1_SUBSCRIPTION_MEMBER_ID_DEACTIVATE: V1SubscriptionMemberIdDeactivate,
        PathValues.V1_MEMBER_MEMBER_ID_LOCATIONCODE: V1MemberMemberIdLocationcode,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V1_USER: V1User,
        PathValues.V1_ORDER: V1Order,
        PathValues.V1_SUBSCRIPTION_MEMBER_ID: V1SubscriptionMemberId,
        PathValues.V1_ACTIVATE_MEMBER_ID_PRODUCT_ID: V1ActivateMemberIdProductId,
        PathValues.V1_CYBERSCAN: V1Cyberscan,
        PathValues.V1_CYBERSCAN_MEMBER_ID: V1CyberscanMemberId,
        PathValues.V1_CYBERSCAN_MEMBER_ID_SUMMARY: V1CyberscanMemberIdSummary,
        PathValues.V1_CYBERSCAN_MEMBER_ID_DATA_TYPE_HASH_EXPOSURES: V1CyberscanMemberIdDataTypeHashExposures,
        PathValues.V1_CYBERSCAN_MEMBER_ID_DATA_TYPE_HASH: V1CyberscanMemberIdDataTypeHash,
        PathValues.V1_SUBSCRIPTION_MEMBER_ID_CANCEL: V1SubscriptionMemberIdCancel,
        PathValues.V1_SUBSCRIPTION_MEMBER_ID_DEACTIVATE: V1SubscriptionMemberIdDeactivate,
        PathValues.V1_MEMBER_MEMBER_ID_LOCATIONCODE: V1MemberMemberIdLocationcode,
    }
)
