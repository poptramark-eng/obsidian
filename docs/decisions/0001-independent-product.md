# ADR 0001: Standalone CBE Product

- Status: Accepted
- Date: 2026-11-25

## Context
This repository implements the separately supplied Kenyan CBE assessment MVP. A distinct project named Sentinel exists but is not the subject of this implementation.

## Decision
Build this repository independently. Do not continue, migrate, fork, or reuse Sentinel code, schema, project state, or assumptions. Similar domain concepts must be independently derived from this product brief.

## Consequences
This repository owns its architecture, models, migrations, seed data, tests and roadmap. Future sessions must read docs/PROJECT_STATE.md. Cross-project reuse requires explicit approval.
