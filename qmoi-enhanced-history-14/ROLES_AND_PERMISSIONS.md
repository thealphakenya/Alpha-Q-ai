# QMOI Role-Based Access Control (RBAC) Documentation

**Status:** 🔄 In Progress  
**Last Updated:** 2024  
**Phase:** Role-Based Access Control Implementation

---

## Table of Contents

1. [Role Overview](#role-overview)
2. [Master Role Permissions](#master-role-permissions)
3. [Sister (Administrator) Role Permissions](#sister-administrator-role-permissions)
4. [User Role Permissions](#user-role-permissions)
5. [Sponsored User Role Permissions](#sponsored-user-role-permissions)
6. [Guest Role Permissions](#guest-role-permissions)
7. [Dashboard Tab Access Matrix](#dashboard-tab-access-matrix)
8. [API Endpoint Access Control](#api-endpoint-access-control)
9. [Implementation Status](#implementation-status)
10. [Testing Results](#testing-results)

---

## Role Overview

The QMOI system implements a hierarchical role-based access control (RBAC) system with five distinct user roles:

| Role        | Display Name           | Level | Description                                                                  |
| ----------- | ---------------------- | ----- | ---------------------------------------------------------------------------- |
| `master`    | Master Administrator   | 5     | Full system access, can manage all users and features                        |
| `master`     | Administrator (Sister) | 4     | Administrative features, user management, cannot access master-only features |
| `user`      | Regular User           | 2     | Basic features, personal data, limited access                                |
| `sponsored` | Sponsored User         | 1     | Limited features specific to sponsored programs                              |
| `guest`     | Guest                  | 0     | Read-only access, cannot perform actions                                     |

---

## Master Role Permissions

**Code Representation:** `"master"`  
**Display Name:** Master Administrator

### Features

- ✅ Full access to all 16 dashboard tabs
- ✅ Can manage all users (create, edit, delete, suspend)
- ✅ Can view all system logs and audit trails
- ✅ Can configure system settings
- ✅ Can approve/reject master actions
- ✅ Can manage sponsored users and programs
- ✅ Can access all financial and revenue features
- ✅ Can manage QVillage enterprise features
- ✅ Can configure biometric authentication methods
- ✅ Can execute master commands in automation systems

### Dashboard Tabs

- Overview ✅
- Chat with QMOI ✅
- QConverse (Voice) ✅
- Biometric Auth ✅
- Access Control ✅
- Memory Awareness ✅
- Parallel Processing ✅
- Accountability ✅
- System Health ✅
- Trading & Revenue ✅
- Financial Manager ✅
- QVillage ✅
- Media Manager ✅
- File Explorer ✅
- Notifications ✅
- Settings ✅

### API Endpoints

All endpoints accessible with master role. See [API Endpoint Access Control](#api-endpoint-access-control) for details.

### Permissions Function

```javascript
hasPermission(perm):
  if role === "master" → return true (all permissions granted)
```

---

## Sister (Administrator) Role Permissions

**Code Representation:** `"master"`  
**Display Name:** Administrator / Sister

### Features

- ✅ Can manage regular users (create, edit, delete)
- ✅ Can view system logs and audit trails
- ✅ Can access administrative dashboard
- ✅ Can configure system settings (limited)
- ✅ Can manage sponsored users (limited)
- ✅ Can access Financial Manager
- ✅ Can access QVillage (limited features)
- ❌ Cannot manage other administrators
- ❌ Cannot access master-only controls
- ❌ Cannot execute master commands

### Dashboard Tabs

- Overview ✅
- Chat with QMOI ✅
- QConverse (Voice) ✅
- Biometric Auth ✅ (view only)
- Access Control ✅
- Memory Awareness ✅
- Parallel Processing ✅
- Accountability ✅
- System Health ✅
- Trading & Revenue ✅
- Financial Manager ✅
- QVillage ✅ (limited)
- Media Manager ✅
- File Explorer ✅
- Notifications ✅
- Settings ✅ (limited)

### API Endpoints

- `/api/auth/login` - ✅ Master login
- `/api/users/*` - ✅ Manage users (except other admins)
- `/api/master/*` - ✅ Most master endpoints
- `/api/master/*` - ❌ Forbidden
- See [API Endpoint Access Control](#api-endpoint-access-control) for complete list

### Permissions Function

```javascript
hasPermission(perm):
  if perm === "master" && role === "master" → return true
  if perm === "viewDashboard" && role === "master" → return true
  if perm === "user" && role === "master" → return true
  → return false
```

---

## User Role Permissions

**Code Representation:** `"user"`  
**Display Name:** Regular User

### Features

- ✅ Can chat with QMOI
- ✅ Can use voice features (QConverse)
- ✅ Can access personal biometric settings
- ✅ Can view personal memory and preferences
- ✅ Can view notifications
- ✅ Can manage personal files
- ✅ Can participate in trading (if enabled)
- ❌ Cannot manage other users
- ❌ Cannot access access control features
- ❌ Cannot view system health or logs
- ❌ Cannot execute administrative actions

### Dashboard Tabs

- Overview ✅ (personal data only)
- Chat with QMOI ✅
- QConverse (Voice) ✅
- Biometric Auth ✅ (personal settings only)
- Access Control ❌
- Memory Awareness ✅ (personal only)
- Parallel Processing ❌
- Accountability ❌
- System Health ❌
- Trading & Revenue ✅
- Financial Manager ❌
- QVillage ❌
- Media Manager ✅ (personal only)
- File Explorer ✅ (personal files only)
- Notifications ✅
- Settings ✅ (personal only)

### API Endpoints

- `/api/auth/login` - ✅ User login
- `/api/users/profile` - ✅ Own profile only
- `/api/users/update` - ✅ Own profile only
- `/api/users/list` - ❌ Forbidden
- `/api/master/*` - ❌ Forbidden
- `/api/master/*` - ❌ Forbidden
- See [API Endpoint Access Control](#api-endpoint-access-control) for complete list

### Permissions Function

```javascript
hasPermission(perm):
  if perm === "user" && (role === "user" || role === "master") → return true
  → return false
```

---

## Sponsored User Role Permissions

**Code Representation:** `"sponsored"`  
**Display Name:** Sponsored User

### Features

- ✅ Limited chat with QMOI
- ✅ Can enroll in sponsored programs
- ✅ Can view personal sponsorship status
- ✅ Can access sponsored-specific features
- ✅ Can participate in sponsored trading (if enabled)
- ❌ Cannot access core features outside sponsorship
- ❌ Cannot manage files
- ❌ Cannot access financial features
- ❌ Cannot manage biometrics

### Dashboard Tabs

- Overview ❌ (redirects to sponsorship dashboard)
- Chat with QMOI ✅ (limited context)
- QConverse (Voice) ❌
- Biometric Auth ❌
- Access Control ❌
- Memory Awareness ❌
- Parallel Processing ❌
- Accountability ❌
- System Health ❌
- Trading & Revenue ✅ (sponsored only)
- Financial Manager ❌
- QVillage ❌
- Media Manager ❌
- File Explorer ❌
- Notifications ✅
- Settings ✅ (sponsored only)

### API Endpoints

- `/api/auth/login` - ✅ Sponsored user login
- `/api/sponsored/*` - ✅ Sponsored-specific endpoints
- Most other endpoints - ❌ Forbidden

### Permissions Function

```javascript
hasPermission(perm):
  if perm === "sponsored" && role === "sponsored" → return true
  → return false
```

---

## Guest Role Permissions

**Code Representation:** `"guest"`  
**Display Name:** Guest

### Features

- ✅ Can view public information only
- ✅ Can access help and documentation
- ❌ Cannot perform any actions
- ❌ Cannot access user data
- ❌ Cannot authenticate with biometrics
- ❌ Cannot use chat or voice features

### Dashboard Tabs

None - Guests should not access the dashboard

### API Endpoints

- `/api/public/*` - ✅ Public endpoints only
- All other endpoints - ❌ Forbidden

---

## Dashboard Tab Access Matrix

| Tab                 | Master | Master | User | Sponsored | Guest |
| ------------------- | ------ | ----- | ---- | --------- | ----- |
| Overview            | ✅     | ✅    | ✅\* | ❌        | ❌    |
| Chat                | ✅     | ✅    | ✅   | ✅\*      | ❌    |
| QConverse           | ✅     | ✅    | ✅   | ❌        | ❌    |
| Biometric Auth      | ✅     | ✅\*  | ✅\* | ❌        | ❌    |
| Access Control      | ✅     | ✅    | ❌   | ❌        | ❌    |
| Memory Awareness    | ✅     | ✅    | ✅\* | ❌        | ❌    |
| Parallel Processing | ✅     | ✅    | ❌   | ❌        | ❌    |
| Accountability      | ✅     | ✅    | ❌   | ❌        | ❌    |
| System Health       | ✅     | ✅    | ❌   | ❌        | ❌    |
| Trading & Revenue   | ✅     | ✅    | ✅   | ✅\*      | ❌    |
| Financial Manager   | ✅     | ✅    | ❌   | ❌        | ❌    |
| QVillage            | ✅     | ✅\*  | ❌   | ❌        | ❌    |
| Media Manager       | ✅     | ✅    | ✅\* | ❌        | ❌    |
| File Explorer       | ✅     | ✅    | ✅\* | ❌        | ❌    |
| Notifications       | ✅     | ✅    | ✅   | ✅        | ❌    |
| Settings            | ✅     | ✅\*  | ✅\* | ✅\*      | ❌    |

**Legend:** ✅ = Full Access | ✅\* = Limited/Personal Data Only | ❌ = No Access

---

## API Endpoint Access Control

### Authentication Endpoints

| Endpoint                     | Method   | Master | Master | User | Sponsored | Guest |
| ---------------------------- | -------- | ------ | ----- | ---- | --------- | ----- |
| `/api/auth/login`            | POST     | ✅     | ✅    | ✅   | ✅        | ❌    |
| `/api/webauthn/register`     | POST     | ✅     | ✅    | ✅   | ❌        | ❌    |
| `/api/webauthn/authenticate` | POST     | ✅     | ✅    | ✅   | ❌        | ❌    |
| `/api/voice/enroll`          | POST     | ✅     | ✅    | ✅   | ❌        | ❌    |
| `/api/voice/verify`          | POST     | ✅     | ✅    | ✅   | ❌        | ❌    |
| `/api/biometric/templates`   | GET/POST | ✅     | ✅    | ✅\* | ❌        | ❌    |
| `/api/biometric/verify`      | POST     | ✅     | ✅    | ✅   | ❌        | ❌    |
| `/api/qmoi/session`          | POST/GET | ✅     | ✅    | ✅   | ✅        | ❌    |

### User Management Endpoints

| Endpoint             | Method | Master | Master | User | Sponsored | Guest |
| -------------------- | ------ | ------ | ----- | ---- | --------- | ----- |
| `/api/users/list`    | GET    | ✅     | ✅    | ❌   | ❌        | ❌    |
| `/api/users/create`  | POST   | ✅     | ✅    | ❌   | ❌        | ❌    |
| `/api/users/profile` | GET    | ✅     | ✅    | ✅\* | ✅\*      | ❌    |
| `/api/users/update`  | PUT    | ✅     | ✅    | ✅\* | ✅\*      | ❌    |
| `/api/users/delete`  | DELETE | ✅     | ✅    | ❌   | ❌        | ❌    |

### Master Endpoints

| Endpoint                      | Method  | Master | Master | User | Sponsored | Guest |
| ----------------------------- | ------- | ------ | ----- | ---- | --------- | ----- |
| `/api/master/sponsored/list`   | GET     | ✅     | ✅    | ❌   | ❌        | ❌    |
| `/api/master/sponsored/create` | POST    | ✅     | ✅    | ❌   | ❌        | ❌    |
| `/api/master/sponsored/delete` | DELETE  | ✅     | ✅    | ❌   | ❌        | ❌    |
| `/api/master/logs`             | GET     | ✅     | ✅    | ❌   | ❌        | ❌    |
| `/api/master/settings`         | GET/PUT | ✅     | ✅\*  | ❌   | ❌        | ❌    |

### Master-Only Endpoints

| Endpoint                         | Method  | Master | Master | User | Sponsored | Guest |
| -------------------------------- | ------- | ------ | ----- | ---- | --------- | ----- |
| `/api/master/system/config`      | GET/PUT | ✅     | ❌    | ❌   | ❌        | ❌    |
| `/api/master/audit/trail`        | GET     | ✅     | ❌    | ❌   | ❌        | ❌    |
| `/api/master/users/master/assign` | PUT     | ✅     | ❌    | ❌   | ❌        | ❌    |
| `/api/master/backup`             | POST    | ✅     | ❌    | ❌   | ❌        | ❌    |

---

## Implementation Status

### ✅ Completed

- [x] Role definitions in MasterContext (master, master, user, guest)
- [x] Permission checking logic (hasPermission function)
- [x] Biometric authentication endpoints created
- [x] Session management with role tracking
- [x] Dashboard components created

### 🔄 In Progress

- [ ] Add "sponsored" role to MasterContext
- [ ] Implement role-based UI rendering in QMOIDashboard
- [ ] Add role checks to all API endpoints
- [ ] Create role-based middleware for API protection

### ❌ Not Started

- [ ] Create test users for each role (Master, Master, User, Sponsored)
- [ ] Implement sponsored user management endpoints
- [ ] Add role-based field masking (hide sensitive data)
- [ ] Create audit logging for role-based access
- [ ] Implement role change history tracking

---

## Testing Results

### Test Status

- ✅ Email/password login tested
- ✅ WebAuthn endpoints tested
- ✅ Voice biometric endpoints tested
- ✅ Biometric template endpoints tested
- ✅ Session management tested
- 🔄 Role-based access needs testing (IN PROGRESS)

### Test Users (To Be Created)

```json
[
  {
    "id": "1",
    "username": "master_admin",
    "password": "hashed_password",
    "role": "Master Administrator",
    "email": "master@qmoi.com"
  },
  {
    "id": "2",
    "username": "sister_admin",
    "password": "hashed_password",
    "role": "Administrator",
    "email": "master@qmoi.com"
  },
  {
    "id": "3",
    "username": "regular_user",
    "password": "hashed_password",
    "role": "User",
    "email": "user@qmoi.com"
  },
  {
    "id": "4",
    "username": "sponsored_user",
    "password": "hashed_password",
    "role": "Sponsored User",
    "email": "sponsored@qmoi.com"
  }
]
```

---

## Role Mapping

The system maps display role names to internal role codes:

```javascript
const roleMap = {
  "Master Administrator": "master",
  Administrator: "master",
  Sister: "master",
  User: "user",
  "Sponsored User": "sponsored",
  Guest: "guest",
};
```

---

## Next Steps

1. **Update MasterContext** - Add "sponsored" role to `UserRole` type
2. **Implement Sponsored Role** - Define permissions for sponsored users
3. **Add Dashboard Role Filtering** - Restrict tab visibility based on role
4. **Secure All Endpoints** - Add role checks to every API route
5. **Create Test Users** - Add users for each role to users.json
6. **Test Role-Based Access** - Verify each role has correct feature access
7. **Document Integration** - Update API reference and endpoint docs

---

**Document Version:** 1.0  
**Author:** QMOI Development  
**Last Updated:** 2024

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
