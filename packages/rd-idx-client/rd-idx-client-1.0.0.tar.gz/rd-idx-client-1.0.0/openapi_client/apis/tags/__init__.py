# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from openapi_client.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    ACCOUNT_CREATION = "Account Creation"
    CYBERSCAN = "Cyberscan"
    MEMBER_DEACTIVATION = "Member Deactivation"
    MEMBER_INFORMATION = "Member Information"
    PRODUCT_ACTIVATION = "Product Activation"
