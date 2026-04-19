# IBS Operations Management System

IBS Operations Management System is a Django-based operations platform designed as a modular foundation for a larger ERP program.

Current modules:

- Operations Dashboard
- Fault Report Management
- PPE Issue Management
- Employee-Issued IT Assets Management
- IT Asset Fault/Damage Management

The architecture and module boundaries are intentionally structured for ERP integration and phased expansion.

---

## ERP Integration Context

This repository represents an operations domain slice that will plug into a bigger ERP platform. Current design goals:

- Keep each business flow isolated by Django app namespace.
- Use predictable URL conventions for integration with ERP navigation.
- Use mode-based behavior (`?mode=...`) to simulate role context at UI/workflow level.
- Preserve locking rules (signatures/resolution) to prevent state corruption.

Planned next phase:

- Additional modules will be added incrementally (HR, procurement, approvals, analytics, and integration adapters).
- Existing modules will be aligned to the ibs ERP authentication/authorization while preserving current workflow constraints.

---

## Module Coverage

### 1) Dashboard

Purpose:

- System landing page and module launcher.

Entry route:

- `/`

### 2) Fault Report Management (`fault_logs`)

Purpose:

- Capture and manage general operational fault reports with optional attachments.

Core capabilities:

- Create, list, detail, edit, delete.
- Attachment upload and attachment delete.

Base route:

- `/faults/`

### 3) PPE Issue Management (`ppe_records`)

Purpose:

- Capture PPE issuance per employee, including multiple issued items.

Core capabilities:

- Create, list, detail, update, delete.
- Staff signature per issued item.
- Record lock when any PPE item is signed.

Base route:

- `/ppe/`

### 4) Employee-Issued IT Assets Management (`assets`)

Purpose:

- Track assignment of one or more IT assets per employee issuance record.

Core capabilities:

- Create, list, detail, update, delete.
- Staff signature per asset item.
- Full record lock when any item is signed.

Base route:

- `/assets/`

### 5) IT Asset Fault/Damage Management (`asset_faults`)

Purpose:

- Capture employee-reported IT asset faults and drive IT workflow (assign, sign, resolve).

Core capabilities:

- Create, list, detail, update, delete (subject to mode/rule constraints).
- IT-only assign step.
- IT-only signature step.
- One-time resolution update (resolution date + resolution description) after IT signature.
- Locked behavior after signing and after resolution is recorded.

Base route:

- `/asset-faults/`

---

## Route Map

### Root and Module Entry Routes

- Dashboard: `/`
- Fault Logs: `/faults/`
- PPE Records: `/ppe/`
- Asset Records: `/assets/`
- Asset Faults: `/asset-faults/`
- Legacy home include: `/home/`

### Fault Logs (`/faults/`)

- List: `/faults/`
- Create: `/faults/new/`
- Detail: `/faults/<id>/`
- Edit: `/faults/<id>/edit/`
- Delete (POST): `/faults/<id>/delete/`
- Delete attachment (POST): `/faults/attachments/<id>/delete/`

### PPE Records (`/ppe/`)

- List: `/ppe/`
- Create: `/ppe/new/`
- Detail: `/ppe/<id>/`
- Update: `/ppe/<id>/update/`
- Edit alias: `/ppe/<id>/edit/`
- Delete: `/ppe/<id>/delete/`
- Sign PPE item (POST): `/ppe/item/<item_id>/sign/`

### Asset Records (`/assets/`)

- List: `/assets/`
- Create: `/assets/new/`
- Detail: `/assets/<id>/`
- Edit: `/assets/<id>/edit/`
- Delete (POST): `/assets/<id>/delete/`
- Sign asset item (POST): `/assets/items/<item_id>/sign/`

### Asset Faults (`/asset-faults/`)

- List: `/asset-faults/`
- Create: `/asset-faults/new/`
- Detail: `/asset-faults/<id>/`
- Edit: `/asset-faults/<id>/edit/`
- Delete (POST): `/asset-faults/<id>/delete/`
- Assign (IT workflow): `/asset-faults/<id>/assign/`
- Sign (IT workflow, POST): `/asset-faults/<id>/sign/`
- Resolve (IT workflow): `/asset-faults/<id>/resolve/`

---

