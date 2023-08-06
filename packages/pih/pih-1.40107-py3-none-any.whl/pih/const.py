from datetime import datetime
from enum import *
import os
from typing import List

from pih.collection import FieldItem, FieldItemList, MessageCommandDescription, ParamItem, PasswordSettings, ServiceRoleDescription, SettingsValue

#deprecated
class DATA_EXTRACTOR:

    USER_NAME_FULL: str = "user_name_full"
    USER_NAME: str = "user_name"
    AS_IS: str = "as_is"


class USER_PROPERTY:

    TELEPHONE_NUMBER: str = "telephoneNumber"
    EMAIL: str = "mail"
    DN: str = "distinguishedName"
    USER_ACCOUNT_CONTROL: str = "userAccountControl"
    LOGIN: str = "samAccountName"
    DESCRIPTION: str = "description"
    PASSWORD: str = "password"
    USER_STATUS: str = "userStatus"
    NAME: str = "name"

class BARCODE:

    FORMAT_DEFAULT: str = "code128"

class FILE:

    class EXTENSION:

        EXCEL_OLD: str = "xls"
        EXCEL_NEW: str = "xlsx"
        JPEG: str = "jpeg"
        PNG: str = "png"
        PYTHON: str = "py"

class URLS:

    MAIN: str = "pacifichosp.com"

class CONST:

    SITE_ADDRESS: str = URLS.MAIN
    MAIL_PREFIX: str = "mail"
    SITE_PROTOCOL: str = "https://"
    UNTRUST_SITE_PROTOCOL: str = "http://"
    EMAIL_ADDRESS: str = f"{MAIL_PREFIX}.{SITE_ADDRESS}"
    TELEPHONE_NUMBER_PREFIX: str = "+7"

    DATE_TIME_SPLITTER: str = "T"
    TIME_FORMAT: str = "%H:%M:00"
    DATE_TIME_FORMAT: str = f"%Y-%m-%d{DATE_TIME_SPLITTER}{TIME_FORMAT}"
    DATE_FORMAT: str = "%d.%m.%Y"

    API_SITE_ADDRESS: str = f"api.{SITE_ADDRESS}"

    PYPI_URL: str = "https://pypi.python.org/pypi/pih/json"

    TELEGRAM_BOT: str ="https://t.me/pacifichospital_bot"

    class DATA_STORAGE:

        DATE_TIME_SPLITTER: str = " "
        DATE_FORMAT: str = "%Y-%m-%d"
        TIME_FORMAT: str = "%H:%M:00"
        DATE_TIME_FORMAT: str = f"{DATE_FORMAT}{DATE_TIME_SPLITTER}{TIME_FORMAT}"

    class CACHE:
        
        class TTL:
            
            USER_WORKSTATIONS: int = 60

    class ERROR:

        class WAPPI:

            PROFILE_NOT_PAID: int = 402

    class TIME_TRACKING:

        REPORT_DAY_PERIOD_DEFAULT: int = 15

    class MESSAGE:

        class WHATSAPP:

            class WAPPI:

                URL_SEND_MESSAGE: str = "https://wappi.pro/api/sync/message/send?profile_id="
                URL_SEND_LIST_MESSAGE: str = "https://wappi.pro/api/sync/message/list/send?profile_id="
                URL_SEND_BUTTONS_MESSAGE: str = "https://wappi.pro/api/sync/message/buttons/send?profile_id="
                URL_GET_MESSAGES: str = "https://wappi.pro/api/sync/messages/get?profile_id="
                PROFILE_ID: str = "e6706eaf-ae17"
                AUTHORICATION: str = "6b356d3f53124af3078707163fdaebca3580dc38"
            
    class PYTHON:

        EXECUTOR: str = "py"
        PYPI: str = "pip"

    class SERVICE:

        NAME: str = "service"

    class FACADE:

        COMMAND_SUFFIX: str = "Core"
        PATH: str = "//pih/facade/"

    class PSTOOLS:

        NAME: str = "PSTools"
        EXECUTOR: str = "PsExec"
        PSKILL: str = "PsKill"

    class MSG:

        NAME: str = "msg"
        EXECUTOR: str = NAME

    class DOCS:

        EXCEL_TITLE_MAX_LENGTH: int = 31

        class INVENTORY:

            NAME_COLUMN_NAME: str = "наименование, назначение и краткая характеристика объекта"
            NUMBER_COLUMN_NAME: str = "инвентарный"
            QUANTITY_COLUMN_NAME: str = "фактическое наличие"
            NAME_MAX_LENTH: int = 30
            QUANTITY_NOT_SET: str = "-"

    class BARCODE_READER:

        PREFIX: str = "("
        SUFFIX: str = ")"

    class AD:

        SEARCH_ATTRIBUTES: List[str] = [
            USER_PROPERTY.LOGIN, USER_PROPERTY.NAME]
        SEARCH_ATTRIBUTE_DEFAULT: str = SEARCH_ATTRIBUTES[0]
        DOMAIN_NAME: str = "fmv"
        DOMAIN_ALIAS: str = "pih"
        DOMAIN_SUFFIX: str = "lan"
        DOMAIN: str = f"{DOMAIN_NAME}.{DOMAIN_SUFFIX}"
        DOMAIN_MAIN: str = DOMAIN
        USER_HOME_FOLDER_DISK: str = "U:"
        OU: str = "OU="
        ROOT_CONTAINER_DN: str = f"{OU}Unit,DC={DOMAIN_NAME},DC={DOMAIN_SUFFIX}"
        WORKSTATIONS_CONTAINER_DN: str = f"{OU}Workstations,{ROOT_CONTAINER_DN}"
        USERS_CONTAINER_DN_SUFFIX: str = f"Users,{ROOT_CONTAINER_DN}"
        ACTIVE_USERS_CONTAINER_DN: str = f"{OU}{USERS_CONTAINER_DN_SUFFIX}"
        INACTIVE_USERS_CONTAINER_DN: str = f"{OU}dead{USERS_CONTAINER_DN_SUFFIX}"
        PATH_ROOT: str = f"\\\{DOMAIN_MAIN}"
        SEARCH_ALL_PATTERN: str = "*"
        GRUOPS_CONTAINER_DN: str = f"{OU}Groups,{ROOT_CONTAINER_DN}"
        JOB_POSITIONS_CONTAINER_DN: str = f"{OU}Job positions,{GRUOPS_CONTAINER_DN}"
        LOCATION_JOINER: str = ":"
        TEMPLATED_USER_SERACH_TEMPLATE: str = "_*_"
        PROPERTY_ROOT_DN: str = f"{OU}Property,{GRUOPS_CONTAINER_DN}"
        PROPERTY_WS_DN: str = f"{OU}WS,{PROPERTY_ROOT_DN}"

        USER_ACCOUNT_CONTROL: List[str] = [
            "SCRIPT",
            "ACCOUNTDISABLE",
            "RESERVED",
            "HOMEDIR_REQUIRED",
            "LOCKOUT",
            "PASSWD_NOTREQD",
            "PASSWD_CANT_CHANGE",
            "ENCRYPTED_TEXT_PWD_ALLOWED",
            "TEMP_DUPLICATE_ACCOUNT",
            "NORMAL_ACCOUNT",
            "RESERVED",
            "INTERDOMAIN_TRUST_ACCOUNT",
            "WORKSTATION_TRUST_ACCOUNT",
            "SERVER_TRUST_ACCOUNT",
            "RESERVED",
            "RESERVED",
            "DONT_EXPIRE_PASSWORD",
            "MNS_LOGON_ACCOUNT",
            "SMARTCARD_REQUIRED",
            "TRUSTED_FOR_DELEGATION",
            "NOT_DELEGATED",
            "USE_DES_KEY_ONLY",
            "DONT_REQ_PREAUTH",
            "PASSWORD_EXPIRED",
            "TRUSTED_TO_AUTH_FOR_DELEGATION",
            "RESERVED",
            "PARTIAL_SECRETS_ACCOUNT"
        ]

        WORKSTATION_PREFIX_LIST: List[str] = ["ws-", "nb-"]

        ADMINISTRATOR: str = "Administrator"
        ADMINISTRATOR_PASSOWORD: str = "Fortun@90"

        class JobPositions(Enum):
            HR: str = auto()
            IT: str = auto()

        class Groups(Enum):
            TimeTrackingReport: str = auto()
            Inventory: str = auto()
            Polibase: str = auto()
            Admin: str = auto()
            ServiceAdmin: str = auto()

        class WSProperties(Enum):
    
            Watchable: int = 1
            Poweroffable: int = 2

    class NAME_POLICY:

        PARTS_LIST_MIN_LENGTH: int = 3
        PART_ITEM_MIN_LENGTH: int = 3

    class RPC:

        PING_COMMAND: str = "__ping__"
        EVENT_COMMAND: str = "__event__"
        SUBSCRIBE_COMMAND: str = "__subscribe__"

        @staticmethod
        def PORT(add: int = 0) -> int:
            return 50051 + add

    class HOST:

        class DEVELOPER:

            NAME: str = "ws-735.fmv.lan"

        class PRINTER_SERVER:

            NAME: str = "fmvdc1.fmv.lan"

        class PRINTER:

            NAME: str = "fmvdc2.fmv.lan"

        class ORION:

            NAME: str = "fmvdc2.fmv.lan"

        class AD:

            NAME: str = "fmvdc2.fmv.lan"

        class DOCS:

            NAME: str = "fmvdc2.fmv.lan"

        class POLIBASE:

            #shit - cause polibase is not accessable
            NAME: str = "fmvpolibase1.fmv.lan"

        class POLIBASE_TEST:
    
            NAME: str = "polibase_test"

        class MESSAGE:

            NAME: str = "backup_worker"

        class LOG_DB:
    
            NAME: str = "backup_worker"

        class HEAT_BEAT:
    
            NAME: str = "backup_worker"

        class FILE_WATCHDOG:

            NAME: str = "backup_worker"

        class MAIL:
        
            NAME: str = "backup_worker"

    class POLIBASE:

        PRERECORDING_PIN: int = 10
        RESERVED_TIME_A_PIN: int = 5
        RESERVED_TIME_B_PIN: int = 6
        RESERVED_TIME_C_PIN: int = 7


        TIME_PART_SYMBOL: str = "_"
        DATE_TIME_FORMAT: str = f"%d.%m.%Y{TIME_PART_SYMBOL}%H:%M:%S"
        TIME_FORMAT: str = "%H:%M:00"
        DATE_IS_NOT_SET_YEAR: int = 1899
        
        INSTANCE: str = "orcl.fmv.lan"
        USER: str = "POLIBASE"
        PASSWORD: str = "POLIBASE"

        class REVIEW_QUEST:
            
            INFORMATION_WAY_TYPES: List[str] = [
                "ваш постоянный клиент",
                "по рекомендации",
                "prodoctorov",
                "2gis",
                "интернет(сайт, яндекс, гугл)",
                "другое"
            ]

            FEEDBAK_CALL_TYPES: dict = {
                1 : "Да",
                2 : "Нет"
            }

            MAX_GRADE: int = 5
            HIGH_GRADE: int = 4
        
        class BARCODE:
            
            class PERSON:
                IMAGE_FORMAT: str =  FILE.EXTENSION.JPEG
            class PERSON_CHART_FOLDER:
                IMAGE_FORMAT: str = FILE.EXTENSION.PNG
            
            FORMAT: str = BARCODE.FORMAT_DEFAULT

            NEW_PATTERN: str = "new_"

            @staticmethod
            def get_file_name(pin: int, with_extension: bool = False) -> str:
                extension: str = f".{CONST.POLIBASE.BARCODE.PERSON.IMAGE_FORMAT}" if with_extension else ""
                return f"{CONST.POLIBASE.BARCODE.NEW_PATTERN}{pin}{extension}"
    
    class VISUAL:

        NUMBER_SYMBOLS: List[str] = [
           "1️⃣",
           "2️⃣",
           "3️⃣", 
           "4️⃣",
           "5️⃣",
           "6️⃣"
        ]

