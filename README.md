# IBS Operations Management System

A Django-based CRUD platform for managing operational workflows within IBS.
Currently includes:

* Fault Report Management
* PPE Issue Management
* Employee-Issued IT Assets Management

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

### 3. Employee-Issued IT Assets Management

Manages issuance and tracking of IT assets assigned to employees:

* Track IT assets issued to employees
* Record asset type, serial numbers, and issue dates
* Maintain assignment per employee
* Provide list view with consistent action buttons (view, edit, delete)
* Provide detailed view with structured layout
* Support controlled updates and deletion
* Prepare for future enhancements like return tracking and audit logs

---

## Technical Stack

* Framework: Django
* Apps (current + planned):

  * fault_logs
  * ppe_records
  * it_assets (planned)
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
* Employee-Issued IT Assets module: Included in scope and structured for implementation
* System ready for ERP integration

---

## Author

FranzAfun
