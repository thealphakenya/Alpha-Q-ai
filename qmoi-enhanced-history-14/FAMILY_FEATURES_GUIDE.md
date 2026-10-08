# QMOI Family Features Guide

## Overview

This document outlines family features available to both Master (Victor) and Sister (Leah), while maintaining privacy boundaries and access restrictions.

---

## Family Member Profiles

### Master (Victor)

- **Role**: Family Owner & Administrator
- **Access Level**: 100 (Full)
- **Relationship**: Primary
- **Responsibilities**: System oversight, major decisions

### Sister (Leah)

- **Role**: Family Member & Collaborator
- **Access Level**: 80 (High)
- **Relationship**: Family
- **Restrictions**: Limited system control, no master-only data

---

## Shared Family Resources

### Family Wallet

A shared financial account that both Victor and Leah can access:

**Victor's Access**:

- ✅ View complete balance and history
- ✅ Approve withdrawals
- ✅ Approve deposits
- ✅ Configure spending limits
- ✅ Set family budget
- ✅ View all transactions
- ✅ Configure wallet security

**Leah's Access**:

- ✅ View current balance
- ✅ Request withdrawals
- ✅ Deposit funds
- ✅ View transaction history
- ✅ Set personal spending limit
- ❌ Approve transactions
- ❌ Configure wallet rules
- ❌ View financial analytics

### Family Projects

Collaborative projects that family members work on together:

**Features**:

- Shared project dashboard
- Task management
- Progress tracking
- Shared deadlines
- Collaboration notes
- File sharing (family only)
- Budget allocation
- Timeline planning

**Victor's Control**:

- Create new projects
- Archive projects
- Allocate budgets
- Set deadlines
- Assign roles
- Review reports

**Leah's Access**:

- View projects
- Update progress
- Comment and collaborate
- Upload shared files
- Request resources

### Family Calendar

Shared calendar for family events and important dates:

**Shared Events**:

- Family meetings
- Project deadlines
- Financial reviews
- Team gatherings
- Holiday schedules
- Vacation planning

**Features**:

- Event creation and editing (both)
- Notifications for upcoming events
- Time zone support
- Recurring events
- Reminder settings

### Family Communication

Secure messaging for family members:

**Features**:

- Direct messaging
- Group family chat
- Notification settings
- Message history
- Search functionality
- File attachments (limited)

**Restrictions**:

- Messages encrypted
- Limited to 30 days history
- No access to old conversations
- Family-only visibility

---

## Family Access Patterns

### What Victor Can See About Family

- ✅ Leah's name and contact
- ✅ Shared resource usage
- ✅ Family project participation
- ✅ Family calendar events
- ✅ Shared wallet activities
- ✅ Family communication
- ❌ Leah's personal messages with others
- ❌ Leah's private data
- ❌ Leah's individual preferences

### What Leah Can See About Family

- ✅ Victor's name
- ✅ Shared resources
- ✅ Family projects status
- ✅ Family calendar
- ✅ Shared wallet
- ✅ Family communication
- ❌ Victor's personal data
- ❌ Victor's financial details
- ❌ Victor's system configuration
- ❌ Trading information

---

## Family Wallet Operations

### Wallet Features

```
Family Wallet: QMOI_FAMILY_001
├── Current Balance: $50,000
├── Monthly Budget: $10,000
├── Spending This Month: $3,450
├── Remaining: $6,550
├── Next Review Date: Feb 1, 2025
└── Security: 2FA Enabled
```

### Withdrawal Request (Leah)

```bash
curl -X POST http://localhost:3001/api/qmoi/family/wallet/request-withdrawal \
  -H "Authorization: Bearer LEAH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 500,
    "purpose": "Project expenses",
    "notes": "Development tools"
  }'
```

### Withdrawal Approval (Victor)

```bash
curl -X POST http://localhost:3001/api/qmoi/family/wallet/approve-withdrawal \
  -H "Authorization: Bearer MASTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "wr_12345",
    "approved": true
  }'
```

### Check Wallet Status (Both)

```bash
curl -X GET http://localhost:3001/api/qmoi/family/wallet/status \
  -H "Authorization: Bearer USER_TOKEN"
```

---

## Family Project Management

### Create Family Project (Victor Only)

```bash
curl -X POST http://localhost:3001/api/qmoi/family/projects \
  -H "Authorization: Bearer MASTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q1 Family Initiative",
    "description": "Quarterly goals and milestones",
    "budget": 5000,
    "deadline": "2025-03-31",
    "members": ["master", "sister"]
  }'
```

### Update Project Status (Both)

```bash
curl -X PUT http://localhost:3001/api/qmoi/family/projects/proj_001 \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "progress": 45,
    "notes": "On schedule for deadline"
  }'
```

### View Family Projects (Both)

```bash
curl -X GET http://localhost:3001/api/qmoi/family/projects \
  -H "Authorization: Bearer USER_TOKEN"
```

---

## Family Calendar Management

### Add Family Event (Both)

```bash
curl -X POST http://localhost:3001/api/qmoi/family/calendar \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Family Financial Review",
    "date": "2025-02-01",
    "time": "14:00",
    "duration": 60,
    "attendees": ["master", "sister"],
    "description": "Monthly review of family finances"
  }'
```

### View Family Calendar (Both)

```bash
curl -X GET http://localhost:3001/api/qmoi/family/calendar \
  -H "Authorization: Bearer USER_TOKEN"
```

### Set Event Reminder (Individual)

```bash
curl -X PUT http://localhost:3001/api/qmoi/family/calendar/event_001/reminder \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "notification",
    "minutesBefore": 15
  }'
```

---

## Family Communication

### Send Family Message

