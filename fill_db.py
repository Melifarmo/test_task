import asyncio
import random
from typing import List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.entities import BuildingModel
from app.db.entities.activity.activity import ActivityModel
from app.db.entities.organisation.organisation import OrganisationModel
from app.db.entities.organisation_phone.organisation_phone import OrganisationPhoneModel
from app.db.entities.organisation_activity.organisation_activity import (
    OrganisationActivityModel,
)
from app.db.sqlalchemy import db_session_factory


async def refresh_all(session: AsyncSession, entities: List[Any]) -> None:
    """
    Общее правило: для каждой добавленной сущности — refresh.
    """
    for entity in entities:
        await session.refresh(entity)


async def create_activities(session: AsyncSession) -> Dict[str, ActivityModel]:
    """
    Создаём дерево деятельностей, включая ветку глубиной 4 уровня:
    Еда -> Мясная продукция -> Колбасные изделия -> Сырокопчёные колбасы
    """
    # 1-й уровень (root)
    food = ActivityModel(title="Еда", parent_id=None)
    cars = ActivityModel(title="Автомобили", parent_id=None)

    # 2-й уровень
    meat = ActivityModel(title="Мясная продукция", parent_id=None)   # временно None
    milk = ActivityModel(title="Молочная продукция", parent_id=None)

    trucks = ActivityModel(title="Грузовые", parent_id=None)
    light = ActivityModel(title="Легковые", parent_id=None)
    parts = ActivityModel(title="Запчасти", parent_id=None)
    accessories = ActivityModel(title="Аксессуары", parent_id=None)

    # 3-й уровень под "Мясная продукция"
    sausages = ActivityModel(title="Колбасные изделия", parent_id=None)

    # 4-й уровень под "Колбасные изделия"
    dry_sausages = ActivityModel(title="Сырокопчёные колбасы", parent_id=None)

    activities = [
        food,
        cars,
        meat,
        milk,
        trucks,
        light,
        parts,
        accessories,
        sausages,
        dry_sausages,
    ]

    session.add_all(activities)
    # первая flush — чтобы появились id
    await session.flush()

    # проставляем parent_id (иерархия)
    # Еда -> Мясная / Молочная
    meat.parent_id = food.id
    milk.parent_id = food.id

    # Автомобили -> дочерние
    trucks.parent_id = cars.id
    light.parent_id = cars.id
    parts.parent_id = cars.id
    accessories.parent_id = cars.id

    # Мясная продукция -> Колбасные изделия -> Сырокопчёные колбасы
    sausages.parent_id = meat.id
    dry_sausages.parent_id = sausages.id

    # вторая flush — чтобы обновлённые parent_id улетели в БД
    await session.flush()
    await refresh_all(session, activities)

    return {
        "Еда": food,
        "Мясная продукция": meat,
        "Молочная продукция": milk,
        "Автомобили": cars,
        "Грузовые": trucks,
        "Легковые": light,
        "Запчасти": parts,
        "Аксессуары": accessories,
        "Колбасные изделия": sausages,
        "Сырокопчёные колбасы": dry_sausages,
    }


async def create_buildings(session: AsyncSession) -> List[BuildingModel]:
    """
    Создаём несколько зданий с адресами и координатами (около Москвы, условно).
    Для 10 организаций 4 зданий достаточно, будем их переиспользовать.
    """
    buildings = [
        BuildingModel(
            address="г. Москва, ул. Ленина 1, офис 3",
            longitude=37.617635,   # Москва, центр
            latitude=55.755814,
        ),
        BuildingModel(
            address="г. Москва, пр-т Мира 10",
            longitude=37.633,      # чуть восточнее
            latitude=55.76,
        ),
        BuildingModel(
            address="г. Москва, ул. Тверская 7",
            longitude=37.604,
            latitude=55.761,
        ),
        BuildingModel(
            address="г. Москва, Блюхера 32/1",
            longitude=37.59,
            latitude=55.76,
        ),
    ]

    session.add_all(buildings)
    await session.flush()
    await refresh_all(session, buildings)

    return buildings


def random_phone() -> str:
    """
    Генерим условный российский номер.
    """
    return f"+7-9{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"


