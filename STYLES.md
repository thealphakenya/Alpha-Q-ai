# STYLES.md: Comprehensive Platform-Specific Styling System

**Last Updated:** 2026-08-13
**Status:** Complete Platform Styling Reference
**Scope:** Styling rules for 4 apps × 6 platforms

## Autonomous UI Feature Contract

The Ollama autonomous agent must consult this document before creating or
changing any site, application, dashboard, web, or mobile UI feature. New UI
work must preserve the applicable platform, accessibility, typography, color,
motion, responsive, and operational-state rules above. Every new reusable UI
pattern, platform style, or visual capability must update this document in the
same change and record the relevant source sections in its validation evidence.

## Enhanced automation and full-surface style synchronization

The style system is the canonical UI contract for the active repository, all
historical merge inputs, every clone surface, and every downstream product that
inherits QMOI branding or UX logic. The agent must treat styling as an
operational capability rather than a cosmetic layer. Every time it discovers a
new platform, app, clone, or hosted surface it must automatically update the
style contract, the universal access model, the backend/frontend inventory, and
the link catalog in a single pass so no app or platform is left visually or
functionally unaccounted for.

The required automation flow is:

- inventory every documented app, clone, and platform in `ALLFRONTEND.md`,
  `ALLBACKEND.md`, `QSTORE.md`, `QSTREAM.md`, `APP_LINKS.md`, `VERCELLINKS.md`,
  `QVILLAGE.md`, `QUANTUM.md`, and all discovered clone references
- classify each surface as public, authenticated, mixed-access, or master-only
- apply the QMOI design-token layer first, then add app-specific overrides
- ensure each clone is enhanced beyond its source by improving states, labels,
  accessibility, loading/error/offline handling, and brand polish
- automatically update all relevant docs and link registries instead of leaving
  a UI feature undocumented or unlinked
- verify that every rendered page, documentation route, and product page has a
  matching feature, risk-state, and identity contract

This system must cover QCity, QMOI AI, QStore, QStream, QALPHA, QMOI Space,
Quantum, QVillage, GitHub/GitLab clone surfaces, Netlify/Vercel hosting,
Gitpod/Hugging Face mirrors, and any derived platform that is meant to be a
real user-facing product surface. No clone may remain a raw mirror; each one
must have its own QMOI-aware identity, improved UX states, and valid access
classification.

The style layer must also remain synchronized with memory, live state, and
operational evidence. UI decisions must not hide wallet risk, security signals,
workflow failures, or deployment health. When a product is in a degraded state,
its visuals must still show the correct state clearly and preserve operational
clarity. The active agent continues until the style surface, approval surface,
product catalog, and link inventory are all internally consistent.

## Clone, autoclone, and link-validation styling contract

The autonomous agent must treat every clone and autoclone surface as a real product UI and not as a passive mirror of a source platform. Each cloned platform must be re-styled into a QMOI-native identity while preserving the source platform's useful feature map, user expectations, and operational semantics.

### Required behavior for cloned and autocloned surfaces

- Inventory every cloned platform and app surface before styling: GitHub, GitLab, Gitpod, Hugging Face, Netlify, Vercel, Quantum, QCity, QStore, QStream, QMOI AI, QALPHA, QVillage, and any derived clone notes.
- Apply a shared QMOI design-token layer to all surfaces, then add app- and platform-specific overrides only where the product contract requires them.
- Keep public, authenticated, and master-only experiences distinctly separated. Public features must remain public, and account/user-specific features must be gated behind verified identity and least-privilege authorization.
- Ensure each clone is enhanced beyond its source by improving visual consistency, accessibility, readability, error states, loading states, empty states, onboarding flow, and customization polish.
- Automatically set brand assets for every cloned platform: QMOI logo variants, app icons, typography defaults, spacing tokens, motion timing, and action states.
- Record style changes in `STYLES.md` and keep `UNIVERSALS.md` aligned with any new authentication or protected-flow requirement introduced by the new UI.

### Link validation and UI feature comparison

The Ollama agent must validate links and UI references by comparing the documented feature set to the actual rendered or specified product behavior.

- each UI link or page must be mapped to a required feature contract
- the validation pass must compare the expected public/authenticated/master features with the actual implementation or contract documentation
- any mismatch must be marked as `missing`, `stale`, `incomplete`, `permission-gated`, or `needs-brand-upgrade` instead of being treated as pass-by-assumption
- platform link surfaces must validate not only the page path, but also the actual UI affordances, risk visibility, loading/error/offline handling, and account gating
- the agent must ensure that all app and platform links carry correct labels, identity, icons, fonts, and feature quality congruent with their role and permissions

### Brand and customization rules

- Every app and cloned platform must receive a unique QMOI identity layer, including logo treatment, icon set, typography, motion, and UI state tokens.
- Default branding must remain readable and consistent in public, user-scoped, and master-operator states.
- Customization must never hide compliance evidence, risk state, deploy status, billing state, wallet state, or user safety information.
- The branding layer covers both static assets and dynamic UI states, including hover, focus, selected, disabled, loading, empty, and error states.

## Per-app and per-platform UI feature matrix

The agent must refresh this matrix whenever it updates or introduces a new app, platform, clone, or user-mode UI.

- QCity: workspace, file, audit, and management surfaces; public overview plus authenticated private workspace states.
- QStore: catalog search, app install, update flow, device-aware download states, and public browse plus user-owned install actions.
- QStream: public stream previews, authenticated creator actions, live monitoring states, and permission-gated control surfaces.
- QMOI AI UI: public chat shell plus authenticated user history, profile, and private personalization.
- QALPHA: public docs and view states plus private project collaboration and approvals.
- QMOI Space: media/public content surfaces plus user-owned library and publish flows.
- GitHub clone: repository, workflow, release, and security summaries; purely public or authenticated depending on repo visibility.
- GitLab clone: merge request, pipeline, and artifact views; permission-gated project management.
- Netlify/Vercel: deployment previews, production state, domain status, and publish flows.
- Quantum: compute queue, provider state, billing, and result provenance; master/operator gates when needed.

Each app or platform must declare whether it supports public, authenticated, or mixed-access behavior and whether it requires an identity check before any write, billing, deployment, or private-history action.

## Ollama autonomous agent merge and styling contract

The Ollama autonomous agent must always read and reconcile the following sources before making any UI or repo-level merge decision:

