from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)
from xml.sax.saxutils import escape

out = Path("output/pdf/redline-operations-technical-handover.pdf")
out.parent.mkdir(parents=True, exist_ok=True)
navy = HexColor("#0B1422")
red = HexColor("#C93943")
ink = HexColor("#1B2635")
muted = HexColor("#607080")
pale = HexColor("#EFF3F7")
s = getSampleStyleSheet()
s.add(
    ParagraphStyle(
        name="cover",
        parent=s["Title"],
        fontName="Helvetica-Bold",
        fontSize=30,
        leading=36,
        textColor=colors.white,
        alignment=TA_LEFT,
        spaceAfter=18,
    )
)
s.add(
    ParagraphStyle(
        name="subcover",
        parent=s["Normal"],
        fontSize=14,
        leading=21,
        textColor=HexColor("#CFD9E5"),
    )
)
s.add(
    ParagraphStyle(
        name="titlex",
        parent=s["Heading1"],
        fontSize=20,
        leading=24,
        textColor=ink,
        spaceAfter=10,
    )
)
s.add(
    ParagraphStyle(
        name="subx",
        parent=s["Heading2"],
        fontSize=11,
        leading=14,
        textColor=red,
        spaceBefore=6,
        spaceAfter=4,
    )
)
s.add(
    ParagraphStyle(
        name="bodyx",
        parent=s["BodyText"],
        fontSize=9,
        leading=13,
        textColor=ink,
        spaceAfter=6,
    )
)
s.add(
    ParagraphStyle(
        name="smallx",
        parent=s["BodyText"],
        fontSize=7.7,
        leading=10,
        textColor=ink,
        spaceAfter=4,
    )
)
s.add(
    ParagraphStyle(
        name="bulx",
        parent=s["BodyText"],
        fontSize=8.5,
        leading=11.5,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3,
        textColor=ink,
    )
)
s.add(
    ParagraphStyle(
        name="callx",
        parent=s["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8.7,
        leading=12,
        textColor=HexColor("#7D252D"),
        backColor=HexColor("#FFF1F1"),
        borderColor=HexColor("#E8C4C7"),
        borderWidth=0.5,
        borderPadding=7,
        spaceBefore=4,
        spaceAfter=7,
    )
)
s.add(
    ParagraphStyle(
        name="codex",
        parent=s["Code"],
        fontName="Courier",
        fontSize=7.7,
        leading=10.5,
        textColor=ink,
        backColor=pale,
        borderPadding=7,
        leftIndent=6,
        rightIndent=6,
        spaceBefore=4,
        spaceAfter=7,
    )
)
s.add(
    ParagraphStyle(
        name="tocx", parent=s["BodyText"], fontSize=8.5, leading=13, textColor=ink
    )
)


def P(x, st="bodyx"):
    return Paragraph(x, s[st])


def page(title, kicker, items):
    a = [P(kicker.upper(), "smallx"), P(title, "titlex")]
    for kind, x in items:
        if kind == "p":
            a.append(P(x))
        elif kind == "h":
            a.append(P(x, "subx"))
        elif kind == "b":
            a.extend(P("- " + z, "bulx") for z in x)
        elif kind == "c":
            a.append(P(x, "callx"))
        elif kind == "code":
            a.append(P(x.replace("\n", "<br/>"), "codex"))
        elif kind == "table":
            rows = [[P(escape(str(v)), "smallx") for v in r] for r in x]
            widths = [1.35 * inch] + [(6.3 * inch - 1.35 * inch) / (len(x[0]) - 1)] * (
                len(x[0]) - 1
            )
            t = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            t.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), navy),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#D3DCE5")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, pale]),
                        ("LEFTPADDING", (0, 0), (-1, -1), 5),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ]
                )
            )
            a.extend([t, Spacer(1, 7)])
    return a


