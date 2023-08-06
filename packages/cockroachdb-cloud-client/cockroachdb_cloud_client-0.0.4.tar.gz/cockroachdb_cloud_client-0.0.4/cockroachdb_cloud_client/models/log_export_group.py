from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogExportGroup")


@attr.s(auto_attribs=True)
class LogExportGroup:
    """LogExportGroup contains an export configuration for a single
    log group which can route logs for a subset of CRDB channels.

        Attributes:
            channels (Union[Unset, List[str]]): channels is a list of CRDB log channels to include in this
                group.
            log_name (Union[Unset, str]):
            min_level (Union[Unset, str]): min_level is the minimum log level to filter to this log
                group. Should be one of INFO, WARNING, ERROR, FATAL.
            redact (Union[Unset, bool]): redact is a boolean that governs whether this log group
                should aggregate redacted logs. Redaction settings will
                inherit from the cluster log export defaults if unset.
    """

    channels: Union[Unset, List[str]] = UNSET
    log_name: Union[Unset, str] = UNSET
    min_level: Union[Unset, str] = UNSET
    redact: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.channels, Unset):
            channels = self.channels

        log_name = self.log_name
        min_level = self.min_level
        redact = self.redact

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if channels is not UNSET:
            field_dict["channels"] = channels
        if log_name is not UNSET:
            field_dict["log_name"] = log_name
        if min_level is not UNSET:
            field_dict["min_level"] = min_level
        if redact is not UNSET:
            field_dict["redact"] = redact

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channels = cast(List[str], d.pop("channels", UNSET))

        log_name = d.pop("log_name", UNSET)

        min_level = d.pop("min_level", UNSET)

        redact = d.pop("redact", UNSET)

        log_export_group = cls(
            channels=channels,
            log_name=log_name,
            min_level=min_level,
            redact=redact,
        )

        log_export_group.additional_properties = d
        return log_export_group

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
