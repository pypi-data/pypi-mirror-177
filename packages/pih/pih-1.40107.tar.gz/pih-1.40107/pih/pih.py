import calendar
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from getpass import getpass
from threading import Thread
from time import sleep
from grpc import StatusCode
import importlib.util
import locale
import os
import platform
import json
import pkg_resources
import requests
import re
import subprocess
from subprocess import DEVNULL, STDOUT, CompletedProcess
import sys
from typing import Any, Callable, List, Tuple
import colorama
from colorama import Back, Style, Fore
from prettytable import PrettyTable
import requests
from requests import ConnectTimeout, Response

try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih.tools import DataTool, EnumTool, PathTool, ResultTool, FullNameTool, PasswordTools, ResultUnpack, DateTimeTool
from pih.rpc import RPC, Error, SubscribtionType
from pih.const import CONST, FIELD_NAME_COLLECTION, FIELD_COLLECTION, FILE, PASSWORD, PATHS, USER_PROPERTY, InternalMessageMethodTypes, MessageChannels, MessageCommands, LogLevels, MarkType, PolibasePersonReviewQuestStep, PolibasePersonNotifierStatus, ServiceCommands, ServiceRoles, Settings, MessageTypes, MessageStatus
from pih.collection import ActionValue, FieldItem, FieldItemList, FullName, InventoryReportItem, MessageCommandDescription, LoginPasswordPair, Mark, MarkDivision, MarkGroup, MarkGroupStatistics, PolibasePersonNotifierItem, ParamItem, PasswordSettings, PolibasePerson, PrinterADInformation, PrinterReport, PrinterStatus, Result, ServiceRoleInformation, ServiceRoleDescription, Subscriber, TemporaryMark, TimeTrackingEntity, TimeTrackingResultByDate, TimeTrackingResultByDivision, TimeTrackingResultByPerson, User, UserContainer, UserWorkstation, WhatsAppMessage, WhatsAppMessageListPayload, WhatsAppMessageButtonsPayload, Workstation, PolibaseReviewQuestItem, SettingsValue, PolibasePersonVisit, PolibasePersonVisitNotification, PolibasePersonVisitNotificationVO, DelayedMessage, BufferedMessageSearchCritery, DelayedMessageVO


def while_not_do(action: Callable[[None], bool], attemp_count: int = None, success_handler: Callable = None) -> None:
    
    while not action():
        if attemp_count is not None:
            if attemp_count == 0:
                break
            attemp_count -= 1
    if success_handler is not None:
        success_handler()

class NotImplemented(BaseException):
    pass


class ZeroReached(BaseException):
    pass


class NotFound(BaseException):
    pass


class IncorrectInputFile(BaseException):
    pass


class NotAccesable(BaseException):
    pass


class NamePolicy:

    @staticmethod
    def get_first_letter(name: str) -> str:
        from transliterate import translit
        letter = name[0]
        if letter.lower() == "ю":
            return "yu"
        return translit(letter, "ru", reversed=True).lower()

    @staticmethod
    def convert_to_login(full_name: FullName) -> FullName:
        return FullName(
            NamePolicy.get_first_letter(
                full_name.last_name),
            NamePolicy.get_first_letter(
                full_name.first_name),
            NamePolicy.get_first_letter(full_name.middle_name))

    @staticmethod
    def convert_to_alternative_login(login_list: FullName) -> FullName:
        return FullName(login_list.first_name, login_list.middle_name, login_list.last_name)

    @staticmethod
    def convert_to_reverse_login(login_list: FullName) -> FullName:
        return FullName(login_list.middle_name, login_list.first_name, login_list.last_name)


