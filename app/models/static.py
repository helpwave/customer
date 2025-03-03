from enum import Enum as PyEnum


class RoleEnum(PyEnum):
    ADMIN = "admin"
    NORMAL = "normal"


class PlanTypeEnum(PyEnum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


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
