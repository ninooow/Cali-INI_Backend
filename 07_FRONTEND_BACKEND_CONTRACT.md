**# 07_FRONTEND_BACKEND_CONTRACT.md — Cali-INI Frontend ↔ Backend Contract**



\> **\*\*Document Status:\*\*** Authoritative Frontend Contract for CURRENT Backend Implementation  

\> **\*\*Source of Truth:\*\*** Implemented FastAPI Backend (\`fastapi_app.py\`, \`models/\`, \`adapters/engine_adapter.py\`, \`services/intelligence_service.py\`)  

\> **\*\*Rule:\*\*** Frontend MUST NOT access PostgreSQL directly or import/execute \`intelligence_engine.py\`.



\---



**## 1. Purpose**



This document defines the strict, binding communication and data contract between:



$$\text{Vue Frontend} \longrightarrow \text{FastAPI REST Backend}$$



**### Architectural Boundary & Isolation**

In the target architecture of Cali-INI:

\`\`\`text

┌────────────────────────────────────────────────────────┐

│                   Vue 3 Frontend                       │

│     (UI Pages, Pinia Store, Visual Components)         │

└──────────────────────────┬─────────────────────────────┘

                           │ HTTP / JSON REST Calls

                           ▼

┌────────────────────────────────────────────────────────┐

│                  FastAPI Backend                       │

│  (Routers, Pydantic Validation, Route Handlers)        │

└──────────────┬───────────────────────────┬─────────────┘

               │                           │

               ▼                           ▼

┌───────────────────────────┐ ┌──────────────────────────┐

│   Database Layer (ORM)    │ │   Intelligence Service   │

│ (PostgreSQL / SQLite Dev) │ │ (EngineDataAdapter, Run) │

└───────────────────────────┘ └────────────┬─────────────┘

                                           │ DataFrames

                                           ▼

                              ┌──────────────────────────┐

                              │  intelligence_engine.py  │

                              └──────────────────────────┘

\`\`\`



1\. **\*\*No Direct Database Access:\*\*** The Vue application MUST NEVER connect directly to PostgreSQL or SQLite.

2\. **\*\*No Analytical Engine Execution:\*\*** The Vue application MUST NEVER import, execute, or replicate calculations from \`intelligence_engine.py\`.

3\. **\*\*No Direct Formula Evaluation:\*\*** Calculations such as condition classification, health index, PCA anomaly scores, Holt-Winters/polynomial forecasts, RCA case similarity ranking, or engineering weekly aggregations are strictly backend-owned.

4\. **\*\*Contract Fidelity:\*\*** The frontend can ONLY consume endpoints and schemas that are **\*\*actually implemented\*\*** in the FastAPI backend. Any frontend specification or design requirement that lacks an active backend endpoint is explicitly designated as \`NOT CURRENTLY EXPOSED BY BACKEND\`.



\---



**## 2. Backend Runtime Contract**



\| Dimension | Implemented Specification |

\|---|---|

\| **\*\*Canonical Entry Point\*\*** | \`fastapi_app.py\` (\`app = FastAPI(title=settings.PROJECT_NAME, openapi_url="/api/v1/openapi.json")\`) |

\| **\*\*API Route Prefix\*\*** | \`/api/v1\` (configured via \`settings.API_V1_PREFIX\` in \`config.py\`) |

\| **\*\*System Endpoints\*\*** | \`/health\` and \`/system\` (exposed at root, outside \`/api/v1\`) |

\| **\*\*OpenAPI / Swagger Documentation\*\*** | \`/docs\` (Swagger UI), \`/redoc\` (ReDoc), \`/api/v1/openapi.json\` |

\| **\*\*Content-Type\*\*** | \`application/json\` (both incoming requests and responses) |

\| **\*\*CORS Policy\*\*** | Permissive in development: \`allow_origins=["\*"]\`, \`allow_credentials=True\`, \`allow_methods=["\*"]\`, \`allow_headers=["\*"]\` |

\| **\*\*Response Envelope Convention\*\*** | **\*\*Consistent list wrapper:\*\*** All list/collection endpoints return an envelope: \`{"data": [...]}\`.\<br>Detail/single item endpoints return the entity object directly (e.g. \`{"asset_id": 1, ...}\`). |

\| **\*\*DateTime Serialization\*\*** | ISO 8601 strings formatted by Pydantic / Python datetime (e.g., \`"2026-10-03T12:00:00"\` or \`"2026-10-03T12:00:00Z"\`). |

\| **\*\*Authentication Status\*\*** | **\*\*NONE / DISABLED.\*\*** There are currently no authentication headers, Bearer tokens, API keys, or session cookies validated by FastAPI middleware or dependencies. |

\| **\*\*Authorization / RBAC Status\*\*** | **\*\*NOT ENFORCED AT RUNTIME.\*\*** The database and user schemas have a \`role\` field (e.g., \`"operator"\`, \`"reliability"\`, \`"engineer"\`), but endpoints do not check user roles or enforce route protection. |



\---



**## 3. Endpoint Inventory**



The current FastAPI backend includes the original operational endpoints plus the Q1–Q3 frontend-readiness APIs for analytics, asset configuration, and dashboard consumption. The endpoint table below is the authoritative runtime inventory:



\| Method | Implemented Endpoint | Domain | Purpose | Request Body / Parameters | Response Structure | Frontend Consumer Page |

\|---|---|---|---|---|---|---|

\| \`GET\` | \`/health\` | System | Basic service liveness probe | None | \`{"status": "healthy"}\` | Monitoring / Health Check |

\| \`GET\` | \`/system\` | System | DB connectivity validation | None | \`{"status": "healthy", "database": "connected"}\` | Monitoring / System Admin |

\| \`GET\` | \`/api/v1/assets\` | Assets | List assets with optional query filters | Query: \`search\`, \`plant\`, \`equipment_type\`, \`criticality\`, \`is_active\` | \`{"data": [AssetResponse, ...]}\` | Dashboard, Asset Management, Operations |

\| \`GET\` | \`/api/v1/assets/{asset_id}\` | Assets | Retrieve single asset profile | Path: \`asset_id\` (int) | \`AssetResponse\` | Asset Management Detail, Problem Verification |

\| \`GET\` | \`/api/v1/telemetry/hourly\` | Telemetry | List hourly time-series measurements | Query: \`asset_id\` (int), \`start\` (datetime), \`end\` (datetime) | \`{"data": [HourlyMeasurementResponse, ...]}\` | Operations → Data Input, Trend Charts |

\| \`POST\` | \`/api/v1/telemetry/hourly\` | Telemetry | Bulk insert hourly measurement rows | Body: \`List[HourlyMeasurementCreate]\` | \`{"data": [HourlyMeasurementResponse, ...]}\` (201 Created) | Operations → Data Input (Form / Upload) |

\| \`GET\` | \`/api/v1/reliability/incidents\` | Reliability | List historical incidents register | None | \`{"data": [IncidentResponse, ...]}\` | Reliability → Incident Register |

\| \`GET\` | \`/api/v1/reliability/incidents/{incident_id}\` | Reliability | Retrieve single incident detail | Path: \`incident_id\` (int) | \`IncidentResponse\` | Reliability → Incident Workspace |

\| \`POST\` | \`/api/v1/reliability/incidents\` | Reliability | Bulk create historical incident records | Body: \`List[IncidentCreate]\` | \`{"data": [IncidentResponse, ...]}\` (201 Created) | Reliability → New Incident / Seeder Import |

\| \`GET\` | \`/api/v1/reliability/rca\` | Reliability | List all RCA headers | None | \`{"data": [RcaHeaderResponse, ...]}\` | Reliability → RCA Investigation List |

\| \`GET\` | \`/api/v1/reliability/rca/{ar_no}\` | Reliability | Retrieve RCA header by AR Number | Path: \`ar_no\` (str) | \`RcaHeaderResponse\` | Reliability → RCA Investigation Detail |

\| \`POST\` | \`/api/v1/reliability/rca\` | Reliability | Bulk create RCA header records | Body: \`List[RcaHeaderCreate]\` | \`{"data": [RcaHeaderResponse, ...]}\` (201 Created) | Reliability → RCA Investigation |

\| \`GET\` | \`/api/v1/reliability/rca/{ar_no}/priority-matrix\` | Reliability | List root cause priority matrix rows | Path: \`ar_no\` (str) | \`{"data": [PriorityMatrixResponse, ...]}\` | Problem Workspace / RCA Investigation |

\| \`POST\` | \`/api/v1/reliability/rca/{ar_no}/priority-matrix\` | Reliability | Bulk create RCA priority matrix rows | Path: \`ar_no\` (str)\<br>Body: \`List[PriorityMatrixCreate]\` | \`{"data": [PriorityMatrixResponse, ...]}\` (201 Created) | RCA Investigation |

\| \`GET\` | \`/api/v1/reliability/rca/{ar_no}/4p\` | Reliability | List 4P verification items for AR | Path: \`ar_no\` (str) | \`{"data": [Rca4pResponse, ...]}\` | RCA Investigation → 4P Tab |

\| \`POST\` | \`/api/v1/reliability/rca/{ar_no}/4p\` | Reliability | Bulk create 4P verification items | Path: \`ar_no\` (str)\<br>Body: \`List[Rca4pCreate]\` | \`{"data": [Rca4pResponse, ...]}\` (201 Created) | RCA Investigation → 4P Tab |

\| \`GET\` | \`/api/v1/reliability/rca/{ar_no}/4m\` | Reliability | List 4M verification items for AR | Path: \`ar_no\` (str) | \`{"data": [Rca4mResponse, ...]}\` | RCA Investigation → 4M Tab |

\| \`POST\` | \`/api/v1/reliability/rca/{ar_no}/4m\` | Reliability | Bulk create 4M verification items | Path: \`ar_no\` (str)\<br>Body: \`List[Rca4mCreate]\` | \`{"data": [Rca4mResponse, ...]}\` (201 Created) | RCA Investigation → 4M Tab |

\| \`GET\` | \`/api/v1/reliability/rca/{ar_no}/capa\` | Reliability | List CAPA actions for AR | Path: \`ar_no\` (str) | \`{"data": [CapaActionResponse, ...]}\` | Reliability → CAPA Tracking / Detail |

\| \`POST\` | \`/api/v1/reliability/rca/{ar_no}/capa\` | Reliability | Bulk create CAPA actions | Path: \`ar_no\` (str)\<br>Body: \`List[CapaActionCreate]\` | \`{"data": [CapaActionResponse, ...]}\` (201 Created) | Reliability → CAPA Form |

\| \`GET\` | \`/api/v1/workflow/tickets\` | Workflow | List all problem tickets | None | \`{"data": [ProblemTicketResponse, ...]}\` | Dashboard, Problem Verification |

\| \`GET\` | \`/api/v1/workflow/tickets/{ticket_id}\` | Workflow | Get single problem ticket detail | Path: \`ticket_id\` (str) | \`ProblemTicketResponse\` | Problem Workspace → Detail |

\| \`POST\` | \`/api/v1/workflow/tickets\` | Workflow | Create a problem ticket (with initial AuditLog) | Body: \`ProblemTicketCreate\` | \`{"data": [ProblemTicketResponse]}\` (201 Created) | Problem Verification / Engine Dispatch |

\| \`PATCH\` | \`/api/v1/workflow/tickets/{ticket_id}\` | Workflow | Update ticket status, operator decision, observations | Path: \`ticket_id\` (str)\<br>Body: \`ProblemTicketUpdate\` | \`ProblemTicketResponse\` | Problem Workspace → Operator Action Modal |

\| \`GET\` | \`/api/v1/workflow/tickets/{ticket_id}/audit_logs\` | Workflow | Get history/audit log for ticket | Path: \`ticket_id\` (str) | \`{"data": [AuditLogResponse, ...]}\` | Problem Workspace → History & Audit Log |

\| \`GET\` | \`/api/v1/users\` | Administration | List registered users | None | \`{"data": [UserResponse, ...]}\` | Administration → Users |

\| \`GET\` | \`/api/v1/users/{user_id}\` | Administration | Get user by ID | Path: \`user_id\` (int) | \`UserResponse\` | Administration → User Detail |

\| \`POST\` | \`/api/v1/users\` | Administration | Create a new user account | Body: \`UserCreate\` | \`{"data": [UserResponse]}\` (201 Created) | Administration → User Create Modal |

\| \`PATCH\` | \`/api/v1/users/{user_id}\` | Administration | Update existing user account | Path: \`user_id\` (int)\<br>Body: \`UserUpdate\` | \`UserResponse\` | Administration → User Edit Modal |



\| `GET` | `/api/v1/analytics/runs` | Analytics | List analysis runs | Query: `status` | `{"data": [...]}` | Analytics / Dashboard |
\| `GET` | `/api/v1/analytics/runs/latest` | Analytics | Get latest analysis run | None | Analysis run object | Dashboard |
\| `GET` | `/api/v1/analytics/runs/{run_id}` | Analytics | Get analysis run by ID | Path: `run_id` | Analysis run object | Analytics |
\| `GET` | `/api/v1/analytics/condition-inferences` | Analytics | Read condition inference results | Query: `run_id`, `asset_id`, `priority` | `{"data": [...]}` | Dashboard / Problem Workspace |
\| `GET` | `/api/v1/analytics/parameter-forecasts` | Analytics | Read parameter forecasts | Query: `run_id`, `asset_id`, `canonical_param` | `{"data": [...]}` | Dashboard / Trend Analysis |
\| `GET` | `/api/v1/analytics/rca-matches` | Analytics | Read ranked RCA matches | Query: `run_id`, `asset_id`, `matched_ar_no` | `{"data": [...]}` | Problem Workspace |
\| `GET` | `/api/v1/assets/{asset_id}/tags` | Assets | List sensor tags for asset | Path: `asset_id` | `{"data": [...]}` | Asset Management |
\| `GET` | `/api/v1/sensor-tags` | Assets | List/filter sensor tags | Query: `asset_id`, `canonical_param`, `is_active` | `{"data": [...]}` | Asset Management |
\| `GET` | `/api/v1/assets/{asset_id}/limits` | Assets | List equipment limits for asset | Path: `asset_id` | `{"data": [...]}` | Asset Management |
\| `GET` | `/api/v1/equipment-limits` | Assets | List/filter equipment limits | Query: `asset_id`, `parameter` | `{"data": [...]}` | Asset Management |
\| `GET` | `/api/v1/analytics/dashboard` | Analytics | Dashboard overview | None | `DashboardOverviewResponse` | Dashboard |

\---



**## 4. Detailed Request and Response Contracts**



**### 4.1 Asset Domain**



**#### List Assets**

\- **\*\*Method & Path:\*\*** \`GET /api/v1/assets\`

\- **\*\*Query Parameters (All Optional):\*\***

  - \`search\`: string (case-insensitive substring filter on \`tag_number\`)

  - \`plant\`: string (exact match on \`plant_code\`)

  - \`equipment_type\`: string (exact match on \`equipment_type\`)

  - \`criticality\`: string (exact match on \`criticality\`, e.g., \`"HIGH"\`, \`"MEDIUM"\`, \`"LOW"\`)

  - \`is_active\`: boolean (\`true\` or \`false\`)

\- **\*\*Response Format (\`200 OK\`):\*\***

\`\`\`json

{

  "data": [

    {

      "asset_id": 1,

      "tag_number": "31-PM-01A",

      "asset_name": "Quench Water Pump A",

      "equipment_type": "Pump",

      "equipment_class": "Rotary",

      "plant_code": "PL01",

      "discipline": "Mechanical",

      "criticality": "HIGH",

      "is_active": true

    }

  ]

}

\`\`\`



**#### Get Asset Detail**

\- **\*\*Method & Path:\*\*** \`GET /api/v1/assets/{asset_id}\`

\- **\*\*Response Format (\`200 OK\`):\*\***

\`\`\`json

{

  "asset_id": 1,

  "tag_number": "31-PM-01A",

  "asset_name": "Quench Water Pump A",

  "equipment_type": "Pump",

  "equipment_class": "Rotary",

  "plant_code": "PL01",

  "discipline": "Mechanical",

  "criticality": "HIGH",

  "is_active": true

}

\`\`\`



*\*Note on Asset Schema:\**

\- \`asset_id\` is system-generated (\`PKBigInteger\`).

\- Fields like \`plant_unit\`, \`design_life\`, \`monitoring_method\`, \`core_mode\`, \`fla_amp\`, \`linked_rca_ar_no\`, \`failure_date\`, \`dominant_failure_mode\` exist in the SQLAlchemy model (\`core.assets\`), but **\*\*are currently omitted\*\*** from \`AssetResponse\`. The frontend receives only the 9 fields shown above.



\---



**### 4.2 Telemetry Domain**



**#### List Hourly Measurements**

\- **\*\*Method & Path:\*\*** \`GET /api/v1/telemetry/hourly\`

\- **\*\*Query Parameters (All Optional):\*\***

  - \`asset_id\`: integer

  - \`start\`: ISO 8601 datetime (e.g. \`2026-10-01T00:00:00\`)

  - \`end\`: ISO 8601 datetime (e.g. \`2026-10-03T23:59:59\`)

\- **\*\*Ordering:\*\*** Sorted descending by \`measured_at\` (\`ORDER BY measured_at DESC\`).

\- **\*\*Response Format (\`200 OK\`):\*\***

\`\`\`json

{

  "data": [

    {

      "asset_id": 1,

      "measured_at": "2026-10-03T12:00:00",

      "feed": 125.4,

      "disp": 4.2,

      "vib": 2.15,

      "temp": 68.4,

      "amp": 142.0,

      "plant_rate": 98.5,

      "run_status": "ON",

      "source_type": "MANUAL"

    }

  ]

}

\`\`\`



**#### Create Hourly Measurements (Bulk)**

\- **\*\*Method & Path:\*\*** \`POST /api/v1/telemetry/hourly\`

\- **\*\*Status Code:\*\*** \`201 Created\`

\- **\*\*Request Body:\*\*** JSON Array of measurement objects (minimum 1 item):

\`\`\`json

[

  {

    "asset_id": 1,

    "measured_at": "2026-10-03T13:00:00",

    "feed": 126.1,

    "disp": 4.1,

    "vib": 2.20,

    "temp": 69.0,

    "amp": 143.2,

    "plant_rate": 99.0,

    "run_status": "ON",

    "source_type": "MANUAL"

  }

]

\`\`\`

\- **\*\*Validation Rules:\*\***

  - \`asset_id\`: required (validated against DB; if nonexistent returns \`400 Bad Request: Asset(s) not found: {id}\`).

  - \`measured_at\`: required (ISO datetime).

  - \`run_status\`: optional, but if supplied must be one of \`["ON", "OFF", "UNKNOWN"]\`.

  - \`source_type\`: defaults to \`"MANUAL"\`.



\---



**### 4.3 Reliability Domain**



**#### Incident Register**

\- **\*\*List Incidents:\*\*** \`GET /api/v1/reliability/incidents\`

\- **\*\*Get Incident Detail:\*\*** \`GET /api/v1/reliability/incidents/{incident_id}\`

\- **\*\*Create Incidents (Bulk):\*\*** \`POST /api/v1/reliability/incidents\` (\`201 Created\`)

\- **\*\*Incident Response Body:\*\***

\`\`\`json

{

  "incident_id": 101,

  "ar_no": "AR-2026-089",

  "plant": "PL01",

  "equipment_class": "Rotary",

  "date_of_occurrence": "2026-08-15T00:00:00",

  "risk_score": 12.0,

  "pic_rca": "Budi Santoso",

  "overall_status": "CLOSED",

  "discipline": "Mechanical",

  "equipment_type": "Centrifugal Pump",

  "component": "Mechanical Seal",

  "failure_mechanism": "Seal Face Wear / Excessive Heat",

  "downtime_hours": 6.5,

  "actual_loss_kusd": 18.4,

  "potential_loss_kusd": 50.0,

  "total_loss_kusd": 68.4,

  "rca_due_date": "2026-09-15T00:00:00",

  "source_type": "MANUAL",

  "created_at": "2026-08-15T10:00:00",

  "updated_at": "2026-08-20T14:30:00"

}

\`\`\`



**#### RCA Headers**

\- **\*\*List RCA Headers:\*\*** \`GET /api/v1/reliability/rca\`

\- **\*\*Get RCA Header:\*\*** \`GET /api/v1/reliability/rca/{ar_no}\`

\- **\*\*Create RCA Headers (Bulk):\*\*** \`POST /api/v1/reliability/rca\` (\`201 Created\`)

\- **\*\*RCA Header Response Body:\*\***

\`\`\`json

{

  "rca_header_id": 45,

  "ar_no": "AR-2026-089",

  "tag_number": "31-PM-01A",

  "plant": "PL01",

  "date_occurrence": "2026-08-15T00:00:00",

  "pre_risk": "HIGH",

  "risk_score": 12.0,

  "pic_rca": "Budi Santoso",

  "procedure_no": "SOP-MEC-31-01",

  "problem_statement": "Elevated vibration and sudden seal leakage during normal rate operation",

  "root_cause_statement": "Thermal degradation of secondary fluoroelastomer O-ring due to flush fluid restriction",

  "source_type": "MANUAL",

  "created_at": "2026-08-16T08:00:00",

  "updated_at": "2026-08-20T14:30:00"

}

\`\`\`



**#### RCA Priority Matrix**

\- **\*\*List:\*\*** \`GET /api/v1/reliability/rca/{ar_no}/priority-matrix\`

\- **\*\*Create (Bulk):\*\*** \`POST /api/v1/reliability/rca/{ar_no}/priority-matrix\`

\- **\*\*Response Item:\*\***

\`\`\`json

{

  "priority_matrix_id": 12,

  "ar_no": "AR-2026-089",

  "root_cause_id": "RC-01",

  "impact_level": "HIGH",

  "control_level": "MEDIUM",

  "priority_rank": 1,

  "description_short": "Plan 11 flush orifice blockage",

  "created_at": "2026-08-16T09:00:00"

}

\`\`\`



**#### RCA 4P Verification (Paper, People, Plant, Process)**

\- **\*\*List:\*\*** \`GET /api/v1/reliability/rca/{ar_no}/4p\`

\- **\*\*Create (Bulk):\*\*** \`POST /api/v1/reliability/rca/{ar_no}/4p\`

\- **\*\*Response Item:\*\***

\`\`\`json

{

  "verification_id": 88,

  "ar_no": "AR-2026-089",

  "parameter_id": "P-01",

  "problem_phenomenon_parameter": "Seal flush piping inspection",

  "result": "VERIFIED",

  "evidence_finding": "Orifice fouled with coke particulates; flush flow reduced by 70%",

  "created_at": "2026-08-17T11:00:00"

}

\`\`\`



**#### RCA 4M Verification (Man, Machine, Method, Material)**

\- **\*\*List:\*\*** \`GET /api/v1/reliability/rca/{ar_no}/4m\`

\- **\*\*Create (Bulk):\*\*** \`POST /api/v1/reliability/rca/{ar_no}/4m\`

\- **\*\*Response Item:\*\***

\`\`\`json

{

  "verification_id": 92,

  "ar_no": "AR-2026-089",

  "factor_id": "M-02",

  "factor_category": "Machine",

  "result": "CONFIRMED",

  "evidence_finding": "O-ring hardened and cracked (Shore A hardness increased to 95)",

  "created_at": "2026-08-17T11:30:00"

}

\`\`\`



**#### RCA CAPA Actions**

\- **\*\*List:\*\*** \`GET /api/v1/reliability/rca/{ar_no}/capa\`

\- **\*\*Create (Bulk):\*\*** \`POST /api/v1/reliability/rca/{ar_no}/capa\`

\- **\*\*Response Item:\*\***

\`\`\`json

{

  "capa_id": 34,

  "ar_no": "AR-2026-089",

  "rc": "RC-01",

  "action_type": "CORRECTIVE",

  "action_plan": "Replace Plan 11 orifice and install flush strainer with differential pressure indicator",

  "target_date": "2026-10-30T00:00:00",

  "pic": "Ahmad Fauzi",

  "status": "OPEN",

  "fingerprint": "a3f5b72e1c9d8e4f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f",

  "created_at": "2026-08-18T10:00:00",

  "updated_at": "2026-08-18T10:00:00"

}

\`\`\`

*\*Note:\** \`fingerprint\` is a mandatory 64-character SHA-256 hash preventing duplicate action plans.



\---



**### 4.4 Workflow / Problem Tickets Domain**



**#### List Problem Tickets**

\- **\*\*Method & Path:\*\*** \`GET /api/v1/workflow/tickets\`

\- **\*\*Response Format (\`200 OK\`):\*\***

\`\`\`json

{

  "data": [

    {

      "ticket_id": "TICKET-20261003-31PM01A",

      "asset_id": 1,

      "opened_at": "2026-10-03T08:00:00",

      "condition_state": "ANOMALY",

      "priority": "P1",

      "owner_role": "Operator",

      "ticket_state": "OPEN",

      "action_status": "NOT_STARTED",

      "normal_streak": 0,

      "matched_rca_ar": "AR-2026-089",

      "evidence_strength": "STRONG",

      "operator_decision": null,

      "last_operator_name": null,

      "operator_comment": null,

      "field_observation": null,

      "update_source": "ENGINE",

      "last_observation_time": null,

      "created_at": "2026-10-03T08:05:00",

      "updated_at": "2026-10-03T08:05:00"

    }

  ]

}

\`\`\`



**#### Get Ticket Detail**

\- **\*\*Method & Path:\*\*** \`GET /api/v1/workflow/tickets/{ticket_id}\`

\- **\*\*Response Format (\`200 OK\`):\*\*** Single \`ProblemTicketResponse\` object (as above).



**#### Create Ticket (Manual / Programmatic Dispatch)**

\- **\*\*Method & Path:\*\*** \`POST /api/v1/workflow/tickets\`

\- **\*\*Status Code:\*\*** \`201 Created\`

\- **\*\*Request Body (\`ProblemTicketCreate\`):\*\***

\`\`\`json

{

  "ticket_id": "TICKET-20261003-31PM01A",

  "asset_id": 1,

  "opened_at": "2026-10-03T08:00:00",

  "condition_state": "ANOMALY",

  "priority": "P1",

  "owner_role": "Operator",

  "ticket_state": "OPEN",

  "action_status": "NOT_STARTED",

  "normal_streak": 0,

  "matched_rca_ar": "AR-2026-089",

  "evidence_strength": "STRONG",

  "update_source": "ENGINE"

}

\`\`\`

*\*Backend Side-Effect:\** Automatically appends an \`AuditLog\` record with \`event_type="CREATE"\`.



**#### Update Ticket (Operator Verification Action)**

\- **\*\*Method & Path:\*\*** \`PATCH /api/v1/workflow/tickets/{ticket_id}\`

\- **\*\*Status Code:\*\*** \`200 OK\`

\- **\*\*Request Body (\`ProblemTicketUpdate\` — all fields optional):\*\***

\`\`\`json

{

  "ticket_state": "IN_PROGRESS",

  "action_status": "INVESTIGATING",

  "operator_decision": "CONFIRMED",

  "last_operator_name": "Rian Kusuma",

  "operator_comment": "Verified mechanical seal gland temperature above 75 degC.",

  "field_observation": "Acoustic emission detected from inboard bearing housing.",

  "last_observation_time": "2026-10-03T11:45:00"

}

\`\`\`

*\*Backend Side-Effect:\** Automatically writes an \`AuditLog\` entry with \`update_source="OPERATOR"\` capturing \`previous_ticket_state\`, \`new_ticket_state\`, \`previous_action_status\`, and \`new_action_status\`.



**#### Get Ticket Audit Logs**

\- **\*\*Method & Path:\*\*** \`GET /api/v1/workflow/tickets/{ticket_id}/audit_logs\`

\- **\*\*Ordering:\*\*** Sorted descending by \`event_time\` (\`ORDER BY event_time DESC\`).

\- **\*\*Response Format (\`200 OK\`):\*\***

\`\`\`json

{

  "data": [

    {

      "audit_id": 501,

      "event_time": "2026-10-03T11:45:00",

      "ticket_id": "TICKET-20261003-31PM01A",

      "asset_id": 1,

      "update_source": "OPERATOR",

      "event_type": "UPDATE",

      "previous_ticket_state": "OPEN",

      "new_ticket_state": "IN_PROGRESS",

      "previous_action_status": "NOT_STARTED",

      "new_action_status": "INVESTIGATING",

      "operator_decision": "CONFIRMED",

      "operator_name": "Rian Kusuma",

      "owner_role": null,

      "field_observation": "Acoustic emission detected from inboard bearing housing.",

      "comment": "Verified mechanical seal gland temperature above 75 degC."

    },

    {

      "audit_id": 500,

      "event_time": "2026-10-03T08:05:00",

      "ticket_id": "TICKET-20261003-31PM01A",

      "asset_id": 1,

      "update_source": null,

      "event_type": "CREATE",

      "previous_ticket_state": null,

      "new_ticket_state": "OPEN",

      "previous_action_status": null,

      "new_action_status": "NOT_STARTED",

      "operator_decision": null,

      "operator_name": null,

      "owner_role": null,

      "field_observation": null,

      "comment": null

    }

  ]

}

\`\`\`



\---



**### 4.5 User Administration Domain**



**#### List Users**

\- **\*\*Method & Path:\*\*** \`GET /api/v1/users\`

\- **\*\*Response Format (\`200 OK\`):\*\***

\`\`\`json

{

  "data": [

    {

      "user_id": 1,

      "username": "operator1",

      "display_name": "Rian Kusuma",

      "email": "rian.kusuma\@chandraasri.net",

      "employee_id": "EMP-3042",

      "role": "operator",

      "discipline": "Operations",

      "is_active": true,

      "created_at": "2026-09-01T08:00:00",

      "updated_at": "2026-09-01T08:00:00"

    }

  ]

}

\`\`\`



**#### Get User Detail**

\- **\*\*Method & Path:\*\*** \`GET /api/v1/users/{user_id}\`

\- **\*\*Response Format (\`200 OK\`):\*\*** Single \`UserResponse\` object.



**#### Create User**

\- **\*\*Method & Path:\*\*** \`POST /api/v1/users\`

\- **\*\*Status Code:\*\*** \`201 Created\`

\- **\*\*Request Body (\`UserCreate\`):\*\***

\`\`\`json

{

  "username": "reliability_lead",

  "display_name": "Siti Nurhaliza",

  "email": "siti.n\@chandraasri.net",

  "employee_id": "EMP-1029",

  "role": "reliability_engineer",

  "discipline": "Reliability",

  "is_active": true

}

\`\`\`

*\*Note:\** Returns \`409 Conflict: Username already exists\` if \`username\` is already registered.



**#### Update User**

\- **\*\*Method & Path:\*\*** \`PATCH /api/v1/users/{user_id}\`

\- **\*\*Status Code:\*\*** \`200 OK\`

\- **\*\*Request Body (\`UserUpdate\`):\*\***

\`\`\`json

{

  "display_name": "Siti Nurhaliza, ST",

  "email": "siti.nurhaliza\@chandraasri.net",

  "role": "reliability_lead",

  "is_active": true

}

\`\`\`



\---



**### 4.6 Analytics Domain (Runtime REST Exposure)**

Q1 analytics read APIs are implemented and read persisted analytical outputs. The frontend must treat these values as read-only engine/system results.

- `GET /api/v1/analytics/runs` — optional filter: `status`.
- `GET /api/v1/analytics/runs/latest` — latest analysis run.
- `GET /api/v1/analytics/runs/{run_id}` — analysis run by ID.
- `GET /api/v1/analytics/condition-inferences` — filters: `run_id`, `asset_id`, `priority`.
- `GET /api/v1/analytics/parameter-forecasts` — filters: `run_id`, `asset_id`, `canonical_param`; ordered by `target_time`.
- `GET /api/v1/analytics/rca-matches` — filters: `run_id`, `asset_id`, `matched_ar_no`; ordered by `rank_no`.
- `GET /api/v1/analytics/dashboard` — dashboard overview containing header, attention summary/items, and active asset count.

Persisted analytics entities remain `AnalysisRun`, `ConditionInference`, `ParameterForecast`, and `RcaMatch`. No engine formulas may be reproduced in Vue.

\---

**## 5. Frontend Page → Backend Mapping**

\| Frontend Area | Implemented Endpoint(s) | Support Status | Notes |
\|---|---|---|---|
\| **Dashboard** | `/api/v1/analytics/dashboard`, `/api/v1/analytics/condition-inferences`, `/api/v1/analytics/parameter-forecasts`, `/api/v1/assets`, `/api/v1/telemetry/hourly` | **PARTIALLY SUPPORTED** | Header, attention, active asset count, persisted inference/forecast data and raw telemetry are available. Unsupported aggregate KPI formulas must display `N/A`; never calculate them in Vue. |
\| **Operations → Data Input** | `GET/POST /api/v1/telemetry/hourly`, `GET /api/v1/assets` | **SUPPORTED** | Hourly input and historical review supported. |
\| **Operations → Problem Verification** | `/api/v1/workflow/tickets`, analytics inference endpoints | **SUPPORTED** | Ticket workflow plus persisted analytical condition data available. |
\| **Problem Workspace → Evidence & RCA** | `/api/v1/analytics/rca-matches`, `/api/v1/reliability/rca/{ar_no}` | **SUPPORTED** | Ranked RCA candidates and RCA detail are exposed. |
\| **Problem Workspace → History & Audit** | `/api/v1/workflow/tickets/{id}/audit_logs` | **SUPPORTED** | Audit history available. |
\| **Reliability → Incident/RCA** | `/api/v1/reliability/incidents`, `/api/v1/reliability/rca/*` | **SUPPORTED** | Existing reliability workflow remains supported. |
\| **Reliability → CAPA Tracking** | `/api/v1/reliability/rca/{ar_no}/capa` | **PARTIALLY SUPPORTED** | Supported per AR; no global CAPA list endpoint. |
\| **Asset Management → Assets** | `/api/v1/assets`, `/api/v1/assets/{id}` | **SUPPORTED** | Existing asset registry APIs. |
\| **Asset Management → Sensor & Parameters** | `/api/v1/assets/{asset_id}/tags`, `/api/v1/sensor-tags` | **SUPPORTED** | Asset-scoped and filterable tag reads are exposed. |
\| **Asset Management → Equipment Limits** | `/api/v1/assets/{asset_id}/limits`, `/api/v1/equipment-limits` | **SUPPORTED** | Asset-scoped and filterable limit reads are exposed. |
\| **Administration → Users** | `/api/v1/users`, `/api/v1/users/{id}` | **SUPPORTED** | Existing user administration APIs. |

\---

**## 6. Dashboard Backend Availability Comparison**

\| Dashboard Capability | Current Backend Status | Source / Rule |
\|---|---|---|
\| **Header Status & Time** | **SUPPORTED** | `/api/v1/analytics/dashboard` returns `scope`, `as_of`, and `data_status`. |
\| **Attention Required** | **SUPPORTED** | Dashboard endpoint returns active-ticket counts by P1–P4 and attention items. |
\| **Active Assets** | **SUPPORTED** | Dashboard endpoint returns `active_assets_count`. |
\| **Condition / Health analytical records** | **SUPPORTED AS PERSISTED ANALYTICS** | `/api/v1/analytics/condition-inferences`. Do not invent a plant-level aggregate KPI. |
\| **Trend Analysis** | **SUPPORTED** | Raw trends from `/api/v1/telemetry/hourly`; forecast traces from `/api/v1/analytics/parameter-forecasts`. |
\| **Parameter Forecasts** | **SUPPORTED** | Forecast estimate, bounds, model family, anchor/target times are exposed. |
\| **RCA Candidate Ranking** | **SUPPORTED** | `/api/v1/analytics/rca-matches`. |
\| **Plant Health Score** | **NOT CURRENTLY EXPOSED AS DASHBOARD KPI** | Display `N/A`; do not calculate in Vue. |
\| **Operating Performance Index** | **NOT CURRENTLY EXPOSED** | Display `N/A`. |
\| **Reliability & Consequence Index** | **NOT CURRENTLY EXPOSED** | Display `N/A`. |
\| **Normalized Load / Production Index** | **NOT CURRENTLY EXPOSED** | Display `N/A`. |
\| **Emission Intensity Proxy** | **NOT CURRENTLY EXPOSED** | Display `N/A`. |

\---

**## 7. Analytical Data Rules & Provenance**



To protect analytical integrity, the frontend must observe strict data ownership rules:



\`\`\`text

┌────────────────────────────────────────────────────────┐

│               ENGINE / SYSTEM CONTROLLED               │

│                  (STRICTLY READ-ONLY)                  │

├────────────────────────────────────────────────────────┤

│ • Condition State (NORMAL, WATCH, WARNING, ANOMALY)   │

│ • Priority Rank (P1, P2, P3, P4)                       │

│ • Health Index / PCA Anomaly Score                     │

│ • Parameter Forecast Estimates & Bounds                │

│ • Matched RCA AR Number & Case Similarity              │

│ • Evidence Strength (STRONG, MODERATE, WEAK)           │

│ • Normal Streak Counter                                │

│ • Reference / Analysis Timestamps                      │

└────────────────────────────────────────────────────────┘

                           ▲

                           │ Never mutate via UI

                           │

┌────────────────────────────────────────────────────────┐

│                     USER EDITABLE                      │

│            (OPERATOR / RELIABILITY WORKFLOW)           │

├────────────────────────────────────────────────────────┤

│ • Ticket State (OPEN, IN_PROGRESS, CLOSED)             │

│ • Action Status (NOT_STARTED, INVESTIGATING, ...)      │

│ • Operator Decision (CONFIRMED, FALSE_ALARM, ...)     │

│ • Field Observation & Physical Symptoms                │

│ • Operator Comment / Notes                             │

│ • Last Operator Name & Observation Time                │

│ • CAPA Action Plans, PIC, Target Dates                 │

│ • Manual Hourly Telemetry Entries                      │

│ • User Account Attributes (display_name, email, etc.) │

└────────────────────────────────────────────────────────┘

\`\`\`



**### Relational Hierarchy in Analytics Engine**

The exposed analytics endpoints follow this persisted relational model:

$$\text{AnalysisRun} \xrightarrow{1:N} \begin{cases}

\text{ConditionInference} & (\text{1 per asset per run}) \\\\

\text{ParameterForecast} & (\text{N per asset: parameter } \times \text{ target time}) \\\\

\text{RcaMatch} & (\text{N ranked candidate ARs per asset})

\end{cases}$$



\---



**## 8. Problem Workflow Contract**



The problem workflow is mediated by \`ProblemTicket\` and \`AuditLog\`.



**### Implemented Problem Ticket Lifecycle**

1\. **\*\*Creation:\*\*** Problem tickets are opened either by the analytical engine upon detecting an anomaly (\`update_source="ENGINE"\`) or via \`POST /api/v1/workflow/tickets\`.

2\. **\*\*Review & Verification:\*\*** The operator reviews the ticket in Problem Workspace and submits field observations via \`PATCH /api/v1/workflow/tickets/{ticket_id}\`.

3\. **\*\*Audit Logging:\*\*** Every create or update operation automatically creates an unalterable \`AuditLog\` row recording who changed what and the transition timestamps.



**### Permitted / Confirmed Field Values**

\- **\*\*\`ticket_state\`:\*\***

  - \`"OPEN"\` (Default upon creation)

  - \`"IN_PROGRESS"\` (Under operator or reliability review)

  - \`"RESOLVED"\` / \`"CLOSED"\`

\- **\*\*\`action_status\`:\*\***

  - \`"NOT_STARTED"\` (Default)

  - \`"INVESTIGATING"\`

  - \`"ACTION_TAKEN"\`

  - \`"MONITORING"\`

  - \`"COMPLETED"\`

\- **\*\*\`operator_decision\`:\*\***

  - \`"CONFIRMED"\` (Physical verification confirmed anomaly)

  - \`"MONITOR"\` (Keep observing, no immediate trip risk)

  - \`"FALSE_ALARM"\` (Instrument glitch or transient spike)

\- **\*\*\`condition_state\` (Engine controlled):\*\***

  - \`"NORMAL"\`

  - \`"WATCH"\`

  - \`"WARNING"\`

  - \`"ANOMALY"\`

\- **\*\*\`priority\` (Engine controlled):\*\***

  - \`"P1"\` (Immediate action / critical risk)

  - \`"P2"\` (Urgent review required)

  - \`"P3"\` (Elevated parameter monitoring)

  - \`"P4"\` (Advisory / normal)



\---



**## 9. Reliability / RCA Knowledge Base Contract**



Historical incidents and Root Cause Analyses form a linked relational graph:



\`\`\`text

Incident Record (ar_no, plant, risk_score, downtime, losses)

   │

   ▼ (Linked via ar_no)

RCA Header (ar_no, problem_statement, root_cause_statement, procedure_no)

   │

   ├──► RCA Priority Matrix (ar_no, root_cause_id, priority_rank, impact_level)

   ├──► RCA 4P Verification (ar_no, parameter_id, result, evidence_finding)

   ├──► RCA 4M Verification (ar_no, factor_id, factor_category, result)

   └──► RCA CAPA Actions    (ar_no, rc, action_plan, target_date, pic, status)

\`\`\`



**### Identifiers & Relational Linking**

\- The canonical identifier connecting all reliability artifacts is **\*\*\`ar_no\`\*\*** (Action Request Number, e.g. \`"AR-2026-089"\`).

\- In \`Incident\`, \`incident_id\` is an internal surrogate integer PK, but \`ar_no\` represents the business key.

\- In \`RCA Header\`, \`ar_no\` is unique and serves as the foreign key target for Priority Matrix, 4P, 4M, and CAPA tables.

\- In \`ProblemTicket\`, when an asset exhibits symptoms matching historical incidents, the backend stores the matched reference in \`ProblemTicket.matched_rca_ar\`. The frontend can navigate directly to the RCA investigation using this key:

  $$\text{ProblemTicket.matched\\\_rca\\\_ar} \longrightarrow \text{GET } \texttt{/api/v1/reliability/rca/\\{matched\\\_rca\\\_ar\\}}$$



\---



**## 10. Asset & Telemetry Contract**



**### Canonical Identifiers**

\- **\*\*\`asset_id\`\*\*** (Integer, primary key): Used for API navigation, filtering telemetry, and database relations.

\- **\*\*\`tag_number\`\*\*** (String, unique business identifier): e.g., \`"31-PM-01A"\`. Displayed in headings, cards, and tables.



**### Telemetry Field Units & Mapping**

The implemented \`HourlyMeasurement\` schema defines six core operational channels:

1\. \`feed\`: Process Feed Rate (Numeric)

2\. \`disp\`: Discharge Pressure / Flow (Numeric)

3\. \`vib\`: Vibration amplitude (Numeric, mm/s RMS)

4\. \`temp\`: Bearing / Casing Temperature (Numeric, °C)

5\. \`amp\`: Motor Current (Numeric, Amperes)

6\. \`plant_rate\`: Overall Plant Operating Rate (Numeric, %)

7\. \`run_status\`: Operating status (\`"ON"\`, \`"OFF"\`, \`"UNKNOWN"\`)



**### Weekly Measurement Handling**

\- Weekly measurements exist in the database table \`telemetry.weekly_measurements\` as pivoted longitudinal indicators (\`Health Status\`, \`Remark\`, weekly sensor aggregates).

\- **\*\*CRITICAL RULE:\*\*** Weekly measurement is **\*\*NOT an operator input form\*\***.

\- The Vue frontend **\*\*must never\*\*** attempt to calculate weekly aggregates (means, medians, peak-holds) from hourly data. Weekly derivation is strictly an offline / backend-owned engineering process.



\---



**## 11. Filtering, Pagination, Sorting, and Search Contract**



The following query behaviors are **\*\*confirmed implemented\*\*** in the FastAPI routes:



\| Endpoint | Implemented Filters / Query Parameters | Pagination Status | Sorting Status |

\|---|---|---|---|

\| \`GET /api/v1/assets\` | • \`search\` (ilike on \`tag_number\`)\<br>• \`plant\` (exact match \`plant_code\`)\<br>• \`equipment_type\` (exact match)\<br>• \`criticality\` (exact match)\<br>• \`is_active\` (boolean) | \`NOT CURRENTLY IMPLEMENTED\`\<br>(Returns all matching rows) | \`NOT CURRENTLY IMPLEMENTED\`\<br>(Database default order) |

\| \`GET /api/v1/telemetry/hourly\` | • \`asset_id\` (int)\<br>• \`start\` (datetime $\ge$)\<br>• \`end\` (datetime $\le$) | \`NOT CURRENTLY IMPLEMENTED\`\<br>(Returns all matching rows) | **\*\*IMPLEMENTED\*\***\<br>\`ORDER BY measured_at DESC\` |

\| \`GET /api/v1/reliability/incidents\` | None | \`NOT CURRENTLY IMPLEMENTED\` | \`NOT CURRENTLY IMPLEMENTED\` |

\| \`GET /api/v1/reliability/rca\` | None | \`NOT CURRENTLY IMPLEMENTED\` | \`NOT CURRENTLY IMPLEMENTED\` |

\| \`GET /api/v1/reliability/rca/{ar_no}/\*\` | Keyed by \`ar_no\` path param | \`NOT CURRENTLY IMPLEMENTED\` | \`NOT CURRENTLY IMPLEMENTED\` |

\| \`GET /api/v1/workflow/tickets\` | None | \`NOT CURRENTLY IMPLEMENTED\` | \`NOT CURRENTLY IMPLEMENTED\` |

\| \`GET /api/v1/workflow/tickets/{id}/audit_logs\` | Keyed by \`ticket_id\` path param | \`NOT CURRENTLY IMPLEMENTED\` | **\*\*IMPLEMENTED\*\***\<br>\`ORDER BY event_time DESC\` |

\| \`GET /api/v1/users\` | None | \`NOT CURRENTLY IMPLEMENTED\` | \`NOT CURRENTLY IMPLEMENTED\` |



*\*Guidance for Frontend:\**  

Because server-side pagination (\`limit\`, \`offset\`, \`page\`) is currently **\*\*NOT implemented\*\*** on any list endpoint, the frontend should:

1\. Provide client-side pagination where large row counts are expected (e.g., Incident Register or Telemetry tables).

2\. Constrain telemetry requests by always providing explicit \`asset_id\`, \`start\`, and \`end\` datetime parameters.



\---



**## 12. Error and Empty-State Contract**



The backend adheres to standard HTTP status codes and error conventions:



**### Observable HTTP Status Codes**

\- **\*\*\`200 OK\`\*\***: Successful query or update.

\- **\*\*\`201 Created\`\*\***: Successful entity creation. Returns the newly created object or list in \`{"data": [...]}\`.

\- **\*\*\`400 Bad Request\`\*\***:

  - Unrecognized foreign keys (e.g. \`POST /api/v1/telemetry/hourly\` with invalid \`asset_id\` returns \`{"detail": "Asset(s) not found: {9999}"}\`).

  - AR Number mismatch between URL path and body payload (returns \`{"detail": "ar_no mismatch"}\`).

\- **\*\*\`404 Not Found\`\*\***:

  - Single entity lookup with nonexistent ID:

    - Asset: \`{"detail": "Asset not found"}\`

    - Incident: \`{"detail": "Incident not found"}\`

    - RCA Header: \`{"detail": "RCA header not found"}\`

    - Problem Ticket: \`{"detail": "Ticket not found"}\`

    - User: \`{"detail": "User not found"}\`

\- **\*\*\`409 Conflict\`\*\***:

  - Creating a user with a duplicate username: \`{"detail": "Username already exists"}\`.

\- **\*\*\`422 Unprocessable Entity\`\*\***:

  - Standard FastAPI / Pydantic validation failure. Returns \`{ "detail": [ { "loc": [...], "msg": "...", "type": "..." } ] }\`.

  - Triggered, for example, if \`run_status\` in hourly telemetry is not \`"ON"\`, \`"OFF"\`, or \`"UNKNOWN"\`.



**### Empty Collection Convention**

When an endpoint returns a list and no records match the criteria, the backend returns:

\`\`\`json

{

  "data": []

}

\`\`\`

The frontend should check \`data.length === 0\` to render appropriate empty states.



\---



**## 13. Frontend Integration Rules**



The future Vue frontend development agent MUST adhere to the following rules:



1\. **\*\*Strict REST Boundary:\*\*** Never attempt to connect directly to PostgreSQL or SQLite.

2\. **\*\*Never Execute Analytical Code:\*\*** Never import or execute \`intelligence_engine.py\`, and never recreate Python machine-learning, PCA anomaly scoring, or forecasting routines in TypeScript/Vue.

3\. **\*\*No Weekly Engineering Derivations:\*\*** Never compute weekly trend consolidations in the frontend. Treat weekly data as backend-owned.

4\. **\*\*No Synthetic API Endpoints:\*\*** Never assume or invoke endpoints that are not listed in Section 3 of this document.

5\. **\*\*No Invented Enums:\*\*** Restrict status, decision, and category values strictly to the values validated by backend models (see Section 8).

6\. **\*\*Read-Only Engine Provenance:\*\*** Treat condition state, priority, health score, PCA score, forecasts, and matched RCA candidate rankings as strictly read-only.

7\. **\*\*Use Canonical IDs for Routing:\*\*** Use numeric \`asset_id\` for telemetry/asset routes and string \`ar_no\` for RCA routes. Use \`tag_number\` solely for presentation headers.

8\. **\*\*Handle Nullable Analytics Gracefully:\*\*** In all components rendering inference, forecast, or RCA data, provide defensive fallbacks for \`null\` or \`undefined\` values.

9\. **\*\*Separate Domain Concepts:\*\*** Maintain a crisp visual and semantic distinction between:

   - Equipment Condition (\`NORMAL\`, \`WATCH\`, \`WARNING\`, \`ANOMALY\`)

   - Risk Priority (\`P1\`, \`P2\`, \`P3\`, \`P4\`)

   - Ticket Workflow State (\`OPEN\`, \`IN_PROGRESS\`, \`CLOSED\`)

   - Action Verification Status (\`NOT_STARTED\`, \`INVESTIGATING\`, \`COMPLETED\`)



\---



**## 14. Backend Gaps Blocking or Impacting Frontend**

Q1–Q3 removed the former analytics, dashboard-summary, sensor-tag, and equipment-limit blockers. Remaining gaps are non-blocking for the frontend MVP:

\| Gap | Status / Frontend Rule |
\|---|---|
\| Aggregate dashboard KPIs (Plant Health Score, Operating Performance, Reliability & Consequence, Normalized Load/Production, Emission Proxy) | Not exposed. Render `N/A`; never derive them in Vue. |
\| Global CAPA list | Not exposed. Use per-AR `/api/v1/reliability/rca/{ar_no}/capa`. |
\| Server-side pagination/sorting | Not generally implemented. Use constrained queries and client-side handling for MVP. |
\| Authentication/session endpoints | Not implemented and outside current scope. Do not invent auth flows. |

\---

**## 15. Frontend Readiness Summary**

The backend is **ready for frontend MVP development**. Q1–Q3 expose analytics reads, dashboard overview, sensor tags, and equipment limits in addition to the previously implemented asset, telemetry, reliability, workflow, and user APIs.

**Ready now:** Dashboard foundation, Operations/Data Input, Problem Verification, Evidence/RCA ranking, Incident/RCA workflows, Asset Management including Sensor Tags and Equipment Limits, and Administration/Users.

**Known constraints:** unsupported aggregate dashboard KPIs must display `N/A`; global CAPA remains AR-scoped; authentication is outside current scope.

**Validation checkpoint (2026-10-04):** Q1–Q3 endpoints were smoke-tested against PostgreSQL and returned successfully. No engine rerun was required.