class PIH:

    NAME: str = "pih"

    class VERSION:

        @staticmethod
        def local() -> str:
            return "1.40107"

        def need_update() -> bool:
            return importlib.util.find_spec(PIH.NAME) is not None and PIH.VERSION.local() < PIH.VERSION.remote()

        @staticmethod
        def remote() -> str:
            req = requests.get(CONST.PYPI_URL)
            version = parse("0")
            if req.status_code == requests.codes.ok:
                data = json.loads(req.text.encode(req.encoding))
                releases = data.get("releases", [])
                for release in releases:
                    ver = parse(release)
                    if not ver.is_prerelease:
                        version = max(version, ver)
            return str(version)

    class ERROR:

        def create_error_header(details: str) -> str:
            return f"\nВерсия: {PIH.VERSION.local()}/{PIH.VERSION.remote()}\nПользователь: {PIH.OS.get_login()}\nКомпьютер: {PIH.OS.get_host()}\n{details}"

        def rpc_error_handler(details: str, code: Tuple, role: ServiceRoles, command: ServiceCommands) -> None:
            if isinstance(command, ServiceCommands) and (role != ServiceRoles.MESSAGE or code != StatusCode.UNAVAILABLE):
                PIH.MESSAGE.from_debug_bot(
                    PIH.ERROR.create_error_header(details), LogLevels.ERROR)
            raise Error(details, code) from None

        def global_except_hook(exctype, value, traceback):
            details_list: List[str] = []
            for item in value.args:
                if isinstance(item, str):
                    details_list.append(item)
            details = "\n".join(details_list)
            PIH.MESSAGE.from_debug_bot(
                PIH.ERROR.create_error_header(details), LogLevels.ERROR)
            sys.__excepthook__(exctype, value, traceback)

        sys.excepthook = global_except_hook

    class UPDATER:

        @staticmethod
        def update_for_service(service_role: ServiceRoles, pih_update: bool = True, modules_update: bool = True, show_output: bool = False) -> bool:
            service_role_value: ServiceRoleDescription = service_role.value
            returncode: int = 0
            if pih_update:
                remote_executor_command_list: List[str] = PIH.PSTOOLS.create_remote_process_executor_for_service_role(
                    service_role, True)
                command_list: List[str] = remote_executor_command_list + \
                    PIH.UPDATER.get_module_updater_command_list(PIH.NAME, None)
                process_result: CompletedProcess = PIH.PSTOOLS.run_command(
                    command_list, show_output)
                returncode = process_result.returncode
            result: bool = returncode == 0
            if modules_update and result:
                installed_module_list: List[str] = {
                    pkg.key.lower() for pkg in pkg_resources.working_set}
                for module_name in [item.lower() for item in service_role_value.modules]:
                    if module_name not in installed_module_list:
                        result = result and PIH.UPDATER.install_module(
                            module_name, show_output=show_output)
                        if result:
                            pkg_resources.working_set.add_entry(module_name)
                        else:
                            break
            return result

        @staticmethod
        def get_module_updater_command_list(module_name: str, version: str = None) -> List[str]:
            return ["-m", CONST.PYTHON.PYPI, "install"] + ([f"{module_name}=={version}"] if version is not None else [module_name, "-U"])

        @staticmethod
        def update_localy(version: str = None, show_output: bool = False) -> bool:
            return PIH.UPDATER.install_module(PIH.NAME, version, show_output)

        @staticmethod
        def install_module(module_name: str, version: str = None, show_output: bool = False) -> bool:
            command_list = PIH.UPDATER.get_module_updater_command_list(
                module_name, version)
            command_list.pop(0)
            process_result: CompletedProcess = PIH.PSTOOLS.run_command(
                command_list, show_output)
            returncode = process_result.returncode
            return returncode == 0

        @staticmethod
        def update_remote(host: str, show_output: bool = False) -> bool:
            remote_executor_command_list: List[str] = PIH.PSTOOLS.create_remote_process_executor(
                host, True)
            command_list: List[str] = remote_executor_command_list + \
                PIH.UPDATER.get_module_updater_command_list()
            process_result: CompletedProcess = PIH.PSTOOLS.run_command(
                command_list, show_output)
            returncode = process_result.returncode
            return returncode == 0

        @staticmethod
        def update_action(start_handler: Callable, update_start_handler: Callable, update_complete_handler: Callable) -> None:
            need_update: bool = PIH.VERSION.need_update()

            def internal_update_action(need_update: bool, start_handler: Callable, update_start_handler: Callable, update_complete_handler: Callable):
                if need_update:
                    update_start_handler()
                    if PIH.UPDATER.update_localy():
                        import importlib
                        importlib.reload(sys.modules[PIH.NAME])
                        importlib.reload(sys.modules[f"{PIH.NAME}.{PIH.NAME}"])
                        update_complete_handler()
                        start_handler()
                else:
                    start_handler()
            Thread(target=internal_update_action, args=(
                need_update, start_handler, update_start_handler, update_complete_handler,)).start()

    class SETTINGS:

        @staticmethod
        def set(settings_item: Settings, value: Any) -> bool:
            return PIH.ACTION.SETTINGS.set(settings_item, value)

        @staticmethod
        def set_default(settings_item: Settings) -> bool:
            return PIH.ACTION.SETTINGS.set_default(settings_item)

        @staticmethod
        def get(settings_item: Settings) -> Any:
            return PIH.RESULT.SETTINGS.get(settings_item).data

        class POLIBASE:

            class REVIEW_QUEST:

                @staticmethod
                def start_time() -> datetime:
                    return DateTimeTool.from_string(PIH.SETTINGS.get(Settings.POLIBASE_PERSON_REVIEW_QUEST_START_TIME), CONST.TIME_FORMAT)

                @staticmethod
                def test() -> bool:
                    return PIH.SETTINGS.get(Settings.POLIBASE_PERSON_REVIEW_QUEST_TEST)

    class PSTOOLS:

        @staticmethod
        def create_remote_process_executor(command_list: List, host: str, login: str = None, password: str = None, interactive: bool = False) -> List[str]:
            host = "\\\\" + host
            user: str = login or (CONST.AD.DOMAIN_NAME +
                                  "\\" + CONST.AD.ADMINISTRATOR)
            password = password or CONST.AD.ADMINISTRATOR_PASSOWORD
            ps_executor_path: str = os.path.join(
                PATHS.WS.PATH, CONST.PSTOOLS.NAME, CONST.PSTOOLS.EXECUTOR)
            return [ps_executor_path, "/accepteula", host, "-i" if interactive else "-d", "-u", user, "-p", password] + command_list

        @staticmethod
        def create_remote_process_executor_for_service_role(value: ServiceRoles, interactive: bool = False) -> List[str]:
            service_role_value: ServiceRoleDescription = value.value
            return PIH.PSTOOLS.create_remote_process_executor([CONST.PYTHON.EXECUTOR], PIH.SERVICE.get_host(value), service_role_value.login, service_role_value.password, interactive)

        @staticmethod
        def run_command(command_list: List[str], show_output: bool) -> CompletedProcess:
            print(" ".join(command_list))
            if show_output:
                process_result = subprocess.run(
                    command_list, text=True)
            else:
                process_result = subprocess.run(
                    command_list, stdout=DEVNULL, stderr=STDOUT, text=True)
            return process_result

    class SERVICE:

        command_map: dict = None

        class ADMIN:

            @staticmethod
            def develope(service_role: ServiceRoles) -> None:
                developer_role_value: ServiceRoleDescription = ServiceRoles.DEVELOPER.value
                service_role_value: ServiceRoleDescription = service_role.value
                service_role_value.host = developer_role_value.host
                service_role_value.port = developer_role_value.port

            @staticmethod
            def isolate(service_role: ServiceRoles) -> None:
                service_role_value: ServiceRoleDescription = service_role.value
                service_role_value.debug = True

            @staticmethod
            def start(service_role: ServiceRoles, check_if_started: bool = True, show_output: bool = False) -> bool:
                if check_if_started:
                    if PIH.SERVICE.check_accessibility(service_role):
                        return None
                service_role_value: ServiceRoleDescription = service_role.value
                remote_executor_command_list: List[str] = PIH.PSTOOLS.create_remote_process_executor_for_service_role(
                    service_role)
                service_file_path: str = None
                if service_role_value.service_path is None:
                    service_file_path = os.path.join(
                        CONST.FACADE.PATH, f"{service_role_value.name}{CONST.FACADE.COMMAND_SUFFIX}", f"{CONST.SERVICE.NAME}.{FILE.EXTENSION.PYTHON}")
                else:
                    service_file_path = os.path.join(
                        service_role_value.service_path, f"{CONST.SERVICE.NAME}.{FILE.EXTENSION.PYTHON}")
                remote_executor_command_list.append(service_file_path)
                #debug = False
                remote_executor_command_list.append("False")
                process_result = PIH.PSTOOLS.run_command(
                    remote_executor_command_list, show_output)
                returncode = process_result.returncode
                if returncode == 2:
                    return False
                service_role_value.pid = returncode
                return True

            @staticmethod
            def stop(role: ServiceRoles, check_if_started: bool = True, show_output: bool = False) -> bool:
                if check_if_started:
                    if not PIH.SERVICE.check_accessibility(role):
                        return None
                service_role_value: ServiceRoleDescription = role.value
                host: str = "\\\\" + PIH.SERVICE.get_host(role)
                ps_kill_executor_path: str = os.path.join(
                    PATHS.WS.PATH, CONST.PSTOOLS.NAME, CONST.PSTOOLS.PSKILL)
                process_result: CompletedProcess = PIH.PSTOOLS.run_command(
                    [ps_kill_executor_path, host, str(service_role_value.pid)], show_output)
                returncode = process_result.returncode
                result: bool = returncode == 0
                if result:
                    service_role_value.pid = -1
                return result

        @staticmethod
        def check_accessibility(role: ServiceRoles) -> bool:
            return PIH.SERVICE.ping(role) is not None

        @staticmethod
        def ping(role: ServiceRoles) -> ServiceRoleInformation:
            service_role_informaion: ServiceRoleInformation = RPC.ping(role)
            if service_role_informaion is not None:
                DataTool.fill_data_from_source(
                    role.value, DataTool.to_data(service_role_informaion))
                service_role_informaion.subscribers = list(map(lambda item: DataTool.fill_data_from_source(
                    Subscriber(), item), service_role_informaion.subscribers))
            return service_role_informaion

        @staticmethod
        def init() -> None:
            if PIH.SERVICE.command_map is None:
                PIH.SERVICE.command_map = {}
                for role in ServiceRoles:
                    for role_command in role.value.commands:
                        PIH.SERVICE.command_map[role_command.name] = role

        @staticmethod
        def get_role_by_command(value: ServiceCommands) -> ServiceRoles:
            return PIH.SERVICE.command_map[value.name] if value.name in PIH.SERVICE.command_map else None

        @staticmethod
        def get_host(service_role: ServiceRoles) -> str:
            role_value: ServiceRoleDescription = service_role.value
            if role_value.debug:
                host = PIH.OS.get_host()
                role_value.host = host
            return role_value.host

        @staticmethod
        def get_port(service_role: ServiceRoles) -> str:
            role_value: ServiceRoleDescription = service_role.value
            return role_value.port

        @staticmethod
        def subscribe_on(service_command: ServiceCommands, type: int = SubscribtionType.AFTER, name: str = None) -> bool:
            return RPC.Service.subscribe_on(service_command, type, name)

        @staticmethod
        def unsubscribe(service_command: ServiceCommands, type: int) -> bool:
            return RPC.Service.unsubscribe(service_command, type,)

    class PATH(PATHS):

        @staticmethod
        def resolve(value: str) -> str:
            if value[0] == "{" and value[-1] == "}":
                value = value[1: -1]
            return PathTool.resolve(value, PIH.OS.get_host())

    class DATA:

        class USER:

            def by_login(value: str) -> User:
                return PIH.RESULT.USER.by_login(value).data

            def by_name(value: str) -> User:
                return PIH.RESULT.USER.by_name(value).data

        class MARK:

            def by_tab_number(value: str) -> User:
                return PIH.RESULT.MARK.by_tab_number(value).data

        class SETTINGS:

            def get(value: Settings) -> Any:
                return PIH.RESULT.SETTINGS.get(value).data

        class FILTER:

            @staticmethod
            def users_by_dn(data: List[User], dn: str) -> List:
                return list(filter(lambda x: x.distinguishedName.find(dn) != -1, data))

        class EXTRACT:

            @staticmethod
            def email(value: str) -> str:
                emails: List[str] = re.findall(
                    r"[A-Za-z0-9_%+-.]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,5}", value)
                if len(emails) > 0:
                    return emails[0]
                return None

            @staticmethod
            def number(value: str, min: int = None, max: int = None) -> int:
                value = value.strip()
                result: int = None
                numbers: List[str] = re.findall(r"\d", value)
                if len(numbers) > 0:
                    result = int(numbers[0])
                    if result < min or result > max:
                        result = None
                return result

            @staticmethod
            def parameter(object: dict, name: str) -> str:
                return object[name] if name in object else ""

            @staticmethod
            def tab_number(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.TAB_NUMBER)

            @staticmethod
            def telephone(user_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.TELEPHONE_NUMBER)

            @staticmethod
            def login(user_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.LOGIN)

            @staticmethod
            def name(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.NAME)

            @staticmethod
            def dn(user_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.DN)

            @staticmethod
            def group_name(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.GROUP_NAME)

            @staticmethod
            def group_id(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.GROUP_ID)

            @staticmethod
            def as_full_name(mark_object: dict) -> FullName:
                return FullNameTool.from_string(PIH.DATA.EXTRACT.full_name(mark_object))

            @staticmethod
            def full_name(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.FULL_NAME)

            @staticmethod
            def person_id(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.PERSON_ID)

            @staticmethod
            def mark_id(mark_object: dict) -> str:
                return PIH.DATA.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.MARK_ID)

            @staticmethod
            def description(object: dict) -> str:
                result = PIH.DATA.EXTRACT.parameter(
                    object, FIELD_NAME_COLLECTION.DESCRIPTION)
                if isinstance(result, Tuple) or isinstance(result, List):
                    return result[0]

            @staticmethod
            def container_dn(user_object: dict) -> str:
                return PIH.DATA.EXTRACT.container_dn_from_dn(PIH.DATA.EXTRACT.dn(user_object))

            @staticmethod
            def container_dn_from_dn(dn: str) -> str:
                return ",".join(dn.split(",")[1:])

        class FORMAT:

            @staticmethod
            def telephone_number(value: str, prefix: str = CONST.TELEPHONE_NUMBER_PREFIX) -> str:
                src_value: str = value
                if value is not None and len(value) > 0:
                    value = re.sub("[\-\(\) ]", "", value)
                    if value.startswith(prefix):
                        value = value[len(prefix):]
                    value = prefix + (value[1:] if (value[0] == "8" or value[0] == "7") else value)
                    pattern: str = "^\\" + prefix + "[0-9]{10}"
                    matcher: re.Match = re.match(pattern, value)
                    if matcher is not None:
                        return matcher.group(0)
                    else:
                        return src_value
                else:
                    return src_value

            @staticmethod
            def name(value: str, remove_non_alpha: bool = False) -> str:
                value_list: List[str] = value.split(" ")
                if len(value_list) == 1:
                    if len(value) > 2:
                        value = value[0].upper() + value[1:].lower()
                    value = re.sub("[^а-яА-Яa-zA-Z]+", "", value) if remove_non_alpha else value
                    return value.strip(" ")
                return " ".join(list(map(lambda item: PIH.DATA.FORMAT.name(item, remove_non_alpha), value_list)))

            @staticmethod
            def location_list(value: str, remove_first: bool = True, reversed: bool = True) -> List[str]:
                location_list: list[str] = value.split(
                    ",")[1 if remove_first else 0:]
                if reversed:
                    location_list.reverse()
                return list(map(
                    lambda item: item.split("=")[-1], location_list))

            @staticmethod
            def get_user_account_control_values(uac: int) -> List[str]:
                result: list[str] = []
                for count, item in enumerate(CONST.AD.USER_ACCOUNT_CONTROL):
                    if (pow(2, count) & uac) != 0:
                        result.append(item)
                return result

        class TELEPHONE_NUMBER:

            @staticmethod
            def by_login(value: str, format: bool = True) -> str:
                result: str = PIH.DATA.USER.by_login(value).telephoneNumber
                return PIH.DATA.FORMAT.telephone_number(result) if format else result

            @staticmethod
            def by_mark_tab_number(value: str, format: bool = True) -> str:
                result: str = PIH.DATA.MARK.by_tab_number(
                    value).telephoneNumber
                return PIH.DATA.FORMAT.telephone_number(result) if format else result

            def by_polibase_person_pin(value: int, format: bool = True) -> bool:
                result: str = PIH.DATA.POLIBASE.person_by_pin(
                    value).telephoneNumber
                return PIH.DATA.FORMAT.telephone_number(result) if format else result

            @staticmethod
            def by_full_name(value: Any, format: bool = True) -> str:
                value_string: str = None
                if isinstance(value, str):
                    value_string = value
                    value = FullNameTool.from_string(value)
                else:
                    value_string = FullNameTool.to_string(value)
                telephone_number: str = PIH.RESULT.MARK.by_full_name(
                    value_string, True).data.telephoneNumber
                if PIH.CHECK.telephone_number(telephone_number):
                    return PIH.DATA.FORMAT.telephone_number(telephone_number) if format else telephone_number
                telephone_number = PIH.RESULT.USER.by_full_name(
                    value_string, True).data.telephoneNumber
                if PIH.CHECK.telephone_number(telephone_number):
                    return PIH.DATA.FORMAT.telephone_number(telephone_number) if format else telephone_number
                details: str = f"Телефон для {value_string} не найден"
                raise NotFound(details)

        class POLIBASE:

            @staticmethod
            def person_by_pin(value: int, test: bool = None) -> PolibasePerson:
                return PIH.RESULT.POLIBASE.person_by_pin(value, test).data

            @staticmethod
            def duplicate_person_for(person: PolibasePerson, check_birth: bool = True) -> PolibasePerson:
                def check_function(check_person: PolibasePerson) -> bool:
                    return check_person.pin != person.pin and (not check_birth or check_person.Birth != person.Birth)
                return ResultTool.get_first_data_element(ResultTool.data_filter(PIH.RESULT.POLIBASE.persons_by_full_name(person.FullName), lambda item: check_function(item)))

    class SESSION:

        login: str = None
        user: User = None
        allowable_groups: List[CONST.AD.Groups] = []

        @staticmethod
        def run_forever() -> None:
            try:
                PR.green("Нажмите Ввод для выхода...")
                input()
            except KeyboardInterrupt:
                pass

        @staticmethod
        def exit(timeout: int = None, message: str = None) -> None:
            if message is not None:
                PR.bad(message)
            timeout = timeout or 5
            sleep(timeout)
            exit()

        @staticmethod
        def get_login() -> str:
            if PIH.SESSION.login is None:
                PIH.SESSION.start(PIH.OS.get_login())
            return PIH.SESSION.login

        @staticmethod
        def get_argv(position: int, default: str = "") -> str:
            argv: List[str] = sys.argv
            argv_len: int = len(argv)
            return argv[position] if argv_len >= position + 1 else default

        @staticmethod
        def get_user() -> User:
            if PIH.SESSION.user is None:
                PIH.SESSION.user = PIH.RESULT.USER.by_login(
                    PIH.SESSION.get_login()).data
            return PIH.SESSION.user

        @staticmethod
        def get_user_given_name() -> str:
            return FullNameTool.to_given_name(PIH.SESSION.get_user().name)

        @staticmethod
        def start(login: str, notify: bool = True) -> None:
            if PIH.SESSION.login is None:
                PIH.SESSION.login = login
                if notify:
                    PIH.MESSAGE.COMMAND.start_session()

        @staticmethod
        def say_hello() -> None:
            PR.init()
            user: User = PIH.SESSION.get_user()
            if user is not None:
                PR.good(f"Добро пожаловать, {user.name}")
                PR.new_line()
                return
            PR.bad(f"Ты кто такой? Давай, до свидания...")
            PIH.SESSION.exit()

        @staticmethod
        def argv(index: int = None) -> List[str]:
            if index is None:
                return sys.argv[1:] if len(sys.argv) > 1 else None
            return sys.argv[index] if len(sys.argv) > index else None

        @staticmethod
        def get_file_path() -> str:
            return PIH.SESSION.argv(0)

        @staticmethod
        def get_file_name() -> str:
            return PathTool.get_file_name(PIH.SESSION.get_file_path())

        @staticmethod
        def add_allowable_group(value: CONST.AD.Groups) -> None:
            PIH.SESSION.allowable_groups.append(value)

        @staticmethod
        def authenticate(exit_on_fail: bool = True) -> bool:
            try:
                PR.green("Инициализация...")
                if PIH.SERVICE.check_accessibility(ServiceRoles.AD):
                    PIH.VISUAL.clear_screen()
                    PR.head1("Пройдите, аутентификацию, пожалуйста.")
                    login: str = PIH.OS.get_login()
                    if not PIH.INPUT.yes_no(f"Использовать логин '{login}'?", True):
                        login = PIH.INPUT.login()
                    password: str = PIH.INPUT.password(is_new=False)
                    if DataTool.rpc_unrepresent(RPC.call(ServiceCommands.authenticate, (login, password))):
                        PIH.SESSION.start(login, False)
                        PIH.MESSAGE.COMMAND.login()
                        PR.good(PR.text_black(
                            f"Добро пожаловать, {PIH.SESSION.get_user().name}..."))
                        return True
                    else:
                        if exit_on_fail:
                            PIH.SESSION.exit(
                                5, "Неверный пароль или логин. До свидания...")
                        else:
                            return False
                else:
                    PR.bad("Сервис аутентификации недоступен. До свидания...")
            except KeyboardInterrupt:
                PIH.SESSION.exit()

    class OS:

        @staticmethod
        def get_login() -> str:
            return os.getlogin()

        @staticmethod
        def get_host() -> str:
            return platform.node()

        @staticmethod
        def get_pid() -> int:
            return os.getppid()

    class RESULT:

        class MESSAGE:

            class DELAYED:

                @staticmethod
                def get(search_condition: BufferedMessageSearchCritery = None, take_to_work: bool = False) -> Result[List[DelayedMessageVO]]:
                    return DataTool.to_result(
                        RPC.call(ServiceCommands.search_buffered_messages, (search_condition, take_to_work)), DelayedMessageVO)

        class SETTINGS:

            @staticmethod
            def key(key: str, default_value: Any = None) -> Result[Any]:
                return DataTool.to_result(
                    RPC.call(ServiceCommands.get_settings_value, (key, default_value)))

            @staticmethod
            def get(settings_item: Settings) -> Result[Any]:
                settings_value: SettingsValue = settings_item.value
                return PIH.RESULT.SETTINGS.key(settings_value.key_name or settings_item.name, settings_value.default_value)

        class WORKSTATION:

            @staticmethod
            def all() -> Result[List[Workstation]]:
                return DataTool.to_result(
                    RPC.call(ServiceCommands.get_all_workstations), Workstation)

            @staticmethod
            def by_login(login: str) -> Result[List[UserWorkstation]]:
                return DataTool.to_result(
                    RPC.call(ServiceCommands.get_workstation_by_user, login), UserWorkstation)

            @staticmethod
            def all_with_user() -> Result[List[UserWorkstation]]:
                return DataTool.to_result(
                    RPC.call(ServiceCommands.get_all_workstations_with_user), UserWorkstation)

        class INVENTORY:

            @staticmethod
            def report(report_file_path: str, open_for_edit: bool = False) -> Result[List[InventoryReportItem]]:
                return DataTool.to_result(
                    RPC.call(ServiceCommands.get_inventory_report, (report_file_path, open_for_edit)), InventoryReportItem)

        class TIME_TRACKING:

            @staticmethod
            def today(tab_number: str = None) -> Result[List[TimeTrackingResultByPerson]]:
                return PIH.RESULT.TIME_TRACKING.create(tab_number=tab_number)

            @staticmethod
            def in_period(day_start: int = 1, day_end: int = None, month: int = None, tab_number: str = None) -> Result[List[TimeTrackingResultByPerson]]:
                now: datetime = datetime.now()
                if month is not None:
                    now = now.replace(month=month)
                start_date: datetime = now.replace(hour=0, minute=0, second=0)
                end_date: datetime = now.replace(hour=23, minute=59, second=59)
                if day_start < 0:
                    start_date -= timedelta(days=abs(day_start))
                else:
                    start_date = start_date.replace(day=day_start)
                if day_end is not None:
                    if day_end < 0:
                        day_end -= timedelta(days=abs(day_start))
                    else:
                        day_end = start_date.replace(day=day_start)
                return PIH.RESULT.TIME_TRACKING.create(start_date, end_date, tab_number)

            @staticmethod
            def create(start_date: datetime = None, end_date: datetime = None, tab_number: str = None) -> Result[List[TimeTrackingResultByPerson]]:
                now: datetime = datetime.now() if start_date is None or end_date is None else None
                start_date = start_date or now.replace(
                    hour=0, minute=0, second=0)
                end_date = end_date or now.replace(
                    hour=23, minute=59, second=59)

                def get_date_or_time(entity: TimeTrackingEntity, date: bool) -> str:
                    return DataTool.not_none_check(entity, lambda: entity.TimeVal.split("T")[not date])
                result_data: dict = {}
                full_name_by_tab_number_map: dict = {}
                result_data = defaultdict(
                    lambda: defaultdict(lambda: defaultdict(list)))
                data: list = DataTool.to_result(RPC.call(
                    ServiceCommands.get_time_tracking, (start_date, end_date, tab_number)), TimeTrackingEntity).data
                for time_tracking_entity in data:
                    tab_number: str = time_tracking_entity.TabNumber
                    full_name_by_tab_number_map[tab_number] = time_tracking_entity.FullName
                    result_data[time_tracking_entity.DivisionName][tab_number][get_date_or_time(time_tracking_entity, True)].append(
                        time_tracking_entity)
                result: List[TimeTrackingResultByDivision] = []
                for division_name in result_data:
                    if division_name is None:
                        continue
                    result_division_item: TimeTrackingResultByDivision = TimeTrackingResultByDivision(
                        division_name)
                    result.append(result_division_item)
                    for tab_number in result_data[division_name]:
                        result_person_item: TimeTrackingResultByPerson = TimeTrackingResultByPerson(
                            tab_number, full_name_by_tab_number_map[tab_number])
                        result_division_item.list.append(result_person_item)
                        for date in result_data[division_name][tab_number]:
                            time_tracking_entity_list: List[TimeTrackingEntity] = result_data[division_name][tab_number][date]
                            time_tracking_enter_entity: TimeTrackingEntity = None
                            time_tracking_exit_entity: TimeTrackingEntity = None
                            for time_tracking_entity_list_item in time_tracking_entity_list:
                                if time_tracking_entity_list_item.Mode == 1:
                                    time_tracking_enter_entity = time_tracking_entity_list_item
                                if time_tracking_entity_list_item.Mode == 2:
                                    time_tracking_exit_entity = time_tracking_entity_list_item
                            duration: int = 0
                            if time_tracking_enter_entity is not None:
                                if time_tracking_exit_entity is not None:
                                    enter_time: datetime = datetime.fromisoformat(
                                        time_tracking_enter_entity.TimeVal).timestamp()
                                    exit_time: datetime = datetime.fromisoformat(
                                        time_tracking_exit_entity.TimeVal).timestamp()
                                    if enter_time < exit_time:
                                        #    enter_time, exit_time = exit_time, enter_time
                                        #    time_tracking_enter_entity, time_tracking_exit_entity = time_tracking_exit_entity, time_tracking_enter_entity
                                        duration = int(exit_time - enter_time)
                                    result_person_item.duration += duration
                            result_person_item.list.append(
                                TimeTrackingResultByDate(date, get_date_or_time(time_tracking_enter_entity, False),
                                                         get_date_or_time(time_tracking_exit_entity, False), duration))
                for division in result:
                    for person in division.list:
                        index: int = 0
                        length = len(person.list)
                        for _ in range(length):
                            item: TimeTrackingResultByDate = person.list[index]
                            if item.duration == 0:
                                # if item.enter_time is None and item.exit_time is not None:
                                if index < length - 1:
                                    item_next: TimeTrackingResultByDate = person.list[index + 1]
                                    if item.exit_time is not None:
                                        if item_next.enter_time is not None:
                                            duration = int(datetime.fromisoformat(item.date + "T" + item.exit_time).timestamp() - datetime.fromisoformat(item_next.date + "T" + item_next.enter_time).timestamp())
                                            item.duration = duration
                                            person.duration += duration
                                            if item_next.exit_time is None:
                                                index += 1
                            index += 1
                            if index >= length - 1:
                                break

                return Result(FIELD_COLLECTION.ORION.TIME_TRACKING_RESULT, result)

        class PRINTER:

            @staticmethod
            def all() -> Result[List[PrinterADInformation]]:
                def filter_by_server_name(printer_list: List[PrinterADInformation]) -> List[PrinterADInformation]:
                    return list(filter(lambda item: item.serverName == CONST.HOST.PRINTER_SERVER.NAME, printer_list))
                result: Result[List[PrinterADInformation]] = DataTool.to_result(
                    RPC.call(ServiceCommands.get_printers), PrinterADInformation)
                return Result(result.fields, filter_by_server_name(result.data))

            @staticmethod
            def report(redirect_to_log: bool = True) -> Result[List[PrinterReport]]:
                return DataTool.to_result(
                    RPC.call(ServiceCommands.printers_report, redirect_to_log), PrinterReport)

            @staticmethod
            def status(redirect_to_log: bool = True) -> Result[List[PrinterStatus]]:
                return DataTool.to_result(
                    RPC.call(ServiceCommands.printers_status, redirect_to_log), PrinterStatus)

        class MARK:

            @staticmethod
            def by_tab_number(value: str) -> Result[Mark]:
                result: Result[Mark] = DataTool.to_result(
                    RPC.call(ServiceCommands.get_mark_by_tab_number, value), Mark)
                if ResultTool.data_is_empty(result):
                    details: str = f"Персона с номером {value} не существует"
                    raise NotFound(details)
                return result

            @staticmethod
            def person_divisions() -> Result[List[Mark]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_person_divisions), MarkDivision)

            @staticmethod
            def by_name(value: str, first_item: bool = False) -> Result[List[Mark]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_mark_by_person_name, value), Mark, first_item)

            @staticmethod
            def by_full_name(value: FullName, first_item: bool = False) -> Result[List[Mark]]:
                return PIH.RESULT.MARK.by_name(FullNameTool.from_string(value), first_item)

            @staticmethod
            def temporary_list() -> Result[List[TemporaryMark]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_temporary_marks), TemporaryMark)

            @staticmethod
            def by_any(value: str) -> Result[List[Mark]]:
                if PIH.CHECK.MARK.tab_number(value):
                    return ResultTool.as_list(PIH.RESULT.MARK.by_tab_number(value))
                elif PIH.CHECK.name(value, True):
                    return PIH.RESULT.MARK.by_name(value)
                return Result(None, None)

            @staticmethod
            def free_list() -> Result[List[Mark]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_free_marks), Mark)

            @staticmethod
            def free_marks_by_group_id(value: int) -> Result[List[Mark]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_free_marks_by_group_id, value), Mark)

            @staticmethod
            def free_marks_group_statistics(show_guest_marks: bool = None) -> Result[List[MarkGroupStatistics]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_free_marks_group_statistics, show_guest_marks), MarkGroupStatistics)

            @staticmethod
            def all() -> Result[List[Mark]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_all_persons), Mark)

            @staticmethod
            def temporary_mark_owner(mark: Mark) -> Result[Mark]:
                return DataTool.check(mark is not None and EnumTool.get(MarkType, mark.type) == MarkType.TEMPORARY, lambda: DataTool.to_result(RPC.call(ServiceCommands.get_owner_mark_for_temporary_mark, mark.TabNumber), Mark), None)

            @staticmethod
            def temporary_mark_owner_by_tab_number(value: str) -> Result[Mark]:
                return PIH.RESULT.MARK.temporary_mark_owner(PIH.RESULT.MARK.by_tab_number(value).data)

        class POLIBASE:

            class NOTIFICATION:

                @staticmethod
                def by(value: PolibasePersonVisitNotification) -> Result[List[PolibasePersonVisitNotification]]:
                    return DataTool.to_result(
                        RPC.call(ServiceCommands.search_polibase_person_visit_notifications, value), PolibasePersonVisitNotification)

                @staticmethod
                def by_message_id(value: int) -> Result[PolibasePersonVisitNotification]:
                    return ResultTool.with_first_data_element(PIH.RESULT.POLIBASE.NOTIFICATION.by(PolibasePersonVisitNotification(messageID=value)))

                @staticmethod
                def by_status(status: PolibasePersonNotifierStatus) -> Result[List[PolibasePersonNotifierItem]]:
                    return DataTool.to_result(
                        RPC.call(ServiceCommands.get_notifier_polibase_persons_by_status, status.value), PolibasePersonNotifierItem)

                @staticmethod
                def by_statuses(status_list: List[PolibasePersonNotifierStatus]) -> Result[List[PolibasePersonNotifierItem]]:
                    return DataTool.to_result(
                        RPC.call(ServiceCommands.get_notifier_polibase_persons_by_status, [list(map(lambda item: item.value, status_list))]), PolibasePersonNotifierItem)

            class VISIT:

                @staticmethod
                def today(test: bool = None) -> Result[List[PolibasePersonVisit]]:
                    return PIH.RESULT.POLIBASE.VISIT.by_registration_date(DateTimeTool.today(), test)

                @staticmethod
                def after_id(value: int, test: bool = None) -> Result[List[PolibasePersonVisit]]:
                    return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_person_visits_after_id, (value, test)), PolibasePersonVisit)

                @staticmethod
                def last_id(test: bool = None) -> Result[int]:
                    return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_person_visits_last_id, test))

                @staticmethod
                def prerecording_today(test: bool = None) -> Result[List[PolibasePersonVisit]]:
                    return PIH.RESULT.POLIBASE.VISIT.prerecording_by_registration_date(DateTimeTool.today(), test)

                @staticmethod
                def by_registration_date(value: datetime, test: bool = None) -> Result[List[PolibasePersonVisit]]:
                    return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_person_visits_by_registration_date, (DateTimeTool.date_to_string(value), test)), PolibasePersonVisit)

                @staticmethod
                def prerecording_by_registration_date(value: datetime = None, test: bool = None) -> Result[List[PolibasePersonVisit]]:
                    def filter_function(value: PolibasePersonVisit) -> bool:
                        return value.pin == CONST.POLIBASE.PRERECORDING_PIN
                    return ResultTool.data_filter(PIH.RESULT.POLIBASE.VISIT.by_registration_date(value, test), filter_function)

            class REVIEW_QUEST:

                @staticmethod
                def by(pin: int = None, is_active: bool = None, is_confirmed: bool = None, begin_date: str = None) -> Result[List[PolibaseReviewQuestItem]]:
                    return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_persons_review_quest, (pin, is_active, is_confirmed, begin_date)), PolibaseReviewQuestItem)

            @staticmethod
            def person_by_pin(value: int, test: bool = None) -> Result[PolibasePerson]:
                result: Result[PolibasePerson] = DataTool.to_result(RPC.call(
                    ServiceCommands.get_polibase_person_by_pin, (value, test)), PolibasePerson)
                if ResultTool.data_is_empty(result):
                    details: str = f"Пациент с персональным идентификационным номером {value} не найден"
                    raise NotFound(details)
                return result

            def persons_pin_by_visit_date(date: datetime, test: bool = None) -> Result[List[int]]:
                if test:
                    return Result(None, [100310])
                return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_persons_pin_by_visit_date, (date.strftime(CONST.DATE_FORMAT), test)))

            @staticmethod
            def person_creator_by_pin(value: int, test: bool = None) -> Result[PolibasePerson]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_person_registrator_by_pin, (value, test)), PolibasePerson)

            @staticmethod
            def persons_by_full_name(value: int, test: bool = None) -> Result[List[PolibasePerson]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_persons_by_full_name, (value, test)), PolibasePerson)

            @staticmethod
            def persons_by_pin(value: List[int], test: bool = None) -> Result[List[PolibasePerson]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_persons_by_pin, (value, test)), PolibasePerson)

            @staticmethod
            def all_persons(test: bool = None) -> Result[List[PolibasePerson]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_all_persons, test), PolibasePerson)

            @staticmethod
            def persons_by_chart_folder_name(value: str, test: bool = None) -> Result[List[PolibasePerson]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_persons_by_chart_folder_name, (value, test)), PolibasePerson)

            @staticmethod
            def person_pin_list_with_old_format_barcode(test: bool = None) -> Result[List[int]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_polibase_person_pin_list_with_old_format_barcode, test))

        class USER:

            @staticmethod
            def by_login(value: str) -> Result[User]:
                result: Result[User] = DataTool.to_result(
                    RPC.call(ServiceCommands.get_user_by_login, value), User, True)
                if ResultTool.data_is_empty(result):
                    details: str = f"Пользователь с логином {value} не существует"
                    raise NotFound(details)
                return result

            @staticmethod
            def by_polibase_pin(value: int) -> Result[User]:
                return PIH.RESULT.USER.by_name(PIH.RESULT.POLIBASE.person_by_pin(value).data.FullName)

            @staticmethod
            def by_workstation_name(name: str) -> Result[User]:
                name = name.lower()
                user_workstation: UserWorkstation = DataTool.to_result(RPC.call(
                    ServiceCommands.get_user_by_workstation, name), UserWorkstation, True).data
                if user_workstation is None:
                    details: str = f"Computer with name {name} is not exists!"
                    raise NotFound(details)
                return PIH.RESULT.USER.by_login(user_workstation.samAccountName) if user_workstation else None

            @staticmethod
            def by_any(value: Any) -> Result[List[User]]:
                if isinstance(value, Mark):
                    return PIH.RESULT.USER.by_name(value.FullName)
                elif isinstance(value, FullName):
                    return PIH.RESULT.USER.by_full_name(value)
                elif isinstance(value, int):
                    return PIH.RESULT.USER.by_polibase_pin(value)
                elif isinstance(value, (Workstation, UserWorkstation)):
                    return PIH.RESULT.USER.by_any(value.name)
                else:
                    if PIH.CHECK.MARK.tab_number(value):
                        return ResultTool.as_list(PIH.RESULT.USER.by_mark_tab_number(value))
                    if PIH.CHECK.WORCKSTATION.name(value):
                        return ResultTool.as_list(PIH.RESULT.USER.by_workstation_name(value))
                    if PIH.CHECK.login(value):
                        return ResultTool.as_list(PIH.RESULT.USER.by_login(value))
                    elif value == "" or PIH.CHECK.name(value):
                        return PIH.RESULT.USER.by_name(value)
                return Result(FIELD_COLLECTION.AD.USER, [])

            @staticmethod
            def by_job_position(job_position: CONST.AD.JobPositions) -> Result[List[User]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_users_by_job_position, job_position.name), User)

            @staticmethod
            def by_group(group: CONST.AD.Groups) -> Result[List[User]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_users_in_group, group.name), User)

            @staticmethod
            def template_list() -> Result[List[User]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_template_users), User)

            @staticmethod
            def containers() -> Result[List[UserContainer]]:
                return DataTool.to_result(RPC.call(
                    ServiceCommands.get_containers), UserContainer)

            @staticmethod
            def by_full_name(value: FullName, get_first: bool = False) -> Result[List[User]]:
                return DataTool.get_first_item(DataTool.to_result(RPC.call(ServiceCommands.get_user_by_full_name, value), User), get_first)

            @staticmethod
            def by_name(value: str) -> Result[List[User]]:
                result: Result[List[User]] = DataTool.to_result(
                    RPC.call(ServiceCommands.get_users_by_name, value), User)
                if ResultTool.data_is_empty(result):
                    details: str = f"Пользователь с именем {value} не найден"
                    raise NotFound(details)
                return result

            @staticmethod
            def active_by_name(value: str) -> Result[List[User]]:
                return DataTool.to_result(RPC.call(ServiceCommands.get_active_users_by_name, value), User)

            @staticmethod
            def all() -> Result[List[User]]:
                return PIH.RESULT.USER.by_name(CONST.AD.SEARCH_ALL_PATTERN)

            @staticmethod
            def all_active() -> Result[List[User]]:
                return PIH.RESULT.USER.active_by_name(CONST.AD.SEARCH_ALL_PATTERN)

            def all_active_with_telephone_number() -> Result[List[User]]:
                def user_with_phone(user: User) -> bool:
                    return PIH.CHECK.telephone_number(user.telephoneNumber)
                return ResultTool.data_filter(PIH.RESULT.USER.all_active(), lambda user: user_with_phone(user))

            @staticmethod
            def by_mark_tab_number(value: str) -> Result[User]:
                result: Result[Mark] = PIH.RESULT.MARK.by_tab_number(value)
                if ResultTool.data_is_empty(result):
                    details: str = f"Карта доступа с номером {value} не найдена"
                    raise NotFound(details)
                return PIH.RESULT.USER.by_mark(result.data)

            @staticmethod
            def by_mark(value: Mark) -> Result[User]:
                return Result(FIELD_COLLECTION.AD.USER, DataTool.check(value, lambda: DataTool.get_first_item(PIH.RESULT.USER.by_full_name(FullNameTool.from_string(value.FullName)).data)))

    class INPUT:

        @staticmethod
        def input(caption: str = None, new_line: bool = True) -> str:
            try:
                if new_line and caption is not None:
                    PR.input(caption)
                return input(PR.TEXT_BEFORE) if new_line else input(PR.TEXT_BEFORE + caption)
            except KeyboardInterrupt:
                raise KeyboardInterrupt()

        @staticmethod
        def telephone_number(format: bool = True, telephone_prefix: str = CONST.TELEPHONE_NUMBER_PREFIX) -> str:
            while True:
                PR.input("Номер телефона")
                use_telephone_prefix: bool = telephone_prefix is not None
                telephone = PIH.INPUT.input(
                    telephone_prefix if use_telephone_prefix else "", False)
                if use_telephone_prefix:
                    telephone = telephone_prefix + telephone
                check: bool = None
                if format:
                    telehone_fixed = PIH.DATA.FORMAT.telephone_number(
                        telephone, telephone_prefix)
                    check = PIH.CHECK.telephone_number(telehone_fixed)
                    if check and telehone_fixed != telephone:
                        telephone = telehone_fixed
                        PR.value("Телефон отформатирован", telephone)
                if check or PIH.CHECK.telephone_number(telephone):
                    return telephone
                else:
                    PR.red("Неверный формат номера телефона!")

        @staticmethod
        def email() -> str:
            while True:
                email = PIH.INPUT.input("Электронная почта")
                if PIH.CHECK.email(email):
                    return email
                else:
                    PR.red("Неверный формат электронной почты!")

        @staticmethod
        def message(prefix: str = None) -> str:
            return (prefix or "") + PIH.INPUT.input(prefix or "Введите сообщение")

        @staticmethod
        def description() -> str:
            PR.input("Введите описание")
            return PIH.INPUT.input()

        @staticmethod
        def login(check_on_exists: bool = False):
            while True:
                login = PIH.INPUT.input("Введите логин")
                if PIH.CHECK.login(login):
                    if check_on_exists and PIH.CHECK.USER.is_exists_by_login(login):
                        PR.red("Логин занят!")
                    else:
                        return login
                else:
                    PR.red("Неверный формат логина!")

        @staticmethod
        def indexed_list(caption: str, name_list: List[Any], caption_list: List[str], by_index: bool = False) -> str:
            return PIH.INPUT.item_by_index(caption, name_list, lambda item, index: caption_list[index if by_index else item])

        @staticmethod
        def indexed_field_list(caption: str, list: FieldItemList) -> str:
            name_list = list.get_name_list()
            return PIH.INPUT.item_by_index(caption, name_list, lambda item, _: list.get_item_by_name(item).caption)

        @staticmethod
        def index(caption: str, data: dict, item_label: Callable = None) -> int:
            selected_index = -1
            length = len(data)
            while True:
                if item_label:
                    max_index: int = len(data)
                    for index, item in enumerate(data):
                        PR.index(index + 1, item_label(item, index), max_index)
                if length == 1:
                    return 0
                selected_index = PIH.INPUT.input(
                    caption + f" (от 1 до {length})")
                if selected_index == "":
                    selected_index = 1
                try:
                    selected_index = int(selected_index) - 1
                    if selected_index >= 0 and selected_index < length:
                        return selected_index
                except ValueError:
                    continue

        @staticmethod
        def item_by_index(caption: str, data: List[Any], item_label: Callable = None) -> dict:
            return data[PIH.INPUT.index(caption, data, item_label)]

        @staticmethod
        def tab_number(check: bool = True) -> str:
            tab_number: str = None
            while True:
                tab_number = PIH.INPUT.input("Введите номер карты доступа")
                if check:
                    if PIH.CHECK.MARK.tab_number(tab_number):
                        return tab_number
                    else:
                        PR.bad("Неправильный формат номера карты доступа")
                        # return None
                else:
                    return tab_number

        @staticmethod
        def password(secret: bool = True, check: bool = False, settings: PasswordSettings = None, is_new: bool = True) -> str:
            PR.input("Введите новый пароль" if is_new else "Введите пароль")
            while True:
                value = getpass("") if secret else PIH.INPUT.input()
                if not check or PIH.CHECK.password(value, settings):
                    return value
                else:
                    PR.red("Пароль не соответствует требованием безопасности")

        @staticmethod
        def same_if_empty(caption: str, src_value: str) -> str:
            value = PIH.INPUT.input(caption)
            if value == "":
                value = src_value
            return value

        @staticmethod
        def name() -> str:
            return PIH.INPUT.input("Введите часть имени")

        @staticmethod
        def full_name(one_line: bool = False) -> FullName:
            if one_line:
                while(True):
                    value: str = PIH.INPUT.input("Введите полное имя")
                    if PIH.CHECK.full_name(value):
                        return FullNameTool.from_string(PIH.DATA.FORMAT.name(value))
                    else:
                        pass
            else:
                def full_name_part(caption: str) -> str:
                    while(True):
                        value: str = PIH.INPUT.input(caption)
                        value = value.strip()
                        if PIH.CHECK.name(value):
                            return PIH.DATA.FORMAT.name(value)
                        else:
                            pass
                return FullName(full_name_part("Введите фамилию"), full_name_part("Введите имя"), full_name_part("Введите отчество"))

        @staticmethod
        def yes_no(text: str = " ", enter_for_yes: bool = False) -> bool:
            text = PR.blue_str(PR.text_color(Fore.WHITE, text))
            PR.write_line(f"{text} \n{PR.green_str(PR.text_black('Да (1 или Ввод)'))} / {PR.red_str(PR.text_black('Нет (Остальное)'), '')}" if enter_for_yes else
                          f"{text} \n{PR.red_str('Да (1)')} / {PR.green_str(PR.text_black('Нет (Остальное или Ввод)'), '')}")
            answer = PIH.INPUT.input()
            answer = answer.lower()
            return answer == "y" or answer == "yes" or answer == "1" or (answer == "" and enter_for_yes)

        class USER:

            @staticmethod
            def container() -> UserContainer:
                result: Result[List[UserContainer]
                               ] = PIH.RESULT.USER.containers()
                PIH.VISUAL.containers_for_result(result, True)
                return PIH.INPUT.item_by_index("Выберите контейнер пользователя, введя индекс", result.data)

            @staticmethod
            def by_name() -> User:
                result: Result[List[User]] = PIH.RESULT.USER.by_name(
                    PIH.INPUT.name())
                result.fields = FIELD_COLLECTION.AD.USER_NAME
                PIH.VISUAL.table_with_caption(
                    result, "Список пользователей", True)
                return PIH.INPUT.item_by_index("Выберите пользователя, введя индекс", result.data)

            @staticmethod
            def template() -> dict:
                result: Result[List[User]] = PIH.RESULT.USER.template_list()
                PIH.VISUAL.template_users_for_result(result, True)
                return PIH.INPUT.item_by_index("Выберите шаблон пользователя, введя индекс", result.data)

            @staticmethod
            def search_attribute() -> str:
                return PIH.INPUT.indexed_field_list("Выберите по какому критерию искать, введя индекс",
                                                    FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE)

            @staticmethod
            def search_value(search_attribute: str) -> str:
                field_item = FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE.get_item_by_name(
                    search_attribute)
                return PIH.INPUT.input(f"Введите {field_item.caption.lower()}")

        class MARK:

            @staticmethod
            def free(group: MarkGroup = None) -> Mark:
                result: Result[List[Mark]] = None
                while True:
                    if group is None:
                        if PIH.INPUT.yes_no("Выбрать группы доступа для карты доступа, введя имени пользователя из этой группы?"):
                            result = PIH.RESULT.MARK.by_name(PIH.INPUT.name())
                            mark_list: List[Mark] = result.data
                            length = len(mark_list)
                            if length > 0:
                                if length > 1:
                                    PIH.VISUAL.table_with_caption_first_title_is_centered(
                                        result, "Найденные пользователи:", True)
                                group = PIH.INPUT.item_by_index(
                                    "Выберите группу доступа", mark_list)
                            else:
                                PR.red(
                                    "Пользователь с введенным именем не найден")
                        else:
                            result = PIH.RESULT.MARK.free_marks_group_statistics(
                                False)
                            data = result.data
                            length = len(data)
                            if length > 0:
                                if length > 1:
                                    PIH.VISUAL.free_marks_group_statistics_for_result(
                                        result, True)
                                group = PIH.INPUT.item_by_index(
                                    "Выберите группу доступа введя индекс", data)
                            else:
                                PR.red("Свободный карт доступа нет!")
                                return None
                    if group is not None:
                        result = PIH.RESULT.MARK.free_marks_by_group_id(
                            group.GroupID)
                        data = result.data
                        length = len(data)
                        if length > 0:
                            if length > 1:
                                PIH.VISUAL.free_marks_by_group_for_result(
                                    group, result, True)
                            return PIH.INPUT.item_by_index(
                                "Выберите карту доступа введя индекс", data)
                        else:
                            PR.red(
                                f"Нет свободных карт для группы доступа '{group.GroupName}'!")
                            return PIH.INPUT.MARK.free()
                    else:
                        pass

            @staticmethod
            def person_division() -> MarkDivision:
                division_list: List[MarkDivision] = PIH.RESULT.MARK.person_divisions(
                ).data
                return PIH.INPUT.item_by_index("Выберите подразделение для персоны, которой принадлежит карта доступа", division_list, lambda item, _: item.name)

            @staticmethod
            def by_name() -> Mark:
                PR.head2("Введите имя персоны")
                result: Result[List[Mark]] = PIH.RESULT.MARK.by_name(
                    PIH.INPUT.name())
                PIH.VISUAL.marks_for_result(result, "Карты доступа", True)
                return PIH.INPUT.item_by_index("Выберите карточку, введя индекс", result.data)

            @staticmethod
            def by_any() -> Mark:
                value: str = PIH.INPUT.input(
                    "Введите часть имени или табельный номер держателя карты")
                result: Result[List[Mark]] = PIH.RESULT.MARK.by_any(value)
                PIH.VISUAL.marks_for_result(result, "Карты доступа", True)
                return PIH.INPUT.item_by_index("Выберите карточку, введя индекс", result.data)

        @staticmethod
        def message_for_user_by_login(login: str) -> str:
            user: User = PIH.RESULT.USER.by_login(login).data
            if user is not None:
                head_string = f"Здравствуйте, {FullNameTool.to_given_name(user.name)}, "
                PR.green(head_string)
                message = PIH.INPUT.input("Введите сообщениеt: ")
                return head_string + message
            else:
                pass

    class CHECK:

        @staticmethod
        def email_accessability(value: str) -> bool:
            return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.check_email_accessibility, value))

        class FILE:

            @staticmethod
            def excel_file(path: str) -> bool:
                return os.path.isfile(path) and PathTool.get_extension(path) in [FILE.EXTENSION.EXCEL_OLD, FILE.EXTENSION.EXCEL_NEW]

        class ACCESS:

            @staticmethod
            def by_group(group: CONST.AD.Groups, exit_on_access_denied: bool = False) -> bool:
                login: str = PIH.SESSION.get_login()
                result: bool = False
                user_list: List[User] = PIH.RESULT.USER.by_group(group).data
                if user_list is not None:
                    for user in user_list:
                        if user.samAccountName == login:
                            PIH.SESSION.add_allowable_group(group)
                            result = True
                            break
                PIH.MESSAGE.from_system_bot(
                    f"Запрос на доступа к группе: {group.name} от пользователя {PIH.SESSION.get_user().name} ({login}). Доступ {'разрешен' if result else 'отклонен'}.", LogLevels.NORMAL if result else LogLevels.ERROR)
                if exit_on_access_denied:
                    if result:
                        return result
                    PIH.SESSION.exit(5, "Функционал недоступен...")
                else:
                    return result

            @staticmethod
            def admin(exit_on_access_denied: bool = False) -> bool:
                return PIH.CHECK.ACCESS.by_group(CONST.AD.Groups.Admin, exit_on_access_denied)

            @staticmethod
            def service_admin() -> bool:
                return PIH.CHECK.ACCESS.by_group(CONST.AD.Groups.ServiceAdmin)

            @staticmethod
            def inventory() -> bool:
                return PIH.CHECK.ACCESS.by_group(CONST.AD.Groups.Inventory)

            @staticmethod
            def polibase() -> bool:
                return PIH.CHECK.ACCESS.by_group(CONST.AD.Groups.Inventory)

        class USER:

            @staticmethod
            def is_exists_by_login(value: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.check_user_exists_by_login, value))

            @staticmethod
            def is_user(user: User) -> bool:
                return PIH.CHECK.full_name(user.name)

            @staticmethod
            def is_acive(user: User) -> bool:
                return user.distinguishedName.find(CONST.AD.ACTIVE_USERS_CONTAINER_DN) != -1

            @staticmethod
            def is_exists_by_full_name(full_name: FullName) -> bool:
                return ResultTool.data_is_empty(PIH.RESULT.USER.by_full_name(full_name))

            @staticmethod
            def search_attribute(value: str) -> bool:
                return value in CONST.AD.SEARCH_ATTRIBUTES

            @staticmethod
            def property(value: str) -> str:
                if value == "":
                    return USER_PROPERTY.TELEPHONE_NUMBER
                return value

        class MARK:

            @staticmethod
            def is_free(tab_number: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.check_mark_free, tab_number))

            @staticmethod
            def is_exists_by_full_name(full_name: FullName) -> bool:
                result: Result[List[Mark]] = PIH.RESULT.MARK.by_name(
                    FullNameTool.to_string(full_name))
                return ResultTool.data_is_empty(result)

            @staticmethod
            def accessible() -> bool:
                return PIH.SERVICE.check_accessibility(ServiceRoles.MARK)

            @staticmethod
            def tab_number(value: str) -> bool:
                return re.fullmatch(r"[0-9]+", value) is not None

        class TIME_TRACKING:

            @staticmethod
            def accessible() -> bool:
                return PIH.CHECK.ACCESS.by_group(CONST.AD.Groups.TimeTrackingReport)

        class INVENTORY:

            @staticmethod
            def is_report_file(file_path: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.check_inventory_report, file_path))

            @staticmethod
            def accessible() -> bool:
                return PIH.SERVICE.check_accessibility(ServiceRoles.DOCS) and PIH.CHECK.ACCESS.inventory()

        class POLIBASE:

            class REVIEW_QUEST:

                @staticmethod
                def high_grade(value: int) -> bool:
                    return value >= CONST.POLIBASE.REVIEW_QUEST.HIGH_GRADE

                def information_way_set(pin: int) -> bool:
                    return not ResultTool.data_is_empty(ResultTool.data_filter(PIH.RESULT.POLIBASE.REVIEW_QUEST.by(pin), lambda item: item.completeDate is not None))

            @staticmethod
            def accessible() -> bool:
                return PIH.SERVICE.check_accessibility(ServiceRoles.POLIBASE) and PIH.CHECK.ACCESS.polibase()

            @staticmethod
            def is_person_chart_folder(name: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.check_polibase_person_chart_folder, name))

            @staticmethod
            def person_is_exists_by_pin(pin: int) -> bool:
                return PIH.RESULT.POLIBASE.person_by_pin(pin).data is not None

            class NOTIFICATION:
    
                @staticmethod
                def exists(value: PolibasePersonVisitNotification) -> bool:
                    return not ResultTool.data_is_empty(PIH.RESULT.POLIBASE.NOTIFICATION.by(value))

        @staticmethod
        def login(value: str) -> bool:
            pattern = r"([a-z]{" + \
                str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}[0-9]*)"
            return re.fullmatch(pattern, value) is not None

        class WORCKSTATION:

            @staticmethod
            def name(value: str) -> bool:
                value = value.lower()
                for prefix in CONST.AD.WORKSTATION_PREFIX_LIST:
                    if value.startswith(prefix):
                        return True
                return False

            @staticmethod
            def has_property(workstation: Workstation, property: CONST.AD.WSProperties) -> bool:
                return (workstation.properties & property.value) != 0

            @staticmethod
            def is_watchable(workstation: Workstation) -> bool:
                return PIH.CHECK.WORCKSTATION.has_property(workstation, CONST.AD.WSProperties.Watchable)

            @staticmethod
            def is_poweroffable(workstation: Workstation) -> bool:
                return PIH.CHECK.WORCKSTATION.has_property(workstation, CONST.AD.WSProperties.Poweroffable)

        @staticmethod
        def telephone_number(value: str) -> bool:
            return not DataTool.is_empty(value) and re.fullmatch(r"^\+[0-9]{11,13}$", value) is not None

        @staticmethod
        def email(value: str, check_accesability: bool = False) -> bool:
            return re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", value) is not None and (not check_accesability or PIH.CHECK.email_accessability(value))

        @staticmethod
        def name(value: str, use_space: bool = False) -> bool:
            pattern = r"[а-яА-ЯёЁ" + (" " if use_space else "") + \
                "]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}$"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def full_name(value: str) -> bool:
            pattern = r"[а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",} [а-яА-ЯёЁ]{" + str(
                CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",} [а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}$"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def password(value: str, settings: PasswordSettings = None) -> bool:
            settings = settings or PASSWORD.SETTINGS.DEFAULT
            return PasswordTools.check_password(value, settings.length, settings.special_characters)

        @staticmethod
        def ping(host: str) -> bool:
            command = ['ping', "-n", '1', host]
            response = subprocess.call(command)
            return response == 0

    message_executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def send_log_message(message: str, channel: MessageChannels = MessageChannels.DEFAULT, level: Any = LogLevels.DEFAULT) -> None:
        level_value: int = None
        level_list: List[LogLevels] = None
        if isinstance(level, LogLevels):
            level_list = [level]
        if isinstance(level, int):
            level_value = level
        if level_value is None:
            level_value = 0
            for level_item in level_list:
                level_value = level_value | level_item.value

        def internal_send_log_message(message: str, channel_name: str, level_value: int) -> None:
            try:
                RPC.call(ServiceCommands.send_log_message,
                         (message, channel_name, level_value))
            except Error as error:
                PR.bad("Log send error")
        PIH.message_executor.submit(internal_send_log_message, message,
                                    channel.name, level_value)

    @staticmethod
    def send_command_message(message_command: MessageCommands, parameters: Tuple = None) -> None:
        message_commnad_description: MessageCommandDescription = message_command.value
        parameter_pattern_list: List = DataTool.as_list(
            message_commnad_description.params)
        parameters = parameters or ()
        parameters_dict: dict = {}
        if len(parameter_pattern_list) > len(parameters):
            raise Exception(
                "Income parameter list length is less that parameter list length of command")
        for index, parameter_pattern_item in enumerate(parameter_pattern_list):
            parameter_pattern: ParamItem = parameter_pattern_item
            parameters_dict[parameter_pattern.name] = parameters[index]

        def internal_send_command_message(command_name: str, parameters: dict) -> None:
            try:
                RPC.call(ServiceCommands.send_command_message,
                         (command_name, parameters))
            except Error:
                PR.bad("Log send error")
        PIH.message_executor.submit(internal_send_command_message,
                                    message_command.name, parameters_dict)

    class MESSAGE:

        class INTERNAL:

            @staticmethod
            def by_user(user: User, message: str, method_type: InternalMessageMethodTypes = InternalMessageMethodTypes.REMOTE) -> bool:
                return PIH.MESSAGE.INTERNAL.by_login(user.samAccountName, message, method_type)

            @staticmethod
            def by_workstation(workstation: Workstation, message: str,  method_type: InternalMessageMethodTypes = InternalMessageMethodTypes.REMOTE) -> bool:
                return PIH.MESSAGE.INTERNAL.by_workstation_name(workstation.name, message, method_type)

            @staticmethod
            def by_workstation_name(workstation_name: str, message: str,  method_type: InternalMessageMethodTypes = InternalMessageMethodTypes.REMOTE) -> bool:
                return PIH.MESSAGE.INTERNAL.by_user(PIH.RESULT.USER.by_workstation_name(workstation_name).data, message, method_type)

            @staticmethod
            def by_login(login: str, message: str, method_type: InternalMessageMethodTypes = InternalMessageMethodTypes.REMOTE) -> bool:
                if RPC.Service.role == ServiceRoles.MESSAGE:
                    method_type = InternalMessageMethodTypes.LOCAL_PSTOOL_MSG
                if method_type == InternalMessageMethodTypes.REMOTE:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.send_internal_message, (login, message)))
                workstation_list: List[UserWorkstation] = PIH.RESULT.WORKSTATION.by_login(
                    login).data
                for workstation_item in workstation_list:
                    workstation: UserWorkstation = workstation_item
                    if method_type == InternalMessageMethodTypes.LOCAL_PSTOOL_MSG:
                        PIH.PSTOOLS.run_command(PIH.PSTOOLS.create_remote_process_executor(
                            [CONST.MSG.EXECUTOR, workstation.samAccountName, message],  workstation.name), False)
                    if method_type == InternalMessageMethodTypes.LOCAL_MSG:
                        PIH.PSTOOLS.run_command(
                            [CONST.MSG.EXECUTOR, workstation.samAccountName, f"/server:{workstation.name}", message], False)
                return True

        class WHATSAPP:

            @staticmethod
            def message_list(telephone_number: str) -> List[WhatsAppMessage]:
                url: str = f"{CONST.MESSAGE.WHATSAPP.WAPPI.URL_GET_MESSAGES}{CONST.MESSAGE.WHATSAPP.WAPPI.PROFILE_ID}&chat_id={telephone_number}@c.us"
                headers: dict = {
                    "Authorization": CONST.MESSAGE.WHATSAPP.WAPPI.AUTHORICATION,
                    "Content-Type": "application/json"
                }
                result: List[WhatsAppMessage] = []
                try:
                    response: Response = requests.get(url, headers=headers)
                except Exception:
                    return result
                response_result: dict = json.loads(response.text)
                for message_item in response_result["messages"]:
                    if message_item["type"] == "chat":
                        result.append(WhatsAppMessage(
                            message_item["body"], message_item["fromMe"], message_item["time"]))
                return result

            @staticmethod
            def send_via_wappi(telephone_number: str, message: Any) -> bool:
                url: str = None
                payload: dict = {"recipient": telephone_number}
                if isinstance(message, str):
                    payload["body"] = message
                    url: str = CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_MESSAGE
                elif isinstance(message, (WhatsAppMessageListPayload, WhatsAppMessageButtonsPayload)):
                    for item in message.__dataclass_fields__:
                        item_value: Any = message.__getattribute__(item)
                        if not DataTool.is_empty(item_value):
                            payload[item] = item_value
                    if isinstance(message, WhatsAppMessageListPayload):
                        url = CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_LIST_MESSAGE
                    else:
                        url = CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_BUTTONS_MESSAGE
                url += CONST.MESSAGE.WHATSAPP.WAPPI.PROFILE_ID
                headers: dict = {"accept": "application/json",
                                 "Authorization": CONST.MESSAGE.WHATSAPP.WAPPI.AUTHORICATION, "Content-Type": "application/json"}
                try:
                    response: Response = requests.post(
                        url, data=json.dumps(payload), headers=headers)
                except ConnectTimeout:
                    return False
                if response.status_code == CONST.ERROR.WAPPI.PROFILE_NOT_PAID:
                    PIH.MESSAGE.from_it_bot(
                        "Аккаунт Wappi (сервис для отправики сообщений в WhatsApp) не оплачен", LogLevels.ERROR)
                return response.status_code == 200

            @staticmethod
            def send_via_browser(telephone_number: str, message: str) -> bool:
                pywhatkit_is_exists: bool = importlib.util.find_spec(
                    "pywhatkit") is not None
                if not pywhatkit_is_exists:
                    PR.green(
                        "Установка библиотеки для отправки сообщения. Ожидайте...")
                    if not PIH.UPDATER.install_module("pywhatkit"):
                        PR.bad(
                            "Ошибка при установке библиотеки для отправки сообщений!")
                try:
                    import pywhatkit as pwk
                    pwk.sendwhatmsg_instantly(telephone_number, message)
                except Exception as уrror:
                    PR.bad("Ошибка при отправке сообщения!")

            @staticmethod
            def send(telephone_number: str, message: Any, via_wappi: bool = True, use_alternative: bool = True) -> bool:
                result: bool = False
                telephone_number = PIH.DATA.FORMAT.telephone_number(telephone_number)
                if via_wappi:
                    result = PIH.MESSAGE.WHATSAPP.send_via_wappi(
                        telephone_number, message)
                if result:
                    return result
                if use_alternative or not via_wappi:
                    return PIH.MESSAGE.WHATSAPP.send_via_browser(telephone_number, message)
                return False

            @staticmethod
            def by_user(user: User, message: Any, via_wappi: bool = True, use_alternative: bool = True) -> bool:
                return PIH.MESSAGE.WHATSAPP.send(user.telephoneNumber, message, via_wappi, use_alternative)

            @staticmethod
            def by_login(login: str, message: Any, via_wappi: bool = True, use_alternative: bool = True) -> bool:
                return PIH.MESSAGE.WHATSAPP.send(PIH.DATA.TELEPHONE_NUMBER.by_login(login), message, via_wappi, use_alternative)

        class COMMAND:

            @staticmethod
            def polibase_persons_with_old_format_barcode_was_detected(persons_pin: List[int]) -> None:
                PIH.send_command_message(
                    MessageCommands.POLIBASE_PERSONS_WITH_OLD_FORMAT_BARCODE_WAS_DETECTED, (len(persons_pin), persons_pin))

            @staticmethod
            def all_polibase_persons_barcode_with_old_format_was_created(persons_pin: List[int]) -> None:
                PIH.send_command_message(
                    MessageCommands.POLIBASE_ALL_PERSON_BARCODES_WITH_OLD_FORMAT_WAS_CREATED, (persons_pin,))

            @staticmethod
            def notify_about_polibase_person_wants_feedback_call_after_review_quest_complete(person: PolibasePerson, review_quest_item: PolibaseReviewQuestItem) -> None:
                PIH.send_command_message(
                    MessageCommands.POLIBASE_PERSON_WANTS_FEEDBACK_CALL_AFTER_REVIEW_QUEST_COMPLETE, (person.FullName, str(person.pin), str(review_quest_item.grade), review_quest_item.message, PIH.DATA.FORMAT.telephone_number(person.telephoneNumber)))

            @staticmethod
            def notify_about_polibase_person_wants_feedback_call_after_review_quest_complete(person: PolibasePerson, review_quest_item: PolibaseReviewQuestItem) -> None:
                PIH.send_command_message(
                    MessageCommands.POLIBASE_PERSON_WANTS_FEEDBACK_CALL_AFTER_REVIEW_QUEST_COMPLETE, (person.FullName, str(person.pin), str(review_quest_item.grade), review_quest_item.message, PIH.DATA.FORMAT.telephone_number(person.telephoneNumber)))

            @staticmethod
            def notify_about_polibase_person_review_quest_complete(person: PolibasePerson, review_quest_item: PolibaseReviewQuestItem) -> None:
                information_way_string: str = CONST.POLIBASE.REVIEW_QUEST.INFORMATION_WAY_TYPES[
                    review_quest_item.informationWay - 1]
                if PIH.CHECK.POLIBASE.REVIEW_QUEST.high_grade(review_quest_item.grade):
                    PIH.send_command_message(MessageCommands.POLIBASE_PERSON_REVIEW_QUEST_RESULT_FOR_HIGH_GRADE, (person.FullName, person.pin, review_quest_item.grade,
                                             information_way_string, PIH.DATA.FORMAT.telephone_number(person.telephoneNumber)))
                else:
                    PIH.send_command_message(MessageCommands.POLIBASE_PERSON_REVIEW_QUEST_RESULT_FOR_LOW_GRADE, (person.FullName, person.pin, review_quest_item.grade, review_quest_item.message,
                                             information_way_string, CONST.POLIBASE.REVIEW_QUEST.FEEDBAK_CALL_TYPES[review_quest_item.feedbackCallStatus], PIH.DATA.FORMAT.telephone_number(person.telephoneNumber)))
            
            @staticmethod
            def polibase_person_visit_was_registered(value: PolibasePersonVisit) -> None:
                PIH.send_command_message(MessageCommands.POLIBASE_PERSON_VISIT_WAS_REGISTERED, (value.FullName, "Предзапись" if value.pin == CONST.POLIBASE.PRERECORDING_PIN else value.pin, value.pin, value))

            @staticmethod
            def polibase_person_visit_notification_was_registered(visit: PolibasePersonVisit, notification: PolibasePersonVisitNotificationVO) -> None:
                PIH.send_command_message(MessageCommands.POLIBASE_PERSON_VISIT_NOTIFICATION_WAS_REGISTERED, (
                    visit.FullName, "Предзапись" if visit.pin == CONST.POLIBASE.PRERECORDING_PIN else visit.pin, notification))

            @staticmethod
            def login() -> None:
                login: str = PIH.SESSION.get_login()
                user: User = PIH.RESULT.USER.by_login(login).data
                PIH.send_command_message(
                    MessageCommands.LOG_IN, (user.name, login, PIH.OS.get_host()))

            @staticmethod
            def start_session() -> None:
                argv = PIH.SESSION.argv()
                argv_str: str = ""
                if argv is not None:
                    argv_str = " ".join(argv)
                    argv_str = f"({argv_str})"
                login: str = PIH.SESSION.get_login()
                user: User = PIH.RESULT.USER.by_login(login).data
                PIH.send_command_message(MessageCommands.START_SESSION, (user.name, login,
                                         f"{PIH.SESSION.get_file_name()} {argv_str}", f"{PIH.VERSION.local()}/{PIH.VERSION.remote()}", PIH.OS.get_host()))

            @staticmethod
            def service_started(role: ServiceRoles) -> None:
                service_role_value: ServiceRoleDescription = role.value
                PIH.send_command_message(MessageCommands.SERVICE_STARTED, (role.name, service_role_value.description,
                                         service_role_value.host, service_role_value.port, service_role_value.pid))

            @staticmethod
            def service_not_started(role: ServiceRoles) -> None:
                service_role_value: ServiceRoleDescription = role.value
                PIH.send_command_message(MessageCommands.SERVICE_NOT_STARTED, (role.name, service_role_value.description,
                                         service_role_value.host, service_role_value.port))

            @staticmethod
            def hr_notify_about_new_employee(login: User) -> None:
                user: User = PIH.RESULT.USER.by_login(login).data
                hr_user: User = ResultTool.get_first_data_element(
                    PIH.RESULT.USER.by_job_position(CONST.AD.JobPositions.HR))
                PIH.send_command_message(MessageCommands.HR_NOTIFY_ABOUT_NEW_EMPLOYEE, (FullNameTool.to_given_name(hr_user.name),
                                                                                        user.name, user.mail))

            @staticmethod
            def it_notify_about_user_creation(login: str, password: str) -> None:
                it_user_list: List[User] = PIH.RESULT.USER.by_job_position(
                    CONST.AD.JobPositions.IT).data
                me_user_login: str = PIH.SESSION.get_login()
                it_user_list = list(
                    filter(lambda user: user.samAccountName != me_user_login, it_user_list))
                it_user: User = it_user_list[0]
                user: User = PIH.RESULT.USER.by_login(login).data
                PIH.send_command_message(MessageCommands.IT_NOTIFY_ABOUT_CREATE_USER, (
                    user.name, user.description, user.samAccountName, password, user.telephoneNumber, user.mail))
                PIH.send_command_message(MessageCommands.IT_TASK_AFTER_CREATE_NEW_USER, (FullNameTool.to_given_name(
                    it_user.name), user.name, user.mail, password))

            @staticmethod
            def it_notify_about_mark_creation(temporary: bool, full_name: Any, tab_number: str = None) -> None:
                name: str = FullNameTool.to_string(full_name) if isinstance(
                    full_name, FullName) else full_name
                mark: Mark = PIH.RESULT.MARK.by_name(name, True).data
                telephone_number: str = PIH.DATA.FORMAT.telephone_number(
                    mark.telephoneNumber)
                if temporary:
                    PIH.send_command_message(MessageCommands.IT_NOTIFY_ABOUT_CREATE_TEMPORARY_MARK,
                                             (name, tab_number, telephone_number))
                else:
                    PIH.send_command_message(MessageCommands.IT_NOTIFY_ABOUT_CREATE_NEW_MARK, (
                        name, telephone_number, mark.TabNumber, mark.GroupName))

            @staticmethod
            def it_notify_about_temporary_mark_return(mark: Mark, temporary_tab_number: int) -> None:
                PIH.send_command_message(
                    MessageCommands.IT_NOTIFY_ABOUT_TEMPORARY_MARK_RETURN, (mark.FullName, temporary_tab_number))

            @staticmethod
            def it_notify_about_mark_return(mark: Mark) -> None:
                PIH.send_command_message(
                    MessageCommands.IT_NOTIFY_ABOUT_MARK_RETURN, (mark.FullName, mark.TabNumber))

            @staticmethod
            def it_notify_about_create_new_mark(full_name: Any) -> None:
                PIH.MESSAGE.COMMAND.it_notify_about_mark_creation(
                    False, full_name)

            @staticmethod
            def it_notify_about_create_temporary_mark(full_name: Any, tab_number: str) -> None:
                PIH.MESSAGE.COMMAND.it_notify_about_mark_creation(
                    True, full_name, tab_number)

            @staticmethod
            def printer_report(name: str, location: str, report: str) -> bool:
                return PIH.send_command_message(MessageCommands.PRINTER_REPORT, (name, location, report))

        @staticmethod
        def to_debug_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.DEBUG_BOT, level)

        @staticmethod
        def from_debug_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.DEBUG, level)

        @staticmethod
        def from_system_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.SYSTEM, level)

        @staticmethod
        def to_system_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.SYSTEM_BOT, level)

        @staticmethod
        def backup(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.BACKUP, level)

        @staticmethod
        def notification(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.NOTIFICATION, level)

        @staticmethod
        def from_printer_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.PRINTER, level)

        @staticmethod
        def to_printer_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.PRINTER_BOT, level)

        @staticmethod
        def from_it_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.IT, level)

        @staticmethod
        def from_feedback_call_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.POLIBASE_PERSON_FEEDBACK_CALL, level)

        @staticmethod
        def from_review_request_result(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.POLIBASE_PERSON_REVIEW_QUEST_RESULT, level)

        @staticmethod
        def to_it_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.send_log_message(message, MessageChannels.IT_BOT, level)

    class VISUAL:

        @staticmethod
        def init() -> None:
            PR.init()

        @staticmethod
        def clear_screen():
            os.system('cls' if os.name == 'nt' else 'clear')

        @staticmethod
        def main_title() -> None:
            PR.cyan(
                PR.text_color(Fore.WHITE, "███ ███ █┼█"))
            PR.cyan(
                PR.text_color(Fore.WHITE, "█▄█ ┼█┼ █▄█"))
            PR.cyan(PR.text_color(Fore.WHITE, "█┼┼ ▄█▄ █┼█") +
                    PR.text_color(Fore.BLACK, f" {PIH.VERSION.local()}"))
            PR.new_line()

        class MARK:

            @staticmethod
            def by_any(value: str) -> None:
                PIH.VISUAL.marks_for_result(
                    PIH.RESULT.MARK.by_any(value), "Результат:")

        class USER:

            @staticmethod
            def result(result: Result, root_location: str = CONST.AD.ACTIVE_USERS_CONTAINER_DN) -> None:
                fields: FieldItemList = result.fields
                base_location_list = PIH.DATA.FORMAT.location_list(
                    root_location, False)
                root_base_location = base_location_list[0:2]
                root_base_location.reverse()
                base_location = CONST.AD.LOCATION_JOINER.join([".".join(
                    root_base_location), CONST.AD.LOCATION_JOINER.join(base_location_list[2:])])
                location_field = fields.get_item_by_name(
                    FIELD_NAME_COLLECTION.DN)
                pevious_caption: str = location_field.caption
                location_field.caption = f"{location_field.caption} from {base_location}"

                def modify_data(field: FieldItem, user: User) -> str:
                    if field.name == USER_PROPERTY.DN:
                        return CONST.AD.LOCATION_JOINER.join(filter(
                            lambda x: x not in base_location_list, PIH.DATA.FORMAT.location_list(user.distinguishedName)))
                    if field.name == USER_PROPERTY.USER_ACCOUNT_CONTROL:
                        return "\n".join(PIH.DATA.FORMAT.get_user_account_control_values(user.userAccountControl))
                    if field.name == USER_PROPERTY.DESCRIPTION:
                        return user.description
                    if field.name == USER_PROPERTY.NAME:
                        return "\n".join(user.name.split(" "))
                    return None
                PIH.VISUAL.table_with_caption(
                    result, "Пользватели:", False, None, modify_data)
                location_field.caption = pevious_caption

        @staticmethod
        def rpc_service_header(host: str, port: int, description: str) -> None:
            PR.blue("PIH service")
            PR.blue(f"Version: {PIH.VERSION.local()}")
            PR.blue(f"PyPi Version: {PIH.VERSION.remote()}")
            PR.green(f"Service host: {host}")
            PR.green(f"Service port: {port}")
            PR.green(f"Service name: {description}")

        @staticmethod
        def service_header(role: ServiceRoles) -> None:
            service_role_value: ServiceRoleDescription = role.value
            if service_role_value.debug:
                PR.blue(f"[Debug]")
            PR.blue("Запуск сервиса")
            PR.blue(f"PIH версия: {PIH.VERSION.remote()}")
            PR.green(f"Хост: {service_role_value.host}")
            PR.green(f"Порт: {service_role_value.port}")
            PR.green(f"Имя сервиса: {service_role_value.name}")
            PR.green(f"Описание сервиса: {service_role_value.description}")
            PR.green(f"Идентификатор процесса: {service_role_value.pid}")

        @staticmethod
        def free_marks(show_guest_marks: bool, use_index: bool = False) -> None:
            mark_list_result: Result[List[Mark]] = PIH.RESULT.MARK.free_list()

            def filter_function(item: Mark) -> bool:
                return EnumTool.get(MarkType, item.type) != MarkType.GUEST
            if not show_guest_marks:
                ResultTool.data_filter(mark_list_result, filter_function)
            PIH.VISUAL.table_with_caption_first_title_is_centered(
                mark_list_result, "Свободные карты доступа:", use_index)

        @staticmethod
        def guest_marks(use_index: bool = False) -> None:
            mark_list_result: Result[List[Mark]] = PIH.RESULT.MARK.free_list()
            mark_list_result.fields.visible(
                FIELD_NAME_COLLECTION.GROUP_NAME, False)

            def filter_function(item: Mark) -> bool:
                return EnumTool.get(MarkType, item.type) == MarkType.GUEST
            ResultTool.data_filter(mark_list_result, filter_function)
            PIH.VISUAL.table_with_caption_first_title_is_centered(
                mark_list_result, "Гостевые карты доступа:", use_index)

        @staticmethod
        def marks_for_result(result: Result, caption: str, use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption_first_title_is_centered(
                result, caption, use_index)

        @staticmethod
        def temporary_candidate_for_mark(mark: Mark) -> None:
            PIH.VISUAL.marks_for_result(
                Result(FIELD_COLLECTION.ORION.FREE_MARK, [mark]), "Временная карта")

        @staticmethod
        def free_marks_group_statistics(use_index: bool = False, show_guest_marks: bool = None) -> None:
            PIH.VISUAL.free_marks_group_statistics_for_result(
                PIH.RESULT.MARK.free_marks_group_statistics(show_guest_marks), use_index)

        @staticmethod
        def free_marks_by_group(group: dict, use_index: bool = False) -> None:
            PIH.VISUAL.free_marks_by_group_for_result(
                PIH.RESULT.MARK.free_marks_by_group_id(group), group, use_index)

        @staticmethod
        def free_marks_group_statistics_for_result(result: Result, use_index: bool) -> None:
            PIH.VISUAL.table_with_caption_last_title_is_centered(
                result, "Свободные карты доступа:", use_index)

        @staticmethod
        def free_marks_by_group_for_result(group: MarkGroup, result: Result, use_index: bool) -> None:
            group_name = group.GroupName
            PIH.VISUAL.table_with_caption_last_title_is_centered(
                result, f"Свободные карты доступа для группы доступа '{group_name}':", use_index)

        @staticmethod
        def temporary_marks(use_index: bool = False,) -> None:
            def modify_table(table: PrettyTable, caption_list: List[str]):
                table.align[caption_list[0]] = "c"
                table.align[caption_list[1]] = "c"
            PIH.VISUAL.table_with_caption(
                PIH.RESULT.MARK.temporary_list(), "Список временных карт:", use_index, modify_table)

        @staticmethod
        def containers_for_result(result: Result, use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption(result, "Подразделение:", use_index)

        @staticmethod
        def table_with_caption_first_title_is_centered(result: Result, caption: str, use_index: bool = False, modify_data_handler: Callable = None) -> None:
            def modify_table(table: PrettyTable, caption_list: List[str]):
                table.align[caption_list[int(use_index)]] = "c"
            PIH.VISUAL.table_with_caption(
                result, caption, use_index, modify_table, modify_data_handler)

        @staticmethod
        def table_with_caption_last_title_is_centered(result: Result, caption: str, use_index: bool = False, modify_data_handler: Callable = None) -> None:
            def modify_table(table: PrettyTable, caption_list: List[str]):
                table.align[caption_list[-1]] = "c"
            PIH.VISUAL.table_with_caption(
                result, caption, use_index, modify_table, modify_data_handler)

        @staticmethod
        def table_with_caption(result: Any, caption: str = None, use_index: bool = False, modify_table_handler: Callable = None, modify_data_handler: Callable = None) -> None:
            if caption is not None:
                PR.cyan(caption)
            is_result_type: bool = isinstance(result, Result)
            field_list = result.fields if is_result_type else ResultUnpack.unpack_fields(
                result)
            data = result.data if is_result_type else ResultUnpack.unpack_data(
                result)
            if DataTool.is_empty(data):
                PR.bad("Не найдено!")
            else:
                if not isinstance(data, list):
                    data = [data]
                if len(data) == 1:
                    use_index = False
                if use_index:
                    field_list.list.insert(0, FIELD_COLLECTION.INDEX)
                caption_list: List = field_list.get_caption_list()

                def create_table(caption_list: List[str]) -> PrettyTable:
                    from prettytable.colortable import ColorTable, Themes
                    table: ColorTable = ColorTable(
                        caption_list, theme=Themes.OCEAN)
                    table.align = "l"
                    if use_index:
                        table.align[caption_list[0]] = "c"
                    return table
                table: PrettyTable = create_table(caption_list)
                if modify_table_handler is not None:
                    modify_table_handler(table, caption_list)
                for index, item in enumerate(data):
                    row_data: List = []
                    for field_item_obj in field_list.get_list():
                        field_item: FieldItem = field_item_obj
                        if field_item.visible:
                            if field_item.name == FIELD_COLLECTION.INDEX.name:
                                row_data.append(str(index + 1))
                            elif not isinstance(item, dict):
                                if modify_data_handler is not None:
                                    modify_item_data = modify_data_handler(
                                        field_item, item)
                                    if modify_item_data is None:
                                        modify_item_data = getattr(
                                            item, field_item.name)
                                    row_data.append(DataTool.check(
                                        modify_item_data, lambda: modify_item_data, "") if modify_item_data is None else modify_item_data)
                                else:
                                    item_data = getattr(item, field_item.name)
                                    row_data.append(DataTool.check(
                                        item_data, lambda: item_data, ""))
                            elif field_item.name in item:
                                item_data = item[field_item.name]
                                if modify_data_handler is not None:
                                    modify_item_data = modify_data_handler(
                                        field_item, item)
                                    row_data.append(
                                        item_data if modify_item_data is None else modify_item_data)
                                else:
                                    row_data.append(item_data)
                    table.add_row(row_data)
                print(table)
                table.clear()

        @staticmethod
        def template_users_for_result(data: dict, use_index: bool = False) -> None:
            def data_handler(field_item: FieldItem, item: User) -> Any:
                filed_name = field_item.name
                if filed_name == FIELD_NAME_COLLECTION.DESCRIPTION:
                    return item.description
                return None
            PIH.VISUAL.table_with_caption(
                data, "Шаблоны для создания аккаунта пользователя:", use_index, None, data_handler)

    class ACTION:

        class MESSAGE:

            class DELAYED:
    
                @staticmethod
                def update(value: DelayedMessageVO, search_critery: BufferedMessageSearchCritery) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.update_buffered_message, (value, search_critery)))

                @staticmethod
                def update_status(value: DelayedMessageVO, status: MessageStatus) -> bool:
                    return PIH.ACTION.MESSAGE.DELAYED.update(DelayedMessageVO(status=status.value), BufferedMessageSearchCritery(id=value.id))

                @staticmethod
                def complete(value: DelayedMessageVO) -> bool:
                    return PIH.ACTION.MESSAGE.DELAYED.update_status(value, MessageStatus.COMPLETE)

                @staticmethod
                def abort(value: DelayedMessageVO) -> bool:
                    return PIH.ACTION.MESSAGE.DELAYED.update_status(value, MessageStatus.ABORT)

                @staticmethod
                def register(message: DelayedMessage) -> int:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.register_buffered_message, PIH.ACTION.MESSAGE.DELAYED.prepeare_message(message)))

                @staticmethod
                def send(message: DelayedMessage) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.send_buffered_message, PIH.ACTION.MESSAGE.DELAYED.prepeare_message(message)))

                @staticmethod
                def prepeare_message(message: DelayedMessage) -> DelayedMessage:
                    if message.type is None:
                        message.type = MessageTypes.WHATSAPP.value
                    if message.date is not None:
                        if isinstance(message.date, datetime):
                            message.date = DateTimeTool.to_string(message.date, CONST.DATA_STORAGE.DATE_TIME_FORMAT)
                    message.status = 0
                    return message


        class SETTINGS:

            @staticmethod
            def key(key: str, value: Any) -> bool:
                return DataTool.rpc_unrepresent(
                    RPC.call(ServiceCommands.set_settings_value, (key, value)))

            @staticmethod
            def set(settings_item: Settings, value: Any) -> bool:
                return PIH.ACTION.SETTINGS.key(settings_item.value.key_name or settings_item.name, value)

            @staticmethod
            def set_default(settings_item: Settings) -> bool:
                return PIH.ACTION.SETTINGS.set(settings_item, settings_item.value.default_value)

        class USER:

            @staticmethod
            def create_from_template(container_dn: str,
                                     full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_user_by_template, (container_dn, full_name, login, password, description, telephone, email)))

            @staticmethod
            def create_in_container(container_dn: str,
                                    full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_user_in_container, (container_dn, full_name, login, password, description, telephone, email)))

            @staticmethod
            def set_telephone(user: User, telephone: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_user_telephone, (user.distinguishedName, telephone)))

            @staticmethod
            def set_password(user: User, password: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_user_password, (user.distinguishedName, password)))

            @staticmethod
            def set_status(user: User, status: str, container: UserContainer) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_user_status, (user.distinguishedName, status, DataTool.check(container, lambda: container.distinguishedName))))

            @staticmethod
            def remove(user: User) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.remove_user, user.distinguishedName))

        class TIME_TRACKING:

            @staticmethod
            def report(path: str, start_date: datetime, end_date: datetime, tab_number: str = None) -> bool:
                now: datetime = datetime.now()
                start_date = now.replace(
                    hour=0, minute=0, day=start_date.day, second=0, month=start_date.month, year=start_date.year)
                end_date = now.replace(hour=23, minute=59, second=0, day=end_date.day,
                                       month=end_date.month, year=end_date.year)
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_time_tracking_report, (path, start_date, end_date, tab_number)))

        class INVENTORY:

            @staticmethod
            def create_barcodes(report_file_path: str, result_directory: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_barcodes_for_inventory, (report_file_path, result_directory)))

            @staticmethod
            def save_report_item(report_file_path: str, item: InventoryReportItem) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.save_report_item, (report_file_path, item)))

            @staticmethod
            def close_report(report_file_path: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.close_inventory_report, report_file_path))

        class PRINTER:

            @staticmethod
            def report() -> bool:
                return not ResultTool.data_is_empty(PIH.RESULT.PRINTER.report())

            @staticmethod
            def status() -> bool:
                return not ResultTool.data_is_empty(PIH.RESULT.PRINTER.status())

        class POLIBASE:

            class NOTIFICATION:

                @staticmethod
                def register(value: PolibasePersonVisitNotificationVO) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.register_polibase_person_visit_notification, value))

                @staticmethod
                def add(person: PolibasePerson) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_notifier_polibase_person, (person.pin, person.FullName, person.telephoneNumber, PolibasePersonNotifierStatus.START.value)))

                @staticmethod
                def set_status(pin: int, status: PolibasePersonNotifierStatus) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_notifier_polibase_person_status_by_pin, (pin, status.value)))


            @staticmethod
            def create_barcode_for_person(pid: int, test: bool = None) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_barcode_for_polibase_person, (pid, test)))

            @staticmethod
            def set_chart_folder_for_person(name: str, pid: int, test: bool = None) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_polibase_person_chart_folder, (name, pid, test)))

            @staticmethod
            def create_barcode_for_person_chart_folder(value: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_barcode_for_polibase_person_chart_folder, (value, value)))

            @staticmethod
            def set_email(value: str, pin: int, test: bool = None) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_polibase_person_email, (value, pin, test)))

            @staticmethod
            def set_person_barcode_by_pin(barcode_file_name: str, pin: int, test: bool = None) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_polibase_person_barcode_by_pin, (barcode_file_name, pin, test)))

            class DB:

                @staticmethod
                def backup(file_name: str = None, debug: bool = None) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_polibase_database_backup, (file_name, debug)))

            class VISIT:

                @staticmethod
                def register(value: PolibasePersonVisit = None) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.register_polibase_person_visit, value))

            class REVIEW_QUEST:

                def clear() -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.clear_polibase_persons_review_quest))

                @staticmethod
                def begin(pin: int) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.begin_polibase_person_review_quest, pin))

                @staticmethod
                def complete(pin: int) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.complete_polibase_person_review_quest, pin))

                @staticmethod
                def set_step(pin: int, step: PolibasePersonReviewQuestStep) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_polibase_person_review_quest_step, (pin, step.value)))

                @staticmethod
                def confirm_step(pin: int) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.confirm_polibase_person_review_quest_step, pin))

                @staticmethod
                def set_grade(pin: int, value: int) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_polibase_person_review_quest_grade, (pin, value)))

                @staticmethod
                def set_information_way(pin: int, value: int):
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_polibase_person_review_quest_information_way, (pin, value)))

                @staticmethod
                def set_message(pin: int, value: str) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_polibase_person_review_quest_message, (pin, value)))

                @staticmethod
                def set_feedback_call_status(pin: int, value: int) -> bool:
                    return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_polibase_person_review_quest_feedback_call_status, (pin, value == 1)))

        class MARK:

            @staticmethod
            def create(full_name: FullName, person_division_id: int,  tab_number: str, telephone: str = None) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_mark, (full_name, person_division_id, tab_number, telephone)))

            @staticmethod
            def set_full_name_by_tab_number(full_name: FullName, tab_number: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_full_name_by_tab_number, (full_name, tab_number)))

            @staticmethod
            def set_telephone_by_tab_number(telephone: str, tab_number: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.set_telephone_by_tab_number, (telephone, tab_number)))

            @staticmethod
            def make_as_free_by_tab_number(tab_number: str) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.make_mark_as_free_by_tab_number, tab_number))

            @staticmethod
            def make_as_temporary(temporary_mark: Mark, owner_mark: Mark) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.make_mark_as_temporary, (temporary_mark.TabNumber, owner_mark.TabNumber)))

            @staticmethod
            def remove(mark: Mark) -> bool:
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.remove_mark_by_tab_number, mark.TabNumber))

        class DOCUMENTS:

            @staticmethod
            def create_for_user(path: str, full_name: FullName, tab_number: str, pc: LoginPasswordPair, polibase: LoginPasswordPair, email: LoginPasswordPair) -> bool:
                locale.setlocale(locale.LC_ALL, 'ru_RU')
                date_now = datetime.now().date()
                date_now_string = f"{date_now.day} {calendar.month_name[date_now.month]} {date_now.year}"
                return DataTool.rpc_unrepresent(RPC.call(ServiceCommands.create_user_document, (path, date_now_string, CONST.SITE_ADDRESS, CONST.SITE_PROTOCOL + CONST.SITE_ADDRESS, CONST.EMAIL_ADDRESS, full_name, tab_number, pc, polibase, email)))

        @staticmethod
        def generate_login(full_name: FullName, ask_for_remove_inactive_user_if_login_is_exists: bool = True, ask_for_use: bool = True) -> str:
            login_list: List[str] = []
            inactive_user_list: List[User] = []
            login_is_exists: bool = False

            def show_user_which_login_is_exists_and_return_user_if_it_inactive(login_string: str) -> User:
                user: User = PIH.RESULT.USER.by_login(login_string).data
                is_active: bool = PIH.CHECK.USER.is_acive(user)
                PR.bad(
                    f"Логин '{login_string}' занят {'активным' if is_active else 'неактивным'} пользователем: {user.name}")
                PR.new_line()
                return user if not is_active else None
            login: FullName = NamePolicy.convert_to_login(full_name)
            login_string: str = FullNameTool.to_string(login, "")
            login_list.append(login_string)
            need_enter_login: bool = False

            def remove_inactive_user_action():
                login_string: str = None
                need_enter_login: bool = False
                if PIH.INPUT.yes_no("Удалить неактивных пользователей, чтобы освободить логин?", True):
                    user_for_remove: User = PIH.INPUT.item_by_index(
                        "Выберите пользователя для удаления, выбрав индекс", inactive_user_list, lambda item, _: f"{item.name} ({item.samAccountName})")
                    PR.new_line()
                    PR.value(f"Пользователь для удаления",
                             user_for_remove.name)
                    if PIH.INPUT.yes_no("Удалить неактивного пользователя?", True):
                        if PIH.ACTION.USER.remove(user_for_remove):
                            PR.good("Удален")
                            login_string = user_for_remove.samAccountName
                            inactive_user_list.remove(user_for_remove)
                        else:
                            PR.bad("Ошибка")
                    else:
                        need_enter_login = True
                else:
                    need_enter_login = True
                return need_enter_login, login_string
            if PIH.CHECK.USER.is_exists_by_login(login_string):
                user: User = show_user_which_login_is_exists_and_return_user_if_it_inactive(
                    login_string)
                if user is not None:
                    inactive_user_list.append(user)
                login_alt: FullName = NamePolicy.convert_to_alternative_login(
                    login)
                login_string = FullNameTool.to_string(login_alt, "")
                login_is_exists = login_string in login_list
                if not login_is_exists:
                    login_list.append(login_string)
                if login_is_exists or PIH.CHECK.USER.is_exists_by_login(login_string):
                    if not login_is_exists:
                        user = show_user_which_login_is_exists_and_return_user_if_it_inactive(
                            login_string)
                        if user is not None:
                            inactive_user_list.append(user)
                    login_reversed: FullName = NamePolicy.convert_to_reverse_login(
                        login)
                    login_is_exists = login_string in login_list
                    login_string = FullNameTool.to_string(login_reversed, "")
                    if not login_is_exists:
                        login_list.append(login_string)
                    if login_is_exists or PIH.CHECK.USER.is_exists_by_login(login_string):
                        if not login_is_exists:
                            user = show_user_which_login_is_exists_and_return_user_if_it_inactive(
                                login_string)
                            if user is not None:
                                inactive_user_list.append(user)
                        if ask_for_remove_inactive_user_if_login_is_exists and len(inactive_user_list) > 0:
                            need_enter_login, login_string = remove_inactive_user_action()
                        if need_enter_login:
                            while True:
                                login_string = PIH.INPUT.login()
                                if PIH.CHECK.USER.is_exists_by_login(login_string):
                                    show_user_which_login_is_exists_and_return_user_if_it_inactive(
                                        login_string)
                                else:
                                    break
            if not need_enter_login and ask_for_remove_inactive_user_if_login_is_exists and len(inactive_user_list) > 0:
                need_enter_login, login_string = remove_inactive_user_action()
                if need_enter_login:
                    return PIH.ACTION.generate_login(full_name, False)
            else:
                if ask_for_use and not PIH.INPUT.yes_no(f"Использовать логин '{login_string}' для аккаунта пользователя?", True):
                    login_string = PIH.INPUT.login(True)

            return login_string

        @staticmethod
        def generate_password(once: bool = False, settings: PasswordSettings = PASSWORD.SETTINGS.DEFAULT) -> str:
            def generate_password_interanal(settings: PasswordSettings = None) -> str:
                return PasswordTools.generate_random_password(settings.length, settings.special_characters,
                                                              settings.order_list, settings.special_characters_count,
                                                              settings.alphabets_lowercase_count, settings.alphabets_uppercase_count,
                                                              settings.digits_count, settings.shuffled)
            while True:
                password = generate_password_interanal(settings)
                if once or PIH.INPUT.yes_no(f"Использовать пароль {password} ?", True):
                    return password
                else:
                    pass

        @staticmethod
        def generate_email(login: str) -> str:
            return "@".join((login, CONST.SITE_ADDRESS))

        @staticmethod
        def generate_user_principal_name(login: str) -> str:
            return "@".join((login, CONST.AD.DOMAIN_MAIN))