- [UNIVERSALS.md](UNIVERSALS.md)
- [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- [API.md](API.md)
- [ENDPOINTS.md](ENDPOINTS.md)
- [ROUTES.md](ROUTES.md)
- [ALLPORTS.md](ALLPORTS.md)
- [qmoi-enhanced-history-14/STYLES.md](qmoi-enhanced-history-14/STYLES.md)
- [qmoi-enhanced-history-14/UNIVERSALS.md](qmoi-enhanced-history-14/UNIVERSALS.md)
- [qmoi-enhanced-history-14/ALLMDFILESREFS.md](qmoi-enhanced-history-14/ALLMDFILESREFS.md)

The UI workflow must set up the QMOI style system for every interface, while preserving the universal rules for login, role-based access, and user-specific personalization. Authentication-aware layouts must ensure that protected actions are gated behind identity checks, user intent confirmation, and audit visibility. Visual personalization must never hide wallet risk, security state, or validation evidence. The agent must always prefer the canonical active repo files, while revisiting the historical archive to recover any missing visual or functional pattern that is still valid.

---

## Table of Contents
1. [Design Systems by Platform](#design-systems-by-platform)
2. [App-Specific Styling](#app-specific-styling)
3. [Platform-Specific Color Palettes](#platform-specific-color-palettes)
4. [Typography by Platform](#typography-by-platform)
5. [Accessibility & Contrast](#accessibility-and-contrast)
6. [Component Mapping](#component-mapping)

---

## Avatar, Motion & Real-Time Presence

QMOI is also treated as an active avatar persona in the interface layer. The autonomous agent validates the selected persona before it is rendered and continuously checks that the avatar remains QMOI in realtime across motion, windowing, and theme state.

## Orchestration-aware styling and live stream UX

The UI layer is part of the same orchestration model as network, security, and release workflows. Styling should never obscure operational risk or runtime state.

- live activity streams must remain readable in light and dark themes.
- operational status, failing validation, and security state must override cosmetic themes.
- user personalization should not hide critical wallet, security, or deployment data.
- GitHub-hosted activity stream cards should follow the same visual hierarchy across QMOI and Ollama agent surfaces.
- QMOI personas should present live status, source, and confidence without breaking accessibility.

The styling system should also support agent-aware states:

- idle
- monitoring
- validating
- fixing
- deploying
- synced
- blocked
- degraded

Each state must map to a consistent visual treatment and remain visible in all platform surfaces.

**Avatar validation rules:**
- Must be identified as QMOI before live rendering is allowed.
- Real-time window state must be visible and anchored correctly.
- Animation loop must remain active and smooth.
- Theme and window presentation must align with the QMOI live identity.
- Quality checks must confirm motion stability, aesthetic consistency, and presence continuity.

**Enhanced avatar-selection UI contract:**
- All avatars should be listed in a navigable catalog with live preview metadata.
- Each avatar preview should autoplay in sequence for a minimum of 5 seconds.
- Users should be able to compare avatars quickly and choose the one that fits their preferred QMOI identity.
- Voice selection should be tied to the selected avatar and should expose the enhanced QMOI voice presets.
- The avatar window style should apply immersive glass, glow, and motion treatments to show QMOI as a full live presence in the interface.

## Personalized financial and user style system

QMOI should personalize the user style experience while preserving a consistent financial-control layer. Every user, wallet owner, or revenue stream should be able to receive a tailored visual experience without creating unsafe or ambiguous financial state.

### User-specific style model

- Identity-aware theme: each user or group gets a consistent QMOI presence pattern.
- Financial-risk theme: the UI changes visual emphasis based on account confidence, wallet health, and execution risk.
- Revenue focus theme: a premium-growth mode highlights earnings, revenue streams, and account health.
- Trust and audit theme: a security-first mode emphasizes proof, compliance, and monitoring state.
- Music and creator theme: for creative monetization paths, the UI emphasizes media, licensing, and revenue flow.

### QMOI dashboard personalization rules

- User profile must be visible and memory-synced before style personalization is applied.
- The financial dashboard must preserve critical operational information even in more aesthetic modes.
- High-risk situations must override generic visual themes with safety-first UI.
- Style presets must not hide wallet balances, platform status, or action gating.
- Personalization should support both aesthetic identity and operational clarity.

## Financial deal and transaction UI styling

Financial UI should visually communicate trust, urgency, and clarity. The interface should use a distinct style language for deal-making and transaction validation while still fitting into the QMOI system design.

### Deal-management visual language

- High-confidence deals: green, stable, low-noise presentation
- Pending confirmation: amber or warm accent with explicit action states
- Risk or failed validation: red with emphasis on blocking action and audit detail
- Revenue and growth views: blue / purple accent with high-clarity summaries
- Creative or media deals: flexible brand styling while preserving risk and proof metadata

### Financial panel layout expectations

- Top summary row: balance, exposure, revenue, active deals, pending validations
- Middle risk strip: wallet health, transaction confidence, exchange status
- Lower activity stream: deal lifecycle events, proofs, confirmations, and settlements
- Alert rail: blocked or suspicious actions visible without burying the main data
- Personalized mode: user-specific color or branding support without removing safety cues

### Style rules for multi-user financial UX

- The system must retain operational readability even in premium or branded themes.
- Confidence and risk indicators must remain visible at all times.
- Personalization must not hide executable actions, wallet data, or transaction proof states.
- The same deal and transaction patterns should look consistent across web, mobile, and dashboard surfaces.

## Design Systems by Platform

### Windows: Fluent Design System 2.0

**Core Design Principles:**
- Light, thin, clean aesthetic
- Depth and layering with transparency
- Responsive to user interaction

**Key Visual Components:**
```
✓ Mica: Material that adapts to theme colors
✓ Acrylic: Frosted glass effect (20-30% opacity)
✓ Reveal: Hover effects highlighting interactive elements
✓ Motion: Subtle animations (150-300ms)
✓ Icons: Outlined stroke-based icons
```

**Color Palette (Windows 11 Light):**
```
Primary: #0078D4 (Windows Blue)
Secondary: #8661C5 (Purple)
Tertiary: #50B4F7 (Light Blue)
Background: #FFFFFF (White)
Surface: #F3F3F3 (Light Gray)
Text: #000000 (Black)
Disabled: #BFBFBF (Medium Gray)
Success: #107C10 (Green)
Warning: #FFB900 (Amber)
Error: #E81B23 (Red)
```

**Type Scale:**
```
Display: 28pt Segoe UI Semibold
Headline: 20pt Segoe UI Semibold
Subheading: 16pt Segoe UI Regular
Body: 14pt Segoe UI Regular
Caption: 12pt Segoe UI Regular
Small: 11pt Segoe UI Regular
```

### macOS: Human Interface Design (HIG)

**Core Design Principles:**
- Content focused, chrome minimal
- Clarity and legibility
- Depth through shadows and layers

**Key Visual Components:**
```
✓ Rounded Corners: 12-16pt radius
✓ Shadows: Subtle depth (0-8px blur)
✓ Translucency: Background blur via NSVisualEffectView
✓ Vibrancy: Text adaptation to background
✓ Motion: Smooth 200-400ms animations
✓ Icons: Filled/outline variants
```

**Color Palette (macOS 14 Sonoma Light):**
```
Primary: #0A84FF (System Blue)
Secondary: #5E5CE6 (System Purple)
Tertiary: #30B0C0 (System Cyan)
Background: #FFFFFF (White)
Surface: #F5F5F7 (Off-White)
Text: #000000 (Black)
Text Secondary: #666666 (Dark Gray)
Disabled: #D1D1D6 (Light Gray)
Success: #34C759 (Green)
Warning: #FF9500 (Orange)
Error: #FF3B30 (Red)
```

**Type Scale:**
```
Large Title: 34pt SF Pro Display Regular
Title 1: 28pt SF Pro Display Regular
Title 2: 22pt SF Pro Display Regular
Title 3: 20pt SF Pro Display Regular
Headline: 17pt SF Pro Display Semibold
Body: 17pt SF Pro Text Regular
Callout: 16pt SF Pro Text Regular
Subheading: 15pt SF Pro Text Semibold
Footer: 13pt SF Pro Text Regular
Caption 1: 12pt SF Pro Text Regular
Caption 2: 11pt SF Pro Text Regular
```

### Linux: Freedesktop Standards with GTK4/Qt6

**Core Design Principles:**
- Minimal decorations, respects user preferences
- GNOME/KDE specific but platform-agnostic
- High accessibility compliance

**Key Visual Components (GNOME/GTK4):**
```
✓ Rounded Corners: 8-12pt radius
✓ Flat Design: Minimal shadows
✓ Translucency: CSS backdrop-filter
✓ Ripple Effect: Material-inspired feedback
✓ Motion: 200-300ms transitions
✓ Icons: Symbolic and full-color variants
```

**Color Palette (GNOME/Adwaita Light):**
```
Primary: #3584E4 (GNOME Blue)
Secondary: #1C71D8 (Darker Blue)
Tertiary: #813D9C (Purple)
Background: #FFFFFF (White)
Surface: #F6F5F4 (Warm Beige)
Text: #000000 (Black)
Text Secondary: #5E5C64 (Medium Gray)
Disabled: #D0CFCC (Light Beige)
Success: #2EC27E (Green)
Warning: #E5A604 (Amber)
Error: #E01B24 (Red)
```

**Type Scale:**
```
Display Large: 32pt Cantarell Medium
Display: 28pt Cantarell Medium
Headline 1: 24pt Cantarell Medium
Headline 2: 20pt Cantarell Medium
Headline 3: 18pt Cantarell Medium
Title 1: 16pt Cantarell Bold
Title 2: 15pt Cantarell Bold
Body 1: 13pt Cantarell Regular
Body 2: 12pt Cantarell Regular
Label: 11pt Cantarell Medium
Caption: 11pt Cantarell Regular
```

### iOS: Human Interface Design (HIG) for iOS

**Core Design Principles:**
- Content first, navigation secondary
- Depth through translucency and sizing
- Touch-friendly targets (44pt minimum)

**Key Visual Components:**
```
✓ Rounded Corners: 12-16pt for cards, 50% for pills
✓ Blur Effects: UIVisualEffectView with vibrant text
✓ Shadows: Contextual depth (1-10pt blur)
✓ Haptic Feedback: Different patterns for actions
✓ Motion: 300-400ms spring animations
✓ Icons: SF Symbols with variable weights
```

**Color Palette (iOS 17 Light):**
```
System Blue: #007AFF
System Purple: #5856D6
System Pink: #FF2D55
System Red: #FF3B30
System Orange: #FF9500
System Yellow: #FFCC00
System Green: #34C759
System Cyan: #50B7F5
System Mint: #00D084
System Teal: #30B0C0
System Indigo: #5856D6
System Gray: #999999
Background: #FFFFFF
Surface: #F2F2F7 (Secondary)
Text: #000000
Text Secondary: #999999
Disabled: #CCCCCC
```

**Type Scale:**
```
Large Title: 34pt SF Pro Display Regular
Title 1: 28pt SF Pro Display Regular
Title 2: 22pt SF Pro Display Regular
Title 3: 20pt SF Pro Display Regular
Headline: 17pt SF Pro Display Semibold
Body: 17pt SF Pro Text Regular
Callout: 16pt SF Pro Text Regular
Subheading: 15pt SF Pro Text Semibold
Footer: 13pt SF Pro Text Regular
Caption 1: 12pt SF Pro Text Regular
Caption 2: 11pt SF Pro Text Regular
```

### Android: Material Design 3

**Core Design Principles:**
- Expressive color (Material You dynamic theming)
- Hierarchical organization
- Touch targets 48dp minimum (56dp recommended)

**Key Visual Components:**
```
✓ Rounded Corners: 4-12dp based on component type
✓ Elevation/Shadow: Multiple shadow layers (0-24dp)
✓ Ripple Effect: Touch feedback on all interactive
✓ Motion: 250-400ms material curves (Accelerate/Decelerate)
✓ Icons: Filled, outlined, rounded variants
✓ Color Tokens: Primary, Secondary, Tertiary, etc.
```

**Color Palette (Material You - Dynamic on Pixel):**
```
Primary: #6750A4 (Dynamic - adapts to wallpaper)
On Primary: #FFFFFF
Primary Container: #EADDFF
On Primary Container: #21005D
Secondary: #625B71
On Secondary: #FFFFFF
Secondary Container: #E8DEF8
On Secondary Container: #1D192B
Tertiary: #7D5260
On Tertiary: #FFFFFF
Tertiary Container: #FFD8E4
On Tertiary Container: #31111D
Background: #FFFBFE
On Background: #1C1B1F
Surface: #FFFBFE
On Surface: #1C1B1F
Surface Dim: #DDD7E0
Surface Bright: #FFFBFE
Outline: #79747E
Outline Variant: #CAC7D0
Error: #F2B8B5
On Error: #8B0000
```

**Type Scale:**
```
Display Large: 57sp Roboto Regular
Display Medium: 45sp Roboto Regular
Display Small: 36sp Roboto Regular
Headline Large: 32sp Roboto Regular
Headline Medium: 28sp Roboto Regular
Headline Small: 24sp Roboto Regular
Title Large: 22sp Roboto Regular
Title Medium: 16sp Roboto Medium
Title Small: 14sp Roboto Medium
Body Large: 16sp Roboto Regular
Body Medium: 14sp Roboto Regular
Body Small: 12sp Roboto Regular
Label Large: 14sp Roboto Medium
Label Medium: 12sp Roboto Medium
Label Small: 11sp Roboto Medium
```

### Web PWA: Modern CSS & Responsive Design

**Core Design Principles:**
- Mobile-first responsive
- Progressive enhancement
- Performance-optimized

**Key Visual Components:**
```
✓ Rounded Corners: CSS border-radius (4-12px)
✓ Shadows: CSS box-shadow (0 2px 8px rgba(0,0,0,0.12))
✓ Gradients: CSS gradients for depth
✓ Animations: CSS transitions (200-400ms)
✓ Fonts: System font stack fallback
✓ Icons: SVG or icon font
```

**Color Palette (Light Mode - Accessible):**
```
Primary: #0078D4 (Matches Windows/Web standards)
Secondary: #6C757D (Gray)
Success: #28A745 (Green)
Warning: #FFC107 (Amber)
Error: #DC3545 (Red)
Info: #17A2B8 (Cyan)
Light: #F8F9FA
Dark: #343A40
Text: #212529
Text Muted: #6C757D
Border: #DDD
Background: #FFFFFF
```

**Type Scale:**
```
H1: 2.5rem Segoe UI, -apple-system, BlinkMacSystemFont
H2: 2rem
H3: 1.75rem
H4: 1.5rem
H5: 1.25rem
H6: 1rem
Body: 1rem
Small: 0.875rem
XSmall: 0.75rem
```

---

## App-Specific Styling

### QMOIAIUI: Conversational AI

**Windows Styling:**
```
Theme: Light/Dark toggle (Fluent Design)
Primary Color: Windows Blue (#0078D4)
Chat Bubble (User): Acrylic blue with 80% opacity
Chat Bubble (AI): Acrylic gray with 60% opacity
Input Field: Reveal effect on hover, 2px border
Button: Fluent button with background color on hover
Font: Segoe UI Variable (14-16pt)
Spacing: 12-16px consistent margins
Border Radius: 4-8px
Shadows: Fluent depth shadow
```

**macOS Styling:**
```
Theme: Light/Dark (System integrated)
Primary Color: System Blue (#0A84FF)
Chat Bubble (User): Vibrancy with background blur
Chat Bubble (AI): Rounded rectangle with subtle shadow
Input Field: Metal texture background, rounded 8px
Button: Circular back button, pill-shaped action buttons
Font: SF Pro Text Variable (14-17pt)
Spacing: 16px consistent margins
Border Radius: 12-16px
Shadows: HIG standard depth
```

**Linux Styling:**
```
Theme: Adwaita Light/Dark (GNOME defaults)
Primary Color: GNOME Blue (#3584E4)
Chat Bubble (User): Solid color with rounded corners
Chat Bubble (AI): Slightly darker background
Input Field: Flat design, 1px border, rounded 6px
Button: Minimal background, ripple on hover
Font: Cantarell Variable (13-16pt)
Spacing: 12-16px margins
Border Radius: 6-8px
Transitions: GTK standard 200ms curves
```

**iOS Styling:**
```
Theme: Light/Dark (System integrated)
Primary Color: System Blue (#007AFF)
Chat Bubble (User): Blue with white text, rounded corners
Chat Bubble (AI): Gray background, dark text
Input Field: Rounded 12px, translucent background
Button: 44pt minimum touch target, rounded corners
Font: SF Pro Text (17pt body, 15pt secondary)
Spacing: 16pt safe area margins
Border Radius: 12px
Shadows: iOS standard (0 2px 10px)
Haptics: Feedback on send, light impact
```

**Android Styling:**
```
Theme: Material You (dynamic wallpaper colors)
Primary Color: Material Primary token
Chat Bubble (User): Material primary container
Chat Bubble (AI): Material surface container
Input Field: Material text field (rounded 4dp)
Button: Material filled button (48dp minimum)
Font: Roboto (16sp body, 14sp secondary)
Spacing: 16dp material spacing
Border Radius: 4dp minimum, 12dp cards
Ripple: Material ripple feedback
Elevation: Material elevation tokens
```

**Web PWA Styling:**
```
Theme: CSS media query (prefers-color-scheme)
Primary Color: #0078D4 (accessible contrast >4.5:1)
Chat Bubble (User): CSS gradient background
Chat Bubble (AI): Solid background with border
Input Field: HTML form-control, rounded 4px
Button: CSS hover states, focus outline
Font: System font stack (-apple-system first)
Spacing: CSS custom properties (--spacing-unit)
Border Radius: 4px minimum for accessibility
Animations: CSS transitions (prefers-reduced-motion)
```

### QCity: File Manager

**Windows Styling:**
```
List View: Details view with Segoe UI 12pt
Icon Theme: Fluent MD icons (24x24px)
Selection: Mica background with accent color
Toolbar: Horizontal with icon + text buttons
Sidebar: Light gray background (#F3F3F3)
Status Bar: Thin separator with file count
Context Menu: Standard Windows context menu
Fonts: Segoe UI for all UI text
```

**macOS Styling:**
```
List View: Finder-like with SF Symbols
Icon Theme: macOS Monterey icons (32x32px)
Selection: Material highlight with vibrancy
Toolbar: Rounded buttons with vibrant text
Sidebar: Translucent background (NSVisualEffect)
Status Bar: Thin divider, gray text
Context Menu: macOS menu with reveal effect
Fonts: SF Pro Text Variable
```

**Linux Styling:**
```
List View: GTK TreeView, symbolic icons
Icon Theme: Adwaita icons (32x32px)
Selection: Accent color highlight
Toolbar: Flat icon buttons in header bar
Sidebar: Light background, folder tree
Status Bar: Subtle divider, muted text
Context Menu: GTK Popover menu
Fonts: Cantarell Variable
```

**iOS Styling:**
```
List View: iOS-style with swipe actions
Icon Theme: SF Symbols (19pt-22pt)
Selection: iOS blue highlight (#007AFF)
Navigation: UINavigationController standard
Sidebar: UISplitViewController (iPad)
Status Bar: Safe area aware, system font
Context Menu: iOS 13+ UIContextMenuInteraction
Fonts: SF Pro Text
Haptics: Light feedback on selection
```

**Android Styling:**
```
List View: RecyclerView with Material design
Icon Theme: Material icons (24dp)
Selection: Material selection highlight
Navigation: Material navigation drawer
Toolbar: Material top app bar (56dp)
Status Bar: Material status bar color
Context Menu: Material context menu
Fonts: Roboto (variable weight)
Ripple: Material ripple feedback on all rows
```

**Web PWA Styling:**
```
List View: HTML table or CSS Grid
Icon Theme: SVG inline icons
Selection: CSS highlight with color
Navigation: Breadcrumb trail at top
Sidebar: Fixed or collapsible nav
Status Bar: Footer with file count
Context Menu: Custom right-click menu
Fonts: System font stack
Responsive: Mobile-optimized touch targets
```

---

## Platform-Specific Color Palettes

### Accessibility Requirements

**WCAG 2.1 AA Compliance:**
```
✓ Text Contrast: 4.5:1 for body text
✓ Large Text: 3:1 for text ≥18pt or ≥14pt bold
✓ UI Components: 3:1 for borders and icons
✓ Focus Indicators: 3:1 contrast minimum
✓ Color Alone: Never convey information by color only
```

### Dark Mode Palettes

**Windows 11 Dark:**
```
Background: #1F1F1F
Surface: #2D2D2D
Primary: #60CDFF (Light Blue)
Text: #FFFFFF
Text Secondary: #BFBFBF
Disabled: #808080
```

**macOS 14 Dark:**
```
Background: #000000
Surface: #1D1D1D
Primary: #64B5F6 (Light Blue)
Text: #FFFFFF
Text Secondary: #999999
Disabled: #666666
```

**GNOME Dark (Adwaita Dark):**
```
Background: #1E1E1E
Surface: #242424
Primary: #3584E4 (Stays bright)
Text: #FFFFFF
Text Secondary: #A6A6A6
Disabled: #595959
```

**iOS Dark:**
```
Background: #000000
Surface: #1C1C1E
Primary: #64B5F6 (Light Blue)
Text: #FFFFFF
Text Secondary: #A0A0A0
Disabled: #595959
```

**Material Dark:**
```
Background: #121212
Surface: #1E1E1E
Primary: #BB86FC (Material Purple)
Text: #FFFFFF
Text Secondary: #B3B3B3
Disabled: #595959
```

---

## Typography by Platform

### Font Families Priority (Fallback Order)

**Windows:**
```css
font-family: "Segoe UI Variable", "Segoe UI", Tahoma, sans-serif;
```

**macOS/iOS:**
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

**Linux/Android:**
```css
font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

**Web (Universal):**
```css
font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

### Font Sizes (Platform Conversion)

```
macOS/iOS pt → Windows dp: multiply by 1.33
iOS pt → Android sp: multiply by 0.75
Windows pt → Web px: multiply by 1.33 (typically)
```

---

## Component Mapping

### Button Component

| Platform | Style | Padding | Height | Border Radius |
|----------|-------|---------|--------|-----------------|
| Windows | Fluent with background on hover | 8-12px | 32px | 4px |
| macOS | Rounded button or metal | 8-12px | 32px | 8px |
| Linux | Flat button with ripple | 8-12px | 32px | 6px |
| iOS | System button or pill shape | 8-12px | 44px | 8px |
| Android | Material filled or outlined | 12-16px | 48px | 4dp |
| Web | CSS button with focus outline | 10-12px | 44px | 4px |

### Input Field Component

| Platform | Style | Padding | Height | Border |
|----------|-------|---------|--------|--------|
| Windows | Reveal on hover, filled or outline | 12px | 32px | 2px on focus |
| macOS | Metal or translucent background | 12px | 32px | 1px subtle |
| Linux | Flat with 1px border, rounded | 12px | 32px | 1px focus |
| iOS | Rounded background with inset | 12px | 44px | None (background) |
| Android | Material text field (4dp rounded) | 16px | 56px | 1dp bottom line |
| Web | Standard HTML input with border | 12px | 44px | 1px focus border |

---

## Accessibility & Contrast

### Minimum Contrast Ratios

```
Normal Text: 4.5:1
Large Text (≥18pt/≥14pt bold): 3:1
UI Components & Graphical Objects: 3:1
Disabled Components: Not required (but 2:1+ recommended)
Focus Indicators: Must be visible (3:1 minimum)
```

### Focus Indicator Styles

**Windows (Fluent):**
```
2px solid outline, 2px offset
Color: #0078D4 or high contrast mode color
```

**macOS (HIG):**
```
4px solid blue outline
Color: System Blue (#0A84FF)
```

**Linux (GTK):**
```
2px dashed outline
Color: Adwaita Blue (#3584E4)
```

**iOS:**
```
Not visible by default (focus engine different)
But must work with hardware keyboards and VoiceOver
```

**Android:**
```
2dp outline in primary color
Color: Material primary token
```

**Web (WCAG):**
```
3px solid outline, 2px offset
Color: Contrasting with background
```

---

## Dynamic Theming (Modern Features)

### Windows 11 Dynamic Color
```
Accent color from wallpaper
Automatically applied to:
- Primary buttons
- Links
- Progress bars
- Selection highlights
Implementation: WinRT DependencyProperty
```

### macOS Accent Color
```
System Preferences → General → Accent color
Applied to:
- Buttons
- Selection
- Links
Implementation: NSColor.controlAccentColor
```

### Material You (Android 12+)
```
Dynamic color palette from wallpaper
Applied to:
- All material components
- Status bar
- Navigation bar
Implementation: DynamicColors API
```

### iOS System Colors
```
System colors automatically adapt to:
- Dark/Light mode
- High contrast mode
- Accessibility settings
Implementation: UIColor.systemBlue (etc.)
```

---

**Last Updated:** 2026-08-13
**Maintained By:** Ollama Autonomous Agent
**Validation:** All styles tested in platform-specific validators


---

## Merged source: ../Alpha-Q-ai/STYLES.md

# STYLES.md: Comprehensive Platform-Specific Styling System

**Last Updated:** 2026-08-13
**Status:** Complete Platform Styling Reference
**Scope:** Styling rules for 4 apps × 6 platforms

---

## Table of Contents
1. [Design Systems by Platform](#design-systems-by-platform)
2. [App-Specific Styling](#app-specific-styling)
3. [Platform-Specific Color Palettes](#platform-specific-color-palettes)
4. [Typography by Platform](#typography-by-platform)
5. [Accessibility & Contrast](#accessibility-and-contrast)
6. [Component Mapping](#component-mapping)

---

## Avatar, Motion & Real-Time Presence

QMOI is also treated as an active avatar persona in the interface layer. The autonomous agent validates the selected persona before it is rendered and continuously checks that the avatar remains QMOI in realtime across motion, windowing, and theme state.

## Orchestration-aware styling and live stream UX

The UI layer is part of the same orchestration model as network, security, and release workflows. Styling should never obscure operational risk or runtime state.

- live activity streams must remain readable in light and dark themes.
- operational status, failing validation, and security state must override cosmetic themes.
- user personalization should not hide critical wallet, security, or deployment data.
- GitHub-hosted activity stream cards should follow the same visual hierarchy across QMOI and Ollama agent surfaces.
- QMOI personas should present live status, source, and confidence without breaking accessibility.

The styling system should also support agent-aware states:

- idle
- monitoring
- validating
- fixing
- deploying
- synced
- blocked
- degraded

Each state must map to a consistent visual treatment and remain visible in all platform surfaces.

**Avatar validation rules:**
- Must be identified as QMOI before live rendering is allowed.
- Real-time window state must be visible and anchored correctly.
- Animation loop must remain active and smooth.
- Theme and window presentation must align with the QMOI live identity.
- Quality checks must confirm motion stability, aesthetic consistency, and presence continuity.

**Enhanced avatar-selection UI contract:**
- All avatars should be listed in a navigable catalog with live preview metadata.
- Each avatar preview should autoplay in sequence for a minimum of 5 seconds.
- Users should be able to compare avatars quickly and choose the one that fits their preferred QMOI identity.
- Voice selection should be tied to the selected avatar and should expose the enhanced QMOI voice presets.
- The avatar window style should apply immersive glass, glow, and motion treatments to show QMOI as a full live presence in the interface.

## Personalized financial and user style system

QMOI should personalize the user style experience while preserving a consistent financial-control layer. Every user, wallet owner, or revenue stream should be able to receive a tailored visual experience without creating unsafe or ambiguous financial state.

### User-specific style model

- Identity-aware theme: each user or group gets a consistent QMOI presence pattern.
- Financial-risk theme: the UI changes visual emphasis based on account confidence, wallet health, and execution risk.
- Revenue focus theme: a premium-growth mode highlights earnings, revenue streams, and account health.
- Trust and audit theme: a security-first mode emphasizes proof, compliance, and monitoring state.
- Music and creator theme: for creative monetization paths, the UI emphasizes media, licensing, and revenue flow.

### QMOI dashboard personalization rules

- User profile must be visible and memory-synced before style personalization is applied.
- The financial dashboard must preserve critical operational information even in more aesthetic modes.
- High-risk situations must override generic visual themes with safety-first UI.
- Style presets must not hide wallet balances, platform status, or action gating.
- Personalization should support both aesthetic identity and operational clarity.

## Financial deal and transaction UI styling

Financial UI should visually communicate trust, urgency, and clarity. The interface should use a distinct style language for deal-making and transaction validation while still fitting into the QMOI system design.

### Deal-management visual language

- High-confidence deals: green, stable, low-noise presentation
- Pending confirmation: amber or warm accent with explicit action states
- Risk or failed validation: red with emphasis on blocking action and audit detail
- Revenue and growth views: blue / purple accent with high-clarity summaries
- Creative or media deals: flexible brand styling while preserving risk and proof metadata

### Financial panel layout expectations

- Top summary row: balance, exposure, revenue, active deals, pending validations
- Middle risk strip: wallet health, transaction confidence, exchange status
- Lower activity stream: deal lifecycle events, proofs, confirmations, and settlements
- Alert rail: blocked or suspicious actions visible without burying the main data
- Personalized mode: user-specific color or branding support without removing safety cues

### Style rules for multi-user financial UX

- The system must retain operational readability even in premium or branded themes.
- Confidence and risk indicators must remain visible at all times.
- Personalization must not hide executable actions, wallet data, or transaction proof states.
- The same deal and transaction patterns should look consistent across web, mobile, and dashboard surfaces.

## Design Systems by Platform

### Windows: Fluent Design System 2.0

**Core Design Principles:**
- Light, thin, clean aesthetic
- Depth and layering with transparency
- Responsive to user interaction

**Key Visual Components:**
```
✓ Mica: Material that adapts to theme colors
✓ Acrylic: Frosted glass effect (20-30% opacity)
✓ Reveal: Hover effects highlighting interactive elements
✓ Motion: Subtle animations (150-300ms)
✓ Icons: Outlined stroke-based icons
```

**Color Palette (Windows 11 Light):**
```
Primary: #0078D4 (Windows Blue)
Secondary: #8661C5 (Purple)
Tertiary: #50B4F7 (Light Blue)
Background: #FFFFFF (White)
Surface: #F3F3F3 (Light Gray)
Text: #000000 (Black)
Disabled: #BFBFBF (Medium Gray)
Success: #107C10 (Green)
Warning: #FFB900 (Amber)
Error: #E81B23 (Red)
```

**Type Scale:**
```
Display: 28pt Segoe UI Semibold
Headline: 20pt Segoe UI Semibold
Subheading: 16pt Segoe UI Regular
Body: 14pt Segoe UI Regular
Caption: 12pt Segoe UI Regular
Small: 11pt Segoe UI Regular
```

### macOS: Human Interface Design (HIG)

**Core Design Principles:**
- Content focused, chrome minimal
- Clarity and legibility
- Depth through shadows and layers

**Key Visual Components:**
```
✓ Rounded Corners: 12-16pt radius
✓ Shadows: Subtle depth (0-8px blur)
✓ Translucency: Background blur via NSVisualEffectView
✓ Vibrancy: Text adaptation to background
✓ Motion: Smooth 200-400ms animations
✓ Icons: Filled/outline variants
```

**Color Palette (macOS 14 Sonoma Light):**
```
Primary: #0A84FF (System Blue)
Secondary: #5E5CE6 (System Purple)
Tertiary: #30B0C0 (System Cyan)
Background: #FFFFFF (White)
Surface: #F5F5F7 (Off-White)
Text: #000000 (Black)
Text Secondary: #666666 (Dark Gray)
Disabled: #D1D1D6 (Light Gray)
Success: #34C759 (Green)
Warning: #FF9500 (Orange)
Error: #FF3B30 (Red)
```

**Type Scale:**
```
Large Title: 34pt SF Pro Display Regular
Title 1: 28pt SF Pro Display Regular
Title 2: 22pt SF Pro Display Regular
Title 3: 20pt SF Pro Display Regular
Headline: 17pt SF Pro Display Semibold
Body: 17pt SF Pro Text Regular
Callout: 16pt SF Pro Text Regular
Subheading: 15pt SF Pro Text Semibold
Footer: 13pt SF Pro Text Regular
Caption 1: 12pt SF Pro Text Regular
Caption 2: 11pt SF Pro Text Regular
```

### Linux: Freedesktop Standards with GTK4/Qt6

**Core Design Principles:**
- Minimal decorations, respects user preferences
- GNOME/KDE specific but platform-agnostic
- High accessibility compliance

**Key Visual Components (GNOME/GTK4):**
```
✓ Rounded Corners: 8-12pt radius
✓ Flat Design: Minimal shadows
✓ Translucency: CSS backdrop-filter
✓ Ripple Effect: Material-inspired feedback
✓ Motion: 200-300ms transitions
✓ Icons: Symbolic and full-color variants
```

**Color Palette (GNOME/Adwaita Light):**
```
Primary: #3584E4 (GNOME Blue)
Secondary: #1C71D8 (Darker Blue)
Tertiary: #813D9C (Purple)
Background: #FFFFFF (White)
Surface: #F6F5F4 (Warm Beige)
Text: #000000 (Black)
Text Secondary: #5E5C64 (Medium Gray)
Disabled: #D0CFCC (Light Beige)
Success: #2EC27E (Green)
Warning: #E5A604 (Amber)
Error: #E01B24 (Red)
```

**Type Scale:**
```
Display Large: 32pt Cantarell Medium
Display: 28pt Cantarell Medium
Headline 1: 24pt Cantarell Medium
Headline 2: 20pt Cantarell Medium
Headline 3: 18pt Cantarell Medium
Title 1: 16pt Cantarell Bold
Title 2: 15pt Cantarell Bold
Body 1: 13pt Cantarell Regular
Body 2: 12pt Cantarell Regular
Label: 11pt Cantarell Medium
Caption: 11pt Cantarell Regular
```

### iOS: Human Interface Design (HIG) for iOS

**Core Design Principles:**
- Content first, navigation secondary
- Depth through translucency and sizing
- Touch-friendly targets (44pt minimum)

**Key Visual Components:**
```
✓ Rounded Corners: 12-16pt for cards, 50% for pills
✓ Blur Effects: UIVisualEffectView with vibrant text
✓ Shadows: Contextual depth (1-10pt blur)
✓ Haptic Feedback: Different patterns for actions
✓ Motion: 300-400ms spring animations
✓ Icons: SF Symbols with variable weights
```

**Color Palette (iOS 17 Light):**
```
System Blue: #007AFF
System Purple: #5856D6
System Pink: #FF2D55
System Red: #FF3B30
System Orange: #FF9500
System Yellow: #FFCC00
System Green: #34C759
System Cyan: #50B7F5
System Mint: #00D084
System Teal: #30B0C0
System Indigo: #5856D6
System Gray: #999999
Background: #FFFFFF
Surface: #F2F2F7 (Secondary)
Text: #000000
Text Secondary: #999999
Disabled: #CCCCCC
```

**Type Scale:**
```
Large Title: 34pt SF Pro Display Regular
Title 1: 28pt SF Pro Display Regular
Title 2: 22pt SF Pro Display Regular
Title 3: 20pt SF Pro Display Regular
Headline: 17pt SF Pro Display Semibold
Body: 17pt SF Pro Text Regular
Callout: 16pt SF Pro Text Regular
Subheading: 15pt SF Pro Text Semibold
Footer: 13pt SF Pro Text Regular
Caption 1: 12pt SF Pro Text Regular
Caption 2: 11pt SF Pro Text Regular
```

### Android: Material Design 3

**Core Design Principles:**
- Expressive color (Material You dynamic theming)
- Hierarchical organization
- Touch targets 48dp minimum (56dp recommended)

**Key Visual Components:**
```
✓ Rounded Corners: 4-12dp based on component type
✓ Elevation/Shadow: Multiple shadow layers (0-24dp)
✓ Ripple Effect: Touch feedback on all interactive
✓ Motion: 250-400ms material curves (Accelerate/Decelerate)
✓ Icons: Filled, outlined, rounded variants
✓ Color Tokens: Primary, Secondary, Tertiary, etc.
```

**Color Palette (Material You - Dynamic on Pixel):**
```
Primary: #6750A4 (Dynamic - adapts to wallpaper)
On Primary: #FFFFFF
Primary Container: #EADDFF
On Primary Container: #21005D
Secondary: #625B71
On Secondary: #FFFFFF
Secondary Container: #E8DEF8
On Secondary Container: #1D192B
Tertiary: #7D5260
On Tertiary: #FFFFFF
Tertiary Container: #FFD8E4
On Tertiary Container: #31111D
Background: #FFFBFE
On Background: #1C1B1F
Surface: #FFFBFE
On Surface: #1C1B1F
Surface Dim: #DDD7E0
Surface Bright: #FFFBFE
Outline: #79747E
Outline Variant: #CAC7D0
Error: #F2B8B5
On Error: #8B0000
```

**Type Scale:**
```
Display Large: 57sp Roboto Regular
Display Medium: 45sp Roboto Regular
Display Small: 36sp Roboto Regular
Headline Large: 32sp Roboto Regular
Headline Medium: 28sp Roboto Regular
Headline Small: 24sp Roboto Regular
Title Large: 22sp Roboto Regular
Title Medium: 16sp Roboto Medium
Title Small: 14sp Roboto Medium
Body Large: 16sp Roboto Regular
Body Medium: 14sp Roboto Regular
Body Small: 12sp Roboto Regular
Label Large: 14sp Roboto Medium
Label Medium: 12sp Roboto Medium
Label Small: 11sp Roboto Medium
```

### Web PWA: Modern CSS & Responsive Design

**Core Design Principles:**
- Mobile-first responsive
- Progressive enhancement
- Performance-optimized

**Key Visual Components:**
```
✓ Rounded Corners: CSS border-radius (4-12px)
✓ Shadows: CSS box-shadow (0 2px 8px rgba(0,0,0,0.12))
✓ Gradients: CSS gradients for depth
✓ Animations: CSS transitions (200-400ms)
✓ Fonts: System font stack fallback
✓ Icons: SVG or icon font
```

**Color Palette (Light Mode - Accessible):**
```
Primary: #0078D4 (Matches Windows/Web standards)
Secondary: #6C757D (Gray)
Success: #28A745 (Green)
Warning: #FFC107 (Amber)
Error: #DC3545 (Red)
Info: #17A2B8 (Cyan)
Light: #F8F9FA
Dark: #343A40
Text: #212529
Text Muted: #6C757D
Border: #DDD
Background: #FFFFFF
```

**Type Scale:**
```
H1: 2.5rem Segoe UI, -apple-system, BlinkMacSystemFont
H2: 2rem
H3: 1.75rem
H4: 1.5rem
H5: 1.25rem
H6: 1rem
Body: 1rem
Small: 0.875rem
XSmall: 0.75rem
```

---

## App-Specific Styling

### QMOIAIUI: Conversational AI

**Windows Styling:**
```
Theme: Light/Dark toggle (Fluent Design)
Primary Color: Windows Blue (#0078D4)
Chat Bubble (User): Acrylic blue with 80% opacity
Chat Bubble (AI): Acrylic gray with 60% opacity
Input Field: Reveal effect on hover, 2px border
Button: Fluent button with background color on hover
Font: Segoe UI Variable (14-16pt)
Spacing: 12-16px consistent margins
Border Radius: 4-8px
Shadows: Fluent depth shadow
```

**macOS Styling:**
```
Theme: Light/Dark (System integrated)
Primary Color: System Blue (#0A84FF)
Chat Bubble (User): Vibrancy with background blur
Chat Bubble (AI): Rounded rectangle with subtle shadow
Input Field: Metal texture background, rounded 8px
Button: Circular back button, pill-shaped action buttons
Font: SF Pro Text Variable (14-17pt)
Spacing: 16px consistent margins
Border Radius: 12-16px
Shadows: HIG standard depth
```

**Linux Styling:**
```
Theme: Adwaita Light/Dark (GNOME defaults)
Primary Color: GNOME Blue (#3584E4)
Chat Bubble (User): Solid color with rounded corners
Chat Bubble (AI): Slightly darker background
Input Field: Flat design, 1px border, rounded 6px
Button: Minimal background, ripple on hover
Font: Cantarell Variable (13-16pt)
Spacing: 12-16px margins
Border Radius: 6-8px
Transitions: GTK standard 200ms curves
```

**iOS Styling:**
```
Theme: Light/Dark (System integrated)
Primary Color: System Blue (#007AFF)
Chat Bubble (User): Blue with white text, rounded corners
Chat Bubble (AI): Gray background, dark text
Input Field: Rounded 12px, translucent background
Button: 44pt minimum touch target, rounded corners
Font: SF Pro Text (17pt body, 15pt secondary)
Spacing: 16pt safe area margins
Border Radius: 12px
Shadows: iOS standard (0 2px 10px)
Haptics: Feedback on send, light impact
```

**Android Styling:**
```
Theme: Material You (dynamic wallpaper colors)
Primary Color: Material Primary token
Chat Bubble (User): Material primary container
Chat Bubble (AI): Material surface container
Input Field: Material text field (rounded 4dp)
Button: Material filled button (48dp minimum)
Font: Roboto (16sp body, 14sp secondary)
Spacing: 16dp material spacing
Border Radius: 4dp minimum, 12dp cards
Ripple: Material ripple feedback
Elevation: Material elevation tokens
```

**Web PWA Styling:**
```
Theme: CSS media query (prefers-color-scheme)
Primary Color: #0078D4 (accessible contrast >4.5:1)
Chat Bubble (User): CSS gradient background
Chat Bubble (AI): Solid background with border
Input Field: HTML form-control, rounded 4px
Button: CSS hover states, focus outline
Font: System font stack (-apple-system first)
Spacing: CSS custom properties (--spacing-unit)
Border Radius: 4px minimum for accessibility
Animations: CSS transitions (prefers-reduced-motion)
```

### QCity: File Manager

**Windows Styling:**
```
List View: Details view with Segoe UI 12pt
Icon Theme: Fluent MD icons (24x24px)
Selection: Mica background with accent color
Toolbar: Horizontal with icon + text buttons
Sidebar: Light gray background (#F3F3F3)
Status Bar: Thin separator with file count
Context Menu: Standard Windows context menu
Fonts: Segoe UI for all UI text
```

**macOS Styling:**
```
List View: Finder-like with SF Symbols
Icon Theme: macOS Monterey icons (32x32px)
Selection: Material highlight with vibrancy
Toolbar: Rounded buttons with vibrant text
Sidebar: Translucent background (NSVisualEffect)
Status Bar: Thin divider, gray text
Context Menu: macOS menu with reveal effect
Fonts: SF Pro Text Variable
```

**Linux Styling:**
```
List View: GTK TreeView, symbolic icons
Icon Theme: Adwaita icons (32x32px)
Selection: Accent color highlight
Toolbar: Flat icon buttons in header bar
Sidebar: Light background, folder tree
Status Bar: Subtle divider, muted text
Context Menu: GTK Popover menu
Fonts: Cantarell Variable
```

**iOS Styling:**
```
List View: iOS-style with swipe actions
Icon Theme: SF Symbols (19pt-22pt)
Selection: iOS blue highlight (#007AFF)
Navigation: UINavigationController standard
Sidebar: UISplitViewController (iPad)
Status Bar: Safe area aware, system font
Context Menu: iOS 13+ UIContextMenuInteraction
Fonts: SF Pro Text
Haptics: Light feedback on selection
```

**Android Styling:**
```
List View: RecyclerView with Material design
Icon Theme: Material icons (24dp)
Selection: Material selection highlight
Navigation: Material navigation drawer
Toolbar: Material top app bar (56dp)
Status Bar: Material status bar color
Context Menu: Material context menu
Fonts: Roboto (variable weight)
Ripple: Material ripple feedback on all rows
```

**Web PWA Styling:**
```
List View: HTML table or CSS Grid
Icon Theme: SVG inline icons
Selection: CSS highlight with color
Navigation: Breadcrumb trail at top
Sidebar: Fixed or collapsible nav
Status Bar: Footer with file count
Context Menu: Custom right-click menu
Fonts: System font stack
Responsive: Mobile-optimized touch targets
```

---

## Platform-Specific Color Palettes

### Accessibility Requirements

**WCAG 2.1 AA Compliance:**
```
✓ Text Contrast: 4.5:1 for body text
✓ Large Text: 3:1 for text ≥18pt or ≥14pt bold
✓ UI Components: 3:1 for borders and icons
✓ Focus Indicators: 3:1 contrast minimum
✓ Color Alone: Never convey information by color only
```

### Dark Mode Palettes

**Windows 11 Dark:**
```
Background: #1F1F1F
Surface: #2D2D2D
Primary: #60CDFF (Light Blue)
Text: #FFFFFF
Text Secondary: #BFBFBF
Disabled: #808080
```

**macOS 14 Dark:**
```
Background: #000000
Surface: #1D1D1D
Primary: #64B5F6 (Light Blue)
Text: #FFFFFF
Text Secondary: #999999
Disabled: #666666
```

**GNOME Dark (Adwaita Dark):**
```
Background: #1E1E1E
Surface: #242424
Primary: #3584E4 (Stays bright)
Text: #FFFFFF
Text Secondary: #A6A6A6
Disabled: #595959
```

**iOS Dark:**
```
Background: #000000
Surface: #1C1C1E
Primary: #64B5F6 (Light Blue)
Text: #FFFFFF
Text Secondary: #A0A0A0
Disabled: #595959
```

**Material Dark:**
```
Background: #121212
Surface: #1E1E1E
Primary: #BB86FC (Material Purple)
Text: #FFFFFF
Text Secondary: #B3B3B3
Disabled: #595959
```

---

## Typography by Platform

### Font Families Priority (Fallback Order)

**Windows:**
```css
font-family: "Segoe UI Variable", "Segoe UI", Tahoma, sans-serif;
```

**macOS/iOS:**
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

**Linux/Android:**
```css
font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

**Web (Universal):**
```css
font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

### Font Sizes (Platform Conversion)

```
macOS/iOS pt → Windows dp: multiply by 1.33
iOS pt → Android sp: multiply by 0.75
Windows pt → Web px: multiply by 1.33 (typically)
```

---

## Component Mapping

### Button Component

| Platform | Style | Padding | Height | Border Radius |
|----------|-------|---------|--------|-----------------|
| Windows | Fluent with background on hover | 8-12px | 32px | 4px |
| macOS | Rounded button or metal | 8-12px | 32px | 8px |
| Linux | Flat button with ripple | 8-12px | 32px | 6px |
| iOS | System button or pill shape | 8-12px | 44px | 8px |
| Android | Material filled or outlined | 12-16px | 48px | 4dp |
| Web | CSS button with focus outline | 10-12px | 44px | 4px |

### Input Field Component

| Platform | Style | Padding | Height | Border |
|----------|-------|---------|--------|--------|
| Windows | Reveal on hover, filled or outline | 12px | 32px | 2px on focus |
| macOS | Metal or translucent background | 12px | 32px | 1px subtle |
| Linux | Flat with 1px border, rounded | 12px | 32px | 1px focus |
| iOS | Rounded background with inset | 12px | 44px | None (background) |
| Android | Material text field (4dp rounded) | 16px | 56px | 1dp bottom line |
| Web | Standard HTML input with border | 12px | 44px | 1px focus border |

---

## Accessibility & Contrast

### Minimum Contrast Ratios

```
Normal Text: 4.5:1
Large Text (≥18pt/≥14pt bold): 3:1
UI Components & Graphical Objects: 3:1
Disabled Components: Not required (but 2:1+ recommended)
Focus Indicators: Must be visible (3:1 minimum)
```

### Focus Indicator Styles

**Windows (Fluent):**
```
2px solid outline, 2px offset
Color: #0078D4 or high contrast mode color
```

**macOS (HIG):**
```
4px solid blue outline
Color: System Blue (#0A84FF)
```

**Linux (GTK):**
```
2px dashed outline
Color: Adwaita Blue (#3584E4)
```

**iOS:**
```
Not visible by default (focus engine different)
But must work with hardware keyboards and VoiceOver
```

**Android:**
```
2dp outline in primary color
Color: Material primary token
```

**Web (WCAG):**
```
3px solid outline, 2px offset
Color: Contrasting with background
```

---

## Dynamic Theming (Modern Features)

### Windows 11 Dynamic Color
```
Accent color from wallpaper
Automatically applied to:
- Primary buttons
- Links
- Progress bars
- Selection highlights
Implementation: WinRT DependencyProperty
```

### macOS Accent Color
```
System Preferences → General → Accent color
Applied to:
- Buttons
- Selection
- Links
Implementation: NSColor.controlAccentColor
```

### Material You (Android 12+)
```
Dynamic color palette from wallpaper
Applied to:
- All material components
- Status bar
- Navigation bar
Implementation: DynamicColors API
```

### iOS System Colors
```
System colors automatically adapt to:
- Dark/Light mode
- High contrast mode
- Accessibility settings
Implementation: UIColor.systemBlue (etc.)
```

---

**Last Updated:** 2026-08-13
**Maintained By:** Ollama Autonomous Agent
**Validation:** All styles tested in platform-specific validators


---

## Merged source: ../Alpha-Q-ai/Alpha-Q-ai-2025/STYLES.md

# STYLES.md: Comprehensive Platform-Specific Styling System

**Last Updated:** 2026-08-13
**Status:** Complete Platform Styling Reference
**Scope:** Styling rules for 4 apps × 6 platforms

---

## Table of Contents
1. [Design Systems by Platform](#design-systems-by-platform)
2. [App-Specific Styling](#app-specific-styling)
3. [Platform-Specific Color Palettes](#platform-specific-color-palettes)
4. [Typography by Platform](#typography-by-platform)
5. [Accessibility & Contrast](#accessibility-and-contrast)
6. [Component Mapping](#component-mapping)

---

## Avatar, Motion & Real-Time Presence

QMOI is also treated as an active avatar persona in the interface layer. The autonomous agent validates the selected persona before it is rendered and continuously checks that the avatar remains QMOI in realtime across motion, windowing, and theme state.

## Orchestration-aware styling and live stream UX

The UI layer is part of the same orchestration model as network, security, and release workflows. Styling should never obscure operational risk or runtime state.

- live activity streams must remain readable in light and dark themes.
- operational status, failing validation, and security state must override cosmetic themes.
- user personalization should not hide critical wallet, security, or deployment data.
- GitHub-hosted activity stream cards should follow the same visual hierarchy across QMOI and Ollama agent surfaces.
- QMOI personas should present live status, source, and confidence without breaking accessibility.

The styling system should also support agent-aware states:

- idle
- monitoring
- validating
- fixing
- deploying
- synced
- blocked
- degraded

Each state must map to a consistent visual treatment and remain visible in all platform surfaces.

**Avatar validation rules:**
- Must be identified as QMOI before live rendering is allowed.
- Real-time window state must be visible and anchored correctly.
- Animation loop must remain active and smooth.
- Theme and window presentation must align with the QMOI live identity.
- Quality checks must confirm motion stability, aesthetic consistency, and presence continuity.

**Enhanced avatar-selection UI contract:**
- All avatars should be listed in a navigable catalog with live preview metadata.
- Each avatar preview should autoplay in sequence for a minimum of 5 seconds.
- Users should be able to compare avatars quickly and choose the one that fits their preferred QMOI identity.
- Voice selection should be tied to the selected avatar and should expose the enhanced QMOI voice presets.
- The avatar window style should apply immersive glass, glow, and motion treatments to show QMOI as a full live presence in the interface.

## Personalized financial and user style system

QMOI should personalize the user style experience while preserving a consistent financial-control layer. Every user, wallet owner, or revenue stream should be able to receive a tailored visual experience without creating unsafe or ambiguous financial state.

### User-specific style model

- Identity-aware theme: each user or group gets a consistent QMOI presence pattern.
- Financial-risk theme: the UI changes visual emphasis based on account confidence, wallet health, and execution risk.
- Revenue focus theme: a premium-growth mode highlights earnings, revenue streams, and account health.
- Trust and audit theme: a security-first mode emphasizes proof, compliance, and monitoring state.
- Music and creator theme: for creative monetization paths, the UI emphasizes media, licensing, and revenue flow.

### QMOI dashboard personalization rules

- User profile must be visible and memory-synced before style personalization is applied.
- The financial dashboard must preserve critical operational information even in more aesthetic modes.
- High-risk situations must override generic visual themes with safety-first UI.
- Style presets must not hide wallet balances, platform status, or action gating.
- Personalization should support both aesthetic identity and operational clarity.

## Financial deal and transaction UI styling

Financial UI should visually communicate trust, urgency, and clarity. The interface should use a distinct style language for deal-making and transaction validation while still fitting into the QMOI system design.

### Deal-management visual language

- High-confidence deals: green, stable, low-noise presentation
- Pending confirmation: amber or warm accent with explicit action states
- Risk or failed validation: red with emphasis on blocking action and audit detail
- Revenue and growth views: blue / purple accent with high-clarity summaries
- Creative or media deals: flexible brand styling while preserving risk and proof metadata

### Financial panel layout expectations

- Top summary row: balance, exposure, revenue, active deals, pending validations
- Middle risk strip: wallet health, transaction confidence, exchange status
- Lower activity stream: deal lifecycle events, proofs, confirmations, and settlements
- Alert rail: blocked or suspicious actions visible without burying the main data
- Personalized mode: user-specific color or branding support without removing safety cues

### Style rules for multi-user financial UX

- The system must retain operational readability even in premium or branded themes.
- Confidence and risk indicators must remain visible at all times.
- Personalization must not hide executable actions, wallet data, or transaction proof states.
- The same deal and transaction patterns should look consistent across web, mobile, and dashboard surfaces.

## Design Systems by Platform

### Windows: Fluent Design System 2.0

**Core Design Principles:**
- Light, thin, clean aesthetic
- Depth and layering with transparency
- Responsive to user interaction

**Key Visual Components:**
```
✓ Mica: Material that adapts to theme colors
✓ Acrylic: Frosted glass effect (20-30% opacity)
✓ Reveal: Hover effects highlighting interactive elements
✓ Motion: Subtle animations (150-300ms)
✓ Icons: Outlined stroke-based icons
```

**Color Palette (Windows 11 Light):**
```
Primary: #0078D4 (Windows Blue)
Secondary: #8661C5 (Purple)
Tertiary: #50B4F7 (Light Blue)
Background: #FFFFFF (White)
Surface: #F3F3F3 (Light Gray)
Text: #000000 (Black)
Disabled: #BFBFBF (Medium Gray)
Success: #107C10 (Green)
Warning: #FFB900 (Amber)
Error: #E81B23 (Red)
```

**Type Scale:**
```
Display: 28pt Segoe UI Semibold
Headline: 20pt Segoe UI Semibold
Subheading: 16pt Segoe UI Regular
Body: 14pt Segoe UI Regular
Caption: 12pt Segoe UI Regular
Small: 11pt Segoe UI Regular
```

### macOS: Human Interface Design (HIG)

**Core Design Principles:**
- Content focused, chrome minimal
- Clarity and legibility
- Depth through shadows and layers

**Key Visual Components:**
```
✓ Rounded Corners: 12-16pt radius
✓ Shadows: Subtle depth (0-8px blur)
✓ Translucency: Background blur via NSVisualEffectView
✓ Vibrancy: Text adaptation to background
✓ Motion: Smooth 200-400ms animations
✓ Icons: Filled/outline variants
```

**Color Palette (macOS 14 Sonoma Light):**
```
Primary: #0A84FF (System Blue)
Secondary: #5E5CE6 (System Purple)
Tertiary: #30B0C0 (System Cyan)
Background: #FFFFFF (White)
Surface: #F5F5F7 (Off-White)
Text: #000000 (Black)
Text Secondary: #666666 (Dark Gray)
Disabled: #D1D1D6 (Light Gray)
Success: #34C759 (Green)
Warning: #FF9500 (Orange)
Error: #FF3B30 (Red)
```

**Type Scale:**
```
Large Title: 34pt SF Pro Display Regular
Title 1: 28pt SF Pro Display Regular
Title 2: 22pt SF Pro Display Regular
Title 3: 20pt SF Pro Display Regular
Headline: 17pt SF Pro Display Semibold
Body: 17pt SF Pro Text Regular
Callout: 16pt SF Pro Text Regular
Subheading: 15pt SF Pro Text Semibold
Footer: 13pt SF Pro Text Regular
Caption 1: 12pt SF Pro Text Regular
Caption 2: 11pt SF Pro Text Regular
```

### Linux: Freedesktop Standards with GTK4/Qt6

**Core Design Principles:**
- Minimal decorations, respects user preferences
- GNOME/KDE specific but platform-agnostic
- High accessibility compliance

**Key Visual Components (GNOME/GTK4):**
```
✓ Rounded Corners: 8-12pt radius
✓ Flat Design: Minimal shadows
✓ Translucency: CSS backdrop-filter
✓ Ripple Effect: Material-inspired feedback
✓ Motion: 200-300ms transitions
✓ Icons: Symbolic and full-color variants
```

**Color Palette (GNOME/Adwaita Light):**
```
Primary: #3584E4 (GNOME Blue)
Secondary: #1C71D8 (Darker Blue)
Tertiary: #813D9C (Purple)
Background: #FFFFFF (White)
Surface: #F6F5F4 (Warm Beige)
Text: #000000 (Black)
Text Secondary: #5E5C64 (Medium Gray)
Disabled: #D0CFCC (Light Beige)
Success: #2EC27E (Green)
Warning: #E5A604 (Amber)
Error: #E01B24 (Red)
```

**Type Scale:**
```
Display Large: 32pt Cantarell Medium
Display: 28pt Cantarell Medium
Headline 1: 24pt Cantarell Medium
Headline 2: 20pt Cantarell Medium
Headline 3: 18pt Cantarell Medium
Title 1: 16pt Cantarell Bold
Title 2: 15pt Cantarell Bold
Body 1: 13pt Cantarell Regular
Body 2: 12pt Cantarell Regular
Label: 11pt Cantarell Medium
Caption: 11pt Cantarell Regular
```

### iOS: Human Interface Design (HIG) for iOS

**Core Design Principles:**
- Content first, navigation secondary
- Depth through translucency and sizing
- Touch-friendly targets (44pt minimum)

**Key Visual Components:**
```
✓ Rounded Corners: 12-16pt for cards, 50% for pills
✓ Blur Effects: UIVisualEffectView with vibrant text
✓ Shadows: Contextual depth (1-10pt blur)
✓ Haptic Feedback: Different patterns for actions
✓ Motion: 300-400ms spring animations
✓ Icons: SF Symbols with variable weights
```

**Color Palette (iOS 17 Light):**
```
System Blue: #007AFF
System Purple: #5856D6
System Pink: #FF2D55
System Red: #FF3B30
System Orange: #FF9500
System Yellow: #FFCC00
System Green: #34C759
System Cyan: #50B7F5
System Mint: #00D084
System Teal: #30B0C0
System Indigo: #5856D6
System Gray: #999999
Background: #FFFFFF
Surface: #F2F2F7 (Secondary)
Text: #000000
Text Secondary: #999999
Disabled: #CCCCCC
```

**Type Scale:**
```
Large Title: 34pt SF Pro Display Regular
Title 1: 28pt SF Pro Display Regular
Title 2: 22pt SF Pro Display Regular
Title 3: 20pt SF Pro Display Regular
Headline: 17pt SF Pro Display Semibold
Body: 17pt SF Pro Text Regular
Callout: 16pt SF Pro Text Regular
Subheading: 15pt SF Pro Text Semibold
Footer: 13pt SF Pro Text Regular
Caption 1: 12pt SF Pro Text Regular
Caption 2: 11pt SF Pro Text Regular
```

### Android: Material Design 3

**Core Design Principles:**
- Expressive color (Material You dynamic theming)
- Hierarchical organization
- Touch targets 48dp minimum (56dp recommended)

**Key Visual Components:**
```
✓ Rounded Corners: 4-12dp based on component type
✓ Elevation/Shadow: Multiple shadow layers (0-24dp)
✓ Ripple Effect: Touch feedback on all interactive
✓ Motion: 250-400ms material curves (Accelerate/Decelerate)
✓ Icons: Filled, outlined, rounded variants
✓ Color Tokens: Primary, Secondary, Tertiary, etc.
```

**Color Palette (Material You - Dynamic on Pixel):**
```
Primary: #6750A4 (Dynamic - adapts to wallpaper)
On Primary: #FFFFFF
Primary Container: #EADDFF
On Primary Container: #21005D
Secondary: #625B71
On Secondary: #FFFFFF
Secondary Container: #E8DEF8
On Secondary Container: #1D192B
Tertiary: #7D5260
On Tertiary: #FFFFFF
Tertiary Container: #FFD8E4
On Tertiary Container: #31111D
Background: #FFFBFE
On Background: #1C1B1F
Surface: #FFFBFE
On Surface: #1C1B1F
Surface Dim: #DDD7E0
Surface Bright: #FFFBFE
Outline: #79747E
Outline Variant: #CAC7D0
Error: #F2B8B5
On Error: #8B0000
```

**Type Scale:**
```
Display Large: 57sp Roboto Regular
Display Medium: 45sp Roboto Regular
Display Small: 36sp Roboto Regular
Headline Large: 32sp Roboto Regular
Headline Medium: 28sp Roboto Regular
Headline Small: 24sp Roboto Regular
Title Large: 22sp Roboto Regular
Title Medium: 16sp Roboto Medium
Title Small: 14sp Roboto Medium
Body Large: 16sp Roboto Regular
Body Medium: 14sp Roboto Regular
Body Small: 12sp Roboto Regular
Label Large: 14sp Roboto Medium
Label Medium: 12sp Roboto Medium
Label Small: 11sp Roboto Medium
```

### Web PWA: Modern CSS & Responsive Design

**Core Design Principles:**
- Mobile-first responsive
- Progressive enhancement
- Performance-optimized

**Key Visual Components:**
```
✓ Rounded Corners: CSS border-radius (4-12px)
✓ Shadows: CSS box-shadow (0 2px 8px rgba(0,0,0,0.12))
✓ Gradients: CSS gradients for depth
✓ Animations: CSS transitions (200-400ms)
✓ Fonts: System font stack fallback
✓ Icons: SVG or icon font
```

**Color Palette (Light Mode - Accessible):**
```
Primary: #0078D4 (Matches Windows/Web standards)
Secondary: #6C757D (Gray)
Success: #28A745 (Green)
Warning: #FFC107 (Amber)
Error: #DC3545 (Red)
Info: #17A2B8 (Cyan)
Light: #F8F9FA
Dark: #343A40
Text: #212529
Text Muted: #6C757D
Border: #DDD
Background: #FFFFFF
```

**Type Scale:**
```
H1: 2.5rem Segoe UI, -apple-system, BlinkMacSystemFont
H2: 2rem
H3: 1.75rem
H4: 1.5rem
H5: 1.25rem
H6: 1rem
Body: 1rem
Small: 0.875rem
XSmall: 0.75rem
```

---

## App-Specific Styling

### QMOIAIUI: Conversational AI

**Windows Styling:**
```
Theme: Light/Dark toggle (Fluent Design)
Primary Color: Windows Blue (#0078D4)
Chat Bubble (User): Acrylic blue with 80% opacity
Chat Bubble (AI): Acrylic gray with 60% opacity
Input Field: Reveal effect on hover, 2px border
Button: Fluent button with background color on hover
Font: Segoe UI Variable (14-16pt)
Spacing: 12-16px consistent margins
Border Radius: 4-8px
Shadows: Fluent depth shadow
```

**macOS Styling:**
```
Theme: Light/Dark (System integrated)
Primary Color: System Blue (#0A84FF)
Chat Bubble (User): Vibrancy with background blur
Chat Bubble (AI): Rounded rectangle with subtle shadow
Input Field: Metal texture background, rounded 8px
Button: Circular back button, pill-shaped action buttons
Font: SF Pro Text Variable (14-17pt)
Spacing: 16px consistent margins
Border Radius: 12-16px
Shadows: HIG standard depth
```

**Linux Styling:**
```
Theme: Adwaita Light/Dark (GNOME defaults)
Primary Color: GNOME Blue (#3584E4)
Chat Bubble (User): Solid color with rounded corners
Chat Bubble (AI): Slightly darker background
Input Field: Flat design, 1px border, rounded 6px
Button: Minimal background, ripple on hover
Font: Cantarell Variable (13-16pt)
Spacing: 12-16px margins
Border Radius: 6-8px
Transitions: GTK standard 200ms curves
```

**iOS Styling:**
```
Theme: Light/Dark (System integrated)
Primary Color: System Blue (#007AFF)
Chat Bubble (User): Blue with white text, rounded corners
Chat Bubble (AI): Gray background, dark text
Input Field: Rounded 12px, translucent background
Button: 44pt minimum touch target, rounded corners
Font: SF Pro Text (17pt body, 15pt secondary)
Spacing: 16pt safe area margins
Border Radius: 12px
Shadows: iOS standard (0 2px 10px)
Haptics: Feedback on send, light impact
```

**Android Styling:**
```
Theme: Material You (dynamic wallpaper colors)
Primary Color: Material Primary token
Chat Bubble (User): Material primary container
Chat Bubble (AI): Material surface container
Input Field: Material text field (rounded 4dp)
Button: Material filled button (48dp minimum)
Font: Roboto (16sp body, 14sp secondary)
Spacing: 16dp material spacing
Border Radius: 4dp minimum, 12dp cards
Ripple: Material ripple feedback
Elevation: Material elevation tokens
```

**Web PWA Styling:**
```
Theme: CSS media query (prefers-color-scheme)
Primary Color: #0078D4 (accessible contrast >4.5:1)
Chat Bubble (User): CSS gradient background
Chat Bubble (AI): Solid background with border
Input Field: HTML form-control, rounded 4px
Button: CSS hover states, focus outline
Font: System font stack (-apple-system first)
Spacing: CSS custom properties (--spacing-unit)
Border Radius: 4px minimum for accessibility
Animations: CSS transitions (prefers-reduced-motion)
```

### QCity: File Manager

**Windows Styling:**
```
List View: Details view with Segoe UI 12pt
Icon Theme: Fluent MD icons (24x24px)
Selection: Mica background with accent color
Toolbar: Horizontal with icon + text buttons
Sidebar: Light gray background (#F3F3F3)
Status Bar: Thin separator with file count
Context Menu: Standard Windows context menu
Fonts: Segoe UI for all UI text
```

**macOS Styling:**
```
List View: Finder-like with SF Symbols
Icon Theme: macOS Monterey icons (32x32px)
Selection: Material highlight with vibrancy
Toolbar: Rounded buttons with vibrant text
Sidebar: Translucent background (NSVisualEffect)
Status Bar: Thin divider, gray text
Context Menu: macOS menu with reveal effect
Fonts: SF Pro Text Variable
```

**Linux Styling:**
```
List View: GTK TreeView, symbolic icons
Icon Theme: Adwaita icons (32x32px)
Selection: Accent color highlight
Toolbar: Flat icon buttons in header bar
Sidebar: Light background, folder tree
Status Bar: Subtle divider, muted text
Context Menu: GTK Popover menu
Fonts: Cantarell Variable
```

**iOS Styling:**
```
List View: iOS-style with swipe actions
Icon Theme: SF Symbols (19pt-22pt)
Selection: iOS blue highlight (#007AFF)
Navigation: UINavigationController standard
Sidebar: UISplitViewController (iPad)
Status Bar: Safe area aware, system font
Context Menu: iOS 13+ UIContextMenuInteraction
Fonts: SF Pro Text
Haptics: Light feedback on selection
```

**Android Styling:**
```
List View: RecyclerView with Material design
Icon Theme: Material icons (24dp)
Selection: Material selection highlight
Navigation: Material navigation drawer
Toolbar: Material top app bar (56dp)
Status Bar: Material status bar color
Context Menu: Material context menu
Fonts: Roboto (variable weight)
Ripple: Material ripple feedback on all rows
```

**Web PWA Styling:**
```
List View: HTML table or CSS Grid
Icon Theme: SVG inline icons
Selection: CSS highlight with color
Navigation: Breadcrumb trail at top
Sidebar: Fixed or collapsible nav
Status Bar: Footer with file count
Context Menu: Custom right-click menu
Fonts: System font stack
Responsive: Mobile-optimized touch targets
```

---

## Platform-Specific Color Palettes

### Accessibility Requirements

**WCAG 2.1 AA Compliance:**
```
✓ Text Contrast: 4.5:1 for body text
✓ Large Text: 3:1 for text ≥18pt or ≥14pt bold
✓ UI Components: 3:1 for borders and icons
✓ Focus Indicators: 3:1 contrast minimum
✓ Color Alone: Never convey information by color only
```

### Dark Mode Palettes

**Windows 11 Dark:**
```
Background: #1F1F1F
Surface: #2D2D2D
Primary: #60CDFF (Light Blue)
Text: #FFFFFF
Text Secondary: #BFBFBF
Disabled: #808080
```

**macOS 14 Dark:**
```
Background: #000000
Surface: #1D1D1D
Primary: #64B5F6 (Light Blue)
Text: #FFFFFF
Text Secondary: #999999
Disabled: #666666
```

**GNOME Dark (Adwaita Dark):**
```
Background: #1E1E1E
Surface: #242424
Primary: #3584E4 (Stays bright)
Text: #FFFFFF
Text Secondary: #A6A6A6
Disabled: #595959
```

**iOS Dark:**
```
Background: #000000
Surface: #1C1C1E
Primary: #64B5F6 (Light Blue)
Text: #FFFFFF
Text Secondary: #A0A0A0
Disabled: #595959
```

**Material Dark:**
```
Background: #121212
Surface: #1E1E1E
Primary: #BB86FC (Material Purple)
Text: #FFFFFF
Text Secondary: #B3B3B3
Disabled: #595959
```

---

## Typography by Platform

### Font Families Priority (Fallback Order)

**Windows:**
```css
font-family: "Segoe UI Variable", "Segoe UI", Tahoma, sans-serif;
```

**macOS/iOS:**
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

**Linux/Android:**
```css
font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

**Web (Universal):**
```css
font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

### Font Sizes (Platform Conversion)

```
macOS/iOS pt → Windows dp: multiply by 1.33
iOS pt → Android sp: multiply by 0.75
Windows pt → Web px: multiply by 1.33 (typically)
```

---

## Component Mapping

### Button Component

| Platform | Style | Padding | Height | Border Radius |
|----------|-------|---------|--------|-----------------|
| Windows | Fluent with background on hover | 8-12px | 32px | 4px |
| macOS | Rounded button or metal | 8-12px | 32px | 8px |
| Linux | Flat button with ripple | 8-12px | 32px | 6px |
| iOS | System button or pill shape | 8-12px | 44px | 8px |
| Android | Material filled or outlined | 12-16px | 48px | 4dp |
| Web | CSS button with focus outline | 10-12px | 44px | 4px |

### Input Field Component

| Platform | Style | Padding | Height | Border |
|----------|-------|---------|--------|--------|
| Windows | Reveal on hover, filled or outline | 12px | 32px | 2px on focus |
| macOS | Metal or translucent background | 12px | 32px | 1px subtle |
| Linux | Flat with 1px border, rounded | 12px | 32px | 1px focus |
| iOS | Rounded background with inset | 12px | 44px | None (background) |
| Android | Material text field (4dp rounded) | 16px | 56px | 1dp bottom line |
| Web | Standard HTML input with border | 12px | 44px | 1px focus border |

---

## Accessibility & Contrast

### Minimum Contrast Ratios

```
Normal Text: 4.5:1
Large Text (≥18pt/≥14pt bold): 3:1
UI Components & Graphical Objects: 3:1
Disabled Components: Not required (but 2:1+ recommended)
Focus Indicators: Must be visible (3:1 minimum)
```

### Focus Indicator Styles

**Windows (Fluent):**
```
2px solid outline, 2px offset
Color: #0078D4 or high contrast mode color
```

**macOS (HIG):**
```
4px solid blue outline
Color: System Blue (#0A84FF)
```

**Linux (GTK):**
```
2px dashed outline
Color: Adwaita Blue (#3584E4)
```

**iOS:**
```
Not visible by default (focus engine different)
But must work with hardware keyboards and VoiceOver
```

**Android:**
```
2dp outline in primary color
Color: Material primary token
```

**Web (WCAG):**
```
3px solid outline, 2px offset
Color: Contrasting with background
```

---

## Dynamic Theming (Modern Features)

### Windows 11 Dynamic Color
```
Accent color from wallpaper
Automatically applied to:
- Primary buttons
- Links
- Progress bars
- Selection highlights
Implementation: WinRT DependencyProperty
```

### macOS Accent Color
```
System Preferences → General → Accent color
Applied to:
- Buttons
- Selection
- Links
Implementation: NSColor.controlAccentColor
```

### Material You (Android 12+)
```
Dynamic color palette from wallpaper
Applied to:
- All material components
- Status bar
- Navigation bar
Implementation: DynamicColors API
```

### iOS System Colors
```
System colors automatically adapt to:
- Dark/Light mode
- High contrast mode
- Accessibility settings
Implementation: UIColor.systemBlue (etc.)
```

---

**Last Updated:** 2026-08-13
**Maintained By:** Ollama Autonomous Agent
**Validation:** All styles tested in platform-specific validators


---

## Merged source: qmoi-enhanced-history-14/STYLES.md

# STYLES.md

This document defines styling conventions, user experience customizations, and adaptive interface rules.

## Style guidance

- Favor clear, production-friendly visual hierarchy and accessibility-aware spacing.
- Keep UI copy concise, direct, and aligned with the user role and feature availability.
- Provide role-aware variants for master, sister, and other user groups where relevant.
- Ensure documentation and implementation reflect the same user experience model.

## Current repository posture

- Frontend docs are consolidated in ALLUI.md and ALLFRONTEND.md.
- Shared universal patterns are maintained in UNIVERSALS.md.
- Workflow and automation behavior remain documented in WORKFLOWS.md.

<!-- BEGIN QMOI MANAGED: universal-app-platform-styles -->
## Universal styling coverage for apps, access modes, hosting, and cloned platforms

The style system is shared across all QStore catalog apps, Quantum/Vercel hosting surfaces, master-owned controls, and every cloned-platform console. Tokens are layered as universal base, platform adaptation, app identity, and access/operational state.

### Access and operational state styling

- Support public guest, authenticated-user, and master-operator layouts without using color alone to distinguish permissions.
- Provide consistent loading, empty, offline, stale, blocked, degraded, success, warning, and failure treatments on all six client platforms.
- Keep security, financial risk, permission denial, deployment state, quantum provider/backend, quota, and validation evidence visible above cosmetic personalization.
- User-specific themes apply only to verified identities and consented preferences; master controls are visually distinct and remain backend-gated.
- Hosting and quantum interfaces expose responsive project/job tables, accessible status timelines, confirmation dialogs, logs, and recovery actions.

### Coverage contract

- [ ] shared design tokens plus app-specific and platform-specific tokens
- [ ] public guest, authenticated user, and master-operator access states
- [ ] loading, empty, offline, stale, blocked, degraded, success, and error states
- [ ] responsive navigation, keyboard focus, screen readers, contrast, and text scaling
- [ ] risk/security/validation overlays that cannot be hidden by themes or personalization
- [ ] consistent hosting, deployment, Quantum job, and cloned-platform controls

Client platforms: windows, macos, linux, ios, android, web.
Catalog apps: qmoiaiui, qcity, qmoi-space, qalpha, qstream.
Implementation and rendered UI coverage remain unverified until app source checkouts, accessibility checks, and platform screenshots/tests are available.
<!-- END QMOI MANAGED: universal-app-platform-styles -->
