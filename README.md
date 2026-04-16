# IBS Operations Management System

A Django-based CRUD platform for managing operational workflows within IBS.
Currently includes:

* Fault Report Management
* PPE Issue Management
* Employee-Issued IT Assets Management
* Operations Dashboard

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

Fully implemented asset issuance workflow using AssetRecord and AssetItem:

* AssetRecord stores employee-level issuance details
* AssetItem stores one or more issued assets per record
* Supports multi-item issuance per employee
* Complete list, detail, create, update, and delete flows
* Signature system aligned with PPE behavior:

  * Staff can sign issued assets
  * Creator cannot sign
  * Once any item is signed, the entire record is locked
  * Locked records cannot be edited or deleted

---

## Routes

* Dashboard -> /
* Fault Logs -> /faults/
* PPE Records -> /ppe/
* Asset Records -> /assets/

Common detail patterns:

* Create -> /new/
* Detail -> /<id>/
* Edit -> /<id>/edit/

---

## Project Structure

```text
ibs-fault-report/
├── config/
├── fault_logs/
├── ppe/
├── assets/
├── dashboard/
├── templates/
├── static/
├── manage.py
```

---

## Technical Stack

* Framework: Django
* Apps (current):

  * fault_logs
  * ppe_records
  * assets (fully implemented)
  * dashboard (entry point)
  * core
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

* Fault Report module: Complete
* PPE module: Complete with signature enforcement
* Assets module: Complete with signature and lock system
* Dashboard: Implemented as system entry point
* System ready for ERP integration

---

## Author

FranzAfun
