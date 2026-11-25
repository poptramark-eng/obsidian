from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKey,
    Index, Integer, Numeric, String, Text, UniqueConstraint, func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    return [item.value for item in enum_cls]


class Base(DeclarativeBase):
    pass


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    SCHOOL_ADMIN = "SCHOOL_ADMIN"
    TEACHER = "TEACHER"


class GradeLevel(str, enum.Enum):
    GRADE_7 = "GRADE_7"
    GRADE_8 = "GRADE_8"
    GRADE_9 = "GRADE_9"


class RubricBand(str, enum.Enum):
    EE = "EE"
    ME = "ME"
    AE = "AE"
    BE = "BE"
    EE1 = "EE1"
    EE2 = "EE2"
    ME1 = "ME1"
    ME2 = "ME2"
    AE1 = "AE1"
    AE2 = "AE2"
    BE1 = "BE1"
    BE2 = "BE2"


class InvoiceStatus(str, enum.Enum):
    PENDING = "PENDING"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    VOID = "VOID"
    OVERDUE = "OVERDUE"


class PaymentStatus(str, enum.Enum):
    INITIALIZED = "INITIALIZED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REVERSED = "REVERSED"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class School(TimestampMixin, Base):
    __tablename__ = "schools"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    county: Mapped[str] = mapped_column(String(100), nullable=False)
    sub_county: Mapped[str | None] = mapped_column(String(100))
    paystack_subaccount_code: Mapped[str | None] = mapped_column(String(100), unique=True)
    platform_fee_bps: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_read_only: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    users: Mapped[list[User]] = relationship(back_populates="school")
    learners: Mapped[list[Learner]] = relationship(back_populates="school")


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("school_id", "email", name="uq_user_school_email"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(180), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    school: Mapped[School | None] = relationship(back_populates="users")


class Learner(TimestampMixin, Base):
    __tablename__ = "learners"
    __table_args__ = (
        UniqueConstraint("school_id", "admission_number", name="uq_learner_school_admission"),
        Index("ix_learner_school_grade", "school_id", "current_grade"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    admission_number: Mapped[str] = mapped_column(String(80), nullable=False)
    nemis_number: Mapped[str | None] = mapped_column(String(80))
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    current_grade: Mapped[GradeLevel] = mapped_column(Enum(GradeLevel, name="grade_level"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    school: Mapped[School] = relationship(back_populates="learners")


class Term(TimestampMixin, Base):
    __tablename__ = "terms"
    __table_args__ = (UniqueConstraint("school_id", "academic_year", "term_number", name="uq_term_school_year_number"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    term_number: Mapped[int] = mapped_column(Integer, nullable=False)
    starts_on: Mapped[date | None] = mapped_column(Date)
    ends_on: Mapped[date | None] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class LearningArea(TimestampMixin, Base):
    __tablename__ = "learning_areas"
    __table_args__ = (UniqueConstraint("curriculum_version", "grade_level", "code", name="uq_learning_area_curriculum_grade_code"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    curriculum_version: Mapped[str] = mapped_column(String(40), default="DEMO-2026", nullable=False)
    grade_level: Mapped[GradeLevel] = mapped_column(Enum(GradeLevel, name="grade_level"), nullable=False)
    code: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Strand(TimestampMixin, Base):
    __tablename__ = "strands"
    __table_args__ = (UniqueConstraint("learning_area_id", "code", name="uq_strand_area_code"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learning_area_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learning_areas.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class SubStrand(TimestampMixin, Base):
    __tablename__ = "sub_strands"
    __table_args__ = (UniqueConstraint("strand_id", "code", name="uq_substrand_strand_code"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strand_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("strands.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class AssessmentRubric(TimestampMixin, Base):
    __tablename__ = "assessment_rubrics"
    __table_args__ = (UniqueConstraint("sub_strand_id", "code", name="uq_rubric_substrand_code"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sub_strand_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sub_strands.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str] = mapped_column(String(40), nullable=False)
    descriptor: Mapped[str] = mapped_column(Text, nullable=False)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class AssessmentRecord(TimestampMixin, Base):
    __tablename__ = "assessment_records"
    __table_args__ = (
        UniqueConstraint("school_id", "learner_id", "rubric_id", "term_id", name="uq_assessment_learner_rubric_term"),
        CheckConstraint("score IS NULL OR (score >= 0 AND score <= 100)", name="ck_assessment_score_range"),
        Index("ix_assessment_school_learner", "school_id", "learner_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    learner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    rubric_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_rubrics.id"), nullable=False)
    term_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("terms.id"), nullable=False)
    assessed_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    band: Mapped[RubricBand] = mapped_column(Enum(RubricBand, name="rubric_band"), nullable=False)
    score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    teacher_descriptor: Mapped[str | None] = mapped_column(Text)
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CoreCompetency(TimestampMixin, Base):
    __tablename__ = "core_competencies"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class LearnerCompetencyAssessment(TimestampMixin, Base):
    __tablename__ = "learner_competency_assessments"
    __table_args__ = (UniqueConstraint("school_id", "learner_id", "competency_id", "term_id", name="uq_learner_competency_term"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    learner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    competency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("core_competencies.id"), nullable=False)
    term_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("terms.id"), nullable=False)
    assessed_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    descriptor: Mapped[str] = mapped_column(Text, nullable=False)


class FeeInvoice(TimestampMixin, Base):
    __tablename__ = "fee_invoices"
    __table_args__ = (
        CheckConstraint("amount_due_cents >= 0 AND amount_paid_cents >= 0", name="ck_invoice_nonnegative_amounts"),
        CheckConstraint("amount_paid_cents <= amount_due_cents", name="ck_invoice_paid_not_over_due"),
        Index("ix_invoice_school_learner_status", "school_id", "learner_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    learner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    term_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("terms.id"), nullable=False)
    invoice_number: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(240), nullable=False)
    amount_due_cents: Mapped[int] = mapped_column(BigInteger, nullable=False)
    amount_paid_cents: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    status: Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus, name="invoice_status"), default=InvoiceStatus.PENDING, nullable=False)
    report_unlocked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    due_date: Mapped[date | None] = mapped_column(Date)


class PaymentTransaction(TimestampMixin, Base):
    __tablename__ = "payment_transactions"
    __table_args__ = (
        CheckConstraint("amount_cents > 0", name="ck_payment_positive_amount"),
        UniqueConstraint("provider_reference", name="uq_payment_provider_reference"),
        Index("ix_payment_school_invoice", "school_id", "invoice_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    invoice_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fee_invoices.id"), nullable=False)
    amount_cents: Mapped[int] = mapped_column(BigInteger, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="KES", nullable=False)
    provider: Mapped[str] = mapped_column(String(30), default="PAYSTACK", nullable=False)
    provider_reference: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus, name="payment_status"), default=PaymentStatus.INITIALIZED, nullable=False)
    channel: Mapped[str | None] = mapped_column(String(30))
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ProcessedWebhook(TimestampMixin, Base):
    __tablename__ = "processed_webhooks"
    __table_args__ = (UniqueConstraint("provider", "event_id", name="uq_processed_webhook_provider_event"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider: Mapped[str] = mapped_column(String(30), default="PAYSTACK", nullable=False)
    event_id: Mapped[str] = mapped_column(String(180), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SchoolPlan(TimestampMixin, Base):
    __tablename__ = "school_plans"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    amount_cents: Mapped[int] = mapped_column(BigInteger, nullable=False)
    interval: Mapped[str] = mapped_column(String(20), default="monthly", nullable=False)
    paystack_plan_code: Mapped[str | None] = mapped_column(String(100), unique=True)


class SchoolSubscription(TimestampMixin, Base):
    __tablename__ = "school_subscriptions"
    __table_args__ = (Index("ix_subscription_school_status", "school_id", "status"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("school_plans.id"), nullable=False)
    paystack_subscription_code: Mapped[str | None] = mapped_column(String(120), unique=True)
    status: Mapped[str] = mapped_column(String(30), default="PENDING", nullable=False)
    current_period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PathwayReadiness(TimestampMixin, Base):
    __tablename__ = "pathway_readiness"
    __table_args__ = (UniqueConstraint("school_id", "learner_id", "academic_year", "pathway", name="uq_pathway_learner_year"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    learner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    pathway: Mapped[str] = mapped_column(String(40), nullable=False)
    readiness_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    scoring_version: Mapped[str] = mapped_column(String(40), nullable=False)
    evidence_summary: Mapped[str] = mapped_column(Text, nullable=False)
