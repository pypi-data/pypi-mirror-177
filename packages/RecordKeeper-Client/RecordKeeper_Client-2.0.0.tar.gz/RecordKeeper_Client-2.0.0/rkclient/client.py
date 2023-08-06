import time
import logging
import datetime
from uuid import UUID, uuid1
from typing import Dict, Any, Optional, Tuple, Callable
from importlib.metadata import version

from rkclient.auth import RK_USER_AUTH_HEADER, RK_PUC_AUTH_HEADER
from rkclient.entities import PEM, Artifact
from rkclient.request import RequestHelper
from rkclient.serialization import PEMSerialization, _encode_as_base64

log = logging.getLogger("rkclient")
RK_VERSION = version('RecordKeeper_Client')


def add_pem_context(files: Dict[str, Any], pem: PEM):
    """
    Helper function to be used when adding RK context to request
    :param files: a dictionary which belongs to Python Requests object
    :return:
    """
    files['rk_context'] = pem.ID.hex


def get_pem_from_request(request) -> Optional[UUID]:
    """
    Helper function to be used when retrieving RK context
    :param request: Flask-request object
    :return:
    """
    rk_context = request.files.get('rk_context', None)
    if rk_context is None:
        return None
    pem_id: str = rk_context.stream.read().decode("UTF8")
    return UUID(hex=pem_id)


class RKClient:
    """
        All network functions return tuple [str, bool]
        If bool is False, str contains error description

        Errors are also logged to rkclient logger
    """

    def __init__(self, receiver_url: str,
                 emitter_id: Optional[UUID] = None,
                 timeout_sec: int = 5,
                 insecure: bool = True,
                 user_auth: str = '',
                 puc_auth: str = ''):
        """

        :param receiver_url:
        :param emitter_id:
        :param timeout_sec:
        :param insecure: set it to True when operating with server that has test SSL certificates
        """

        receiver_url = receiver_url.rstrip('/')
        self.receiver_request = RequestHelper(receiver_url, timeout_sec, insecure, user_auth, puc_auth)
        log.info(f"ver {RK_VERSION}, connecting to: {receiver_url}")

        if emitter_id is None:
            emitter_id = uuid1()
        self.emitter_id = emitter_id

        if user_auth:
            log.info(f"Authorizing with {RK_USER_AUTH_HEADER} header")
        elif puc_auth:
            log.info(f"Authorizing with {RK_PUC_AUTH_HEADER} header")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @staticmethod
    def get_version() -> str:
        """
        :return: Version of RKClient
        """
        return RK_VERSION

    def prepare_pem(self,
                    pem_type: str,
                    predecessor_id: Optional[UUID] = None,
                    properties: Optional[Dict] = None,
                    tag_name: str = 'latest',
                    tag_namespace: Optional[UUID] = None) -> PEM:
        """
        In memory creation of PEM
        :param pem_type: user defined type of event
        :param predecessor_id: pass None if this event doesn't have a predecessor
        :param properties:
        :param tag_name:
        :param tag_namespace:
        :return: new PEM
        """
        uid = uuid1()
        now = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        pem = PEM(uid, pem_type, predecessor_id, self.emitter_id, now)
        if properties is not None:
            pem.Properties = properties
        pem.Tag = tag_name
        if tag_namespace is None:
            pem.TagNamespace = self.emitter_id.hex
        else:
            pem.TagNamespace = tag_namespace.hex
        return pem

    def prepare_artifact(self,
                         artifact_type: str,
                         properties: Dict[str, str],
                         uid: Optional[UUID] = None) -> Artifact:
        """
        In memory creation of Artifact. It needs to be passed to PEM.add_uses/produces_artifact()
        :param artifact_type:
        :param properties:
        :param uid:
        :return: new Artifact
        """
        if uid is None:
            uid = uuid1()
        art = Artifact(uid, artifact_type, properties)
        return art

    def send_pem(self, pem: PEM) -> Tuple[str, bool]:
        """
        Sends PEM to Record Keeper.
        :return: check class description
        """
        def _send_pem():
            payload: str = PEMSerialization.to_json(pem)
            log.debug(f"sending PEM: {payload}")
            return self.receiver_request.post("/pem", payload)

        return _handle_request(_send_pem, "Sending PEM")

    def ping(self) -> Tuple[str, bool]:
        """
        :return: check class description
        """
        def _ping():
            return self.receiver_request.get("/ping")

        return _handle_request(_ping, "Pinging")

    def get_info(self) -> Tuple[str, bool]:
        """
        Returns json with 'postgres_enabled' and 'neo4j_enabled' bools, and 'version' with string semver
        :return: check class description
        TODO: return object instead of str
        """
        def _get_info():
            return self.receiver_request.get("/info", )

        return _handle_request(_get_info, "Getting info", True)

    def get_tag(self, namespace: UUID, tag_name: str) -> Tuple[str, bool]:
        """
        Returned tag is UUID in hex (do: UUID(hex=result))
        :return: check class description
        """
        def _get_tag():
            tag_base64 = _encode_as_base64(tag_name)
            return self.receiver_request.get(f"/tag/{namespace.hex}/{tag_base64}")

        return _handle_request(_get_tag, "Getting tag", True)

    def set_tag(self, namespace: UUID, tag_name: str, pem: PEM) -> Tuple[str, bool]:
        """
        Sets tag_name on pem.ID, within namespace
        :param tag_name: can contain space, / and other characters, but recommended charset: is A-Za-z0-9_-
        :param namespace:
        :param pem:
        :return: check class description
        """
        def _set_tag():
            tag_base64 = _encode_as_base64(tag_name)
            return self.receiver_request.post(f"/tag/{namespace.hex}/{tag_base64}/{pem.ID.hex}", tag_base64)

        return _handle_request(_set_tag, "Setting tag")


def _handle_request(func: Callable, name: str, ret_text_on_ok: bool = False) -> Tuple[str, bool]:
    """
    Wraps the error, logging and exception handling.
    """
    text, ok = func()
    if not ok:
        msg = f"{name} failed: {text}"
        log.error(msg)
        return msg, False
    if ret_text_on_ok:
        return text, True
    else:
        return 'OK', True

