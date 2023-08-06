# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from openapi_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    V1_USER = "/v1/user"
    V1_ORDER = "/v1/order"
    V1_SUBSCRIPTION_MEMBER_ID = "/v1/subscription/{memberId}"
    V1_ACTIVATE_MEMBER_ID_PRODUCT_ID = "/v1/activate/{memberId}/{productId}"
    V1_CYBERSCAN = "/v1/cyberscan"
    V1_CYBERSCAN_MEMBER_ID = "/v1/cyberscan/{memberId}"
    V1_CYBERSCAN_MEMBER_ID_SUMMARY = "/v1/cyberscan/{memberId}/summary"
    V1_CYBERSCAN_MEMBER_ID_DATA_TYPE_HASH_EXPOSURES = "/v1/cyberscan/{memberId}/{dataType}/{hash}/exposures"
    V1_CYBERSCAN_MEMBER_ID_DATA_TYPE_HASH = "/v1/cyberscan/{memberId}/{dataType}/{hash}"
    V1_SUBSCRIPTION_MEMBER_ID_CANCEL = "/v1/subscription/{memberId}/cancel"
    V1_SUBSCRIPTION_MEMBER_ID_DEACTIVATE = "/v1/subscription/{memberId}/deactivate"
    V1_MEMBER_MEMBER_ID_LOCATIONCODE = "/v1/member/{memberId}/locationcode"