class PATH_SHARE:

    NAME: str = "shares"
    PATH: str = os.path.join(CONST.AD.PATH_ROOT, NAME)


class PATH_IT:

    NAME: str = "5. IT"
    NEW_EMPLOYEES_NAME: str = "New employees"
    ROOT: str = os.path.join(PATH_SHARE.PATH, NAME)

    @staticmethod
    def NEW_EMPLOYEE(name: str) -> str:
        return os.path.join(os.path.join(PATH_IT.ROOT, PATH_IT.NEW_EMPLOYEES_NAME), name)

class PATH_APP:

    NAME: str = "apps"
    FOLDER: str = os.path.join(CONST.FACADE.PATH, NAME)

class PATH_APP_DATA:

    NAME: str = "data"
    FOLDER: str = os.path.join(PATH_APP.FOLDER, NAME)

class PATH_POLIBASE_APP_DATA:
    
    NAME: str = "polibase"
    FOLDER: str = os.path.join(PATH_APP_DATA.FOLDER, NAME)
    PERSON_CHART_FOLDER: str = os.path.join(FOLDER, "person chart folder")

class PATH_USER:

    NAME: str = "homes"
    HOME_FOLDER: str = os.path.join(CONST.AD.PATH_ROOT, NAME)
    HOME_FOLDER_FULL: str = os.path.join(CONST.AD.PATH_ROOT, NAME)

    @staticmethod
    def get_document_name(user_name: str, login: str = None) -> str:
        return PATH_IT.NEW_EMPLOYEE(user_name) + (f" ({login})" if login else "") + ".docx"

class PATH_POLIBASE:
    
    NAME: str = CONST.HOST.POLIBASE.NAME
    TEST_SUFFIX: str = "_test"
    PERSON_CHART_FOLDER: str = PATH_POLIBASE_APP_DATA.PERSON_CHART_FOLDER


    @staticmethod
    def get_person_folder(pin: int, test: bool = False) -> str:
        root: str = PATH_POLIBASE.NAME
        if test:
            if root.find(".") != -1:
                root_parts: List = root.split(".")
                root_parts[0] += PATH_POLIBASE.TEST_SUFFIX
                root = ".".join(root_parts)
            else:
                root += PATH_POLIBASE.TEST_SUFFIX
        return os.path.join(os.path.join(f"//{root}", "polibaseData", "PERSONS"), str(pin))

class PATH_WS:

    NAME: str = f"WS{CONST.FACADE.COMMAND_SUFFIX}"
    PATH: str = os.path.join(CONST.FACADE.PATH, NAME)


