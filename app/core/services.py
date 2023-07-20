from datetime import datetime
from typing import List, Union

from app.crud.charity_project import CRUDCharityProject
from app.models.charity_project import CharityProject
from app.models.donation import Donation


def close_invested_object(
    obj_to_close: Union[CharityProject, Donation],
) -> None:
    obj_to_close.fully_invested = True
    obj_to_close.close_date = datetime.now()


def investment(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]]
):
    if sources:
        for not_invested_obj in sources:
            need_to_invest = not_invested_obj.full_amount - not_invested_obj.invested_amount

            to_invest = (
                need_to_invest if need_to_invest < target.full_amount else target.full_amount
            )

            not_invested_obj.invested_amount += to_invest
            target.invested_amount += to_invest
            target.full_amount -= to_invest

            if not_invested_obj.full_amount == not_invested_obj.invested_amount:
                close_invested_object(not_invested_obj)

            if not target.full_amount:
                close_invested_object(target)
                break
            CRUDCharityProject.save()
    return target