pages = []
pages.append(
    [
        Spacer(1, 1.1 * inch),
        P("REDLINE<br/>OPERATIONS", "cover"),
        P(
            "Technical project handover<br/>Emergency Operations Center coordination network",
            "subcover",
        ),
        Spacer(1, 1.2 * inch),
        P("SOURCE-GROUNDED SYSTEM REVIEW  |  15 NOVEMBER 2026", "smallx"),
        Spacer(1, 0.2 * inch),
        P(
            "Prepared for senior engineering, architecture, project review and technical transition. Describes the supplied implementation and distinguishes it from future recommendations.",
            "subcover",
        ),
    ]
)
names = [
    "Executive summary",
    "Project vision and operational context",
    "System overview and current workflow",
    "Technology stack and rationale",
    "Architecture and component boundaries",
    "Feature inventory: overview and command views",
    "Feature inventory: response departments",
    "Feature inventory: logistics and public information",
    "Feature inventory: network and continuity",
    "Page-by-page guide and navigation",
    "UI/UX design decisions",
    "Data model and lifecycle",
    "Security design and gaps",
    "Disaster response workflow and scenario",
    "Engineering decisions and tradeoffs",
    "Differentiation and business value",
    "Scalability, availability, and recovery",
    "Roadmap and delivery sequencing",
    "Lessons learned",
    "Conclusion and handover checklist",
]
rows = [[P("SEC.", "smallx"), P("SECTION", "smallx"), P("PAGE", "smallx")]] + [
    [P(str(i), "tocx"), P(n, "tocx"), P(str(i + 2), "tocx")]
    for i, n in enumerate(names, 1)
]
t = Table(
    rows,
    colWidths=[0.55 * inch, 5.15 * inch, 0.6 * inch],
    rowHeights=[0.24 * inch] + [0.245 * inch] * 20,
)
t.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), navy),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#D3DCE5")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, pale]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
pages.append(
    [
        P("DOCUMENT GUIDE", "smallx"),
        P("Contents", "titlex"),
        P(
            "Page numbers include cover and contents. This report is grounded in the source project at Desktop/redline. UI labels and sample values are described as prototype content, not verified live telemetry."
        ),
        t,
        Spacer(1, 8),
        P(
            "Evidence rule: separate implemented behavior, presentational claims, and recommended production capabilities.",
            "callx",
        ),
    ]
)
pages.append(
    page(
        "Executive summary",
        "01 | Project purpose",
        [
            ("h", "Purpose and problem"),
            (
                "p",
                "Redline Operations is presented as an Emergency Operations Center (EOC) coordination platform for disaster response. It addresses operational fragmentation: command staff, dispatch, medical services, logistics, infrastructure and public information need a shared operating picture. The current project demonstrates a command-center interface and network segmentation concept in a single-page React application.",
            ),
            ("h", "Audience and expected impact"),
            (
                "p",
                "Target roles represented include EOC operator, dispatch coordinator, medical coordinator, logistics lead, public information officer, network/security operator and continuity administrator. Intended outcomes are faster awareness, clearer prioritization, controlled interdepartmental communication and continuity during a site outage.",
            ),
            ("h", "What exists today"),
            (
                "b",
                [
                    "Nine views: Overview, VLAN Segments, ACL Security, Coordination Server, Remote Site Sync, Dispatch Center, Medical Network, Logistics Network and Public Information.",
                    "Operational cards and records are in source constants; interactions mostly update local React state or show notices.",
                    "Stack is React 19, TypeScript, Vite and Tailwind CSS. No backend, database, authentication library, map SDK or API client appears in the inspected project.",
                ],
            ),
            (
                "c",
                "Prototype boundary: the UI communicates the shape of an EOC product, but its values and status indicators are not connected to real emergency operations. Treat it as a demonstrator, not a dispatch or life-safety system.",
            ),
            ("h", "Handover outcome"),
            (
                "p",
                "This report provides a page guide, technical baseline, target data/security model, response workflow and prioritized next steps without presenting proposed infrastructure as deployed capability.",
            ),
        ],
    )
)
pages.append(
    page(
        "Project vision and operational context",
        "02 | Why an EOC platform",
        [
            ("h", "Operational problem"),
            (
                "p",
                "Disaster response crosses organizations. Incident facts may arrive through calls, field radio, public reports, hospital feeds and infrastructure operators. Separate tools and inconsistent status language obscure which incident is authoritative, which units are committed, where supplies are available and what the public has been told.",
            ),
            ("h", "Vision"),
            (
                "p",
                "Redline’s stated vision is a common coordination environment where incident status, resource posture, infrastructure health and verified advisories can be reviewed together. The prototype makes the concept visible through persistent departmental navigation and compact operational panels.",
            ),
            ("h", "Operational goals"),
            (
                "b",
                [
                    "Present a shared, prioritized picture that can be scanned under time pressure.",
                    "Reduce handoff ambiguity by associating work with incidents, assignments and status.",
                    "Expose constrained capacity, communications health and site continuity.",
                    "Support coordinated public messaging after verification.",
                    "Create an auditable record and after-action evidence in a future connected release.",
                ],
            ),
            ("h", "Users and decisions"),
            (
                "p",
                "Dispatch validates calls and assigns responders; medical coordination needs receiving capacity; logistics needs inventory and convoy status; public information needs controlled publishing; infrastructure staff need network/failover context; command needs escalation and an overall picture.",
            ),
            (
                "c",
                "The README states the product narrative. Specific incidents, counts, addresses, network addresses and facility values in the interface are illustrative sample data, not verified facts.",
            ),
            ("h", "Success measures"),
            (
                "p",
                "For production, measure acknowledgement and assignment time, stale/conflicting updates, resource utilization, advisory verification latency, availability during connectivity loss and after-action record completeness.",
            ),
        ],
    )
)
pages.append(
    page(
        "System overview and current workflow",
        "03 | Product shape",
        [
            (
                "p",
                "Redline is a browser single-page dashboard. A fixed sidebar changes the selected section without a route transition; a shared top bar holds status controls; the content region changes to show metrics, panels and actions. Responsive CSS collapses the sidebar and reflows panels on narrow screens.",
            ),
            ("h", "Current interaction path"),
            (
                "code",
                "Operator opens Overview\n -> reviews sample network posture and incident feed\n -> selects a department or infrastructure view\n -> changes filters, toggles, text or checkboxes\n -> local React state updates visible UI\n -> page reload restores source-defined initial state",
            ),
            ("h", "Architecture diagram - as implemented"),
            (
                "code",
                "Browser\n  React App (navigation + conditional view rendering)\n    |-- in-file constants (sample incidents, VLANs, logs)\n    |-- in-memory useState (filters, toggles, forms, notices)\n    |-- App.css + index.css (presentation/responsive layout)\n  Vite development/build toolchain\n  No network service, API, persistence layer or database",
            ),
            ("h", "Intended product journey"),
            (
                "p",
                "An authorized operator signs in, joins an incident or operational period, verifies incoming reports, coordinates assignments, receives field status, escalates needs, updates public information through approval, and closes the incident with a durable record. Only the visual navigation concept and local interaction examples are implemented.",
            ),
            ("h", "System boundary"),
            (
                "p",
                "No implemented identity boundary, multi-user synchronization, map, integration adapter, durable storage, notification transport or incident lifecycle service is in the inspected source.",
            ),
        ],
    )
)
pages.append(
    page(
        "Technology stack and rationale",
        "04 | Dependencies found",
        [
            (
                "table",
                [
                    [
                        "Technology",
                        "Purpose / observed use",
                        "Fit, alternatives and tradeoffs",
                    ],
                    [
                        "React 19",
                        "UI rendering and local state in src/App.tsx.",
                        "Declarative UI and ecosystem. Alternatives: Vue, Svelte, Angular. Monolithic view should be decomposed.",
                    ],
                    [
                        "TypeScript 6",
                        "Typed sections, icons, records and state.",
                        "Catches structural errors at build time. Alternatives: JS or other typed stacks. Types do not validate runtime payloads.",
                    ],
                    [
                        "Vite 8",
                        "Development and production bundling.",
                        "Fast modern ESM toolchain. Alternatives: webpack, Parcel, framework build tools. Not a backend or host.",
                    ],
                    [
                        "Tailwind CSS 4",
                        "Imported through Vite plugin; current visual styling is primarily handwritten CSS.",
                        "Can accelerate consistent styling. Alternatives: CSS Modules, vanilla CSS. Mixed conventions need governance.",
                    ],
                    [
                        "React DOM",
                        "Browser rendering entry in src/main.tsx.",
                        "Standard React web target.",
                    ],
                ],
            ),
            ("h", "Runtime and deployment facts"),
            (
                "p",
                "package.json defines dev, build, lint and preview scripts. Vite uses React and Tailwind plugins. No Node/Express app, Supabase client, PostgreSQL driver, map integration, auth SDK, cloud SDK or hosting configuration appears in the inspected files.",
            ),
            ("h", "Selection rationale and alternatives"),
            (
                "p",
                "The stack is a small, familiar frontend setup for rapid iteration and static builds. The repository does not record decision documents; rationales here are architectural fit assessments, not historical selection claims. Choose backend, database, identity, mapping and hosting only after operational, residency, security, availability and offline requirements are agreed.",
            ),
            (
                "c",
                "Backend technology is not selected in code. PostgreSQL, Supabase, Node.js, maps, identity services and cloud hosting are unselected options, not deployed components.",
            ),
        ],
    )
)
pages.append(
    page(
        "Architecture and component boundaries",
        "05 | Current and target boundaries",
        [
            ("h", "Frontend today"),
            (
                "p",
                "src/main.tsx mounts App. App.tsx owns section types, navigation definitions, seed arrays, metrics, view rendering and interactions. App.css defines component/layout styling; index.css imports Tailwind and global rules. View selection is conditional JSX rather than route/page modules.",
            ),
            ("h", "Request and data flow today"),
            (
                "p",
                "There is no application request lifecycle. Vite serves development assets and produces frontend output. React renders constants; actions update local component state. No authenticated session, database query or cross-user event is performed by inspected UI.",
            ),
            ("h", "Recommended architecture"),
            (
                "code",
                "Browser UI (typed feature modules)\n -> API gateway / application service\n    -> identity + policy enforcement\n    -> incident, resource, reports and comms services\n    -> relational store + audit ledger\n    -> integration adapters (GIS, hospitals, alerts)\n -> event broker / notification workers\n -> observability, backup, recovery and admin controls",
            ),
            ("h", "Suggested boundaries"),
            (
                "b",
                [
                    "Shell: navigation, operating period, identity, incident severity and connection state.",
                    "Features: incident, resource assignment, medical capacity, logistics, advisories and continuity operations.",
                    "Shared contracts: validated schemas, identifiers, timestamps, status enums and authorization rules.",
                    "Integration layer: monitored adapters with retries, idempotency, source attribution and health reporting.",
                ],
            ),
            ("h", "Security target"),
            (
                "p",
                "Use managed identity with MFA for privileged roles, server-side authorization, encrypted transport/storage, auditable changes, least-privilege service identities and tested recovery. None is proven by presentational labels.",
            ),
        ],
    )
)
pages.append(
    page(
        "Feature inventory: overview and command views",
        "06 | Platform functions",
        [
            ("h", "Overview dashboard"),
            (
                "p",
                "Purpose: orient command staff to network posture and active signals. It displays four network metrics, an illustrated core/VLAN topology, segment utilization, dispatch feed, ACL summary and remote sync status. Buttons navigate or show notices; metrics are static sample values.",
            ),
            ("h", "VLAN Segments"),
            (
                "p",
                "Purpose: inspect segmented network capacity/status. It shares the Overview rendering path and describes Dispatch, Medical, Logistics and Public Info segments. Subnets, host capacity and bandwidth are sample data; device discovery or telemetry ingestion is absent.",
            ),
            ("h", "ACL Security"),
            (
                "p",
                "Purpose: illustrate policy posture and review access events. Sample rules, simulated source/destination/protocol selectors and seeded permit/drop entries are shown. Simulation appends local state; it does not configure a firewall or query enforcement hardware.",
            ),
            ("h", "Business value if connected"),
            (
                "p",
                "A verified command view can reduce context switching and surface deterioration early. A live implementation must disclose source, timestamp, confidence and stale state for every signal.",
            ),
            ("h", "Technical implementation"),
            (
                "p",
                "Composition uses static arrays, conditional JSX, Icon and Metric helpers and local React state in App.tsx. No domain service, persistence, event stream or backend authorization exists for these features.",
            ),
        ],
    )
)
pages.append(
    page(
        "Feature inventory: response departments",
        "07 | Dispatch and medical",
        [
            ("h", "Dispatch Center"),
            (
                "p",
                "The view presents sample incident metrics, a filterable queue with severity, one selected structure-fire assignment panel, four selectable units, escalation and assignment feedback. Filters and selection are local. New Incident and Assign actions provide visual feedback; no dispatch record or unit task is persisted.",
            ),
            ("h", "Medical Network"),
            (
                "p",
                "Displays sample bed counts for six named facilities, occupancy, triage category totals, ambulance availability and routing card. Route action produces a notice only. No HL7/FHIR or hospital feed is implemented; facility values are not verified live data.",
            ),
            ("h", "Production workflow needs"),
            (
                "b",
                [
                    "Incident: unique ID, source, location, received/verified time, severity, status, owner and history.",
                    "Assignment: capability match, availability lock, accepting unit, dispatch/arrival times and cancellation/reassignment reason.",
                    "Capacity: source/freshness, service types, confidence, update policy and fallback contact.",
                    "High-impact actions: server authorization, conflict handling, idempotency and audit evidence.",
                ],
            ),
            ("h", "Business value"),
            (
                "p",
                "Connected, governed workflows could support mobilization and destination decisions. Until integrations and authoritative data exist, mark cards prominently as demo data to avoid operational confusion.",
            ),
        ],
    )
)
pages.append(
    page(
        "Feature inventory: logistics and public information",
        "08 | Supply and alerts",
        [
            ("h", "Logistics Network"),
            (
                "p",
                "Sample view shows convoy status, supply readiness, distribution sites, next delivery, inventory for water/rations/generators/fuel and a convoy list with location/ETA. Refresh and route actions show transient notices. Inventory, telemetry and geospatial routing are not service-backed.",
            ),
            ("h", "Public Information"),
            (
                "p",
                "Includes broadcast posture, advisory count/reach, a 280-character composer, publish button and local advisory list. Publish prepends text to React state. No approval, identity check, channel, delivery receipt or durable public record exists.",
            ),
            ("h", "Operational controls to add"),
            (
                "b",
                [
                    "Inventory ledger: units, lot/source, reserved/on-hand/available quantity and reconciliation.",
                    "Convoy: manifest, driver/vehicle, route, check-ins, exceptions and proof of delivery.",
                    "Message lifecycle: draft, review, approval, scheduled, published, amended, withdrawn; preserve actor and timestamps.",
                    "Channel audience, translation, accessibility, delivery acknowledgement and correction procedure.",
                ],
            ),
            ("h", "Risk and value"),
            (
                "p",
                "Stale inventory or unapproved instructions can cause harm. Usefulness depends on reliable sources, freshness, ownership, review controls and fallback communications.",
            ),
        ],
    )
)
pages.append(
    page(
        "Feature inventory: network and continuity",
        "09 | Infrastructure operator views",
        [
            ("h", "Coordination Server"),
            (
                "p",
                "Shows sample core health, CPU, memory, database synchronization, host/IP/subnet/gateway, uptime and backup time. PostgreSQL/protocol names are UI literals; no server monitor, database connection, replication agent or backup task is present.",
            ),
            ("h", "Remote Site Sync"),
            (
                "p",
                "Displays primary and Continuity Center backup sites, replication wording and a sync time. Failover control toggles local state/copy. It does not route traffic, promote a database or prevent split brain.",
            ),
            ("h", "Topology and VLANs"),
            (
                "p",
                "Illustrates four segments with example private IP ranges and host utilization. It communicates intended logical segmentation. Source does not provision VLANs, apply ACLs, inspect packets or validate reachability.",
            ),
            ("h", "Continuity requirements"),
            (
                "p",
                "Production failover needs health checks, quorum/leader semantics, fencing, data-loss objectives, traffic changes, secrets access, authorization and rollback. Test restore from real backups and measure RPO/RTO.",
            ),
            (
                "c",
                "Never treat “LIVE,” “protected,” “synced” or “secure connection” as proof of actual service state. Derive operational status from monitored evidence, freshness and source details.",
            ),
        ],
    )
)
pages.append(
    page(
        "Page-by-page guide and navigation",
        "10 | All selectable views",
        [
            (
                "table",
                [
                    ["View", "Purpose and content", "Action / dependency"],
                    [
                        "Overview",
                        "Command posture, topology, VLANs, feed, ACL, remote sync.",
                        "Navigation/sample actions; no backend.",
                    ],
                    [
                        "VLAN Segments",
                        "Segment capacity and topology.",
                        "Shares Overview path; sample data.",
                    ],
                    [
                        "ACL Security",
                        "Illustrative rules and permit/drop feed.",
                        "Local simulation; no firewall API.",
                    ],
                    [
                        "Coordination Server",
                        "Core service and node health panels.",
                        "No monitoring API.",
                    ],
                    [
                        "Remote Site Sync",
                        "Primary/backup status and failover.",
                        "Local toggle only.",
                    ],
                    [
                        "Dispatch Center",
                        "Incident queue, filters, assignment.",
                        "Local state and notices.",
                    ],
                    [
                        "Medical Network",
                        "Capacity, triage, ambulance routing.",
                        "No hospital API.",
                    ],
                    [
                        "Logistics Network",
                        "Inventory and convoy status.",
                        "No logistics API.",
                    ],
                    [
                        "Public Information",
                        "Composer and active advisories.",
                        "Local state only.",
                    ],
                ],
            ),
            ("h", "Shared shell"),
            (
                "p",
                "All views use the same sidebar and top bar. The top bar includes alert-level selector, failover control, notification affordance and uptime. Sidebar navigation changes section state; mobile menu opens the sidebar over a backdrop.",
            ),
            ("h", "Requested pages not present"),
            (
                "p",
                "No separate login, incident detail, emergency map, reports, settings, admin console, profile or notification-center page is present. There is no route framework. The profile card is static shell content, not an account workflow.",
            ),
            ("h", "Navigation lifecycle"),
            (
                "p",
                "Navigation changes state and rendered branch. No URL/deep link, permission gate, browser history workflow or unsaved-form warning is evident. Future routes should make access and return paths explicit.",
            ),
        ],
    )
)
pages.append(
    page(
        "UI/UX design decisions",
        "11 | Interaction and visual system",
        [
            ("h", "Visual hierarchy"),
            (
                "p",
                "Dark navy surfaces, red emphasis, uppercase labels, compact system type and dense panels create a command-center appearance. Metrics precede detail panels; color and short words communicate priority. Document color meanings and never use color alone.",
            ),
            ("h", "Responsive behavior"),
            (
                "p",
                "CSS breakpoints near 1200, 950 and 680 px adjust sidebar, panel columns, metric grids and navigation. On mobile the sidebar becomes an off-canvas drawer, spacing tightens and some table columns hide. Validate field devices, zoom, landscape and low bandwidth.",
            ),
            ("h", "Accessibility observed and gaps"),
            (
                "p",
                "Global styles define keyboard focus outlines on controls; buttons and labels are used for many actions. Add semantic landmarks/headings, names for icon-only actions, status announcements, mobile focus management, contrast checks, non-color status cues and reduced motion.",
            ),
            ("h", "Information safety"),
            (
                "p",
                "Metrics should expose value, unit, source and update time; distinguish unknown, stale and disconnected states. Current cards often omit units/freshness and “live” treatment can imply real-time data. Use a prominent demo banner until connected to authoritative sources.",
            ),
            ("h", "Design rationale limits"),
            (
                "p",
                "No design-system document or user research is included. The above describes visible styling and recommendations, not validated usability outcomes.",
            ),
        ],
    )
)
pages.append(
    page(
        "Data model and lifecycle",
        "12 | Current state and target entities",
        [
            ("h", "Current storage"),
            (
                "p",
                "The app uses arrays/scalars in App.tsx and component state via useState. No schema, migration, API contract or persistent store is included. Reload restores initial examples. PostgreSQL appears as UI text, not a configured connection.",
            ),
            ("h", "Recommended conceptual ERD"),
            (
                "code",
                "Organization 1---* User *---* Role\nOrganization 1---* Incident 1---* IncidentUpdate\nIncident *---* Resource via Assignment\nResource 1---* Position / StatusEvent\nIncident 1---* SituationReport\nFacility 1---* CapacitySnapshot\nSupplyItem 1---* InventoryMovement\nConvoy 1---* CheckIn; Convoy *---* Shipment\nAdvisory 1---* Approval; Advisory *---* Delivery\nAll changes -> append-only AuditEvent",
            ),
            ("h", "Core fields and constraints"),
            (
                "b",
                [
                    "Stable UUID/ULID identifiers; UTC timestamps; explicit source/received/verified times.",
                    "Incident status/severity enums and transition rules; location coordinate reference, precision and provenance.",
                    "Assignment enforces unit availability with transaction conflict handling.",
                    "Capacity/telemetry observations carry source, measured/ingested time, confidence and stale threshold.",
                    "Audit records actor, action, object, time, outcome and correlation ID; protect against mutation.",
                ],
            ),
            ("h", "Lifecycle"),
            (
                "p",
                "Ingest and deduplicate a report, validate provenance, create/link incident, authorize triage, record assignments and field updates, publish reviewed advisories, resolve/close under policy, retain by jurisdiction and preserve after-action evidence. Define retention, legal hold and correction semantics before production.",
            ),
        ],
    )
)
pages.append(
    page(
        "Security design and gaps",
        "13 | Production controls required",
        [
            ("h", "Implemented security evidence"),
            (
                "p",
                "The source includes security-themed labels, VLAN/ACL illustrations and focus styling. No sign-in, session management, backend policy, role model, secrets handling, encryption setup, input schema validation, audit store or security configuration is present. A frontend cannot secure privileged operations by itself.",
            ),
            ("h", "Target identity and authorization"),
            (
                "p",
                "Adopt managed identity or a deliberately operated alternative; require MFA for privileged users and short-lived revocable sessions. Define organization, operating period and role scopes. Enforce authorization on server for every action and at data layer where feasible. Minimize medical/PII access.",
            ),
            ("h", "Application and data controls"),
            (
                "b",
                [
                    "Validate payloads server-side; encode output; address injection, CSRF, XSS, SSRF and abuse risks relevant to chosen architecture.",
                    "Use TLS, encryption at rest, key rotation, secret isolation and least-privilege identities.",
                    "Apply rate limits, idempotency, concurrency controls and safe errors to operational APIs.",
                    "Audit access, assignment, severity changes, exports, advisory approval and failover.",
                    "Segment network/admin planes, monitor privileged actions, patch dependencies and scan builds.",
                ],
            ),
            ("h", "Privacy and governance"),
            (
                "p",
                "Classify data, define purpose and retention, constrain cross-agency sharing, redact exports and document breach response. Map applicable jurisdiction and agreements before provider selection.",
            ),
            (
                "c",
                "“Secure connection” and “protected” strings are presentational text. Do not use this prototype with real personal, medical, incident or dispatch data.",
            ),
        ],
    )
)
pages.append(
    page(
        "Disaster response workflow and scenario",
        "14 | End-to-end target operation",
        [
            ("h", "Workflow stages"),
            (
                "b",
                [
                    "1. Intake: source, time, location and evidence; traceable report.",
                    "2. Validation: deduplicate, verify location/hazard, assign confidence and severity.",
                    "3. Coordination: designate incident owner, objectives and authorized notifications.",
                    "4. Assignment: check capabilities, availability and location; issue task and record acknowledgement.",
                    "5. Field updates: timestamp source/connectivity; surface stale or conflicting reports.",
                    "6. Escalation: raise unmet needs, life-safety risks, thresholds and outages.",
                    "7. Public information: source, review, approve, publish, acknowledge and correct advisory.",
                    "8. Resolution: demobilize, record disposition, final report, retention and after-action artifacts.",
                ],
            ),
            ("h", "Illustrative severe structure fire"),
            (
                "p",
                "A 911 call reports a multi-alarm fire with possible occupants. Dispatch records the call, confirms address/risk and an incident lead sets objectives. Engine, medic and command units are proposed; each acknowledges and reports en route/on scene. Medical coordination checks receiving capacity from a verified feed. Logistics stages water and protective equipment. Command escalates additional alarms or capacity limits. Public information approves a road closure advisory, tracks delivery and amends it when access reopens. Closure preserves updates, assignments and decisions.",
            ),
            ("h", "Prototype alignment"),
            (
                "p",
                "Dispatch shows a queue and assignment controls; Public Information shows a composer; Medical and Logistics views show capacity/inventory concepts. They do not share durable entities or services, so this is a target workflow rather than current end-to-end capability.",
            ),
        ],
    )
)
pages.append(
    page(
        "Engineering decisions and tradeoffs",
        "15 | Observed choices",
        [
            (
                "table",
                [
                    ["Observation", "Benefit", "Tradeoff / next step"],
                    [
                        "Single React component",
                        "Fast concept iteration and straightforward demo.",
                        "High coupling; split shell, feature modules, models and hooks.",
                    ],
                    [
                        "Local state and seeded data",
                        "Demo interactions without services.",
                        "No persistence/collaboration/audit; define API contracts and demo mode.",
                    ],
                    [
                        "Conditional section rendering",
                        "Simple nine-view navigation.",
                        "No deep links or route access; add routing when needed.",
                    ],
                    [
                        "Handwritten CSS + Tailwind plugin",
                        "Fine-grained visual control.",
                        "Mixed conventions; establish design tokens/components.",
                    ],
                    [
                        "Illustrative infrastructure terms",
                        "Makes concept tangible.",
                        "Could imply verified telemetry; show source, age and simulated state.",
                    ],
                ],
            ),
            ("h", "Next decisions"),
            (
                "p",
                "Set data classification, offline needs, agency boundaries, availability/recovery goals, identity/audit requirements, integration standards, hosting region and operating owner before choosing backend products. Record decisions, alternatives, consequences and revisit triggers.",
            ),
            ("h", "Engineering foundations"),
            (
                "p",
                "Add feature modules and domain types; runtime validation; loading/error/empty/stale states; structured logs and correlation; configuration separation; dependency governance; accessibility review; and integration contracts. Automated tests belong in a planned engineering workstream before production readiness; none were run for this documentation task.",
            ),
        ],
    )
)
pages.append(
    page(
        "Differentiation and business value",
        "16 | Product thesis",
        [
            ("h", "Potential value proposition"),
            (
                "p",
                "Redline’s proposed differentiation combines emergency coordination with visible communications and continuity posture: dispatch, medical capacity, logistics, public advisories and segmented EOC infrastructure in one interface. This is a thesis illustrated by UI, not independently validated competitive research.",
            ),
            ("h", "Potential operational advantages"),
            (
                "b",
                [
                    "Common picture may reduce tool switching and improve shared context.",
                    "Department views can focus each team on relevant decisions and constraints.",
                    "Clear escalation and assignment records can reduce handoff ambiguity.",
                    "Continuity visibility can clarify degraded operations and backup readiness.",
                    "Reviewed messaging can support consistent public updates and corrections.",
                ],
            ),
            ("h", "Claims to prove"),
            (
                "p",
                "Compare against EOC/CAD, incident command, resource logistics, GIS, mass notification and network tools. Validate interoperability, training, offline performance, ownership, role controls, accessibility, integration cost and measured outcomes.",
            ),
            ("h", "Business measures"),
            (
                "p",
                "Track adoption/training time, acknowledgement and assignment latency, duplicate entry, report freshness, resource utilization, advisory delivery latency, uptime through connectivity loss, recovery time and after-action completeness.",
            ),
            (
                "c",
                "Do not claim AI, real-time feeds, secure multi-agency operations, automated dispatch or predictive capability until implemented and measured.",
            ),
        ],
    )
)
pages.append(
    page(
        "Scalability, availability, and recovery",
        "17 | Future-state engineering",
        [
            ("h", "Scale by workload and agency boundary"),
            (
                "p",
                "Start with a modular service and relational store sized from realistic loads. Separate interactive queries, high-frequency telemetry, file/media and outbound messaging when measured need or isolation warrants. Scope tenants/orgs; apply quotas and fair scheduling.",
            ),
            ("h", "Horizontal scaling and performance"),
            (
                "p",
                "Keep API workers stateless where possible; use health-aware load balancing, pooling, bounded queues, backpressure and caches only with a safe freshness contract. Partition/archive time-series and event data based on query/retention needs. Make integrations idempotent and replayable.",
            ),
            ("h", "Availability and degraded mode"),
            (
                "p",
                "Define SLOs and failure budgets. Provide redundant identity, network paths and service instances; test site loss. Decide which workflows operate offline, how local events sync, conflicts resolve and stale data is shown. Queue critical actions durably before acknowledgement.",
            ),
            ("h", "Recovery"),
            (
                "p",
                "Document RPO/RTO, backup encryption/ownership, restore validation, key recovery and dependency order. Exercise restore/failover with measured results. Prevent split brain and test rollback. “Replication in sync” must come from monitored evidence.",
            ),
            ("h", "Not present in this repository"),
            (
                "p",
                "No load balancer, cache, database, backup job, multiregion configuration, telemetry collector or recovery automation appears in source.",
            ),
        ],
    )
)
pages.append(
    page(
        "Roadmap and delivery sequencing",
        "18 | Recommended phases",
        [
            (
                "table",
                [
                    ["Horizon", "Outcomes"],
                    [
                        "Short term",
                        "Label demo data; decompose App.tsx; define incident/resource/advisory contracts; establish routing and role-aware UX prototype; document classification and operational requirements.",
                    ],
                    [
                        "Medium term",
                        "Build authenticated API and durable incident/resource/audit storage; implement assignment and advisory approval; integrate one authoritative dispatch/medical/logistics source; establish monitoring and recovery exercises.",
                    ],
                    [
                        "Long term",
                        "Mobile responder workflow with offline sync; interagency federation; GIS and satellite-derived inputs; optimization/predictive analytics/AI only with validated data, human oversight, monitoring and fallback.",
                    ],
                ],
            ),
            ("h", "Sequencing rationale"),
            (
                "p",
                "A narrow verified incident-to-assignment-to-update workflow will validate domain contracts and trust before adding multiple integrations. Public messaging, medical data, prediction and federation require governance and safety review as well as engineering.",
            ),
            ("h", "Roadmap exit criteria"),
            (
                "b",
                [
                    "Named operational owner and validated user workflow.",
                    "Source quality, latency and failure behavior measured.",
                    "Identity, permissions, audit, retention and recovery reviewed.",
                    "Field usability, accessibility and degraded connectivity validated.",
                    "Human override and manual fallbacks documented for automated recommendations.",
                ],
            ),
        ],
    )
)
pages.append(
    page(
        "Lessons learned",
        "19 | Engineering reflection",
        [
            ("h", "What the prototype does well"),
            (
                "p",
                "The interface makes a broad EOC concept quickly legible, gives departmental roles recognizable views and allows local interaction demonstrations with little infrastructure.",
            ),
            ("h", "Challenges and tradeoffs"),
            (
                "p",
                "A single component is quick to build but mixes shell, domain constants, view layout and interactions. Static data makes visual review easy but can be mistaken for authoritative operations. Strong status language improves scanability but increases risk when unsupported by telemetry. A visual failover action can mislead if the operational mechanism is not real.",
            ),
            ("h", "What to do differently"),
            (
                "b",
                [
                    "Mark every simulated record and status clearly from the first prototype.",
                    "Separate domain concepts and user workflows before multiplying views.",
                    "Define provenance, timestamps and stale semantics as first-class data.",
                    "Co-design with dispatchers, responders, command, medical and communications staff.",
                    "Build around resilient manual fallback and recovery exercises, not only normal-path UX.",
                ],
            ),
            ("h", "Open questions"),
            (
                "p",
                "Which agencies and jurisdictions? What data can be shared? Which offline actions are essential? What integrations are authoritative? Who approves public messages? What are required SLO/RPO/RTO targets? Who owns 24/7 support and security response?",
            ),
        ],
    )
)
pages.append(
    page(
        "Conclusion and handover checklist",
        "20 | Summary and transition",
        [
            ("h", "Conclusion"),
            (
                "p",
                "Redline Operations is a promising EOC interface prototype with coherent departmental navigation and visible incident, medical, logistics, public information, network and continuity concepts. The codebase is frontend-only. The next milestone is defining trustworthy data, identity, integrations and recovery boundaries, then implementing one end-to-end workflow with measured outcomes.",
            ),
            ("h", "Technical handover checklist"),
            (
                "b",
                [
                    "Project root: Desktop/redline. Entry: src/main.tsx; main UI: src/App.tsx; styles: src/App.css and src/index.css.",
                    "Scripts: npm run dev, npm run build, npm run lint, npm run preview.",
                    "No backend/API keys or service configuration identified in inspected files.",
                    "Before pilot: label data sources; implement authorization, durable audit, monitoring, backup/restore and manual fallback.",
                    "Deployment environment, owners, data agreements, production SLOs and response procedures remain to be assigned.",
                ],
            ),
            ("h", "Document scope"),
            (
                "p",
                "This report is a source-grounded handover of the supplied repository snapshot. It is not a certification, threat assessment, or evidence of operational readiness.",
            ),
            ("h", "Source files inspected"),
            (
                "p",
                "README.md; package.json; vite.config.ts; tsconfig.app.json; src/App.tsx; src/App.css; src/index.css; src/main.tsx. The repository has no schema, server, API specification or deployment manifest among the inspected project files.",
            ),
            (
                "c",
                "Transition recommendation: treat all embedded operational figures as demo content and establish the backend trust model before any field pilot.",
            ),
        ],
    )
)