class PATHS:

    SHARE: PATH_SHARE = PATH_SHARE()
    IT: PATH_IT = PATH_IT()
    USER: PATH_USER = PATH_USER()
    POLIBASE: PATH_POLIBASE = PATH_POLIBASE()
    WS: PATH_WS = PATH_WS()

class MarkType(Enum):

    NORMAL: int = auto()
    FREE: int = auto()
    GUEST: int = auto()
    TEMPORARY: int = auto()


class FIELD_NAME_COLLECTION:

    FULL_NAME: str = "FullName"
    TYPE: str = "type"
    GROUP_NAME: str = "GroupName"
    GROUP_ID: str = "GroupID"
    COMMENT: str = "Comment"
    CHART_FOLDER: str = "ChartFolder"
    BIRTH: str = "Birth"
    TAB_NUMBER: str = "TabNumber"
    OWNER_TAB_NUMBER: str = "OwnerTabNumber"
    NAME: str = USER_PROPERTY.NAME
    MIDNAME: str = "MidName"
    PERSON_ID: str = "pID"
    MARK_ID: str = "mID"
    ID: str = "id"
    PIN: str = "pin"
    VISIT_ID: str = "visitID"
    MESSAGE_ID: str = "messageID"
    VALUE: str = "value"
    FILE: str = "file"
    DIVISION_NAME: str = "DivisionName"
    BARCODE: str = "barcode"
    PROPERTIES: str = "properties"
    MESSAGE: str = "message"
    STATUS: str = "status"
    FEEDBACK_CALL_STATUS: str = "feedbackCallStatus"
    REGISTRATION_DATE: str = "registrationDate"
    TYPE: str = "type"

    PORT_NAME: str = "portName"

    SEARCH_ATTRIBUTE_LOGIN: str = USER_PROPERTY.LOGIN
    SEARCH_ATTRIBUTE_NAME: str = USER_PROPERTY.NAME

    TELEPHONE_NUMBER: str = USER_PROPERTY.TELEPHONE_NUMBER
    EMAIL: str = USER_PROPERTY.EMAIL
    DN: str = USER_PROPERTY.DN
    LOGIN: str = USER_PROPERTY.LOGIN
    DESCRIPTION: str = USER_PROPERTY.DESCRIPTION
    PASSWORD: str = USER_PROPERTY.PASSWORD
    ACCESSABLE: str = "accessable"
    STEP: str = "step"
    STEP_CONFIRMED: str = "stepConfirmed"
    GRADE: str = "grade"
    INFORMATION_WAY: str = "informationWay"
    TIME: str = "time"

    TIMESTAMP: str = "timestamp"
    DATE: str = "date"
    BEGIN_DATE: str = "beginDate"
    COMPLETE_DATE: str = "completeDate"
    RECIPIENT: str = "recipient"
    TYPE: str = "type"

    INVENTORY_NUMBER: str = "inventory_number"
    QUANTITY: str = "quantity"
    ROW: str = "row"
    NAME_COLUMN: str = "name_column"
    INVENTORY_NUMBER_COLUMN: str = "inventory_number_column"
    QUANTITY_COLUMN: str = "quantity_column"

    TEMPLATE_USER_CONTAINER: str = "templated_user"
    CONTAINER: str = "container"

    REMOVE: str = "remove"
    AS_FREE: str = "as_free"
    CANCEL: str = "cancel"


class FIELD_ITEM_COLLECTION:

    TAB_NUMBER: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.TAB_NUMBER, "Табельный номер")
    OWNER_TAB_NUMBER: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.OWNER_TAB_NUMBER, "Табельный номер владельца")
    FULL_NAME: FieldItem = FieldItem(
        FIELD_NAME_COLLECTION.FULL_NAME, "Полное имя")
    

