from typing import List, Optional

from rhino_health.lib.endpoints.dataschema.dataschema_dataclass import Dataschema, FutureDataschema
from rhino_health.lib.endpoints.endpoint import Endpoint
from rhino_health.lib.utils import rhino_error_wrapper


class DataschemaEndpoints(Endpoint):
    """
    @autoapi False
    """

    @property
    def dataschema_data_class(self):
        """
        @autoapi False
        :return:
        """
        return Dataschema

    @rhino_error_wrapper
    def get_dataschemas(self, dataschema_uids: Optional[List[str]] = None) -> List[Dataschema]:
        """
        @autoapi True
        Gets the Dataschemas with the specified DATASCHEMA_UIDS

        .. warning:: This feature is under development and the interface may change
        """
        if not dataschema_uids:
            return self.session.get("/dataschemas/").to_dataclasses(self.dataschema_data_class)
        else:
            return [
                self.session.get(f"/dataschemas/{dataschema_uid}/").to_dataclass(
                    self.dataschema_data_class
                )
                for dataschema_uid in dataschema_uids
            ]


class DataschemaFutureEndpoints(DataschemaEndpoints):
    """
    @objname DataschameEndpoints
    """

    @property
    def dataschema_data_class(self):
        return FutureDataschema

    @rhino_error_wrapper
    def create_dataschema(self, dataschema):
        """
        @autoapi False

        .. warning:: This feature is under development and incomplete
        """
        return self.session.post("/dataschemas", dataschema.create_data)

    @rhino_error_wrapper
    def get_dataschema_csv(self, dataschema_uid: str):
        """
        @autoapi False

        .. warning:: This feature is under development and incomplete
        """
        return self.session.get(f"/dataschemas/{dataschema_uid}/export_to_csv")

    @rhino_error_wrapper
    def remove_dataschema(self, dataschema_uid: str):
        """
        Removes a Dataschema with the DATASCHAMA_UID from the system
        .. warning:: This feature is under development and incomplete
        """
        return self.session.post(f"/dataschemas/{dataschema_uid}/remove")
