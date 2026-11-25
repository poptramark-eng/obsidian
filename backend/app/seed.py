"""Idempotent demo data loader. All curriculum text is illustrative, not official KICD content."""
import asyncio
from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.db import SessionFactory
from app.models import (
    AssessmentRubric, CoreCompetency, FeeInvoice, GradeLevel, InvoiceStatus,
    Learner, LearningArea, School, Strand, SubStrand, Term, User, UserRole,
)
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended().hash("ChangeMe123!")

AREAS = [
    ("MAT", "Mathematics"),
    ("SCI", "Integrated Science"),
    ("PTS", "Pre-Technical Studies"),
    ("ENG", "English"),
    ("CAS", "Creative Arts & Sports"),
]
COMPETENCIES = [
    ("COMMUNICATION", "Communication and Collaboration"),
    ("CRITICAL_THINKING", "Critical Thinking and Problem Solving"),
    ("CREATIVITY", "Creativity and Imagination"),
    ("CITIZENSHIP", "Citizenship"),
    ("DIGITAL_LITERACY", "Digital Literacy"),
    ("LEARNING_TO_LEARN", "Learning to Learn"),
    ("SELF_EFFICACY", "Self-Efficacy"),
]
DEMO_SCHOOLS = [
    ("KSI-DEMO-001", "Nyota Junior School", "Kisii", "Kitutu Chache"),
    ("KSI-DEMO-002", "Mwangaza Junior School", "Kisii", "Bonchari"),
]
GIVEN_NAMES = ["Achieng", "Wanjiku", "Otieno", "Kamau", "Atieno", "Mwangi", "Nyaboke", "Omondi", "Chebet", "Maina"]
FAMILY_NAMES = ["Ouma", "Kiptoo", "Moraa", "Njoroge", "Akinyi", "Barasa", "Wekesa", "Nyongesa", "Abdi", "Mutua"]


async def get_or_create(session, model, filters: dict, values: dict | None = None):
    result = await session.execute(select(model).filter_by(**filters))
    instance = result.scalar_one_or_none()
    if instance is None:
        instance = model(**filters, **(values or {}))
        session.add(instance)
        await session.flush()
    return instance


async def seed() -> None:
    async with SessionFactory() as session:
        async with session.begin():
            schools = []
            for code, name, county, sub_county in DEMO_SCHOOLS:
                school = await get_or_create(
                    session, School, {"code": code},
                    {"name": name, "county": county, "sub_county": sub_county,
                     "is_active": True, "platform_fee_bps": 250},
                )
                schools.append(school)

            for code, name in COMPETENCIES:
                await get_or_create(
                    session, CoreCompetency, {"code": code},
                    {"name": name, "description": f"Illustrative descriptor for {name.lower()}."},
                )

            for grade in GradeLevel:
                for area_code, area_name in AREAS:
                    area = await get_or_create(
                        session, LearningArea,
                        {"curriculum_version": "DEMO-2026", "grade_level": grade, "code": area_code},
                        {"name": area_name, "is_demo": True},
                    )
                    strand = await get_or_create(
                        session, Strand, {"learning_area_id": area.id, "code": "STR-01"},
                        {"name": f"{area_name}: foundational concepts",
                         "description": "Illustrative sample strand; replace with verified curriculum data."},
                    )
                    sub_strand = await get_or_create(
                        session, SubStrand, {"strand_id": strand.id, "code": "SUB-01"},
                        {"name": "Exploration and application",
                         "description": "Illustrative sample sub-strand for local development."},
                    )
                    await get_or_create(
                        session, AssessmentRubric, {"sub_strand_id": sub_strand.id, "code": "RUB-01"},
                        {"descriptor": "Demonstrates the skill independently in familiar contexts. (Demo descriptor)"},
                    )
                    await get_or_create(
                        session, AssessmentRubric, {"sub_strand_id": sub_strand.id, "code": "RUB-02"},
                        {"descriptor": "Applies the skill with guidance and identifies areas for improvement. (Demo descriptor)"},
                    )

            for school_index, school in enumerate(schools):
                admin = await get_or_create(
                    session, User, {"school_id": school.id, "email": f"admin{school_index + 1}@demo.cbe.local"},
                    {"full_name": f"{school.name} Administrator", "password_hash": password_hash,
                     "role": UserRole.SCHOOL_ADMIN, "is_active": True},
                )
                teacher = await get_or_create(
                    session, User, {"school_id": school.id, "email": f"teacher{school_index + 1}@demo.cbe.local"},
                    {"full_name": f"{school.name} Teacher", "password_hash": password_hash,
                     "role": UserRole.TEACHER, "is_active": True},
                )
                term = await get_or_create(
                    session, Term,
                    {"school_id": school.id, "academic_year": 2026, "term_number": 1},
                    {"name": "Term 1 2026", "starts_on": date(2026, 1, 5),
                     "ends_on": date(2026, 4, 3), "is_current": True},
                )

                for index in range(15):
                    grade = list(GradeLevel)[index % 3]
                    first = GIVEN_NAMES[(index + school_index * 3) % len(GIVEN_NAMES)]
                    last = FAMILY_NAMES[(index * 3 + school_index) % len(FAMILY_NAMES)]
                    learner = await get_or_create(
                        session, Learner,
                        {"school_id": school.id, "admission_number": f"{school.code}-{index + 1:03d}"},
                        {"nemis_number": f"DEMO-NEMIS-{school_index + 1}-{index + 1:04d}",
                         "first_name": first, "last_name": last,
                         "gender": "FEMALE" if index % 2 == 0 else "MALE",
                         "current_grade": grade, "is_active": True},
                    )
                    if index < 3:
                        await get_or_create(
                            session, FeeInvoice,
                            {"school_id": school.id, "invoice_number": f"{school.code}-2026-T1-{index + 1:03d}"},
                            {"learner_id": learner.id, "term_id": term.id,
                             "description": "Term 1 learner portfolio levy (demo)",
                             "amount_due_cents": 150000, "amount_paid_cents": 0,
                             "status": InvoiceStatus.PENDING, "due_date": date(2026, 3, 31)},
                        )

        print("Demo seed complete: 2 schools, 4 school users, 30 learners, 15 grade-area catalog entries and sample rubrics.")
        print("Demo user password for all seeded accounts: ChangeMe123! (change immediately; never use in production).")


if __name__ == "__main__":
    asyncio.run(seed())