class FIELD_COLLECTION:

    INDEX: FieldItem = FieldItem("__Index__", "Индекс", True)

    VALUE: FieldItem = FieldItem("", "Значение", True)
    VALUE_LIST: FieldItem = FieldItem("", "Список значений", True)

    class ORION:

        MARK_ACTION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.REMOVE, "Удалить"),
            FieldItem(FIELD_NAME_COLLECTION.AS_FREE, "Сделать свободной"),
            FieldItem(FIELD_NAME_COLLECTION.CANCEL, "Оставить")
        )

        GROUP_BASE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.GROUP_NAME, "Уровень доступа"),
            FieldItem(FIELD_NAME_COLLECTION.COMMENT, "Описание", False)
        )

        TAB_NUMBER_BASE: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.TAB_NUMBER)

        FREE_MARK: FieldItemList = FieldItemList(
            TAB_NUMBER_BASE, GROUP_BASE)

        TAB_NUMBER: FieldItemList = FieldItemList(
            TAB_NUMBER_BASE,
            FieldItem(FIELD_NAME_COLLECTION.DIVISION_NAME, "Подразделение"),
            GROUP_BASE).position(FIELD_NAME_COLLECTION.DIVISION_NAME, 2)

        TEMPORARY_MARK: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.TAB_NUMBER,
            FIELD_ITEM_COLLECTION.OWNER_TAB_NUMBER,
            FIELD_ITEM_COLLECTION.FULL_NAME,
            FieldItem(FIELD_NAME_COLLECTION.PERSON_ID, "Person ID", False),
            FieldItem(FIELD_NAME_COLLECTION.MARK_ID, "Mark ID", False)
        )

        PERSON: FieldItemList = FieldItemList(
            TAB_NUMBER,
            FieldItem(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER,
                      "Телефон", True),
            FIELD_ITEM_COLLECTION.FULL_NAME
        ).position(FIELD_NAME_COLLECTION.FULL_NAME, 1).position(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, 2)

        PERSON_DIVISION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.ID, "ID", False),
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Название подразделения")
        )

        PERSON_EXTENDED: FieldItemList = FieldItemList(
            PERSON,
            FieldItem(FIELD_NAME_COLLECTION.PERSON_ID, "Person ID", False),
            FieldItem(FIELD_NAME_COLLECTION.MARK_ID, "Mark ID", False)
        )

        GROUP: FieldItemList = FieldItemList(
            GROUP_BASE,
            FieldItem(FIELD_NAME_COLLECTION.GROUP_ID, "Group id", False)
        ).visible(FIELD_NAME_COLLECTION.COMMENT, True)

        GROUP_STATISTICS: FieldItemList = FieldItemList(
            GROUP,
            FieldItem("Count", "Количество"),
        ).visible(FIELD_NAME_COLLECTION.COMMENT, False)

        TIME_TRACKING: FieldItemList = FieldItemList(FIELD_ITEM_COLLECTION.FULL_NAME,
                                                     FIELD_ITEM_COLLECTION.TAB_NUMBER,
                                                     FieldItem(
                                                         "TimeVal", "Время"),
                                                     FieldItem(
                                                         "Remark", "Remark"),
                                                     FieldItem(
                                                         "Mode", "Mode"))

        TIME_TRACKING_RESULT: FieldItemList = FieldItemList(
            FIELD_ITEM_COLLECTION.FULL_NAME,
            FIELD_ITEM_COLLECTION.TAB_NUMBER,
            FieldItem(
                "Date", "Дата"),
            FieldItem(
                "EnterTime", "Время прихода"),
            FieldItem(
                "ExitTime", "Время ухода"),
            FieldItem(
                "Duration", "Продолжительность"))

    class INRENTORY:

        ITEM: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME,
                      "Название инвентарного объекта"),
            FieldItem(FIELD_NAME_COLLECTION.INVENTORY_NUMBER,
                      "Инвентарный номер"),
            FieldItem(FIELD_NAME_COLLECTION.QUANTITY, "Количество"),
            FieldItem(FIELD_NAME_COLLECTION.NAME_COLUMN, None, False),
            FieldItem(FIELD_NAME_COLLECTION.INVENTORY_NUMBER_COLUMN, None, False),
            FieldItem(FIELD_NAME_COLLECTION.QUANTITY_COLUMN, None, False)
        )

    class AD:

        WORKSTATION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Имя компьютера"),
            FieldItem(FIELD_NAME_COLLECTION.PROPERTIES, "Свойства")
        )

        USER_WORKSTATION: FieldItemList = FieldItemList(
            WORKSTATION,
            FieldItem(FIELD_NAME_COLLECTION.ACCESSABLE, "Доступен"),
            FieldItem(FIELD_NAME_COLLECTION.LOGIN, "Имя залогированного пользователя")
        )

        SEARCH_ATTRIBUTE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.SEARCH_ATTRIBUTE_LOGIN, "Логин"),
            FieldItem(FIELD_NAME_COLLECTION.SEARCH_ATTRIBUTE_NAME, "Имя")
        )

        CONTAINER: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Название"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Описание")
        )

        USER_NAME: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Имя пользователя")
        )

        TEMPLATED_USER: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Описание"))

        USER: FieldItemList = FieldItemList(CONTAINER,
                                            FieldItem(FIELD_NAME_COLLECTION.LOGIN, "Логин"),
                                            FieldItem(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, "Телефон"),
                                            FieldItem(FIELD_NAME_COLLECTION.EMAIL, "Электронная почта"),
                                            FieldItem(FIELD_NAME_COLLECTION.DN, "Размещение"),
                                            FieldItem("userAccountControl", "Свойства аккаунта")).position(FIELD_NAME_COLLECTION.DESCRIPTION, 4)

        CONTAINER_TYPE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.TEMPLATE_USER_CONTAINER,
                      "Шаблонный пользователь"),
            FieldItem(FIELD_NAME_COLLECTION.CONTAINER, "Контейнер"))


    class POLIBASE:

        PERSON_BASE: FieldItemList = FieldItemList(FieldItem(FIELD_NAME_COLLECTION.PIN, "Номер пациента"),
                                              FieldItem(FIELD_NAME_COLLECTION.FULL_NAME, "ФИО пациента"),
                                              FieldItem(FIELD_NAME_COLLECTION.TELEPHONE_NUMBER, "Телефон"))

        PERSON_VISIT: FieldItemList = FieldItemList(PERSON_BASE,
                                              FieldItem(FIELD_NAME_COLLECTION.REGISTRATION_DATE, "Дата регистрации"))

        PERSON: FieldItemList = FieldItemList(PERSON_BASE,
                                              FieldItem(FIELD_NAME_COLLECTION.BIRTH, "День рождения", True, "datetime"),
                                              FieldItem(FIELD_NAME_COLLECTION.EMAIL, "Электронная почта"),
                                              FieldItem(FIELD_NAME_COLLECTION.CHART_FOLDER, "Папка карты пациента"),
                                              FieldItem(FIELD_NAME_COLLECTION.COMMENT, "Комментарий"))


    class POLICY:

        PASSWORD_TYPE: FieldItemList = FieldItemList(
            FieldItem("PC", "PC"),
            FieldItem("EMAIL", "Email"),
            FieldItem("SIMPLE", "Simple"),
            FieldItem("STRONG", "Strong"))

    class PRINTER:

        MAIN: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Name"),
            FieldItem("serverName", "Server name"),
            FieldItem("portName", "Host name"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Description"),
            FieldItem("adminDescription", "Admin description", False),
            FieldItem("driverName", "Driver name")
        )


class FIELD_COLLECTION_ALIAS(Enum):
    TIME_TRACKING: FieldItem = FIELD_COLLECTION.ORION.TIME_TRACKING
    PERSON: FieldItem = FIELD_COLLECTION.ORION.PERSON
    TEMPORARY_MARK: FieldItem = FIELD_COLLECTION.ORION.TEMPORARY_MARK
    POLIBASE_PERSON: FieldItem = FIELD_COLLECTION.POLIBASE.PERSON
    POLIBASE_PERSON_VISIT: FieldItem = FIELD_COLLECTION.POLIBASE.PERSON_VISIT
    PERSON_DIVISION: FieldItem = FIELD_COLLECTION.ORION.PERSON_DIVISION
    PERSON_EXTENDED: FieldItem = FIELD_COLLECTION.ORION.PERSON_EXTENDED
    WORKSTATION: FieldItem = FIELD_COLLECTION.AD.WORKSTATION
    USER_WORKSTATION: FieldItem = FIELD_COLLECTION.AD.USER_WORKSTATION
    VALUE: FieldItem = FIELD_COLLECTION.VALUE
    VALUE_LIST: FieldItem = FIELD_COLLECTION.VALUE_LIST

class PolibasePersonNotifierStatus(Enum):
    START: int = auto()
    TELEPHONE_NUMBER_IS_NOT_SET: int = auto()
    TELEPHONE_NUMBER_IS_WRONG: int = auto()
    ALLOW: int = auto()
    REJECTED: int = auto()
    ASK_FOR_EMAIL: int = auto()
    ASK_FOR_EMAIL_CONFIRMED: int = auto()
    EMAIL_IS_WRONG: int = auto()
    EMAIL_IS_WRONG_CONFIRMED: int = auto()
    EMAIL_IS_SET: int = auto()


class PolibasePersonVisitNotificationType(Enum):
    VISIT_GREETING: int = 1
    VISIT_REMINDER: int = 2

class PolibasePersonReviewQuestStep(Enum):
    BEGIN: int = auto()
    #
    ASK_GRADE: int = auto()
    ASK_FEEDBACK_CALL: int = auto()
    ASK_INFORMATION_WAY: int = auto()
    #
    COMPLETE: int = auto()

LINK_EXT = "lnk"

class PrinterCommands(Enum):
    REPORT: str = "report"
    STATUS: str = "status"


class PASSWORD_GENERATION_ORDER:

    SPECIAL_CHARACTER: str = "s"
    LOWERCASE_ALPHABET: str = "a"
    UPPERCASE_ALPHABET: str = "A"
    DIGIT: str = "d"
    DEFAULT_ORDER_LIST: List[str] = [SPECIAL_CHARACTER,
                                     LOWERCASE_ALPHABET, UPPERCASE_ALPHABET, DIGIT]


class PASSWORD:

    class SETTINGS:

        SIMPLE: PasswordSettings = PasswordSettings(
            3, "", PASSWORD_GENERATION_ORDER.DEFAULT_ORDER_LIST, 0, 3, 0, 0, False)
        NORMAL: PasswordSettings = PasswordSettings(
            8, "!@#", PASSWORD_GENERATION_ORDER.DEFAULT_ORDER_LIST, 3, 3, 1, 1, False)
        STRONG: PasswordSettings = PasswordSettings(
            10, "#%+\-!=@()_",  PASSWORD_GENERATION_ORDER.DEFAULT_ORDER_LIST, 3, 3, 2, 2, True)
        DEFAULT: PasswordSettings = NORMAL
        PC: PasswordSettings = NORMAL
        EMAIL: PasswordSettings = NORMAL

    def get(name: str) -> SETTINGS:
        return PASSWORD.__getattribute__(PASSWORD.SETTINGS, name)


