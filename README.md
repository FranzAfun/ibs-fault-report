# IBS Operations Management System

A Django-based CRUD platform for managing operational workflows within IBS.
Currently includes:

* Fault Report Management
* PPE Issue Management

The system is structured for clean integration into a larger ERP environment.

---

## Modules

### 1. Fault Report Management

Handles full lifecycle of fault reporting:

* Create fault reports
* View centralized fault log
* Update status and resolution
* Assign responsibility
* Controlled deletion

---

### 2. PPE Issue Management

Manages issuance and tracking of PPE items per employee:

* Create PPE issue records
* Dynamic PPE item entries (add/remove rows)
* Clean tabular listing with action controls
* Detail view with structured layout
* Signature workflow:

  * Staff can sign issued PPE
  * Creator cannot sign
  * Once signed:

    * No edits allowed
    * No deletion allowed
    * Record becomes read-only

---

## Technical Stack

* Framework: Django
* Apps:

  * fault_logs
  * ppe_records
* Environment-based configuration
* Production-ready setup with secure defaults

---

## UI/UX Direction

* Clean, structured, professional layout
* Consistent action buttons (icon-based)
* Card-based sections for readability
* Controlled interactions (no accidental actions)
* Consistent behavior across modules

---

## Current Status

* Fault Report module: Functional CRUD with styled UI
* PPE module: Fully functional with signature enforcement and role-based behavior
* System ready for ERP integration

---

## Author

FranzAfun
