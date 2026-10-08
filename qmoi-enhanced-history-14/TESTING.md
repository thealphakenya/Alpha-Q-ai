# Testing Guide

## Overview

QMOI Enhanced uses Jest for unit and integration testing. This guide covers how to run, write, and maintain tests.

## Running Tests

### All Tests

```bash
npm test
```

### Specific Test File

```bash
npm test -- __tests__/api/auth.test.ts
```

### Watch Mode

```bash
npm test -- --watch
```

### Coverage Report

```bash
npm test -- --coverage
```

### Specific Test Suite

```bash
npm test -- --testNamePattern="User Registration"
```

## Test Structure

### Test Files Location

```
__tests__/
├── api/
│   ├── auth.test.ts
│   ├── payments.test.ts
│   └── wallets.test.ts
├── integration/
│   └── user-registration.test.ts
└── utils/
    └── test-helpers.ts
```

## Unit Tests

### API Tests

#### Authentication Tests (`__tests__/api/auth.test.ts`)

Tests JWT token generation, verification, and validation:

```bash
npm test -- __tests__/api/auth.test.ts
```

**Test Cases:**

- ✓ JWT token generation
- ✓ JWT token verification
- ✓ Email validation
- ✓ Password validation
- ✓ Expired token detection
- ✓ Invalid token rejection

#### Payment Tests (`__tests__/api/payments.test.ts`)

Tests payment initiation and webhook handling:

```bash
npm test -- __tests__/api/payments.test.ts
```

**Test Cases:**

- ✓ Payment initiation
- ✓ M-Pesa payment processing
- ✓ PayPal payment processing
- ✓ Stripe payment processing
- ✓ Webhook signature verification
- ✓ Transaction status updates
- ✓ Phone number validation

#### Wallet Tests (`__tests__/api/wallets.test.ts`)

Tests wallet CRUD operations:

```bash
npm test -- __tests__/api/wallets.test.ts
```

**Test Cases:**

- ✓ Create wallet
- ✓ Get wallet details
- ✓ Update wallet
- ✓ Delete wallet
- ✓ List wallets with pagination
- ✓ Balance updates
- ✓ Prevent deletion of non-empty wallets
- ✓ Concurrent operations

## Integration Tests

### User Registration Flow (`__tests__/integration/user-registration.test.ts`)

Tests complete registration workflow:

```bash
npm test -- __tests__/integration/user-registration.test.ts
```

**Test Cases:**

- ✓ User registration with valid data
- ✓ Email already exists validation
- ✓ Password requirements enforcement
- ✓ JWT token generation
- ✓ User profile creation
- ✓ Wallet creation for new user
- ✓ Email verification (if enabled)
- ✓ Profile retrieval after registration
- ✓ Authentication required for protected endpoints

## Test Helpers

### Using Test Utilities (`__tests__/utils/test-helpers.ts`)

The test helpers library provides:

```typescript
// Create mock requests
const mockRequest = createMockRequest({
  method: "POST",
  headers: { Authorization: "Bearer token" },
  body: { email: "test@example.com" },
});

// Generate test data
const testUser = generateTestUser();
const testWallet = generateTestWallet(testUser.id);

// Create mock services
const mockAuthService = createMockAuthService();
const mockEmailService = createMockEmailService();

// Assert responses
expectSuccess(response, 200);
expectError(response, 400, "Invalid request");
```

## Writing New Tests

### Template for API Test

```typescript
import { describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { POST } from "@/app/api/example/route";
import { createMockRequest } from "@/__tests__/utils/test-helpers";

describe("Example Endpoint", () => {
  let mockRequest: any;

  beforeEach(() => {
    mockRequest = createMockRequest({
      method: "POST",
      headers: {
        Authorization: "Bearer test-token",
        "Content-Type": "application/json",
      },
    });
  });

  afterEach(() => {
    // Cleanup
  });

  it("should handle successful request", async () => {
    const response = await POST(mockRequest);
    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty("success", true);
  });

  it("should reject unauthorized requests", async () => {
    const unauthorizedRequest = createMockRequest({
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    const response = await POST(unauthorizedRequest);
    expect(response.status).toBe(401);
  });

  it("should validate input data", async () => {
    mockRequest.body = {
      /* invalid data */
    };
    const response = await POST(mockRequest);
    expect(response.status).toBe(400);
  });
});
```

### Template for Integration Test