class LogTypes(Enum):
    MESSAGE: str = "message"
    COMMAND: str = "command"
    DEFAULT: str = MESSAGE


class MessageChannels(Enum):
    BACKUP: int = auto()
    NOTIFICATION: int = auto()
    DEBUG: int = auto()
    DEBUG_BOT: int = auto()
    PRINTER: int = auto()
    PRINTER_BOT: int = auto()
    SYSTEM: int = auto()
    SYSTEM_BOT: int = auto()
    HR: int = auto()
    HR_BOT: int = auto()
    IT: int = auto()
    IT_BOT: int = auto()
    POLIBASE_PERSON_FEEDBACK_CALL: int = auto()
    POLIBASE_PERSON_REVIEW_QUEST_RESULT: int = auto()
    DEFAULT: int = NOTIFICATION


class LogLevels(Enum):
    NORMAL: int = 1
    ERROR: int = 2
    EVENT: int = 4
    DEBUG: str = 8
    TASK: int = 16
    NOTIFICATION: str = 32
    SILENCE: str = 4048
    DEFAULT: str = NORMAL


class ServiceCommands(Enum):
    ping: int = auto()
    subscribe: int = auto()
    unsubscribe: int = auto()
    unsubscribe_all: int = auto()
    #Log
    send_log_message: int = auto()
    send_command_message: int = auto()
    send_internal_message: int = auto()
    send_buffered_message: int = auto()
    #Documents
    create_user_document: int = auto()
    create_time_tracking_report: int = auto()
    create_barcodes_for_inventory: int = auto()
    create_barcode_for_polibase_person: int = auto()
    create_barcode_for_polibase_person_chart_folder: int = auto()
    check_inventory_report: int = auto()
    get_inventory_report: int = auto()
    save_inventory_report_item: int = auto()
    close_inventory_report: int = auto()
    #Polibase
    get_polibase_person_by_pin: int = auto()
    get_polibase_persons_by_pin: int = auto()
    get_polibase_persons_by_chart_folder_name: int = auto() 
    get_polibase_persons_by_full_name: int = auto()
    get_polibase_person_pin_list_with_old_format_barcode: int = auto()
    get_polibase_person_registrator_by_pin: int = auto()
    get_polibase_persons_pin_by_visit_date: int = auto()
    #
    get_polibase_person_visits_by_registration_date: int = auto()
    get_polibase_person_visits_last_id: int = auto()
    get_polibase_person_visits_after_id: int = auto()
    #
    set_polibase_person_chart_folder: int = auto()
    set_polibase_person_email: int = auto()
    set_polibase_person_barcode_by_pin: int = auto()
    check_polibase_person_chart_folder: int = auto()

    #ActiveDirectory
    check_user_exists_by_login: int = auto()
    get_user_by_full_name: int = auto()
    get_users_by_name: int = auto()
    get_active_users_by_name: int = auto()
    get_user_by_login: int = auto()
    get_template_users: int = auto()
    get_containers: int = auto()
    get_users_by_job_position: int = auto()
    get_users_in_group: int = auto()
    create_user_by_template: int = auto()
    create_user_in_container: int = auto()
    set_user_telephone: int = auto()
    authenticate: int = auto()
    set_user_password: int = auto()
    set_user_status: int = auto()
    get_printers: int = auto()
    remove_user: int = auto()
    get_all_workstations: int = auto()
    get_all_workstations_with_user: int = auto()
    get_workstation_by_user: int = auto()
    get_user_by_workstation: int = auto()
    #Printer
    printers_report: int = auto()
    printers_status: int = auto()
    #Orion
    get_free_marks: int = auto()
    get_temporary_marks: int = auto()
    get_person_divisions: int = auto()
    get_time_tracking: int = auto() 
    get_all_persons: int = auto()
    get_owner_mark_for_temporary_mark: int = auto()
    get_mark_by_tab_number: int = auto()
    get_mark_by_person_name: int = auto()
    get_free_marks_group_statistics: int = auto()
    get_free_marks_by_group_id: int = auto()
    set_full_name_by_tab_number: int = auto()
    set_telephone_by_tab_number: int = auto()
    check_mark_free: int = auto()
    create_mark: int = auto()
    remove_mark_by_tab_number: int = auto()
    make_mark_as_free_by_tab_number: int = auto()
    make_mark_as_temporary: int = auto()
    #PolibaseDatabaseBackup
    create_polibase_database_backup: int = auto()
    #DataStorage::PolibaseReviewQuest
    get_polibase_persons_review_quest: int = auto()
    set_polibase_person_review_quest_step: int = auto()
    set_polibase_person_review_quest_grade: int = auto()
    begin_polibase_person_review_quest: int = auto()
    complete_polibase_person_review_quest: int = auto()
    confirm_polibase_person_review_quest_step: int = auto()
    set_polibase_person_review_quest_information_way: int = auto()
    set_polibase_person_review_quest_message: int = auto()
    set_polibase_person_review_quest_feedback_call_status: int = auto()
    clear_polibase_persons_review_quest: int = auto()
    #DataStorage::Settings
    set_settings_value: int = auto()
    get_settings_value: int = auto()
    #HeatBeat
    heat_beat: int = auto()
    #Notifier
    create_notifier_polibase_person: int = auto()
    get_notifier_polibase_person_by_pin: int = auto()
    get_notifier_polibase_persons_by_status: int = auto()
    set_notifier_polibase_person_status_by_pin: int = auto()
    #Visit
    register_polibase_person_visit: int = auto()
    search_polibase_person_visits: int = auto()
    #Visit notification
    register_polibase_person_visit_notification: int = auto()
    search_polibase_person_visit_notifications: int = auto()
    #
    check_email_accessibility: int = auto()
    #
    register_buffered_message: int = auto()
    search_buffered_messages: int = auto()
    update_buffered_message: int = auto()
    

