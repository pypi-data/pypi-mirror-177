from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.list_apps_response_200_item_execution_mode import ListAppsResponse200ItemExecutionMode
from ..models.list_apps_response_200_item_extra_perms import ListAppsResponse200ItemExtraPerms
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAppsResponse200Item")


@attr.s(auto_attribs=True)
class ListAppsResponse200Item:
    """
    Attributes:
        id (Union[Unset, int]):
        workspace_id (Union[Unset, str]):
        path (Union[Unset, str]):
        summary (Union[Unset, str]):
        version (Union[Unset, int]):
        extra_perms (Union[Unset, ListAppsResponse200ItemExtraPerms]):
        execution_mode (Union[Unset, ListAppsResponse200ItemExecutionMode]):
    """

    id: Union[Unset, int] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    summary: Union[Unset, str] = UNSET
    version: Union[Unset, int] = UNSET
    extra_perms: Union[Unset, ListAppsResponse200ItemExtraPerms] = UNSET
    execution_mode: Union[Unset, ListAppsResponse200ItemExecutionMode] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        workspace_id = self.workspace_id
        path = self.path
        summary = self.summary
        version = self.version
        extra_perms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_perms, Unset):
            extra_perms = self.extra_perms.to_dict()

        execution_mode: Union[Unset, str] = UNSET
        if not isinstance(self.execution_mode, Unset):
            execution_mode = self.execution_mode.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if path is not UNSET:
            field_dict["path"] = path
        if summary is not UNSET:
            field_dict["summary"] = summary
        if version is not UNSET:
            field_dict["version"] = version
        if extra_perms is not UNSET:
            field_dict["extra_perms"] = extra_perms
        if execution_mode is not UNSET:
            field_dict["execution_mode"] = execution_mode

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        path = d.pop("path", UNSET)

        summary = d.pop("summary", UNSET)

        version = d.pop("version", UNSET)

        _extra_perms = d.pop("extra_perms", UNSET)
        extra_perms: Union[Unset, ListAppsResponse200ItemExtraPerms]
        if isinstance(_extra_perms, Unset):
            extra_perms = UNSET
        else:
            extra_perms = ListAppsResponse200ItemExtraPerms.from_dict(_extra_perms)

        _execution_mode = d.pop("execution_mode", UNSET)
        execution_mode: Union[Unset, ListAppsResponse200ItemExecutionMode]
        if isinstance(_execution_mode, Unset):
            execution_mode = UNSET
        else:
            execution_mode = ListAppsResponse200ItemExecutionMode(_execution_mode)

        list_apps_response_200_item = cls(
            id=id,
            workspace_id=workspace_id,
            path=path,
            summary=summary,
            version=version,
            extra_perms=extra_perms,
            execution_mode=execution_mode,
        )

        list_apps_response_200_item.additional_properties = d
        return list_apps_response_200_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
