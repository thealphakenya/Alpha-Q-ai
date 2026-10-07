# QMOI Enhanced - Production-Ready Fintech Platform

[![CI/CD](https://github.com/thealphakenya/qmoi-enhanced/workflows/CI%2FCD/badge.svg)](https://github.com/thealphakenya/qmoi-enhanced/actions)
[![Code Quality](https://img.shields.io/badge/code%20quality-A-brightgreen)](./CODE_QUALITY.md)
[![TypeScript](https://img.shields.io/badge/typescript-5.2-blue)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/node-20%2B-brightgreen)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

QMOI Enhanced is a production-ready financial platform built with modern web technologies. It provides user authentication, wallet management, transaction processing, and multi-provider payment integration.

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- npm or yarn
- PostgreSQL 12+ (or SQLite for development)
- Redis (optional, for caching)

### Installation

```bash
# Clone repository
git clone https://github.com/thealphakenya/qmoi-enhanced.git
cd qmoi-enhanced

# Install dependencies
npm install

# Setup environment
cp .env.local.example .env.local

# Run database migrations
npx prisma migrate dev

# Start development server
npm run dev
```

Visit `http://localhost:3000` - application is ready!

## 📚 Documentation

### Getting Started

- [Quick Start Guide](./QUICK_START.md) - 5-minute setup
- [Production Setup](./PRODUCTION_SETUP.md) - Production deployment guide
- [Environment Configuration](./ENVIRONMENT_CONFIG.md) - Environment variables guide

### API & Integration

- [API Documentation](./API.md) - Complete API reference
- [Postman Collection](./postman-collection.json) - Importable API collection

### Development

- [Testing Guide](./TESTING.md) - Writing and running tests
- [Development Setup](./DEVELOPMENT.md) - Detailed dev environment setup

### Operations

- [Deployment Guide](./DEPLOYMENT.md) - Multi-platform deployment (Docker, Heroku, AWS)
- [Performance Guide](./PERFORMANCE_GUIDE.md) - Optimization strategies
- [Monitoring Guide](./MONITORING.md) - Observability and alerts

### Security

- [Security Guide](./SECURITY.md) - Security best practices
- [Security Policy](./SECURITY_POLICY.md) - Reporting vulnerabilities

## 🏗️ Architecture

### Tech Stack

```
Frontend: Next.js 15.5 + React 18.2 + TypeScript 5.2
Backend: Next.js API Routes + Node.js
Database: PostgreSQL/SQLite + Prisma ORM
Cache: Redis
Auth: JWT + bcrypt
Payments: M-Pesa + PayPal + Stripe
Email: SendGrid
Notifications: Twilio, Telegram, WhatsApp
Container: Docker + Docker Compose
CI/CD: GitHub Actions
```

### Directory Structure

```
qmoi-enhanced/
├── app/
│   ├── api/                    # API routes
│   │   ├── auth/              # Authentication endpoints
│   │   ├── payments/          # Payment endpoints
│   │   ├── users/             # User endpoints
│   │   ├── wallets/           # Wallet endpoints
│   │   ├── transactions/      # Transaction endpoints
│   │   └── webhooks/          # Webhook handlers
│   ├── components/            # React components
│   ├── layout.tsx             # Root layout
│   └── page.tsx               # Home page
├── lib/
│   ├── db/
│   │   ├── prisma.ts          # Prisma client
│   │   └── services.ts        # Database services
│   ├── auth/
│   │   └── service.ts         # Authentication service
│   ├── email/
│   │   └── service.ts         # Email service
│   ├── payments/
│   │   └── service.ts         # Payment processing
│   └── notifications/
│       └── service.ts         # SMS/Telegram/WhatsApp
├── prisma/
│   ├── schema.prisma          # Data models
│   └── migrations/            # Database migrations
├── __tests__/
│   ├── api/                   # API tests
│   ├── integration/           # Integration tests
│   └── utils/                 # Test utilities
├── .github/
│   └── workflows/             # GitHub Actions
├── scripts/
│   ├── healthcheck.sh         # Health verification
│   ├── backup.sh              # Database backup
│   └── migrate.sh             # Safe migrations
├── docker-compose.yml         # Local development stack
├── Dockerfile                 # Production image
├── PRODUCTION_SETUP.md        # Production guide
├── DEPLOYMENT.md              # Deployment guide
├── API.md                     # API reference
└── package.json               # Dependencies
```

## 🔑 Core Features

### User Management

- ✅ User registration with validation
- ✅ JWT-based authentication
- ✅ User profiles with customizable fields
- ✅ Password security with bcrypt
- ✅ Account recovery

### Wallet Management

- ✅ Multi-currency wallets
- ✅ Balance tracking
- ✅ Wallet creation/update/deletion
- ✅ Wallet history

### Payment Integration

- ✅ M-Pesa integration
- ✅ PayPal integration
- ✅ Stripe integration
- ✅ Webhook handlers
- ✅ Transaction tracking

### Notifications

- ✅ Email notifications (SendGrid)
- ✅ SMS notifications (Twilio)
- ✅ WhatsApp notifications
- ✅ Telegram notifications

### Security

- ✅ JWT authentication
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ CORS configuration

## 🧪 Testing

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- __tests__/api/auth.test.ts

# Watch mode
npm test -- --watch
```

**Coverage Thresholds:** 70% branches, functions, lines, statements

## 🚢 Deployment

### Docker

```bash
docker build -t qmoi-enhanced .
docker run -e DATABASE_URL="..." -p 3000:3000 qmoi-enhanced
```

### Docker Compose

```bash
docker-compose up
```

### Heroku

```bash
heroku create qmoi-app
git push heroku main
```

### AWS

See [DEPLOYMENT.md](./DEPLOYMENT.md) for ECS, Lambda, RDS setup

## 📊 Monitoring

Monitor application health via:

- **Sentry:** Error tracking
- **Datadog:** Metrics and logs
- **New Relic:** Performance monitoring
- **AWS CloudWatch:** Infrastructure metrics

See [MONITORING.md](./MONITORING.md) for setup

## 🔐 Security

- ✅ End-to-end encryption for payments
- ✅ Rate limiting (100 req/hr per user)
- ✅ CORS restricted to known domains
- ✅ HTTPS only (production)
- ✅ Secrets management (AWS Secrets Manager)
- ✅ Regular security audits
- ✅ GDPR compliant

See [SECURITY.md](./SECURITY.md) for details

## 📈 Performance

**Benchmarks:**

- Page load: < 3 seconds
- API response: < 200ms
- Database query: < 100ms
- Lighthouse: > 90

**Optimizations:**

- Next.js code splitting
- Database indexes
- Redis caching
- Image optimization
- Bundle optimization

See [PERFORMANCE_GUIDE.md](./PERFORMANCE_GUIDE.md) for details

## 🛠️ Development

### Setup Development Environment

```bash
npm install
cp .env.local.example .env.local
npx prisma migrate dev
npm run dev
```

### Code Quality

```bash
# Run linter
npm run lint

# Type check
npm run type-check

# Format code
npm run format
```

### Database Management

```bash
# Create migration
npx prisma migrate dev --name add_feature

# Reset database
npx prisma migrate reset

# Open Prisma Studio
npx prisma studio
```

## 📝 API Examples

### Register User

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePassword123!@#"
  }'
```

### Get User Profile

```bash
curl http://localhost:3000/api/users/profile \
  -H "Authorization: Bearer {token}"
```

### Create Wallet

```bash
curl -X POST http://localhost:3000/api/wallets \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"currency": "KES"}'
```

See [API.md](./API.md) for complete reference

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing`)
5. Open pull request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines

## 📄 License

MIT License - see [LICENSE](./LICENSE) file

## 🆘 Support

- **Documentation:** https://docs.qmoi.app
- **Issues:** https://github.com/thealphakenya/qmoi-enhanced/issues
- **Security:** security@qmoi.app
- **Email:** support@qmoi.app

## 🎯 Roadmap

### Q1 2024

- [ ] 2FA (Two-Factor Authentication)
- [ ] Advanced analytics dashboard
- [ ] Transaction history export (CSV/PDF)
- [ ] Recurring payments

### Q2 2024

- [ ] Mobile app (React Native)
- [ ] Business accounts
- [ ] Advanced reporting
- [ ] API webhooks v2

### Q3 2024

- [ ] AI-powered fraud detection
- [ ] Tokenization for payment methods
- [ ] Advanced account security
- [ ] Multi-language support

### Q4 2024

- [ ] Peer-to-peer transfers
- [ ] Investment features
- [ ] Advanced compliance tools
- [ ] Global expansion

## 🎓 Learning Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Prisma Documentation](https://www.prisma.io/docs/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Node.js Best Practices](https://nodejs.org/en/docs/guides/)
- [OWASP Security](https://owasp.org/www-project-top-ten/)

## 🙏 Acknowledgments

Built with modern technologies and best practices for production-grade applications.

---

**Made with ❤️ by QMOI Enhanced Team**

Last updated: 2024-01-09

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10428`; directories: `1268`; Markdown: `2416`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2109, orchestration=2061, qteam_accountability=2049, release_tag_publish=2088, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2221`; needs review: `187`; metric candidate lines: `52705`; percentage occurrences: `22237`.
- Markdown word count: `3550281`; heuristic sentence count: `673664`; sentence records indexed: `673664`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29834` metric claims; `10658` completion claims; `29737` metric and `10529` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13328`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `39967` lines in `3666` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `286`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
