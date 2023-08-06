from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.log_export_group import LogExportGroup
from ..models.log_export_type import LogExportType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CockroachCloudEnableLogExportEnableLogExportRequest")


@attr.s(auto_attribs=True)
class CockroachCloudEnableLogExportEnableLogExportRequest:
    """
    Attributes:
        auth_principal (Union[Unset, str]): auth_principal is either the AWS Role ARN that identifies a role
            that the cluster account can assume to write to CloudWatch or the
            GCP Project ID that the cluster service account has permissions to
            write to for cloud logging.
        groups (Union[Unset, List[LogExportGroup]]): groups is a collection of log group configurations that allows the
            customer to define collections of CRDB log channels that are aggregated
            separately at the target sink.
        log_name (Union[Unset, str]): log_name is an identifier for the logs in the customer's log sink.
        redact (Union[Unset, bool]): redact allows the customer to set a default redaction policy for
            logs before they are exported to the target sink. If a group config
            omits a redact flag and this one is set to `true`, then that group
            will receive redacted logs.
        region (Union[Unset, str]): region allows the customer to override the destination region for
            all logs for a cluster.
        type (Union[Unset, LogExportType]): LogExportType encodes the cloud selection that we're exporting to
            along with the cloud logging platform.

            Currently, each cloud has a single logging platform.
    """

    auth_principal: Union[Unset, str] = UNSET
    groups: Union[Unset, List[LogExportGroup]] = UNSET
    log_name: Union[Unset, str] = UNSET
    redact: Union[Unset, bool] = UNSET
    region: Union[Unset, str] = UNSET
    type: Union[Unset, LogExportType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auth_principal = self.auth_principal
        groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()

                groups.append(groups_item)

        log_name = self.log_name
        redact = self.redact
        region = self.region
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auth_principal is not UNSET:
            field_dict["auth_principal"] = auth_principal
        if groups is not UNSET:
            field_dict["groups"] = groups
        if log_name is not UNSET:
            field_dict["log_name"] = log_name
        if redact is not UNSET:
            field_dict["redact"] = redact
        if region is not UNSET:
            field_dict["region"] = region
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        auth_principal = d.pop("auth_principal", UNSET)

        groups = []
        _groups = d.pop("groups", UNSET)
        for groups_item_data in _groups or []:
            groups_item = LogExportGroup.from_dict(groups_item_data)

            groups.append(groups_item)

        log_name = d.pop("log_name", UNSET)

        redact = d.pop("redact", UNSET)

        region = d.pop("region", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, LogExportType]
        if _type is None:
            type = None
        elif isinstance(_type, Unset):
            type = UNSET
        else:
            type = LogExportType(_type)

        cockroach_cloud_enable_log_export_enable_log_export_request = cls(
            auth_principal=auth_principal,
            groups=groups,
            log_name=log_name,
            redact=redact,
            region=region,
            type=type,
        )

        cockroach_cloud_enable_log_export_enable_log_export_request.additional_properties = d
        return cockroach_cloud_enable_log_export_enable_log_export_request

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
