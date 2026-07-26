import asyncio
from datetime import date, timedelta, time
from sqlalchemy import select
from app.database.session import AsyncSessionLocal, engine
from app.models.base import Base
from app.models.user import User, UserRole, Profile
from app.models.medication import Medication, MedicationType, MedicationStatus
from app.models.infusion import Infusion, InfusionStatus
from app.models.schedule import MedicationSchedule
from app.models.prescription import Prescription
from app.models.settings import UserSettings
from app.core.security import hash_pin

START_DATE = date(2026, 7, 26)


async def seed_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        existing = await session.execute(select(User))
        if existing.scalars().first():
            print("Database already seeded.")
            return

        pin_hash = hash_pin("1234")

        male_user = User(
            name="Erkak",
            pin_hash=pin_hash,
            role=UserRole.MALE,
            is_active=True,
        )
        female_user = User(
            name="Ayol",
            pin_hash=pin_hash,
            role=UserRole.FEMALE,
            is_active=True,
        )
        session.add(male_user)
        session.add(female_user)
        await session.flush()

        male_profile = Profile(
            user_id=male_user.id,
            display_name="Erkak",
            language="ru",
            timezone="Asia/Tashkent",
        )
        female_profile = Profile(
            user_id=female_user.id,
            display_name="Ayol",
            language="ru",
            timezone="Asia/Tashkent",
        )
        session.add(male_profile)
        session.add(female_profile)

        male_settings = UserSettings(
            user_id=male_user.id,
            notifications_enabled=True,
            sound_enabled=True,
            language="ru",
            timezone="Asia/Tashkent",
        )
        female_settings = UserSettings(
            user_id=female_user.id,
            notifications_enabled=True,
            sound_enabled=True,
            language="ru",
            timezone="Asia/Tashkent",
        )
        session.add(male_settings)
        session.add(female_settings)

        # --- Female Prescription ---
        female_prescription = Prescription(
            doctor="Бекенова Малика Камилджановна",
            hospital=None,
            diagnosis=(
                "Гипогонадотропная ЯН обусловленная гипофункцией щитовидной железы. "
                "Диффузный зоб 1 степени. Гипотиреоз. "
                "Функциональная гиперпролактинемия. Бесплодие I."
            ),
            date=START_DATE,
            notes=None,
            user_id=female_user.id,
            created_by=female_user.id,
            updated_by=female_user.id,
        )
        session.add(female_prescription)

        # --- Female Medications ---
        female_meds_data = [
            {
                "name": "Сейодин",
                "type": MedicationType.CAPSULE,
                "dosage": "1 kapsula",
                "instruction": "Ovqatdan keyin",
                "frequency": "Kuniga 1 marta (ertalab)",
                "times": ["08:00"],
                "duration_days": 90,
                "notes": "Tarkibi: Yod, Selen, Rux, Metionin",
            },
            {
                "name": "Vitamin E NERO 400mg",
                "type": MedicationType.VITAMIN,
                "dosage": "1 kapsula",
                "instruction": "Ovqatdan keyin",
                "frequency": "Kuniga 3 marta",
                "times": ["08:00", "14:00", "20:00"],
                "duration_days": 30,
                "notes": None,
            },
            {
                "name": "Vitamin D 5000 ED",
                "type": MedicationType.VITAMIN,
                "dosage": "1 kapsula",
                "instruction": "Ovqatdan keyin",
                "frequency": "Kuniga 1 marta (ertalab)",
                "times": ["08:00"],
                "duration_days": 90,
                "notes": None,
            },
            {
                "name": "Квинофолик",
                "type": MedicationType.CAPSULE,
                "dosage": "1 kapsula",
                "instruction": "Ovqatdan keyin",
                "frequency": "Kuniga 2 marta",
                "times": ["08:00", "20:00"],
                "duration_days": 90,
                "notes": None,
            },
            {
                "name": "Андровумен",
                "type": MedicationType.PACKET,
                "dosage": "1 paketik 50ml suvga",
                "instruction": "Uxlashdan oldin",
                "frequency": "Kuniga 1 marta (kechasi)",
                "times": ["21:00"],
                "duration_days": 30,
                "notes": None,
            },
            {
                "name": "Достинекс 0.5mg",
                "type": MedicationType.TABLET,
                "dosage": "1/4 tabletka",
                "instruction": "Seshanba va Payshanba kuni soat 21:00 da",
                "frequency": "Haftasiga 2 marta (Se, Pa)",
                "times": ["21:00"],
                "duration_days": 90,
                "notes": "Faqat Seshanba va Payshanba kunlari",
            },
            {
                "name": "Сибисил",
                "type": MedicationType.CAPSULE,
                "dosage": "1 kapsula",
                "instruction": "Ovqatdan 30 daqiqa oldin",
                "frequency": "Kuniga 1 marta",
                "times": ["07:30"],
                "duration_days": 60,
                "notes": None,
            },
            {
                "name": "Дюфастон 10mg",
                "type": MedicationType.TABLET,
                "dosage": "1 tabletka",
                "instruction": "Kuniga 3 marta, 10 kun",
                "frequency": "Kuniga 3 marta (10 kun)",
                "times": ["08:00", "14:00", "20:00"],
                "duration_days": 10,
                "start_date": date(2026, 8, 6),
                "notes": "6-avgustdan boshlab 10 kun",
            },
        ]

        for med_data in female_meds_data:
            med_start = med_data.get("start_date", START_DATE)
            end_date = med_start + timedelta(days=med_data["duration_days"])
            med = Medication(
                name=med_data["name"],
                type=med_data["type"],
                dosage=med_data["dosage"],
                instruction=med_data["instruction"],
                frequency=med_data["frequency"],
                times=med_data["times"],
                start_date=med_start,
                end_date=end_date,
                duration_days=med_data["duration_days"],
                status=MedicationStatus.ACTIVE,
                notes=med_data["notes"],
                user_id=female_user.id,
                created_by=female_user.id,
                updated_by=female_user.id,
            )
            session.add(med)
            await session.flush()

            for time_str in med_data["times"]:
                parts = time_str.split(":")
                sched = MedicationSchedule(
                    medication_id=med.id,
                    scheduled_time=time(int(parts[0]), int(parts[1])),
                    day_of_week=None,
                    created_by=female_user.id,
                    updated_by=female_user.id,
                )
                session.add(sched)

        # --- Female Infusions (Kapelnitsa) ---
        female_infusions_data = [
            {
                "name": "Immunoglobulin",
                "solution": "NaCl 0.9% 200ml",
                "volume": "200ml",
                "frequency": "Har kuni",
                "total_sessions": 5,
                "duration_days": 5,
                "notes": None,
            },
        ]

        for inf_data in female_infusions_data:
            inf_end = START_DATE + timedelta(days=inf_data["duration_days"])
            inf = Infusion(
                name=inf_data["name"],
                solution=inf_data["solution"],
                volume=inf_data["volume"],
                frequency=inf_data["frequency"],
                time=time(9, 0),
                status=InfusionStatus.ACTIVE,
                start_date=START_DATE,
                end_date=inf_end,
                duration_days=inf_data["duration_days"],
                total_sessions=inf_data["total_sessions"],
                completed_sessions=0,
                notes=inf_data["notes"],
                user_id=female_user.id,
                created_by=female_user.id,
                updated_by=female_user.id,
            )
            session.add(inf)

        # --- Male Oral Medications ---
        male_meds_data = [
            {
                "name": "Уростим 50mg",
                "type": MedicationType.TABLET,
                "dosage": "1 tabletka",
                "instruction": "Ovqatdan oldin",
                "frequency": "Kuniga 1 marta (ertalab)",
                "times": ["07:30"],
                "duration_days": 30,
                "notes": None,
            },
            {
                "name": "Фурамаг 50mg",
                "type": MedicationType.CAPSULE,
                "dosage": "1 kapsula",
                "instruction": "Ovqatdan keyin",
                "frequency": "Kuniga 3 marta",
                "times": ["08:00", "14:00", "20:00"],
                "duration_days": 10,
                "notes": None,
            },
            {
                "name": "Цистокс Д форте",
                "type": MedicationType.PACKET,
                "dosage": "1 paketik 50ml suvga",
                "instruction": "Ovqatdan keyin",
                "frequency": "Kuniga 1 marta (kechasi)",
                "times": ["20:30"],
                "duration_days": 15,
                "notes": None,
            },
        ]

        for med_data in male_meds_data:
            end_date = START_DATE + timedelta(days=med_data["duration_days"])
            med = Medication(
                name=med_data["name"],
                type=med_data["type"],
                dosage=med_data["dosage"],
                instruction=med_data["instruction"],
                frequency=med_data["frequency"],
                times=med_data["times"],
                start_date=START_DATE,
                end_date=end_date,
                duration_days=med_data["duration_days"],
                status=MedicationStatus.ACTIVE,
                notes=med_data["notes"],
                user_id=male_user.id,
                created_by=male_user.id,
                updated_by=male_user.id,
            )
            session.add(med)
            await session.flush()

            for time_str in med_data["times"]:
                parts = time_str.split(":")
                sched = MedicationSchedule(
                    medication_id=med.id,
                    scheduled_time=time(int(parts[0]), int(parts[1])),
                    day_of_week=None,
                    created_by=male_user.id,
                    updated_by=male_user.id,
                )
                session.add(sched)

        await session.commit()
        print("Database seeded successfully!")
        print(f"  - Female user (Ayol): PIN 1234, {len(female_meds_data)} medications")
        print(f"  - Male user (Erkak): PIN 1234, {len(male_meds_data)} medications (no suppository)")


async def reset_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await seed_database()


if __name__ == "__main__":
    asyncio.run(seed_database())
