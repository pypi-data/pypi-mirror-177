import typing_extensions

from openapi_client.apis.tags import TagValues
from openapi_client.apis.tags.account_creation_api import AccountCreationApi
from openapi_client.apis.tags.cyberscan_api import CyberscanApi
from openapi_client.apis.tags.member_deactivation_api import MemberDeactivationApi
from openapi_client.apis.tags.member_information_api import MemberInformationApi
from openapi_client.apis.tags.product_activation_api import ProductActivationApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ACCOUNT_CREATION: AccountCreationApi,
        TagValues.CYBERSCAN: CyberscanApi,
        TagValues.MEMBER_DEACTIVATION: MemberDeactivationApi,
        TagValues.MEMBER_INFORMATION: MemberInformationApi,
        TagValues.PRODUCT_ACTIVATION: ProductActivationApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ACCOUNT_CREATION: AccountCreationApi,
        TagValues.CYBERSCAN: CyberscanApi,
        TagValues.MEMBER_DEACTIVATION: MemberDeactivationApi,
        TagValues.MEMBER_INFORMATION: MemberInformationApi,
        TagValues.PRODUCT_ACTIVATION: ProductActivationApi,
    }
)