class ServiceRoles(Enum):

    MESSAGE: ServiceRoleDescription = ServiceRoleDescription(
                                            name="Message",
                                            description="Message api service",
                                            #!!!
                                            host=CONST.HOST.MESSAGE.NAME, 
                                            port=CONST.RPC.PORT(2),
                                            commands=[
                                                        ServiceCommands.send_log_message,
                                                        ServiceCommands.send_command_message,
                                                        ServiceCommands.send_internal_message,
                                                        ServiceCommands.send_buffered_message
                                                    ],
                                            modules=["telegram-send"])


    DATA_STORAGE: ServiceRoleDescription = ServiceRoleDescription(
                                            name="DataStorage",
                                            description="DataStorage api service", 
                                            host=CONST.HOST.MESSAGE.NAME, 
                                            port=CONST.RPC.PORT(1),
                                            commands=[
                                                        ServiceCommands.get_notifier_polibase_person_by_pin,
                                                        ServiceCommands.get_notifier_polibase_persons_by_status,
                                                        ServiceCommands.set_notifier_polibase_person_status_by_pin,
                                                        ServiceCommands.create_notifier_polibase_person,
                                                        #
                                                        ServiceCommands.get_polibase_persons_review_quest,
                                                        ServiceCommands.set_polibase_person_review_quest_step,
                                                        ServiceCommands.begin_polibase_person_review_quest,
                                                        ServiceCommands.complete_polibase_person_review_quest,
                                                        ServiceCommands.set_polibase_person_review_quest_grade,
                                                        ServiceCommands.set_polibase_person_review_quest_information_way,
                                                        ServiceCommands.set_polibase_person_review_quest_message,
                                                        ServiceCommands.set_polibase_person_review_quest_feedback_call_status,
                                                        ServiceCommands.confirm_polibase_person_review_quest_step,
                                                        ServiceCommands.clear_polibase_persons_review_quest,
                                                        #
                                                        ServiceCommands.register_polibase_person_visit,
                                                        ServiceCommands.search_polibase_person_visits,
                                                        #
                                                        ServiceCommands.register_polibase_person_visit_notification,
                                                        ServiceCommands.search_polibase_person_visit_notifications,
                                                        #
                                                        ServiceCommands.register_buffered_message,
                                                        ServiceCommands.search_buffered_messages,
                                                        ServiceCommands.update_buffered_message,
                                                        #
                                                        ServiceCommands.get_settings_value,
                                                        ServiceCommands.set_settings_value,
                                                    ],
                                            modules=["mysql-connector-python", "pysos"])

    HEART_BEAT: ServiceRoleDescription = ServiceRoleDescription(
        name="HeartBeat",
        description="Heart beat api service",
        host=CONST.HOST.HEAT_BEAT.NAME,
        port=CONST.RPC.PORT(2),
        commands=[ServiceCommands.heat_beat],
        modules=["schedule"])

    FILE_WATCHDOG: ServiceRoleDescription = ServiceRoleDescription(
        name="FileWatchdog",
        description="FileWatchdog api service",
        host=CONST.HOST.FILE_WATCHDOG.NAME,
        port=CONST.RPC.PORT(3),
        modules=["watchdog"])

    MAIL: ServiceRoleDescription = ServiceRoleDescription(
        name="Mail",
        description="Mail api service",
        host=CONST.HOST.MAIL.NAME,
        port=CONST.RPC.PORT(4),
        commands=
                [
                    ServiceCommands.check_email_accessibility
                ],
        modules=["py3-validate-email", "verify-email"])

    AD: ServiceRoleDescription = ServiceRoleDescription(
                                                name="ActiveDirectory",
                                                description="Active directory api service",
                                                host=CONST.HOST.AD.NAME,
                                                port=CONST.RPC.PORT(),
                                                commands=
                                                        [
                                                            ServiceCommands.authenticate,
                                                            ServiceCommands.check_user_exists_by_login,
                                                            ServiceCommands.get_user_by_full_name,
                                                            ServiceCommands.get_users_by_name,
                                                            ServiceCommands.get_active_users_by_name,
                                                            ServiceCommands.get_user_by_login,
                                                            ServiceCommands.get_template_users,
                                                            ServiceCommands.get_containers,
                                                            ServiceCommands.get_users_by_job_position,
                                                            ServiceCommands.get_users_in_group, 
                                                            ServiceCommands.get_printers,
                                                            ServiceCommands.get_all_workstations,
                                                            ServiceCommands.get_all_workstations_with_user,
                                                            ServiceCommands.get_workstation_by_user,
                                                            ServiceCommands.get_user_by_workstation,
                                                            ServiceCommands.create_user_by_template,
                                                            ServiceCommands.create_user_in_container,
                                                            ServiceCommands.set_user_telephone,
                                                            ServiceCommands.set_user_password,
                                                            ServiceCommands.set_user_status,
                                                            ServiceCommands.remove_user
                                                        ],
                                                modules=["pyad", "pywin32", "wmi"]
                                            )

    DOCS: ServiceRoleDescription = ServiceRoleDescription(
                                                name="Docs", 
                                                description="Documents api service",
                                                host=CONST.HOST.DOCS.NAME,
                                                port=CONST.RPC.PORT(1),
                                                commands=
                                                        [
                                                            ServiceCommands.get_inventory_report,
                                                            ServiceCommands.create_user_document,
                                                            ServiceCommands.create_time_tracking_report,
                                                            ServiceCommands.create_barcodes_for_inventory,
                                                            ServiceCommands.create_barcode_for_polibase_person,
                                                            ServiceCommands.create_barcode_for_polibase_person_chart_folder,
                                                            ServiceCommands.check_inventory_report,
                                                            ServiceCommands.save_inventory_report_item,
                                                            ServiceCommands.close_inventory_report
                                                        ],
        modules=["xlsxwriter", "xlrd", "xlutils", "openpyxl",
                                                    "python-barcode", "Pillow", "transliterate"]
                                            )

    PRINTER: ServiceRoleDescription = ServiceRoleDescription(
                                                    name="Printer",
                                                    description="Printer api service", 
                                                    host=CONST.HOST.PRINTER.NAME, 
                                                    port=CONST.RPC.PORT(2),
                                                    commands=
                                                            [
                                                                ServiceCommands.printers_report,
                                                                ServiceCommands.printers_status
                                                            ]
                                                           )

    MARK: ServiceRoleDescription = ServiceRoleDescription(
                                                name="Orion",
                                                description="Orion api service",
                                                host=CONST.HOST.ORION.NAME,
                                                port=CONST.RPC.PORT(3),
                                                commands=
                                                        [
                                                            ServiceCommands.get_free_marks,
                                                            ServiceCommands.get_temporary_marks,
                                                            ServiceCommands.get_person_divisions,
                                                            ServiceCommands.get_time_tracking,
                                                            ServiceCommands.get_all_persons,
                                                            ServiceCommands.get_mark_by_tab_number,
                                                            ServiceCommands.get_mark_by_person_name,
                                                            ServiceCommands.get_free_marks_group_statistics,
                                                            ServiceCommands.get_free_marks_by_group_id,
                                                            ServiceCommands.get_owner_mark_for_temporary_mark,
                                                            ServiceCommands.set_full_name_by_tab_number, 
                                                            ServiceCommands.set_telephone_by_tab_number,
                                                            ServiceCommands.check_mark_free,
                                                            ServiceCommands.create_mark,
                                                            ServiceCommands.make_mark_as_free_by_tab_number,
                                                            ServiceCommands.make_mark_as_temporary,
                                                            ServiceCommands.remove_mark_by_tab_number,
                                                        ],
                                               modules=["pymssql"])


    POLIBASE: ServiceRoleDescription = ServiceRoleDescription(
                                                    name="Polibase",
                                                    description="Polibase api service & FastApi server",
                                                    host=CONST.HOST.POLIBASE.NAME,
                                                    port=CONST.RPC.PORT(),
                                                    commands=[
                                                                ServiceCommands.get_polibase_person_by_pin,
                                                                ServiceCommands.get_polibase_persons_by_pin,
                                                                ServiceCommands.get_polibase_persons_by_full_name,
                                                                ServiceCommands.get_polibase_persons_by_chart_folder_name,
                                                                ServiceCommands.get_polibase_person_registrator_by_pin,
                                                                ServiceCommands.get_polibase_person_pin_list_with_old_format_barcode,
                                                                #trash start
                                                                ServiceCommands.get_polibase_persons_pin_by_visit_date,
                                                                ServiceCommands.get_polibase_person_visits_by_registration_date,
                                                                ServiceCommands.get_polibase_person_visits_after_id,
                                                                ServiceCommands.get_polibase_person_visits_last_id,
                                                                #
                                                                ServiceCommands.set_polibase_person_chart_folder,
                                                                ServiceCommands.set_polibase_person_email,
                                                                ServiceCommands.set_polibase_person_barcode_by_pin,
                                                                ServiceCommands.check_polibase_person_chart_folder
                                                            ], 
                                                    modules=["cx-Oracle", "fastapi", "uvicorn[all]", "transliterate"])

    POLIBASE_DATABASE: ServiceRoleDescription = ServiceRoleDescription(
        name="PolibaseDB",
        description="Polibase database api",
        host=CONST.HOST.POLIBASE.NAME,
        port=CONST.RPC.PORT(1),
        commands=[
                    ServiceCommands.create_polibase_database_backup
                ],
        modules=[])

    POLIBASE_APP: ServiceRoleDescription = ServiceRoleDescription(
                                                name="PolibaseApp",
                                                description="Polibase Application service",
                                                host=CONST.HOST.POLIBASE.NAME,
                                                port=CONST.RPC.PORT(2),
                                                commands=[
                                                        ], 
                                                modules=[])


    DEVELOPER: ServiceRoleDescription = ServiceRoleDescription(
        name="Developer",
        description="Developer service",
        host=CONST.HOST.DEVELOPER.NAME,
        port=CONST.RPC.PORT(4),
        visible_for_admin = False,
        keep_alive = False,
        weak_subscribtion = True)

    DEVELOPER2: ServiceRoleDescription = ServiceRoleDescription(
        name="Developer2",
        description="Developer2 service",
        host=CONST.HOST.DEVELOPER.NAME,
        port=CONST.RPC.PORT(5),
        visible_for_admin = False,
        keep_alive = False,
        weak_subscribtion = True)