async def create_organisations(
    session: AsyncSession,
    buildings: List[BuildingModel],
    activities: Dict[str, ActivityModel],
) -> List[OrganisationModel]:
    """
    Создаём ровно 10 организаций с телефонами и привязками к зданиям.
    (Привязка к activity см. в link_orgs_activities)
    """
    orgs = [
        OrganisationModel(
            title="ООО «Молочные реки»",
            building_id=buildings[0].id,
        ),
        OrganisationModel(
            title="ООО «Мясной двор»",
            building_id=buildings[1].id,
        ),
        OrganisationModel(
            title="ООО «Все для авто»",
            building_id=buildings[2].id,
        ),
        OrganisationModel(
            title="ИП «Автоаксессуары плюс»",
            building_id=buildings[2].id,
        ),
        OrganisationModel(
            title="ООО «Фермерские продукты»",
            building_id=buildings[3].id,
        ),
        OrganisationModel(
            title="ООО «Городские молочные продукты»",
            building_id=buildings[1].id,
        ),
        OrganisationModel(
            title="ООО «ГрузАвтоТранс»",
            building_id=buildings[0].id,
        ),
        OrganisationModel(
            title="ООО «Легковичок»",
            building_id=buildings[2].id,
        ),
        OrganisationModel(
            title="ООО «Автозапчасти 24»",
            building_id=buildings[3].id,
        ),
        OrganisationModel(
            title="ИП «Аксессуары для всех»",
            building_id=buildings[1].id,
        ),
    ]

    session.add_all(orgs)
    await session.flush()  # нужны id организаций для телефонов

    # Телефоны
    phones: List[OrganisationPhoneModel] = []
    for org in orgs:
        # каждой организации – 1–3 телефона
        for _ in range(random.randint(1, 3)):
            phones.append(
                OrganisationPhoneModel(
                    phone=random_phone(),
                    organisation_id=org.id,
                )
            )

    session.add_all(phones)
    await session.flush()
    await refresh_all(session, orgs + phones)

    return orgs


async def link_orgs_activities(
    session: AsyncSession,
    orgs: List[OrganisationModel],
    activities: Dict[str, ActivityModel],
) -> None:
    """
    Привязка организаций к видам деятельности через таблицу organisation_activities.

    ВАЖНО:
    - У ПЕРВОЙ организации (orgs[0]) — 4 уровня активности:
      Еда, Мясная продукция, Колбасные изделия, Сырокопчёные колбасы.
    """
    org_to_acts: Dict[int, List[ActivityModel]] = {
        # org[0]: все 4 уровня по ветке Еда -> ... -> Сырокопчёные колбасы
        orgs[0].id: [
            activities["Еда"],
            activities["Мясная продукция"],
            activities["Колбасные изделия"],
            activities["Сырокопчёные колбасы"],
        ],
        # далее — просто разумное распределение
        orgs[1].id: [
            activities["Мясная продукция"],
            activities["Еда"],
        ],
        orgs[2].id: [
            activities["Автомобили"],
            activities["Запчасти"],
        ],
        orgs[3].id: [
            activities["Аксессуары"],
            activities["Автомобили"],
        ],
        orgs[4].id: [
            activities["Молочная продукция"],
            activities["Еда"],
        ],
        orgs[5].id: [
            activities["Молочная продукция"],
        ],
        orgs[6].id: [
            activities["Грузовые"],
            activities["Автомобили"],
        ],
        orgs[7].id: [
            activities["Легковые"],
            activities["Автомобили"],
        ],
        orgs[8].id: [
            activities["Запчасти"],
        ],
        orgs[9].id: [
            activities["Аксессуары"],
        ],
    }

    links: List[OrganisationActivityModel] = []
    for org_id, acts in org_to_acts.items():
        for act in acts:
            links.append(
                OrganisationActivityModel(
                    organisation_id=org_id,
                    activity_id=act.id,
                )
            )

    session.add_all(links)
    await session.flush()
    await refresh_all(session, links)


async def main():
    """
    Точка входа для заполнения базы мок-данными.

    Важно: предполагается, что db_session_factory — это async_sessionmaker[AsyncSession],
    т.е. используется как:

        async with db_session_factory() as session:
            ...
    """
    async with db_session_factory() as session:
        # одна общая транзакция; commit произойдёт при выходе из begin()
        async with session.begin():
            activities = await create_activities(session)
            buildings = await create_buildings(session)
            orgs = await create_organisations(session, buildings, activities)
            await link_orgs_activities(session, orgs, activities)


if __name__ == "__main__":
    asyncio.run(main())
