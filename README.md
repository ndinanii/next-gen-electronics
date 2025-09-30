### Salesforce Data Modeling and Management

> A practical mini‑project to design a simple Salesforce data model for NextGen Electronics, import clean data, enforce data quality, and surface insights via reporting. Managed end‑to‑end with Notion for planning, tasks, and submission tracking.
> 

---

## Table of contents

- Overview
- Objectives
- Architecture and data model
- Notion project management
- Implementation steps
- Python CSV generation
- Metadata XML for custom fields
- Data import
- Data quality rules
- Reporting
- Testing and QA
- Repository structure
- How to run locally
- Assumptions and limitations
- Future improvements
- Screenshots and artifacts
- License

---

## Overview

This repository documents the complete process of modeling and managing sales data in Salesforce for the fictional NextGen Electronics sales team. The project uses:

- Salesforce custom objects and fields for Leads and Opportunities
- A relationship from Opportunity to its “Original Lead”
- Validation and duplicate rules for data quality
- Python to generate clean CSVs for import at scale
- Salesforce metadata XML to define custom fields
- A report that shows “Opportunities from Converted Leads” filtered by Original Lead
- Notion as the single source of truth for tasks, notes, and submission assets

---

## Objectives

- Design a lightweight data model to track the lead lifecycle through to opportunity.
- Enforce data quality with validation and duplicate management.
- Automate repeatable data preparation using Python-generated CSVs.
- Produce a report focused on opportunities derived from converted leads.
- Maintain transparent process documentation and assets.

---

## Architecture and data model

- Custom objects
    - Lead__c
    - Opportunity__c
- Key fields (examples)
    - Lead__c
        - Email__c (Text, unique)
        - Phone__c (Text)
        - Status__c (Picklist: New, Working, Qualified, Converted)
    - Opportunity__c
        - Amount__c (Currency)
        - Stage__c (Picklist: Prospecting, Qualification, Proposal, Closed Won, Closed Lost)
        - CloseDate__c (Date)
        - OriginalLead__c (Lookup to Lead__c)
- Relationship
    - Opportunity__c.OriginalLead__c → Lead__c

Note: In a production org, we use standard Lead and Opportunity objects. For teaching purposes, this project uses clearly named custom objects and fields.

---

## Notion project management

- Central project page: goals, context, and embedded task boards
- Linked task databases for micro-steps and checklists
- Dedicated pages for each major step:
    - Create Custom Lead Object
    - Create Custom Opportunity Object
    - Define Fields
    - Set Up Relationships
    - Validation Rule
    - Duplicate Management
    - Data Import
    - Report Generation
    - Project Submission
- Outcome
    - Clear sequencing
    - Daily progress tracking
    - Single place to collect screenshots, notes, and final submission links

---

## Implementation steps

1. Plan the scope and success criteria in Notion.
2. Create custom objects Lead__c and Opportunity__c.
3. Add custom fields with metadata XML and deploy to the org.
4. Define the OriginalLead__c lookup on Opportunity__c.
5. Add validation rules (e.g., require CloseDate for advanced stages).
6. Configure duplicate rules on leads (keyed by email).
7. Prepare source data with Python and generate CSVs.
8. Import data in Salesforce (leads first, then opportunities).
9. Build the “Opportunities from Converted Leads” report.
10. Document outcomes, screenshots, and repository links in Notion.

---

## Python CSV generation

Goal: deterministically produce clean, import‑ready datasets and avoid spreadsheet drift.

- Input sources
    - seed/leads_seed.json
    - seed/opportunities_seed.json
- Transformations
    - Normalize emails and phones
    - Map lead statuses
    - Derive OriginalLead keys for opportunity rows
    - Validate required fields and log anomalies


---

## Metadata XML for custom fields

Fields were defined via Salesforce metadata to ensure reproducibility. Example fragments:

- Lead__c.fields-meta.xml

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>Email__c</fullName>
  <externalId>true</externalId>
  <label>Email</label>
  <length>80</length>
  <required>true</required>
  <type>Text</type>
  <unique>true</unique>
</CustomField>
```

- Opportunity__c.fields-meta.xml

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>OriginalLead__c</fullName>
  <label>Original Lead</label>
  <referenceTo>Lead__c</referenceTo>
  <relationshipLabel>Opportunities</relationshipLabel>
  <relationshipName>Opportunities</relationshipName>
  <type>Lookup</type>
</CustomField>
```

Deploy with SFDX:

```bash
sfdx force:source:deploy -p force-app/main/default/objects
```

---

## Data import

The Process: 

1. Import Leads
    - Map columns: Name, Email__c, Phone__c, Status__c
    - Email__c acts as an external ID and dedupe key


Tools

- Data Import Wizard for small datasets, or Data Loader/SFDX for bulk
- Validate row counts and spot‑check records post‑import

---

## Data quality rules

- Validation rule example (Opportunity)
    - Purpose: prevent moving beyond Qualification without CloseDate
    - Formula:
        
        ```
        AND(
          ISPICKVAL(Stage__c, "Proposal"),
          ISBLANK(CloseDate__c)
        )
        ```
        
    - Error: “Close Date is required before Proposal stage.”
- Duplicate management (Lead)
    - Matching rule on Email__c
    - Duplicate rule to block automatic insert on exact match
    - CSV generator also pre‑filters obvious dups

---

## Reporting

Report: “Opportunities from Converted Leads”

- Type: Opportunities with lookup to Original Lead
- Filters:
    - Original Lead: not blank
    - Stage: All open and closed
- Columns:
    - Opportunity Name
    - Amount
    - Stage
    - Close Date
    - Original Lead → Name, Email
- Summaries:
    - Sum(Amount) by Stage
- Save and add to a dashboard if needed

---

## Testing and QA

- Unit checks in Python to ensure required fields are present
- Post‑import spot checks:
    - Sample 10 Leads and 10 Opportunities
    - Verify lookup integrity for OriginalLead__c
- Report verification:
    - Totals align with imported opportunity count and sum

---



## Assumptions and limitations

- Custom objects are used for clarity in learning contexts.
- Email__c serves as a unique external ID for leads.
- Example validation and picklists are minimal and can be extended.
- Sample datasets are intentionally small for demonstration.

---

## Future improvements

- Add flows to auto‑create Opportunity on Lead conversion.
- Introduce Apex triggers for additional integrity checks.
- Enrich duplicate rules with fuzzy matching on name + phone.
- Publish dashboards for pipeline health and lead conversion.
- CI for metadata validation and test deployments.

---

## Screenshots and artifacts

- Org setup, object manager, field definitions
- Data import mappings and results
- Validation and duplicate rule configurations
- Final report view
- Submission page and repository link managed in Notion

---

## License

MIT unless otherwise noted.

---

### Notes on process and tooling

- Why Python?
    - Reproducible transformations and deterministic outputs
    - Easier to validate, normalize, and log data issues
- Why metadata XML?
    - Version control and repeatable deployments
    - Clear diffs for field changes

---