class SubscribtionType:
    BEFORE: int = 1
    AFTER: int = 2

class InternalMessageMethodTypes(Enum):

    REMOTE: int = auto()
    LOCAL_MSG: int = auto()
    LOCAL_PSTOOL_MSG: int = auto()

class MessageTypes(Enum):

    WHATSAPP: int = 1
    TELEGRAM: int = 2
    INTERNAL: int = 3


class MessageStatus(Enum):

    REGISTERED: int = 0
    COMPLETE: int = 1
    AT_WORK: int = 2
    ERROR: int = 3
    ABORT: int = 4

class PolibasePersonVisitStatus:

    CONFIRMED :int = 107


class Settings(Enum):

    WHATSAPP_MESSAGE_COUNTER: SettingsValue = SettingsValue(None, 20)
    #
    POLIBASE_PERSON_REVIEW_QUEST_TEST: SettingsValue = SettingsValue(None, True)
    POLIBASE_PERSON_REVIEW_QUEST_STATUS: SettingsValue = SettingsValue(
        None, True)
    POLIBASE_PERSON_REVIEW_QUEST_START_TIME: SettingsValue = SettingsValue(
        None, "9:00")
    POLIBASE_PERSON_REVIEW_QUEST_MAX_WORKERS: SettingsValue = SettingsValue(
        None, 20)
    POLIBASE_PERSON_REVIEW_QUEST_WAIT_TIME: SettingsValue = SettingsValue(
        None, 15)
    #
    POLIBASE_PERSON_VISIT_NEED_REGISTER_GREETING_NOTIFICATION: SettingsValue = SettingsValue(
        None, True)
    POLIBASE_PERSON_VISIT_NEED_REGISTER_REMINDER_NOTIFICATION: SettingsValue = SettingsValue(
        None, True)
    POLIBASE_PERSON_VISIT_TIME_BEFORE_REMINDER_NOTIFICATION_IN_MINUTES: SettingsValue = SettingsValue(
        None, 60)
    POLIBASE_PERSON_VISIT_NEED_CONFIRMATION_STATUS_FOR_SEND_NOTIFICATION: SettingsValue = SettingsValue(
        None, False)
    POLIBASE_PERSON_VISIT_NOTIFICATION_TEST_TELEPHONE_NUMBER: SettingsValue = SettingsValue(
        None, "+79146717744")
    POLIBASE_PERSON_VISIT_LAST_ADDED_ID: SettingsValue = SettingsValue(None, None)
    WHATSAPP_FUNCTIONAL_IS_ON: SettingsValue = SettingsValue(
        None, True)
    WHATSAPP_BUFFERED_MESSAGE_MIN_DELAY_IN_MILLISECONDS: SettingsValue = SettingsValue(
        None, 200)
    WHATSAPP_BUFFERED_MESSAGE_MAX_DELAY_IN_MILLISECONDS: SettingsValue = SettingsValue(
        None, 800)