## Mode Query Parameter Guide (`?mode=`)

Several modules use a mode query parameter to control workflow behavior. Typical examples:

- `/asset-faults/5/?mode=it`
- `/ppe/3/?mode=staff`
- `/assets/7/?mode=staff`
- `/assets/7/?mode=creator`

Supported and expected values:

- `staff`: employee/staff signing context.
- `it`: IT workflow context (primarily for `asset_faults`).
- `creator`: creator/admin-like context (practical behavior is default non-staff context in current implementation).

Important note about typos:

- A typo such as `?mode=stff` is not treated as `staff`. It behaves as an unknown mode (default behavior), which can hide signing actions and/or show non-staff actions depending on module logic.

### Behavior Summary by Module

#### PPE (`/ppe/`)

- `?mode=staff`
  - Allowed: sign unsigned PPE items from detail page.
  - Not allowed: edit/delete actions from detail page.
- `?mode=creator` (or any non-staff value)
  - Allowed: view and, if record is not locked, edit/delete.
  - Not allowed: signing items.
- Lock rule:
  - If any item is signed, record becomes read-only (no edit/delete).

#### Assets (`/assets/`)

- `?mode=staff`
  - Allowed: sign unsigned asset items from detail page.
  - Not allowed: edit/delete actions.
- `?mode=creator` (or any non-staff value)
  - Allowed: view and, if record is not locked, edit/delete.
  - Not allowed: signing items.
- Lock rule:
  - If any item is signed, the record is locked from edit/delete.

#### Asset Faults (`/asset-faults/`)

- `?mode=it`
  - Allowed: assign, sign, resolve.
  - Not allowed: create from list, full-form edit.
  - Resolve lock: once `resolution_date` is set, resolution cannot be edited again.
- `?mode=staff`
  - Allowed: view list/detail.
  - Not allowed: full-form edit and delete.
- `?mode=creator` (or default/no mode)
  - Allowed: create; edit/delete only while unsigned and not restricted by lock conditions.
  - Not allowed: IT-only assign/sign/resolve actions.
- Lock rules:
  - After IT signature, full edit/delete are blocked.
  - After resolution is recorded, resolve action is blocked from further changes.

#### Fault Logs (`/faults/`)

- No active `mode` behavior is currently enforced in views.
- Standard CRUD + attachment flow applies.

---

## Quick Link Examples

- Dashboard: `/`
- PPE list: `/ppe/`
- PPE detail in staff mode: `/ppe/3/?mode=staff`
- Assets list: `/assets/`
- Asset detail in creator mode: `/assets/5/?mode=creator`
- Asset detail in staff mode: `/assets/5/?mode=staff`
- Asset Fault list: `/asset-faults/`
- Asset Fault detail in IT mode: `/asset-faults/5/?mode=it`
- Asset Fault resolve page in IT mode: `/asset-faults/5/resolve/?mode=it`

---

## Project Structure (Current)

```text
ibs-fault-report/
├── config/
├── dashboard/
├── fault_logs/
│   ├── management/
│   ├── migrations/
│   ├── static/fault_logs/
│   └── templates/fault_logs/
├── ppe_records/
│   ├── migrations/
│   └── templates/ppe_records/
├── assets/
│   ├── migrations/
│   └── templates/assets/
├── asset_faults/
│   ├── migrations/
│   └── ...
├── templates/
│   ├── dashboard/
│   └── asset_faults/
├── media/
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

## Technical Stack

- Framework: Django 6.x
- Database: SQLite (current local setup)
- Server-side rendering: Django templates
- Main installed apps:
  - `dashboard`
  - `fault_logs`
  - `ppe_records`
  - `assets`
  - `asset_faults`
  - `core`

---

## Current Status and Roadmap

Current state:

- Dashboard module: active.
- Fault Logs module: active.
- PPE module: active with signature and lock constraints.
- Assets module: active with signature and lock constraints.
- Asset Faults module: active with IT assign/sign/resolve workflow and one-time resolution lock.

Roadmap:

- More ibs ERP modules(digital forms) will be added.
- Existing mode-based behavior will transition to centralized ERP role/permission enforcement.
- API and integration adapters will be introduced as ERP orchestration layer is finalized.

---

## Author

FranzAfun