def decorate(c, d):
    n = c.getPageNumber()
    w, h = letter
    if n == 1:
        c.saveState()
        c.setFillColor(navy)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setFillColor(red)
        c.rect(0, 0, 12, h, fill=1, stroke=0)
        c.restoreState()
        return
    c.saveState()
    c.setStrokeColor(HexColor("#D8E0E8"))
    c.line(0.72 * inch, 0.57 * inch, w - 0.72 * inch, 0.57 * inch)
    c.setFont("Helvetica", 7.2)
    c.setFillColor(muted)
    c.drawString(0.72 * inch, 0.38 * inch, "REDLINE OPERATIONS  |  TECHNICAL HANDOVER")
    c.drawRightString(w - 0.72 * inch, 0.38 * inch, f"{n}  |  15 NOV 2026")
    c.setFillColor(red)
    c.rect(0.72 * inch, h - 0.54 * inch, 0.28 * inch, 0.04 * inch, fill=1, stroke=0)
    c.restoreState()


doc = SimpleDocTemplate(
    str(out),
    pagesize=letter,
    leftMargin=0.72 * inch,
    rightMargin=0.72 * inch,
    topMargin=0.72 * inch,
    bottomMargin=0.77 * inch,
    title="Redline Operations - Technical Project Handover",
    author="OpenAI Codex",
    subject="Source-grounded EOC technical handover",
)
story = []
for i, x in enumerate(pages):
    story.extend(x)
    if i < len(pages) - 1:
        story.append(PageBreak())
doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
print(f"Created {out.resolve()} from {len(pages)} designed pages")
