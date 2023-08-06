from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.day_data_by_hour_transfer import DayDataByHourTransfer
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDayPeriodRequest")


@attr.s(auto_attribs=True)
class UpdateDayPeriodRequest:
    """
    Attributes:
        execution_id (Union[Unset, None, str]):
        day_data (Union[Unset, None, DayDataByHourTransfer]):
        unit (Union[Unset, None, str]):
    """

    execution_id: Union[Unset, None, str] = UNSET
    day_data: Union[Unset, None, DayDataByHourTransfer] = UNSET
    unit: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        execution_id = self.execution_id
        day_data: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.day_data, Unset):
            day_data = self.day_data.to_dict() if self.day_data else None

        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if execution_id is not UNSET:
            field_dict["executionId"] = execution_id
        if day_data is not UNSET:
            field_dict["dayData"] = day_data
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        execution_id = d.pop("executionId", UNSET)

        _day_data = d.pop("dayData", UNSET)
        day_data: Union[Unset, None, DayDataByHourTransfer]
        if _day_data is None:
            day_data = None
        elif isinstance(_day_data, Unset):
            day_data = UNSET
        else:
            day_data = DayDataByHourTransfer.from_dict(_day_data)

        unit = d.pop("unit", UNSET)

        update_day_period_request = cls(
            execution_id=execution_id,
            day_data=day_data,
            unit=unit,
        )

        return update_day_period_request
