from enum import Enum as PyEnum

from pydantic import EmailStr, Field

Mail = EmailStr

PostalCode = Field(
    ...,
    pattern=r"^[A-Za-z0-9\- ]{3,10}$",
    description=(
        "A postal code, consisting of alphanumeric characters, spaces, or "
        "hyphens. Must be between 3 and 10 characters long. Example: '1234AB' "
        "or '123 456'."
    ),
    examples=["12345", "1234AB", "123 456", "A1B-2C3", "98765"],
)

PhoneNumber = Field(
    ...,
    pattern=r"^\+?[0-9\s\-\(\)]{7,15}$",
    description=(
        "A phone number, which may include an optional '+' for international "
        "dialing. It can include digits, spaces, dashes, parentheses, and must"
        " be between 7 and 15 characters long. Example: '+1 (555) 123-4567' "
        "or '555-123-4567'."
    ),
    examples=[
        "+49 170 1234567",
        "+1 (555) 123-4567",
        "555-123-4567",
        "+44 20 7946 0958",
        "(123) 456-7890",
    ],
)


HouseNumber = Field(
    ...,
    pattern=r"^[0-9]{1,6}([A-Za-z]|\-[0-9]{1,3}|\/[0-9]{1,3})?$",
    description=(
        "A house number, which can be a number between 1 and 6 digits long. "
        "It may include letters, hyphenated numbers, or fraction-like formats "
        "(e.g., '123', '45A', '123-45', '12/3')."
    ),
    examples=["123A", "45", "123-45", "12/3", "1505-B", "101-A"],
)

WebURL: str = Field(
    ...,
    pattern=r"^https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+(?:\:[0-9]+)?"
    r"(?:/[^\s]*)?$",
    description=(
        "A valid web URL, starting with 'http://' or 'https://'. It can "
        "include domain names, optional ports, and paths. Example: "
        "'https://www.example.com' or 'http://example.com:8080/path'."
    ),
    examples=[
        "https://www.helpwave.de",
        "https://www.example.com",
        "http://example.com:8080/path",
        "https://mywebsite.org",
    ],
)


class RoleEnum(PyEnum):
    ADMIN = "admin"
    NORMAL = "normal"


class PlanTypeEnum(PyEnum):
    ONCE = "once"
    RECURRING = "recurring"
    LIFETIME = "lifetime"
    TRIAL = "trial"


class InvoiceStatusEnum(PyEnum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"


class MessageStatusEnum(PyEnum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"


class ContractKeyEnum(PyEnum):
    AGB_APP_ZUM_DOC_PATIENT = "agb_app_zum_doc_patient"
    AGB_MEDIQUU_CONNECT = "agb_mediquu_connect"
    AGB_APP_ZUM_DOC = "agb_app_zum_doc"
    AGB_MEDIQUU_NETZMANAGER = "agb_mediquu_netzmanager"
    AGB_MEDIQUU_CHAT = "agb_mediquu_chat"
    PRIVACY_CONCEPT = "privacy_concept"
    PRIVACY_CONCEPT_TASKS = "privacy_concept_tasks"
    AVV = "avv"
    AVV_TASKS = "avv_tasks"
    NDA = "nda"
    SUB = "sub"
    TOM = "tom"
