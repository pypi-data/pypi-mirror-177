from typing import Any, List

from torque.base import Resource, ResourceManager
from torque.constants import BLUEPRINT_SOURCE_TYPE_API_MAP


class Blueprint(Resource):
    def __init__(self, manager: ResourceManager, name: str, url: str, enabled: bool, source_type: str):
        super(Blueprint, self).__init__(manager)

        self.name = name
        self.url = url
        self.enabled = enabled
        self.source_type = source_type

    @classmethod
    def json_deserialize(cls, manager: ResourceManager, json_obj: dict):
        try:
            # spec2 check
            if "details" in json_obj:
                json_obj = json_obj["details"]
            bp = Blueprint(
                manager,
                json_obj.get("blueprint_name", None) or json_obj.get("name", None),
                json_obj.get("url", None),
                json_obj.get("enabled", True),
                json_obj.get("blueprint_source_type", ""),
            )
        except KeyError as e:
            raise NotImplementedError(f"unable to create object. Missing keys in Json. Details: {e}")

        # TODO(ddovbii): set all needed attributes
        bp.errors = json_obj.get("errors", [])
        bp.description = json_obj.get("description", "")
        return bp

    def json_serialize(self) -> dict:
        return {
            "name": self.name,
            "published": self.enabled,
            "source type": self.source_type,
        }

    def table_serialize(self) -> dict:
        return {
            "name": self.name,
            "published": self.enabled,
            "source type": self.source_type,
        }


class BlueprintsManager(ResourceManager):
    resource_obj = Blueprint

    def get(self, blueprint_name: str, source_type: str) -> Blueprint:
        bp_json = self._get_blueprint(blueprint_name, source_type)
        return Blueprint.json_deserialize(self, bp_json)

    def get_detailed(self, blueprint_name, source_type):
        return self._get_blueprint(blueprint_name, source_type)

    def _get_blueprint(self, blueprint_name, source_type):
        url = f"catalog/{blueprint_name}"
        query = None
        api_source_type = BLUEPRINT_SOURCE_TYPE_API_MAP.get(source_type, None)
        if api_source_type:
            query = {"blueprint_source_type": api_source_type}
        return self._get(url, query_params=query)

    def list(self) -> List[Blueprint]:
        url = "blueprints"
        result_json = self._list(path=url)
        return [self.resource_obj.json_deserialize(self, obj) for obj in result_json]

    def list_detailed(self) -> Any:
        url = "blueprints"
        result_json = self._list(path=url)
        return result_json

    def validate(self, b64_blueprint_content: str, blueprint: str = "") -> dict:
        url = "validations/blueprints"
        params = {"blueprint_name": blueprint, "blueprint_raw_64": b64_blueprint_content}
        result_json = self._post(url, params)
        return result_json
