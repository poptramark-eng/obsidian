# Project State — Kenyan CBE Assessment Management System

> Authoritative continuation document. Read this before changes in future sessions and update it at the end of each session.

## Identity
- Product: independent Kenyan CBE School Assessment Management System MVP.
- Repository: https://github.com/poptramark-eng/obsidian (main).
- This is a standalone implementation. It is NOT a continuation, fork, migration, or replacement of Sentinel. Do not import Sentinel code, schemas, decisions, or assumptions unless explicitly requested.
- Requirements source: product brief supplied 2026-11-25.

## Strict product scope
1. Hierarchical assessment: Grade Level → Learning Area → Strand → Sub-strand → Assessment Rubric. Support EE/ME/AE/BE and EE1, EE2, ME1, ME2, AE1, AE2, BE1, BE2; teacher qualitative descriptors; seven CBE core competencies.
2. Grade 9 → Grade 10 pathway analysis using Grades 7–9 performance for STEM, Social Sciences, and Arts & Sports Science.
3. Paystack-only school payments: subaccounts, configurable platform fee and transaction splits, parent report access after levy payment, M-Pesa Express/STK Push and cards, plus school SaaS subscriptions. Arrears should switch school operations to read-only mode.

Out of scope: transport, library, hostel, HR/payroll and generic ERP modules.

## Stack
- Backend: Python 3.12+, FastAPI, SQLAlchemy 2 async, Alembic, Pydantic v2, httpx.
- Data/queues: PostgreSQL, Redis, Arq.
- PDF: evaluate WeasyPrint vs ReportLab before choosing.
- Frontend: Next.js App Router, React, TypeScript, Tailwind CSS, TanStack Query, React Hook Form, Zod, Lucide.
- Payments: Paystack exclusively.
- Local orchestration: Docker Compose (PostgreSQL, Redis, backend, frontend).

## Non-negotiable engineering guardrails
- Every school-owned table has school_id. Enforce tenant scope in server dependencies and every query; test cross-tenant denial.
- Money is PostgreSQL BIGINT in KES cents. Never use float for money; convert validated decimal strings to integer cents at API boundaries.
- Verify Paystack x-paystack-signature as HMAC-SHA512 over raw request bytes before parsing JSON. Persist processed event identity/reference and make processing idempotent and transactionally safe.
- Teacher bulk grading endpoint: POST /api/v1/assessments/bulk. Validate the complete batch before persistence.
- Enforce RBAC and tenant isolation on the server, not only in the UI.
- Do not fabricate official KICD curriculum or rubric data. Demo seed is explicitly illustrative and curriculum data must be versioned/importable from authoritative material.
- Learner Admission/NEMIS number is a lookup identifier, not an authentication secret. Never expose reports before payment and suitable verification.
- Keep invoice status, payment status and report entitlement distinct.

## Initial domain
School, User, Learner, Term, LearningArea, Strand, SubStrand, AssessmentRecord, FeeInvoice, PaymentTransaction, ProcessedWebhook. Add CurriculumGrade, AssessmentRubric, CoreCompetency, LearnerCompetencyAssessment, plans/subscriptions and pathway configuration as needed. Global curriculum catalog may be global/versioned; school-owned records must be tenant-scoped.

## Roles
SUPER_ADMIN, SCHOOL_ADMIN, TEACHER. Do not introduce roles without a documented requirement.

## Milestones
- [x] Confirm repository identity and independent project boundary.
- [x] Create initial README.
- [x] Step 1: initial scaffold, Compose, environment template, backend/frontend skeleton committed (runtime verification pending).
- [ ] Step 1 verification: validate Compose and build/start services where runtime permits.
- [x] Step 2: initial SQLAlchemy async domain models, Alembic environment/initial migration, deterministic Kenyan CBE demo seed committed (runtime verification pending).
- [ ] Step 2 verification: compile/import, migrate disposable PostgreSQL, seed idempotently, test money and tenant constraints.
- [ ] Step 3: JWT/RBAC, tenant dependencies, bulk assessment APIs, pathway service.
- [ ] Step 4: Paystack service and secure idempotent webhook engine.
- [ ] Step 5: asynchronous PDF learner portfolio.
- [ ] Step 6: Next.js admin, teacher grid and parent portal.

## Decisions and unresolved facts
- UUID primary keys; UTC timestamps.
- Store KES cents as integers; API must not accept binary floats for monetary values.
- Keep curriculum catalog versioned and separate from learner assessments.
- Use durable job/outbox handling so a database commit cannot silently lose a queued PDF task.
- Verify current Paystack Kenya support and exact settlement behavior before claiming a subaccount can settle directly to an M-Pesa till/paybill. Do not assume till/paybill is a supported settlement destination.
- Curriculum seed is illustrative, not official or complete KICD content.
- Pathway weights and evidence thresholds are configurable/versioned; no official policy weights have been supplied.

## Current state — 2026-11-25
- Repository: poptramark-eng/obsidian, default branch main.
- Added README, independent-product ADR, project-state file, Docker Compose, .env.example, backend package/settings/async DB/models/Alembic/seed, and Next.js app skeleton.
- Demo seed creates two Kisii schools, four school users, 30 learners, Grade 7–9 sample learning-area catalog and sample rubrics/competencies. Demo descriptors are explicitly illustrative.
- No Sentinel code or assumptions are intentionally reused.
- Runtime verification has NOT been run from this session. Step 1/2 are scaffolded, not yet verified.
- Next: validate Python imports/SQLAlchemy metadata/Alembic against PostgreSQL; validate Docker Compose and Next.js build; fix any issues before Step 3.

## Session handoff protocol
At every session end, update milestone checkboxes, current state, changed paths, validation commands/results, decisions, blockers and exact next action. Never claim tests passed unless they were run. Keep this file as the first document future agents read.