class MessageCommands(Enum):

    DEBUG: MessageCommandDescription = MessageCommandDescription(
        "It is a debug command", MessageChannels.NOTIFICATION, LogLevels.DEBUG.value)
        
    PRINTER_REPORT: MessageCommandDescription = MessageCommandDescription("Принтер {printer_name} ({location}):\n {printer_report}", MessageChannels.PRINTER, LogLevels.NORMAL.value, (ParamItem(
        "printer_name", "Name of printer"), ParamItem("location", "Location"), ParamItem("printer_report", "Printer report")))
    #
    LOG_IN: MessageCommandDescription = MessageCommandDescription(
        "Пользователь {full_name} ({login}) вошел с компьютера {computer_name}", MessageChannels.SYSTEM, LogLevels.NORMAL.value, (ParamItem("full_name", "Name of user"), ParamItem("login", "Login of user"), ParamItem("computer_name", "Name of computer")))

    START_SESSION: MessageCommandDescription = MessageCommandDescription(
        "Пользователь {full_name} ({login}) начал пользоваться программой {app_name}.\nВерсия: {version}.\nНазвание компьютера: {computer_name}", MessageChannels.SYSTEM, LogLevels.NORMAL.value, (ParamItem("full_name", "Name of user"), ParamItem("login", "Login of user"), ParamItem("app_name", "Name of user"),  ParamItem("version", "Version"), ParamItem("computer_name", "Name of computer")))

    SERVICE_STARTED: MessageCommandDescription = MessageCommandDescription(
        "Сервис {service_name} ({service_description}) запущен!\nИмя хоста: {host_name}\nПорт: {port}\nИдентификатор процесса: {pid}\n", MessageChannels.SYSTEM, LogLevels.NORMAL.value, (ParamItem("service_name", "Name of service"), ParamItem("service_description", "Description of service"), ParamItem("host_name", "Name of host"), ParamItem("port", "Port"), ParamItem("pid", "PID")))
    
    SERVICE_NOT_STARTED: MessageCommandDescription = MessageCommandDescription(
        "Сервис {service_name} ({service_description}) запущен!\nИмя хоста: {host_name}\nПорт: {port}\n", MessageChannels.SYSTEM, LogLevels.ERROR.value, (ParamItem("service_name", "Name of service"), ParamItem("service_description", "Description of service"), ParamItem("host_name", "Name of host"), ParamItem("port", "Port")))

    #
    POLIBASE_DB_BACKUP_START: MessageCommandDescription = MessageCommandDescription(
        "Start Polibase DataBase Dump backup {one}",  MessageChannels.BACKUP, LogLevels.NORMAL.value, (ParamItem("one", ""),))
    
    POLIBASE_DB_BACKUP_COMPLETE: MessageCommandDescription = MessageCommandDescription(
        "Complete Polibase DataBase Dump backup",  MessageChannels.BACKUP, LogLevels.NORMAL.value)
    #
    HR_NOTIFY_ABOUT_NEW_EMPLOYEE: MessageCommandDescription = MessageCommandDescription("День добрый, {hr_given_name}.\nДокументы для нового сотрудника: {employee_full_name} готовы!\nЕго корпоративная почта: {employee_email}.", MessageChannels.HR, LogLevels.NOTIFICATION.value, (ParamItem(
        "hr_given_name", "Имя руководителя отдела HR"), ParamItem("employee_full_name", "ФИО нового сотрудника"), ParamItem("employee_email", "Корпаротивная почта нового сотрудника")))
    #
    IT_NOTIFY_ABOUT_CREATE_USER: MessageCommandDescription = MessageCommandDescription("Добрый день, отдел Информационных технологий.\nДокументы для нового пользователя: {name} готовы!\nОписание: {description}\nЛогин: {login}\nПароль: {password}\nТелефон: {telephone_number}\nЭлектронная почта: {email}", MessageChannels.IT, LogLevels.NOTIFICATION.value, (ParamItem(
        "name", ""), ParamItem("description", ""), ParamItem("login", ""), ParamItem("password", ""), ParamItem("telephone_number", ""),  ParamItem("email", "")))

    IT_NOTIFY_ABOUT_CREATE_NEW_MARK: MessageCommandDescription = MessageCommandDescription("Добрый день, отдел Информационных технологий.\nКарта доступа для новой персоны: {name} готова!\nТелефон: {telephone_number}\nНомер карты доступа: {tab_number}\nГруппа доступа: {group_name}", MessageChannels.IT, LogLevels.NOTIFICATION.value, (ParamItem(
        "name", ""), ParamItem("telephone_number", ""), ParamItem("tab_number", ""), ParamItem("group_name", "")))

    IT_NOTIFY_ABOUT_CREATE_TEMPORARY_MARK: MessageCommandDescription = MessageCommandDescription("Добрый день, отдел Информационных технологий.\nВременная карта доступа для персоны: {name} готова!\nНомер карты: {tab_number}\nТелефон: {telephone_number}", MessageChannels.IT, LogLevels.NOTIFICATION.value, (ParamItem(
        "name", ""), ParamItem("tab_number", ""), ParamItem("telephone_number", "")))

    IT_NOTIFY_ABOUT_TEMPORARY_MARK_RETURN: MessageCommandDescription = MessageCommandDescription("Добрый день, отдел Информационных технологий.\nВременная карта доступа для персоны: {name} возвращена!\nНомер карты: {tab_number}", MessageChannels.IT, LogLevels.NOTIFICATION.value, (ParamItem(
        "name", ""), ParamItem("tab_number", "")))

    IT_NOTIFY_ABOUT_MARK_RETURN: MessageCommandDescription = MessageCommandDescription("Добрый день, отдел Информационных технологий.\nКарта доступа для персоны: {name} возвращена!\nНомер карты: {tab_number}", MessageChannels.IT, LogLevels.NOTIFICATION.value, (ParamItem(
        "name", ""), ParamItem("tab_number", "")))

    IT_TASK_AFTER_CREATE_NEW_USER: MessageCommandDescription = MessageCommandDescription("Добрый день, {it_user_name}.\nНеобходимо создать почту для пользователя: {name}\nАдресс электронной почты: {mail}\nПароль: {password}", MessageChannels.IT, LogLevels.TASK.value, (ParamItem(
        "it_user_name", ""), ParamItem("name", ""), ParamItem("mail", ""), ParamItem("password", "")))

    WORKSTATION_IS_NOT_ACCESSABLE: MessageCommandDescription = MessageCommandDescription(
        "Компьютер {workstation_name} вне сети", MessageChannels.IT, LogLevels.ERROR.value, [ParamItem("workstation_name", "")])

    #POLIBASE

    POLIBASE_PERSON_VISIT_WAS_REGISTERED: MessageCommandDescription = MessageCommandDescription("Зарегистрировано новое посещение: {name} ({type_string})", MessageChannels.NOTIFICATION, LogLevels.NOTIFICATION.value, (ParamItem(
        "name", ""), ParamItem("type_string", ""), ParamItem("visit", "")))

    POLIBASE_PERSON_VISIT_NOTIFICATION_WAS_REGISTERED: MessageCommandDescription = MessageCommandDescription("Зарегистрировано новое уведомление посещение: {name} ({type_string})", MessageChannels.NOTIFICATION, LogLevels.SILENCE.value, (ParamItem(
        "name", ""), ParamItem("type_string", ""), ParamItem("notification", "")))

    POLIBASE_PERSONS_WITH_OLD_FORMAT_BARCODE_WAS_DETECTED: MessageCommandDescription = MessageCommandDescription(
        "Полибейс: обнаружены пациенты со старым форматом или отсутствующим штрих-кодом в количестве {persons_pin_length}", MessageChannels.NOTIFICATION, LogLevels.SILENCE.value, (ParamItem("persons_pin_length", ""), ParamItem("persons_pin", "")))
    
    POLIBASE_ALL_PERSON_BARCODES_WITH_OLD_FORMAT_WAS_CREATED: MessageCommandDescription = MessageCommandDescription(
        "Полибейс: все новые штрих-коды созданы", MessageChannels.NOTIFICATION, LogLevels.SILENCE.value, [ParamItem("persons_pin", "")])

    POLIBASE_PERSON_WANTS_FEEDBACK_CALL_AFTER_REVIEW_QUEST_COMPLETE: MessageCommandDescription = MessageCommandDescription("Клиент {name} ({pin}) запросил обратный звонок.\nОценка: {grade}\nПричина: {message}\nТелефон: {telephone_number}",  MessageChannels.POLIBASE_PERSON_FEEDBACK_CALL, LogLevels.NOTIFICATION.value, (ParamItem(
        "name", ""), ParamItem("pin", ""), ParamItem("grade", ""), ParamItem("message", ""), ParamItem("telephone_number", "")))

    POLIBASE_PERSON_REVIEW_QUEST_RESULT_FOR_HIGH_GRADE: MessageCommandDescription = MessageCommandDescription("Клиент {name} ({pin}) завершил опрос.\nОценка: {grade}\nОткуда узнал о нас: {information_way}\nТелефон: {telephone_number}",  MessageChannels.POLIBASE_PERSON_REVIEW_QUEST_RESULT, LogLevels.NOTIFICATION.value, (ParamItem(
        "name", ""), ParamItem("pin", ""), ParamItem("grade", ""), ParamItem("information_way", ""), ParamItem("telephone_number", "")))

    POLIBASE_PERSON_REVIEW_QUEST_RESULT_FOR_LOW_GRADE: MessageCommandDescription = MessageCommandDescription("Клиент {name} ({pin}) завершил опрос.\nОценка: {grade}\nПричина: {message}\nОткуда узнал о нас: {information_way}\nЗапросил обратный звонок: {feedback_call}\nТелефон: {telephone_number}",  MessageChannels.POLIBASE_PERSON_REVIEW_QUEST_RESULT, LogLevels.NOTIFICATION.value, (ParamItem(
        "name", ""), ParamItem("pin", ""), ParamItem("grade", ""), ParamItem("message", ""), ParamItem("information_way", ""), ParamItem("feedback_call", ""), ParamItem("telephone_number", "")))