class PR:

    TEXT_BEFORE: str = ""
    TEXT_AFTER: str = ""

    INDEX: str = "  "
    INDEX_COUNT: int = 0

    @staticmethod
    def indent(count: int = 1):
        PR.INDEX_COUNT = count
        PR.TEXT_BEFORE = PR.INDEX*count

    @staticmethod
    def reset_indent():
        PR.TEXT_BEFORE = ""

    @staticmethod
    def restore_indent():
        PR.indent(PR.INDEX_COUNT)

    @staticmethod
    def init() -> None:
        colorama.init()

    @staticmethod
    def text_color(color: int, text: str) -> str:
        return f"{color}{text}{Fore.RESET}"

    @staticmethod
    def text_black(string: str) -> str:
        return PR.text_color(Fore.BLACK, string)

    @staticmethod
    def color_str(color: int, string: str, text_before: str = None, text_after: str = None) -> str:
        string = f" {string} "
        text_before = text_before if text_before is not None else PR.TEXT_BEFORE
        text_after = text_after if text_after is not None else PR.TEXT_AFTER
        return f"{text_before}{color}{string}{Back.RESET}{text_after}"

    @staticmethod
    def color(color: int, string: str, text_before: str = None, text_after: str = None) -> None:
        PR.write_line(PR.color_str(color, string, text_before, text_after))

    @staticmethod
    def write_line(string: str) -> None:
        print(string)

    @staticmethod
    def index(index: int, string: str, max_index: int = None) -> None:
        indent: str = ""
        if max_index is not None:
            indent = " " * (len(str(max_index)) - len(str(index)))
        PR.write_line(f"{index}. {indent}{string}")

    @staticmethod
    def input(caption: str) -> None:
        PR.write_line(PR.input_str(caption, PR.TEXT_BEFORE, text_after=":"))

    @staticmethod
    def input_str(caption: str, text_before: str = None, text_after: str = None) -> str:
        return PR.white_str(f"{Fore.BLACK}{caption}{Fore.RESET}", text_before, text_after)

    @staticmethod
    def value(caption: str, value: str, text_before: str = None) -> None:
        text_before = text_before or PR.TEXT_BEFORE
        PR.cyan(caption, text_before, f": {value}")

    @staticmethod
    def get_action_value(caption: str, value: str, show: bool = True) -> ActionValue:
        if show:
            PR.value(caption, value)
        return ActionValue(caption, value)

    @staticmethod
    def head(caption: str) -> None:
        PR.cyan(caption)

    @staticmethod
    def head1(caption: str) -> None:
        PR.magenta(caption)

    @staticmethod
    def head2(caption: str) -> None:
        PR.yellow(PR.text_color(Fore.BLACK, caption))

    @staticmethod
    def new_line() -> None:
        print()

    @staticmethod
    def bad_str(caption: str) -> str:
        return PR.red_str(caption)

    @staticmethod
    def bad(caption: str) -> str:
        PR.write_line(PR.bad_str(caption))

    @staticmethod
    def notify_str(caption: str) -> str:
        return PR.yellow_str(caption)

    @staticmethod
    def notify(caption: str) -> str:
        PR.write_line(PR.notify_str(caption))

    @staticmethod
    def good_str(caption: str) -> str:
        return PR.green_str(caption)

    @staticmethod
    def good(caption: str) -> str:
        PR.write_line(PR.good_str(PR.text_black(caption)))

    @staticmethod
    def green_str(string: str, text_before: str = None, text_after: str = None) -> str:
        return PR.color_str(Back.GREEN, string, text_before, text_after)

    @staticmethod
    def green(string: str, text_before: str = None, text_after: str = None) -> None:
        PR.write_line(PR.green_str(string, text_before, text_after))

    @staticmethod
    def yellow_str(string: str, text_before: str = None, text_after: str = None) -> str:
        return PR.color_str(Back.YELLOW, string, text_before, text_after)

    @staticmethod
    def yellow(string: str, text_before: str = None, text_after: str = None) -> None:
        text_before = text_before or PR.TEXT_BEFORE
        text_after = text_after or PR.TEXT_AFTER
        PR.write_line(PR.yellow_str(string, text_before, text_after))

    @staticmethod
    def black_str(string: str, text_before: str = None, text_after: str = None) -> str:
        return PR.color_str(Back.BLACK, string, text_before, text_after)

    @staticmethod
    def black(string: str, text_before: str = None, text_after: str = None) -> None:
        PR.write_line(PR.black_str(string, text_before, text_after))

    @staticmethod
    def white_str(string: str, text_before: str = None, text_after: str = None) -> str:
        return PR.color_str(Back.WHITE, string, text_before, text_after)

    @staticmethod
    def white(string: str, text_before: str = None, text_after: str = None) -> None:
        PR.write_line(PR.white_str(string, text_before, text_after))

    @staticmethod
    def draw_line(color: str = Back.LIGHTBLUE_EX, char: str = " ", width: int = 80) -> None:
        PR.write_line("") if color is None else PR.color(color, char*width)

    @staticmethod
    def line() -> None:
        PR.new_line()
        PR.draw_line(Back.WHITE, PR.text_color(Fore.BLACK, "_"), width=128)
        PR.new_line()

    @staticmethod
    def magenta_str(string: str, text_before: str = None, text_after: str = None) -> str:
        return PR.color_str(Back.LIGHTMAGENTA_EX, string, text_before, text_after)

    @staticmethod
    def magenta(string: str, text_before: str = None, text_after: str = None) -> None:
        PR.write_line(PR.magenta_str(string, text_before, text_after))

    @staticmethod
    def cyan(string: str, text_before: str = None, text_after: str = None) -> None:
        PR.write_line(PR.cyan_str(string, text_before, text_after))

    @staticmethod
    def cyan_str(string: str, text_before: str = None, text_after: str = None) -> str:
        return PR.color_str(Back.CYAN, string, text_before, text_after)

    @staticmethod
    def red(string: str, text_before: str = None, text_after: str = None) -> None:
        PR.write_line(PR.red_str(string, text_before, text_after))

    @staticmethod
    def red_str(string: str, text_before: str = None, text_after: str = None) -> str:
        return PR.color_str(Back.LIGHTRED_EX, string, text_before, text_after)

    @staticmethod
    def blue(string: str, text_before: str = None, text_after: str = None) -> None:
        PR.write_line(PR.blue_str(string, text_before, text_after))

    @staticmethod
    def blue_str(string: str, text_before: str = None, text_after: str = None) -> str:
        return PR.color_str(Back.BLUE, string, text_before, text_after)

    @staticmethod
    def bright(string: str, text_before: str = None, text_after: str = None) -> None:
        PR.write_line(PR.bright_str(string, text_before, text_after))

    @staticmethod
    def bright_str(string: str, text_before: str = None, text_after: str = None) -> str:
        return PR.color_str(Style.BRIGHT, string, text_before, text_after)

    @staticmethod
    def get_number(value: int) -> str:
        return CONST.VISUAL.NUMBER_SYMBOLS[value - 1]


