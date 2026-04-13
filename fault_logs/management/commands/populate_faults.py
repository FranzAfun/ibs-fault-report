from datetime import time, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from fault_logs.models import FaultReport


class Command(BaseCommand):
    help = (
        "Populate 15 realistic industrial FaultReport records for smart metering "
        "and fuel tank monitoring scenarios."
    )

    def handle(self, *args, **options):
        today = timezone.localdate()

        records = [
            {
                "reference_number": "FR-2026-0001",
                "days_ago": 32,
                "report_time": time(7, 45),
                "reporter_name": "Arman Rizal",
                "role": "Control Room Operator",
                "reporter_contact": "+62-811-7301-441 | arman.rizal@ibs.local",
                "location": "Terminal A - Smart Meter Node SM-14",
                "complaint_summary": "Smart meter at dispenser line 14 stopped transmitting consumption pulses during peak loading.",
                "investigation_findings": "Pulse output board on SM-14 was heat-stressed and intermittently failing after 18 minutes of operation.",
                "resolution": "Replaced pulse output board, reseated communication harness, and validated pulse continuity under full load.",
                "action_taken_by": "Instrumentation Team - R. Nugroho",
                "status": FaultReport.Status.CLOSED,
                "resolution_days": 2,
            },
            {
                "reference_number": "FR-2026-0002",
                "days_ago": 31,
                "report_time": time(9, 10),
                "reporter_name": "Maya Putri",
                "role": "Tank Farm Supervisor",
                "reporter_contact": "+62-812-9004-117 | maya.putri@ibs.local",
                "location": "Tank Farm B - Diesel Tank TK-03",
                "complaint_summary": "Fuel tank level dashboard displayed negative inventory values during morning reconciliation.",
                "investigation_findings": "Ultrasonic probe was offset by 27 mm due to a loosened mounting collar after vibration events.",
                "resolution": "Recalibrated probe reference zero, replaced collar assembly, and aligned inventory conversion table.",
                "action_taken_by": "Tank Instrumentation Unit - H. Yusran",
                "status": FaultReport.Status.RESOLVED,
                "resolution_days": 1,
            },
            {
                "reference_number": "FR-2026-0003",
                "days_ago": 29,
                "report_time": time(11, 25),
                "reporter_name": "Dian Prasetyo",
                "role": "SCADA Analyst",
                "reporter_contact": "+62-813-4422-506 | dian.prasetyo@ibs.local",
                "location": "Central Monitoring - AMI Gateway GW-02",
                "complaint_summary": "AMI gateway for smart metering cluster C went offline, causing delayed billing data ingestion.",
                "investigation_findings": "Gateway LTE modem firmware entered a reboot loop after corrupt APN profile sync.",
                "resolution": "Applied stable modem firmware build, restored APN profile from backup, and monitored for 12-hour stability.",
                "action_taken_by": "Telemetry Support - S. Hartanto",
                "status": FaultReport.Status.CLOSED,
                "resolution_days": 2,
            },
            {
                "reference_number": "FR-2026-0004",
                "days_ago": 27,
                "report_time": time(8, 35),
                "reporter_name": "Rina Maulida",
                "role": "Safety Officer",
                "reporter_contact": "+62-852-6001-844 | rina.maulida@ibs.local",
                "location": "Tank Farm A - Overfill Sensor OF-07",
                "complaint_summary": "Overfill alarm on TK-07 triggered repeatedly despite stable fill level and normal transfer rates.",
                "investigation_findings": "Condensation ingress inside junction box created intermittent high-resistance contacts on alarm line.",
                "resolution": "Re-terminated wiring, replaced sealing gland, and installed moisture-absorbing cartridge in enclosure.",
                "action_taken_by": "Electrical Maintenance - A. Wirawan",
                "status": FaultReport.Status.RESOLVED,
                "resolution_days": 2,
            },
            {
                "reference_number": "FR-2026-0005",
                "days_ago": 25,
                "report_time": time(10, 5),
                "reporter_name": "Fikri Wahono",
                "role": "Field Technician",
                "reporter_contact": "+62-813-1045-333 | fikri.wahono@ibs.local",
                "location": "Distribution Yard - Smart Valve Meter SMV-09",
                "complaint_summary": "Remote disconnect command completed but meter valve remained partially open on SMV-09.",
                "investigation_findings": "Actuator torque threshold parameter was set below required closing force after previous firmware update.",
                "resolution": "Adjusted torque threshold profile, executed controlled closure cycle, and verified zero-flow condition.",
                "action_taken_by": "Metering Reliability Team - T. Gunawan",
                "status": FaultReport.Status.CLOSED,
                "resolution_days": 3,
            },
            {
                "reference_number": "FR-2026-0006",
                "days_ago": 23,
                "report_time": time(13, 15),
                "reporter_name": "Nabila Siregar",
                "role": "Inventory Controller",
                "reporter_contact": "+62-811-5520-872 | nabila.siregar@ibs.local",
                "location": "Bulk Fuel Depot - Tank Cluster C",
                "complaint_summary": "Daily fuel reconciliation showed 1.8% variance between smart meter throughput and tank dip totals.",
                "investigation_findings": "Duplicate telemetry packets from one edge collector inflated totalized smart meter volume.",
                "resolution": "Enabled packet de-duplication on ingestion service and rebuilt daily totals from raw event timeline.",
                "action_taken_by": "Data Integration Team - P. Samuel",
                "status": FaultReport.Status.RESOLVED,
                "resolution_days": 1,
            },
            {
                "reference_number": "FR-2026-0007",
                "days_ago": 21,
                "report_time": time(14, 20),
                "reporter_name": "Yusuf Mahendra",
                "role": "Maintenance Planner",
                "reporter_contact": "+62-812-6610-098 | yusuf.mahendra@ibs.local",
                "location": "Station E - Smart Meter SM-22",
                "complaint_summary": "SM-22 reported repeated battery low alarms and unscheduled resets during load transitions.",
                "investigation_findings": "Backup battery pack had elevated internal resistance and failed to support modem startup current.",
                "resolution": "Replaced battery pack and updated preventive replacement interval from 24 to 18 months.",
                "action_taken_by": "Field Service - L. Febrianto",
                "status": FaultReport.Status.CLOSED,
                "resolution_days": 2,
            },
            {
                "reference_number": "FR-2026-0008",
                "days_ago": 19,
                "report_time": time(6, 55),
                "reporter_name": "Lina Ramadhani",
                "role": "Instrumentation Engineer",
                "reporter_contact": "+62-813-5509-210 | lina.ramadhani@ibs.local",
                "location": "Tank Farm D - Probe Cabinet PC-11",
                "complaint_summary": "Tank level trend for TK-11 became noisy and unreadable after overnight rainfall.",
                "investigation_findings": "Water ingress in probe cabinet caused signal grounding fluctuations on the 4-20mA channel.",
                "resolution": "Installed new IP67 cabinet door seal, replaced terminal strip, and validated stable signal variance <0.2%.",
                "action_taken_by": "Instrumentation Team - D. Akbar",
                "status": FaultReport.Status.RESOLVED,
                "resolution_days": 2,
            },
            {
                "reference_number": "FR-2026-0009",
                "days_ago": 17,
                "report_time": time(15, 40),
                "reporter_name": "Budi Santosa",
                "role": "Telemetry Technician",
                "reporter_contact": "+62-811-4308-765 | budi.santosa@ibs.local",
                "location": "Remote Meter Site RS-05",
                "complaint_summary": "Smart meter communication uptime at RS-05 dropped below SLA due to unstable GSM signal.",
                "investigation_findings": "Directional antenna alignment shifted 12 degrees after mast maintenance, reducing link quality.",
                "resolution": "Realigned antenna, tightened mast bracket, and updated alert threshold for early RF degradation warnings.",
                "action_taken_by": "Telecom Support - G. Kurnia",
                "status": FaultReport.Status.CLOSED,
                "resolution_days": 1,
            },
            {
                "reference_number": "FR-2026-0010",
                "days_ago": 15,
                "report_time": time(9, 50),
                "reporter_name": "Sarah Wijaya",
                "role": "Operations Superintendent",
                "reporter_contact": "+62-813-7702-401 | sarah.wijaya@ibs.local",
                "location": "Tank Farm C - Leak Detection Channel LD-04",
                "complaint_summary": "Fuel tank monitoring panel showed recurring micro-leak alerts without corresponding pressure drop.",
                "investigation_findings": "Leak channel baseline drifted after sensor replacement due to missed zero-baseline commissioning step.",
                "resolution": "Performed baseline recalibration and executed 6-hour pressure hold test with no leakage detected.",
                "action_taken_by": "Integrity Team - J. Wicaksono",
                "status": FaultReport.Status.RESOLVED,
                "resolution_days": 2,
            },
            {
                "reference_number": "FR-2026-0011",
                "days_ago": 13,
                "report_time": time(12, 5),
                "reporter_name": "Nina Kartika",
                "role": "Customer Interface Officer",
                "reporter_contact": "+62-812-7448-990 | nina.kartika@ibs.local",
                "location": "Smart Metering Hub - Prepaid Channel",
                "complaint_summary": "Multiple prepaid smart meters rejected valid top-up tokens during synchronization window.",
                "investigation_findings": "Token validation service had stale encryption key cache after scheduled key rotation.",
                "resolution": "Refreshed key cache across validation nodes and replayed failed token transactions from queue.",
                "action_taken_by": "Platform Operations - I. Hidayat",
                "status": FaultReport.Status.CLOSED,
                "resolution_days": 1,
            },
            {
                "reference_number": "FR-2026-0012",
                "days_ago": 11,
                "report_time": time(16, 30),
                "reporter_name": "Farhan Yulianto",
                "role": "Process Engineer",
                "reporter_contact": "+62-813-8806-331 | farhan.yulianto@ibs.local",
                "location": "Depot C - Tank Temperature Module TT-02",
                "complaint_summary": "Compensated volume calculations were overstated after noon due to missing temperature correction.",
                "investigation_findings": "Temperature compensation flag was disabled during previous diagnostics and not re-enabled.",
                "resolution": "Re-enabled compensation logic, validated API gravity correction, and regenerated daily stock report.",
                "action_taken_by": "Process Controls - M. Ridwan",
                "status": FaultReport.Status.RESOLVED,
                "resolution_days": 2,
            },
            {
                "reference_number": "FR-2026-0013",
                "days_ago": 9,
                "report_time": time(8, 20),
                "reporter_name": "Kevin Halim",
                "role": "Digital Systems Engineer",
                "reporter_contact": "+62-811-9210-554 | kevin.halim@ibs.local",
                "location": "Meter Lab - Firmware Validation Bench",
                "complaint_summary": "Latest smart meter firmware introduced intermittent counter freeze on high-frequency pulse inputs.",
                "investigation_findings": "Regression identified in interrupt debounce logic under edge-case burst traffic.",
                "resolution": "Rolled back affected meters to stable firmware and deployed hotfix with revised debounce routine.",
                "action_taken_by": "Embedded Systems Team - C. Aditya",
                "status": FaultReport.Status.CLOSED,
                "resolution_days": 2,
            },
            {
                "reference_number": "FR-2026-0014",
                "days_ago": 7,
                "report_time": time(5, 55),
                "reporter_name": "Putri Nirmala",
                "role": "Shift Supervisor",
                "reporter_contact": "+62-812-3300-612 | putri.nirmala@ibs.local",
                "location": "Generator Yard - Day Tank DT-01",
                "complaint_summary": "Low-level alarm on generator day tank remained latched after refill completion.",
                "investigation_findings": "Relay output card retained stale latch state after transient undervoltage on panel PSU.",
                "resolution": "Replaced output relay card and installed PSU line conditioner to prevent latch-state corruption.",
                "action_taken_by": "Electrical Reliability - F. Syahputra",
                "status": FaultReport.Status.RESOLVED,
                "resolution_days": 1,
            },
            {
                "reference_number": "FR-2026-0015",
                "days_ago": 5,
                "report_time": time(17, 10),
                "reporter_name": "Rafi Pranata",
                "role": "Data Quality Specialist",
                "reporter_contact": "+62-811-2107-478 | rafi.pranata@ibs.local",
                "location": "Central Data Hub - Fuel Telemetry Stream",
                "complaint_summary": "Fuel tank monitoring events arrived with timestamp skew causing incorrect incident chronology in dashboards.",
                "investigation_findings": "One edge gateway NTP source drifted by 94 seconds after fallback to local oscillator mode.",
                "resolution": "Repointed gateway to redundant NTP pool and backfilled corrected event timestamps to analytics store.",
                "action_taken_by": "Data Platform Team - W. Darman",
                "status": FaultReport.Status.CLOSED,
                "resolution_days": 1,
            },
        ]

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for item in records:
                report_date = today - timedelta(days=item["days_ago"])
                date_of_resolution = report_date + timedelta(days=item["resolution_days"])

                defaults = {
                    "report_date": report_date,
                    "report_time": item["report_time"],
                    "reporter_name": item["reporter_name"],
                    "role": item["role"],
                    "reporter_contact": item["reporter_contact"],
                    "location": item["location"],
                    "complaint_summary": item["complaint_summary"],
                    "investigation_findings": item["investigation_findings"],
                    "resolution": item["resolution"],
                    "action_taken_by": item["action_taken_by"],
                    "status": item["status"],
                    "date_of_resolution": date_of_resolution,
                }

                candidate = FaultReport(reference_number=item["reference_number"], **defaults)
                candidate.clean()

                _, created = FaultReport.objects.update_or_create(
                    reference_number=item["reference_number"],
                    defaults=defaults,
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"populate_faults completed: {created_count} created, {updated_count} updated (total {len(records)} records)."
            )
        )
