from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(session: AsyncSession):
    donat = 0
    project = 0

    money = await session.execute(
        select(Donation).where(~Donation.fully_invested))
    money = money.scalars().all()

    prjcts = await session.execute(
        select(CharityProject).where(~CharityProject.fully_invested))
    prjcts = prjcts.scalars().all()

    while donat < len(money) and project < len(prjcts):
        balance = money[donat].full_amount - money[donat].invested_amount
        pr_bl = prjcts[project].full_amount - prjcts[project].invested_amount
        free_for_investing = min(balance, pr_bl)
        money[donat].invested_amount += free_for_investing
        prjcts[project].invested_amount += free_for_investing

        if money[donat].full_amount == money[donat].invested_amount:
            setattr(money[donat], 'fully_invested', True)
            setattr(money[donat], 'close_date', datetime.now())
            donat += 1

        if prjcts[project].full_amount == prjcts[project].invested_amount:
            setattr(prjcts[project], 'fully_invested', True)
            setattr(prjcts[project], 'close_date', datetime.now())
            project += 1

    session.add_all(money + prjcts)
    await session.commit()