class ActionStack(List):

    def __init__(self, caption: str = "", *argv):
        self.acion_value_list: List[ActionValue] = []
        self.captiin = caption
        for arg in argv:
            self.append(arg)
        self.start()

    def call_actions_by_index(self, index: int = 0, change: bool = False):
        previous_change: bool = False
        while True:
            try:
                action_value: ActionValue = self[index]()
                if action_value:
                    if change or previous_change:
                        previous_change = False
                        if index in self.acion_value_list:
                            self.acion_value_list[index] = action_value
                        else:
                            self.acion_value_list.append(action_value)
                    else:
                        self.acion_value_list.append(action_value)
                index = index + 1
                if index == len(self) or change:
                    break
            except KeyboardInterrupt:
                PR.new_line()
                PR.bad("Повтор предыдущих действия")
                PR.new_line()
                if index > 0:
                    previous_change = True
                    # self.show_action_values()
                    #index = index - 1
                else:
                    continue

    def show_action_values(self) -> None:
        def label(item: ActionValue, _):
            return item.caption
        self.call_actions_by_index(PIH.INPUT.index(
            "Выберите свойство для изменения, введя индекс", self.acion_value_list, label), True)

    def start(self):
        self.call_actions_by_index()
        while True:
            PR.new_line()
            PR.head2(self.captiin)
            for action_value in self.acion_value_list:
                PR.value(action_value.caption, action_value.value)
            if PIH.INPUT.yes_no("Данные верны?", True):
                break
            else:
                self.show_action_values()

class A:

    R = PIH.RESULT
    D = PIH.DATA
    A = PIH.ACTION 
    M = PIH.MESSAGE
    RM = R.MESSAGE
    AM = A.MESSAGE 
    RMD = RM.DELAYED
    AMD = AM.DELAYED
    MI = M.INTERNAL
    MC = M.COMMAND
    MW = M.WHATSAPP
    S = PIH.SETTINGS
    C = PIH.CHECK
    AP = A.POLIBASE
    CP = C.POLIBASE 
    DP = D.POLIBASE
    RP = R.POLIBASE 
    APV = AP.VISIT
    RPV = RP.VISIT
    APN = AP.NOTIFICATION
    RPN = RP.NOTIFICATION
    CPN = CP.NOTIFICATION
    