```typescript
import { describe, it, expect } from "@jest/globals";
import { register } from "@/lib/auth/service";
import { getUserProfile } from "@/lib/db/services";

describe("User Registration Flow", () => {
  it("should complete registration and create profile", async () => {
    // Step 1: Register user
    const user = await register(
      "test@example.com",
      "testuser",
      "SecurePassword123!@#",
    );

    expect(user).toHaveProperty("id");
    expect(user.email).toBe("test@example.com");

    // Step 2: Verify profile created
    const profile = await getUserProfile(user.id);
    expect(profile).toBeDefined();
    expect(profile?.userId).toBe(user.id);

    // Step 3: Verify can login
    const token = generateJWT(user.id);
    expect(token).toBeDefined();
  });
});
```

## Coverage Requirements

### Minimum Coverage Thresholds

- **Branches**: 70%
- **Functions**: 70%
- **Lines**: 70%
- **Statements**: 70%

### View Coverage Report

```bash
npm test -- --coverage
```

### Coverage Report Output

```
------------|----------|----------|----------|----------|----------|
File        |  % Stmts | % Branch | % Funcs  | % Lines  | Uncovered |
------------|----------|----------|----------|----------|----------|
All files   |   75.23  |   70.14  |   78.91  |   74.89  |           |
------------|----------|----------|----------|----------|----------|
```

## Testing Best Practices

### 1. Arrange-Act-Assert Pattern

```typescript
it("should update user profile", async () => {
  // Arrange
  const user = createTestUser();
  const updateData = { firstName: "John" };

  // Act
  const result = await updateUserProfile(user.id, updateData);

  // Assert
  expect(result.firstName).toBe("John");
});
```

### 2. Use Descriptive Test Names

```typescript
// ❌ Bad
it("works", () => {});

// ✓ Good
it("should update user firstName and return updated profile", () => {});
```

### 3. Keep Tests Focused

```typescript
// ❌ Testing multiple things
it("should register and create wallet and send email", () => {});

// ✓ Single responsibility
it("should register user with valid credentials", () => {});
it("should create default wallet on registration", () => {});
it("should send verification email on registration", () => {});
```

### 4. Mock External Dependencies

```typescript
// Mock payment provider
jest.mock("@/lib/payments/service", () => ({
  initiatePayment: jest.fn().mockResolvedValue({
    transactionId: "test-123",
    status: "pending",
  }),
}));
```

### 5. Test Error Scenarios

```typescript
it("should reject invalid email format", async () => {
  const result = register("invalid-email", "user", "password");
  await expect(result).rejects.toThrow("Invalid email");
});
```

## Debugging Tests

### Run Single Test

```bash
npm test -- -t "should update user profile"
```

### Run Tests in Debug Mode

```bash
node --inspect-brk ./node_modules/.bin/jest --runInBand
```

### Add Breakpoints

```typescript
it("should handle payment", async () => {
  debugger; // Breakpoint here
  const payment = await processPayment(1000);
  expect(payment.status).toBe("success");
});
```

### View Test Output

```bash
npm test -- --verbose
```

## Continuous Integration

Tests run automatically on:

- **Pull Requests**: All tests must pass
- **Commits to main**: All tests must pass
- **Daily Schedule**: Full test suite + coverage check

### GitHub Actions Workflow

See `.github/workflows/ci-cd.yml` for CI configuration.

## E2E Testing (Future)

Plan to add Playwright/Cypress for end-to-end testing:

```bash
# Install Playwright
npm install -D @playwright/test

# Run E2E tests
npm run test:e2e
```

Example E2E test:

```typescript
import { test, expect } from "@playwright/test";

test("user can register and login", async ({ page }) => {
  // Navigate to register page
  await page.goto("/register");

  // Fill registration form
  await page.fill('input[name="email"]', "test@example.com");
  await page.fill('input[name="password"]', "SecurePassword123!@#");
  await page.fill('input[name="confirmPassword"]', "SecurePassword123!@#");

  // Submit form
  await page.click('button[type="submit"]');

  // Verify redirect to dashboard
  await expect(page).toHaveURL("/dashboard");
});
```

## Performance Testing

Monitor test execution time:

```bash
npm test -- --detectOpenHandles
```

Optimize slow tests by:

1. Reducing database calls
2. Mocking external services
3. Using in-memory databases for tests

## Troubleshooting

### Tests Fail Locally but Pass in CI

- Clear node_modules: `rm -rf node_modules && npm install`
- Reset database: `npx prisma migrate reset`
- Check Node version: `node --version` (should match .nvmrc)

### Database Connection Errors

```bash
# Use test database
export DATABASE_URL="file:./test.db"
npx prisma migrate deploy
npm test
```

### Tests Timeout

Increase timeout:

```typescript
it("slow test", async () => {
  // test code
}, 10000); // 10 second timeout
```

### Mock Not Working

```typescript
// Clear all mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
});
```

## Support

For testing questions:

- Review test examples in `__tests__/`
- Check Jest documentation: https://jestjs.io
- Ask in GitHub discussions

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