```bash
curl -X POST http://localhost:3001/api/qmoi/family/messages \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "sister",
    "message": "Project update: 60% complete",
    "attachments": []
  }'
```

### Retrieve Family Messages

```bash
curl -X GET http://localhost:3001/api/qmoi/family/messages \
  -H "Authorization: Bearer USER_TOKEN"
```

### Search Family Communication

```bash
curl -X GET "http://localhost:3001/api/qmoi/family/messages/search?query=project" \
  -H "Authorization: Bearer USER_TOKEN"
```

---

## Family Settings

### Configure Family Preferences (Victor)

```bash
curl -X POST http://localhost:3001/api/qmoi/family/settings \
  -H "Authorization: Bearer MASTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "budgetAlert": 500,
    "monthlyReviewDay": 1,
    "notificationPreference": "both",
    "currency": "USD",
    "timeZone": "Africa/Nairobi"
  }'
```

### Update Personal Family Preferences (Both)

```bash
curl -X PUT http://localhost:3001/api/qmoi/family/settings/personal \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notifications": true,
    "emailDigest": "weekly",
    "theme": "dark"
  }'
```

---

## Family Notifications

### What Triggers Family Notifications

**For Victor (Master)**:

- ✉️ Leah requests wallet withdrawal
- ✉️ Project milestones reached
- ✉️ Wallet spending exceeds limit
- ✉️ New family messages
- ✉️ Upcoming family events
- ✉️ Monthly financial review due

**For Leah (Sister)**:

- ✉️ Withdrawal approved/rejected
- ✉️ Project updates from Victor
- ✉️ New wallet transfers
- ✉️ Family calendar invitations
- ✉️ New family messages
- ✉️ Budget alerts

### Notification Preferences

- Email notifications
- In-app notifications
- SMS alerts (for critical)
- Notification frequency (real-time, hourly, daily)
- Quiet hours (no notifications)

---

## Family Financial Review Process

### Monthly Review (1st of Month)

**Victor Prepares**:

1. Gathers wallet transactions
2. Reviews family spending
3. Checks budget compliance
4. Prepares financial summary
5. Schedules review meeting

**Review Meeting**:

1. Both members discuss finances
2. Review budget allocation
3. Plan upcoming expenses
4. Address any concerns
5. Set goals for next month

**Victor Updates**:

1. Records decisions
2. Updates budgets
3. Configures alerts
4. Sends summary to Leah

---

## Family Data Security

### Encryption

- All shared data encrypted in transit (HTTPS)
- Family wallet data encrypted at rest
- Messages end-to-end encrypted
- Credentials never shared

### Access Logging

- All family resource access logged
- Who accessed what and when
- Changes tracked and auditable
- Security alerts for unusual access

### Data Retention

- Family messages: 30 days default
- Transaction history: 12 months
- Calendar events: Until archived
- Project data: Retained indefinitely

### Privacy

- Family data segregated from other users
- Guest users cannot access any family data
- Each member sees only their permitted data
- Personal preferences remain private

---

## Family Collaboration Best Practices

### For Victor (Master)

1. ✅ Review family settings monthly
2. ✅ Approve wallet requests promptly
3. ✅ Keep Leah informed of decisions
4. ✅ Maintain financial transparency
5. ✅ Set clear project deadlines
6. ✅ Schedule regular reviews

### For Leah (Sister)

1. ✅ Use clear project communications
2. ✅ Submit wallet requests with details
3. ✅ Attend family meetings
4. ✅ Update project progress regularly
5. ✅ Keep personal data private
6. ✅ Respect access boundaries

---

## Family Feature Limits

### Wallet Limits

- **Daily Withdrawal Limit**: $5,000
- **Monthly Budget**: $10,000
- **Single Request Maximum**: $2,000
- **Message Length**: 5,000 characters

### Communication Limits

- **Message History**: 30 days
- **File Size**: 50 MB per attachment
- **Daily Messages**: No limit
- **Storage**: 1 GB per user

### Project Limits

- **Active Projects**: 10 maximum
- **Team Members Per Project**: Unlimited
- **File Storage**: 500 MB per project
- **History Retention**: 24 months

---

## Troubleshooting Family Features

### Cannot Access Family Wallet

**Solution**:

1. Verify your role (must be master or sister)
2. Check authentication token
3. Verify wallet is not locked
4. Contact master if issue persists

### Withdrawal Request Rejected

**Possible Reasons**:

- Exceeds daily limit ($5,000)
- Exceeds monthly budget ($10,000)
- Insufficient funds
- Victor hasn't approved yet

### Cannot See Family Projects

**Solution**:

1. Verify you're assigned to project
2. Check if project is archived
3. Refresh browser
4. Check project sharing settings

---

## Family Feature Roadmap

**Upcoming Features**:

- [ ] Shared expense splitting
- [ ] Family goal tracking
- [ ] Budget forecasting
- [ ] Automated savings plans
- [ ] Family financial reports
- [ ] Voice/video conferencing
- [ ] Document collaboration
- [ ] Family achievements tracking

---

## Support & Assistance

**For Family Issues**:

- Contact Victor (Master) for account issues
- Contact QMOI support for feature issues
- Review family logs for history
- Check shared documentation

---

**Document Version**: 1.0.0  
**Last Updated**: January 28, 2026  
**Status**: Active & Production Ready  
**Audience**: Family Members (Victor & Leah)

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10435`; directories: `1269`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2110, orchestration=2061, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52722`; percentage occurrences: `22237`.
- Markdown word count: `3552546`; heuristic sentence count: `673863`; sentence records indexed: `673863`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29844` metric claims; `10662` completion claims; `29747` metric and `10533` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13340`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40017` lines in `3670` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `287`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
