QMOI UNIVERSAL MULTI-PLATFORM / ALL-DEVICE ARCHITECTURE

Remote build + real artifacts + device installation + hands-free operation + universal memory + future-platform extensibility

Repositories

- "thealphakenya/Alpha-Q-ai"
- "thealphakenya/qmoi-enhanced"

Primary objectives

QMOI shall be designed around one universal source architecture that can produce platform-specific applications through platform adapters and remote builders.

The target architecture is:

QMOI SOURCE
        ↓
UNIVERSAL CORE
        ↓
PLATFORM ADAPTERS
        ↓
TARGET DISCOVERY
        ↓
TARGET MATRIX
        ├── Android
        ├── Android TV
        ├── Wear OS
        ├── iOS
        ├── iPadOS
        ├── tvOS
        ├── watchOS
        ├── visionOS
        ├── Windows
        ├── macOS
        ├── Linux
        ├── Web
        ├── PWA
        ├── ChromeOS
        ├── embedded systems
        ├── automotive systems
        ├── future platforms
        └── newly discovered targets
        ↓
REMOTE BUILD ORCHESTRATOR
        ↓
TARGET-SPECIFIC BUILD WORKER
        ↓
REAL ARTIFACT
        ↓
SIGNING / PACKAGING
        ↓
ARTIFACT INTEGRITY VALIDATION
        ↓
INSTALLATION / DEPLOYMENT TEST
        ↓
RUNTIME TEST
        ↓
ACCESSIBILITY TEST
        ↓
HANDS-FREE TEST
        ↓
DEVICE CAPABILITY TEST
        ↓
MEMORY / IDENTITY SYNCHRONIZATION TEST
        ↓
EVIDENCE
        ↓
RELEASE / DEPLOYMENT

---

1. Core principle

QMOI must distinguish:

SOURCE SUPPORT

from:

BUILD SUPPORT

from:

ARTIFACT SUPPORT

from:

INSTALLATION SUPPORT

from:

RUNTIME SUPPORT

from:

PHYSICAL DEVICE VERIFICATION

A platform must never be marked completely supported merely because documentation or source files mention that platform.

The existing Alpha-Q-ai production master plan already explicitly states that documentation is not proof of implementation and that success must not be reported merely because Ollama or a workflow ran successfully.

That rule should become fundamental to QBUILD.

---

2. One source tree

QMOI should maintain one universal logical application source.

Conceptually:

qmoI/
│
├── core/
│   ├── intelligence/
│   ├── memory/
│   ├── identity/
│   ├── orchestration/
│   ├── networking/
│   ├── security/
│   ├── accessibility/
│   ├── voice/
│   ├── vision/
│   ├── automation/
│   ├── synchronization/
│   └── capabilities/
│
├── apps/
│   ├── qmoiaiui/
│   ├── qcity/
│   ├── qmoi-space/
│   └── qalpha/
│
├── platform/
│   ├── android/
│   ├── android-tv/
│   ├── wear-os/
│   ├── ios/
│   ├── ipados/
│   ├── tvos/
│   ├── watchos/
│   ├── visionos/
│   ├── windows/
│   ├── macos/
│   ├── linux/
│   ├── web/
│   ├── pwa/
│   ├── chromeos/
│   ├── automotive/
│   ├── embedded/
│   └── future/
│
├── device/
│   ├── discovery/
│   ├── capabilities/
│   ├── profiles/
│   ├── permissions/
│   ├── sensors/
│   ├── accessibility/
│   └── handsfree/
│
├── build/
│   ├── manifests/
│   ├── adapters/
│   ├── workers/
│   ├── signing/
│   ├── artifacts/
│   └── verification/
│
└── tests/
    ├── universal/
    ├── platform/
    ├── device/
    ├── accessibility/
    ├── handsfree/
    ├── memory/
    ├── installation/
    └── runtime/

The physical repositories can retain their current structures where necessary; this is the logical architecture QMOI should converge toward rather than requiring an unsafe wholesale rewrite.

---

3. Target matrix

The target matrix should be expanded from the existing six-platform model.

The repositories currently define:

Windows
macOS
Linux
iOS
Android
Web/PWA

and four applications:

QMOIAIUI
QCity
QMOI Space
QALPHA

The existing feature matrix contains platform-specific integrations and says the autonomous agent validates each app/platform combination.

The expanded matrix should be:

DESKTOP

Windows
Windows x64
Windows ARM64

macOS
macOS Intel
macOS Apple Silicon
macOS Universal

Linux
x86_64
ARM64
major desktop environments

MOBILE

Android
Android ARM64
Android ARM32 where required
Android x86_64

iOS
iPadOS

TV

Android TV
Google TV-compatible Android targets
tvOS

WEARABLE

Wear OS
watchOS

IMMERSIVE

visionOS
other XR/AR/VR targets through adapters

WEB

Web
PWA
desktop browsers
mobile browsers
embedded webviews

OTHER

ChromeOS
automotive platforms
embedded Linux
IoT-capable environments
kiosk systems
industrial terminals
future platforms

---

4. Android

The Android adapter must cover more than simply producing an APK.

Existing repository requirements already include:

- ContentProvider
- DocumentsProvider
- MediaStore
- notification channels
- Material You
- launcher shortcuts
- widgets
- share intents
- App Links
- billing
- TalkBack
- scoped storage
- adaptive icons.

The new Android build matrix should additionally manage:

APK
AAB
arm64-v8a
armeabi-v7a
x86_64
debug
release
internal
beta
production

Automated tests:

compile
package
sign
install
launch
login
permissions
storage
notifications
widgets
deep links
share intents
background work
network loss
offline operation
memory recovery
voice input
voice output
TalkBack
orientation
foldables
multi-window
battery behavior
update
rollback

---

5. Android TV

Add a dedicated Android TV adapter.

It should detect and implement:

TV launcher
remote-control navigation
D-pad
voice remote
large-screen UI
10-foot UI
focus management
media playback
TV content recommendations
background playback
HD/4K rendering
remote accessibility

Artifacts:

Android TV APK
Android TV AAB where applicable

Verification:

install
launch
D-pad navigation
remote control
voice command
media playback
resume
network recovery
accessibility
uninstall
update

---

6. Wear OS

QMOI should provide a dedicated wearable adapter.

Features:

small display layouts
tiles
complications
notifications
voice interaction
haptic feedback
health/sensor integration where permitted
battery-aware operation
offline operation
phone companion communication

Artifacts:

Wear OS package

The system must not assume that a normal Android phone APK is equivalent to a Wear OS application.

---

7. iOS

Existing QMOI documentation already includes:

- FileProvider
- Document Picker
- Handoff
- Siri Shortcuts
- iCloud/CloudKit
- App Clips
- widgets
- share extensions
- Universal Links
- in-app purchases
- VoiceOver
- Dynamic Type
- haptic feedback.

The remote Apple builder should therefore perform:

source checkout
↓
dependency resolution
↓
Xcode build
↓
archive
↓
sign
↓
export
↓
IPA
↓
install/test
↓
runtime validation
↓
evidence

The user's local phone/PC does not need Xcode.

The remote Apple environment does.

---

8. iPadOS

Treat iPadOS separately from iOS because the device interaction model differs.

Test:

split screen
multi-window
Stage Manager where supported
keyboard
trackpad
Apple Pencil where applicable
drag/drop
Files
widgets
orientation
external display
Handoff
Universal Links
voice interaction
accessibility

---

9. tvOS

Create a separate tvOS target.

Test:

Siri Remote
focus engine
10-foot UI
media playback
AirPlay
remote navigation
voice control
accessibility
large-screen rendering
network recovery

Artifact:

tvOS archive/package suitable for the intended Apple distribution/testing path

---

10. watchOS

Create a dedicated watchOS target.

Test:

Digital Crown
small-screen UI
complications
notifications
haptics
voice interaction
paired-device synchronization
offline behavior
battery constraints
accessibility

---

11. visionOS

Create a dedicated visionOS adapter.

Test where supported:

spatial UI
windowed experience
immersive experience
hand interaction
eye tracking
voice
spatial audio
accessibility
scene persistence
device synchronization

QMOI must not claim visionOS support unless a real target build and appropriate runtime validation exists.

---

12. Windows

Existing QMOI platform specifications include:

- Windows notifications
- media keys
- taskbar integration
- Windows Hello
- Fluent Design
- optional Cortana integration
- clipboard history
- virtual desktop support
- registry persistence
- Game Bar integration
- WinGet updates
- Explorer context menu.

QBUILD should produce:

EXE
MSI
portable EXE where supported
x64
ARM64

Then:

install
launch
Start Menu
file associations
Explorer integration
notifications
media keys
Hello
update
uninstall
registry cleanup

---

13. macOS

Existing requirements include:

- Notification Center
- Spotlight
- Spotlight Actions
- Dock menu
- menu-bar integration
- Handoff
- iCloud
- AirDrop
- Universal Links
- Metal
- AppleScript
- dark mode
- automatic updates.

Build:

.app
.dmg
ZIP where useful
arm64
x86_64
Universal

Then:

codesign
notarization where applicable
Gatekeeper validation
install
launch
Spotlight
Dock
Handoff
dark mode
update
uninstall

---

14. Linux

Existing QMOI requirements include:

- D-Bus
- desktop entries
- AppStream
- Freedesktop notifications
- MPRIS
- XDG
- Wayland
- systemd
- portals
- IBus/Fcitx
- AT-SPI
- PulseAudio/PipeWire
- multiple desktop environments.

QBUILD should generate where supported:

AppImage
DEB
RPM
Flatpak
Snap

and test:

Ubuntu
Debian
Fedora
Arch-compatible environment
GNOME
KDE
XFCE
Wayland
X11

The existing QA document already specifies AppImage, Snap, Flatpak, DEB, RPM, X11/Wayland and D-Bus tests.

---

15. Web and PWA

Existing QMOI web features include:

- Service Worker
- IndexedDB
- Web Workers
- WebSocket
- Web Audio
- Speech Recognition
- Speech Synthesis
- notifications
- persistent storage
- Share API
- WebRTC
- responsive design
- offline support.

QBUILD should therefore produce:

production web bundle
PWA
container/deployment package

Then automatically test:

Chrome
Edge
Firefox
Safari
Android browser
iOS Safari
offline
service worker
cache
IndexedDB
WebSocket
voice
speech
notifications
WebRTC
responsive layouts
keyboard
screen reader
installation
update
rollback

---

16. QCity

The existing QCity matrix is particularly important.

It includes platform-specific file-management integrations such as:

Windows

Explorer integration
NTFS attributes
alternate data streams
file metadata
Quick Access
preview pane
ZIP
UNC paths
OneDrive
Windows Search
ACLs
thumbnail cache

macOS

Finder
Quick Look
Spotlight
Finder Sync
SMB
extended attributes
Trash
aliases/symlinks
AirDrop
iCloud Drive
FSEvents

Linux

Nautilus/Dolphin
MIME
thumbnails
mount points
symlinks
permissions
SELinux
ACLs
Trash
custom actions
plugins
D-Bus thumbnailer

iOS

Files
iCloud Drive
On-My-iPhone
Document Picker
Share Sheet
Open In
Quick Look
drag/drop
Shortcuts
PhotoKit
document preview
Handoff

Android

DocumentsProvider
MediaStore
Storage Access Framework
Content Intent
shortcuts
MIME associations
thumbnail cache
multi-user support where available
foldables
adaptive icons
gesture navigation
Quick Share

Web

drag/drop
File API
Fetch
Blob
Streams
WebRTC
SharedArrayBuffer
Clipboard
keyboard
PWA installation
responsive layouts
virtual scrolling

All of these should become actual automated capability tests rather than merely documentation entries.

---

17. QMOI Space

QMOI Space must be treated as a native media platform, not simply a generic UI.

The current matrix includes:

Windows

media keys
taskbar controls
H.264/HEVC/AV1
WASAPI
Direct3D
Media Foundation
DirectShow
DXVA
WMP compatibility
voice playback control
Bluetooth audio
spatial audio

macOS

AVFoundation
media keys
AirPlay
spatial audio
Metal
Core Media
HEVC
audio routing
Now Playing
Control Center
AirDrop
Handoff

Linux

PulseAudio
MPRIS
PipeWire
ALSA
V4L2
FFmpeg
Wayland
D-Bus
media keys
Bluetooth
systemd
screen-awake integration

iOS

AVPlayer
AirPlay
Picture-in-Picture
Lock Screen controls
Now Playing
Handoff
haptics
Dynamic Island
MediaRemote
AVAudioSession
PhotoKit

Android

ExoPlayer
MediaSession
AudioFocus
Bluetooth
MediaStore
PiP
notifications
spatial audio
HLS
DASH
metadata
foldables

Web

HTML5 media
MediaSource
WebGL
Web Audio
Fullscreen
keyboard
gestures
Media Session
PiP
MediaStream
BroadcastChannel
Service Worker caching

These capabilities should feed directly into QDEVICE's media capability detector.

---

18. QALPHA

QALPHA is not simply another application.

It is the development/IDE environment.

Existing requirements include:

Windows

PowerShell
Registry
BAT/CMD
COM
Windows API
Visual Studio
MSVC
Windows Defender integration
Windows Terminal
Quick Edit
Clipboard
Windows Sandbox

macOS

Xcode
AppleScript
LLDB
Objective-C
Swift
LLVM
xcodebuild
code signing
notarization
CocoaPods
Zsh
Rosetta

Linux

GCC/Clang
GDB
Make/CMake
Bash/Zsh
systemd
Docker
SSH
package managers
timers
Valgrind
perf
LSP

iOS

Swift Playgrounds
Xcode previews
iOS Simulator
Xcode Server
TestFlight
App Store Connect
provisioning
capabilities
signing
entitlements
live issues
Swift Package Manager

Android

Gradle
Android Studio
emulators
ADB
Kotlin coroutines
Jetpack
Material
ProGuard/R8
manifest editor
resources
drawable preview
lint

Web

JavaScript debugging
network inspector
storage inspector
performance profiler
accessibility audit
Lighthouse
npm/yarn
Webpack/Vite
ESLint
Prettier
Jest
coverage

These capabilities should be remotely available even when QALPHA itself is running from a low-resource client.

---

19. QMOI universal device layer

Introduce:

QDEVICE

as the universal device abstraction.

Every connected/recognized device gets a capability profile:

{
  "device_id": "...",
  "platform": "...",
  "os": "...",
  "os_version": "...",
  "architecture": "...",
  "cpu": "...",
  "gpu": "...",
  "ram": "...",
  "storage": "...",
  "display": "...",
  "audio": "...",
  "microphone": true,
  "camera": true,
  "bluetooth": true,
  "wifi": true,
  "cellular": true,
  "gps": true,
  "nfc": false,
  "biometrics": true,
  "voice_input": true,
  "voice_output": true,
  "screen_reader": "...",
  "eye_tracking": false,
  "gesture_input": true,
  "external_display": true,
  "offline_storage": true
}

QMOI chooses its runtime and artifact based on this capability profile.

---

20. QFORALLDEVICES

Create:

QFORALLDEVICES.md

as the master device-universality specification.

Its purpose:

Every supported device
→ one QMOI identity
→ one capability profile
→ one synchronization protocol
→ one accessibility contract
→ one hands-free contract
→ one memory contract
→ one security contract
→ one update contract

It should cover:

phones
tablets
laptops
desktops
servers
TVs
wearables
cars
headsets
AR devices
VR devices
kiosks
embedded systems
IoT devices
smart displays
gaming devices
industrial terminals
education devices
assistive devices
future devices

A new device must not require redesigning QMOI's core.

It requires a new adapter.

---

21. QILDEVICES

Create:

QILDEVICES.md

as the implementation-level device integration contract.

It should define:

device discovery
device identity
device capabilities
transport
authentication
permissions
installation
deployment
runtime control
telemetry
logging
memory synchronization
hands-free interfaces
accessibility
update
rollback
decommissioning

The distinction should be:

QFORALLDEVICES
    = universal specification

QILDEVICES
    = implementation/integration specification

---

22. Future platforms

QMOI cannot literally build for a platform that has not yet been invented or whose SDK/specification does not exist.

Instead, QMOI should be designed to automatically recognize:

NEW_PLATFORM_DETECTED

and generate:

platform adapter specification
capability mapping
build requirements
runtime requirements
accessibility mapping
hands-free mapping
memory adapter
artifact format
installation adapter
deployment adapter
test suite

The flow becomes:

NEW PLATFORM
     ↓
DISCOVER
     ↓
IDENTIFY SDK / ABI / UI / SECURITY MODEL
     ↓
GENERATE ADAPTER
     ↓
VALIDATE ADAPTER
     ↓
REMOTE BUILDER
     ↓
BUILD
     ↓
INSTALL
     ↓
RUNTIME TEST
     ↓
REGISTER PLATFORM

This is the realistic way to support future platforms.

---

23. Platform adapter contract

Every platform adapter should expose:

detect()
capabilities()
prepare()
build()
package()
sign()
install()
launch()
test()
collect_logs()
collect_metrics()
sync_memory()
uninstall()
update()
rollback()

For example:

AndroidAdapter
iOSAdapter
WindowsAdapter
MacOSAdapter
LinuxAdapter
WebAdapter
AndroidTVAdapter
WearOSAdapter
TVOSAdapter
WatchOSAdapter
VisionOSAdapter
FuturePlatformAdapter

---

24. QBUILD

Create:

QBUILD

as the universal remote build controller.

Input:

application: QMOIAIUI

targets:
  - android
  - android-tv
  - wear-os
  - ios
  - ipados
  - windows
  - macos
  - linux
  - web
  - tvos
  - watchos
  - visionos

mode: release

verification:
  build: true
  artifact: true
  signature: true
  installation: true
  runtime: true
  accessibility: true
  handsfree: true
  memory_sync: true

---

25. Remote build architecture

The local machine must not need platform SDKs.

PHONE / LOW-END PC
        │
        │ small control request
        ▼
QBUILD API
        │
        ▼
BUILD QUEUE
        │
        ├── Android worker
        ├── Android TV worker
        ├── Wear OS worker
        ├── Linux worker
        ├── Windows worker
        ├── macOS worker
        ├── iOS worker
        ├── iPadOS worker
        ├── tvOS worker
        ├── watchOS worker
        ├── visionOS worker
        └── Web worker

GitHub Actions can serve as one execution backend. Your existing repository already uses GitHub-hosted execution, autonomous workflows and multi-platform orchestration.

---

26. Remote toolchains

The toolchain belongs to the remote worker.

For example:

Android worker
→ Android SDK
→ Gradle
→ NDK
→ signing tools

Windows worker
→ Visual Studio/MSVC/.NET
→ signing tools

Linux worker
→ GCC/Clang
→ package tools

Apple worker
→ macOS
→ Xcode
→ signing/notarization infrastructure

Web worker
→ Node/npm/pnpm
→ browser tooling
→ PWA tooling

Your current "BUILD.md" still documents local installation of Visual Studio Build Tools, Xcode, Android Studio/SDK, Linux packages and signing tools. The new remote architecture should move those requirements into the builder rather than your personal machine.

---

27. Real artifact requirement

Every successful build must produce a real artifact.

Examples:

Android
    .apk
    .aab

Windows
    .exe
    .msi

macOS
    .app
    .dmg

Linux
    .AppImage
    .deb
    .rpm
    .flatpak
    .snap

iOS/iPadOS
    .ipa / appropriate archive/distribution artifact

Apple TV
    appropriate tvOS archive/distribution artifact

watchOS
    appropriate watchOS archive/distribution artifact

visionOS
    appropriate visionOS archive/distribution artifact

Web
    production deployment bundle
    PWA

---

28. Artifact verification

Never accept:

workflow = green

as artifact proof.

Require:

artifact exists
artifact non-zero
artifact expected type
artifact expected architecture
artifact contains expected application ID
artifact version correct
artifact commit correct
artifact checksum generated
artifact signature valid
artifact package structurally valid

---

29. Installation verification

The next stage:

REAL ARTIFACT
     ↓
INSTALL
     ↓
VERIFY INSTALLED VERSION
     ↓
LAUNCH
     ↓
SMOKE TEST

Example:

Android
APK → emulator/device → install → launch

Windows
MSI → Windows VM/device → install → launch

macOS
DMG/APP → Mac worker → install → launch

Linux
DEB/AppImage/etc. → Linux environment → install → launch

Web
bundle → deployment → browser → PWA install → launch

iOS
IPA/distribution artifact → authorized Apple test environment/device → install → launch

---

30. Runtime verification

Test actual behavior:

startup
login
memory
conversation
voice
file operations
media
network
offline
notifications
permissions
accessibility
hands-free
cross-device synchronization
update
recovery

---

31. Evidence states

Use:

SOURCE_VERIFIED

BUILD_VERIFIED

ARTIFACT_VERIFIED

SIGNATURE_VERIFIED

INSTALL_VERIFIED

LAUNCH_VERIFIED

RUNTIME_VERIFIED

ACCESSIBILITY_VERIFIED

HANDSFREE_VERIFIED

MEMORY_SYNC_VERIFIED

PHYSICAL_DEVICE_VERIFIED

RELEASE_VERIFIED

Never collapse all of them into one green status.

---

32. QMOI operational awareness

The word "conscious" should be implemented carefully.

QMOI should not make an unverified claim that software has human-like consciousness.

Instead implement:

CONTINUOUS OPERATIONAL AWARENESS

meaning QMOI knows, through measurable state:

where it is running
which user/session is active
which device is active
which capabilities exist
which version is running
which memory state is current
which remote services are available
which tasks are active
which tasks are paused
which devices are synchronized
which permissions are available
which platform constraints exist
which failures occurred
which recovery actions are pending

That gives the practical behavior you want without confusing operational state awareness with a claim of consciousness.

---

33. QIDENTITY

Create a universal:

QIDENTITY

for QMOI.

It must remain stable across:

phone
tablet
PC
Mac
web
TV
watch
car
headset
remote server
Codespace
cloud worker

Each instance receives:

instance_id
device_id
platform_id
installation_id
session_id
memory_cursor
capability_hash
software_version

---

34. Universal QMOI identity

The identity model becomes:

                    QMOI IDENTITY
                         │
           ┌─────────────┼─────────────┐
           │             │             │
       Device A       Device B      Device C
           │             │             │
        Android        Windows        Web
           │             │             │
        instance       instance       instance
           └─────────────┼─────────────┘
                         │
                   shared state

The applications are separate instances of the same QMOI system rather than isolated copies.

---

35. Universal memory

Create:

QMEMORY

with layers:

L1: ephemeral session state

L2: device-local encrypted state

L3: user/account memory

L4: application memory

L5: cross-device synchronized memory

L6: repository/development memory

L7: operational/event memory

L8: long-term archive

---

36. Memory synchronization

Your repositories already have a real-time memory architecture involving:

- "QMOI_REALTIME_MEMORY_INDEX.md"
- ".qmoi_memory_index.json"
- SHA-256 tracking
- cross-device sync
- real-time updates
- automatic file tracking
- checkpoints.

The new system should extend this beyond repository files into application state.

---

37. Event-based memory synchronization

Instead of copying the entire memory database between devices:

DEVICE A
    ↓
memory event
    ↓
QMEMORY BUS
    ↓
DEVICE B
DEVICE C
DEVICE D

Events:

{
  "event_id": "...",
  "device_id": "...",
  "user_id": "...",
  "memory_namespace": "conversation",
  "sequence": 12345,
  "timestamp": "...",
  "operation": "UPSERT",
  "object_id": "...",
  "payload_hash": "...",
  "previous_version": "...",
  "new_version": "..."
}

This is more scalable than constantly copying entire memory stores.

---

38. Conflict resolution

If two devices modify the same state:

DEVICE A
    ↓
version 100

DEVICE B
    ↓
version 101

QMOI must not blindly overwrite.

Use:

causal ordering
version vectors
timestamps as secondary evidence
conflict classification
deterministic merge
manual resolution where necessary

---

39. Offline memory

If a device loses connectivity:

OFFLINE
   ↓
local encrypted event queue
   ↓
continue operation
   ↓
network restored
   ↓
reconnect
   ↓
authenticate
   ↓
upload events
   ↓
receive remote events
   ↓
merge
   ↓
verify

This is especially important for:

Android
iOS
laptops
vehicles
wearables
remote areas

---

40. Memory synchronization frequency

The existing QMOI documentation describes five-second memory synchronization and real-time tracking.

Keep that as a configurable target, but do not force every platform to synchronize every five seconds.

Use:

real-time
near-real-time
periodic
offline
eventual

depending on:

battery
network
data cost
device capability
user settings
importance

For example:

critical security event → immediate

conversation state → near-real-time

large media metadata → batched

telemetry → adaptive

low-data mode → compressed/batched

---

41. Low-bandwidth synchronization

For your mobile/Codespace use case:

delta synchronization
compression
deduplication
hash-based change detection
binary patching
event batching
adaptive polling
WebSocket when useful
fallback polling
metadata-first synchronization
artifact-on-demand downloading

A phone should not download a 1 GB build artifact merely to display:

BUILD SUCCESS

It should receive:

build ID
status
artifact size
checksum
download link
test summary

and download the artifact only when requested.

---

42. QMOI hands-free architecture

Create:

QHANDSFREE

with:

voice
gesture
eye tracking
head movement
touch
switch access
keyboard
remote control
camera-based interaction
assistive technologies

The repositories already explicitly describe hands-free controls through voice, gestures and eye tracking.

---

43. Universal voice interface

QMOI should support:

wake word where permitted
push-to-talk
continuous conversation
speech-to-text
natural-language commands
text-to-speech
voice confirmation
voice navigation
voice authentication where supported

Example:

"QMOI, build the Android, Windows and Web versions."

QMOI:
"Build request created.
Android: building.
Windows: queued.
Web: building."

Then:

"QMOI, install the Android build."

→ select verified artifact
→ verify device
→ request permission if needed
→ install
→ launch
→ test

---

44. Gesture control

Depending on platform capabilities:

swipe
pinch
tap
double tap
long press
air gesture
remote gesture
controller input

The adapter chooses what exists.

---

45. Eye-control interface

Where the device exposes appropriate APIs:

gaze
dwell
selection
scroll
focus
confirmation

Where it doesn't:

QHANDSFREE capability = unavailable

not:

PASS

---

46. Accessibility-first architecture

Accessibility should not be a separate afterthought.

The existing platform matrix already includes:

VoiceOver
TalkBack
AT-SPI
keyboard navigation
high contrast
Dynamic Type
screen-reader support

and the QA documentation calls for VoiceOver, NVDA/JAWS, magnification and other accessibility testing.

Create:

QACCESSIBILITY

with:

screen reader
keyboard
switch access
voice control
magnification
high contrast
reduced motion
captions
audio descriptions
haptic alternatives
large text
color independence
focus management
semantic labels
alternative input

---

47. Accessibility validation pipeline

Every release:

BUILD
 ↓
ACCESSIBILITY STATIC SCAN
 ↓
AUTOMATED UI TEST
 ↓
SCREEN READER TEST
 ↓
KEYBOARD TEST
 ↓
MAGNIFICATION TEST
 ↓
CONTRAST TEST
 ↓
REDUCED MOTION TEST
 ↓
PLATFORM-SPECIFIC ACCESSIBILITY TEST

---

48. Universal capability negotiation

At startup:

QMOI
 ↓
QDEVICE
 ↓
CAPABILITY DISCOVERY
 ↓
FEATURE NEGOTIATION

Example:

{
  "voice": true,
  "camera": true,
  "eye_tracking": false,
  "gesture": true,
  "haptics": true,
  "screen_reader": "TalkBack",
  "offline_storage": true,
  "gpu_acceleration": true
}

QMOI then chooses the correct interaction mode.

---

49. Graceful degradation

If a device doesn't have:

camera

use:

voice/text

If it doesn't have:

microphone

use:

touch/keyboard

If it doesn't have:

GPU

use:

CPU rendering

If it doesn't have:

persistent storage

use:

remote memory

If it doesn't support:

push notifications

use:

polling / platform alternative

This is how QMOI becomes genuinely portable.

---

50. Cross-device continuity

A user should be able to:

start conversation on phone
        ↓
continue on laptop
        ↓
continue on web
        ↓
continue on TV
        ↓
continue through voice on wearable

with:

same identity
same authorized memory
same conversation
same preferences
same task state
same QMOI configuration

The repositories already specify Handoff/Continuity and cloud synchronization on Apple platforms, along with cloud sync for QMOI accounts.

---

51. Task continuity

If QMOI is building something:

Phone:
"Build QCity for Android and Windows."

        ↓

Remote execution begins.

        ↓

Phone disconnects.

        ↓

Laptop reconnects.

        ↓

QMOI:
"Build still running.
Android: 74%
Windows: queued."

The execution must live remotely rather than inside the phone session.

This matches the existing QMOI production architecture, which requires remote execution to survive Codespace shutdown and resume when the user reconnects.

---

52. Cross-repository architecture

Use:

Alpha-Q-ai
      ↕
QMOI workspace/sync broker
      ↕
qmoi-enhanced

Both directions must work.

The existing master plan explicitly requires:

Alpha-Q-ai → qmoi-enhanced

and the inverse:

qmoi-enhanced → Alpha-Q-ai

with validation, PRs, checks, merge verification and synchronization.

---

53. Responsibility split

Alpha-Q-ai

Primary:

QMOI orchestration
global execution
Q.0.0.N
cross-repository coordination
remote build requests
device orchestration
memory coordination
evidence
release coordination
global monitoring

qmoi-enhanced

Primary:

platform implementation
application implementation
feature validators
QBUILD workers
QDEVICE adapters
runtime tests
accessibility tests
hands-free tests
artifact verification
platform-specific integration

---

54. QMOI central orchestrator

The existing "QMOIORCHESTRATOR.md" already calls for a central service above:

workflow orchestrators
runner orchestrators
release orchestrators
AI-agent orchestrators
network orchestrators
security orchestrators
style orchestration

and requires discovery, capability detection, health evaluation, cross-repository awareness and runtime synchronization.

Extend that registry with:

build orchestrator
device orchestrator
memory orchestrator
hands-free orchestrator
accessibility orchestrator
artifact orchestrator
deployment orchestrator
future-platform orchestrator

---

55. QORCHESTRATOR registry

Every subsystem should expose:

{
  "orchestrator_id": "...",
  "domain": "build",
  "version": "...",
  "capabilities": [],
  "health": "healthy",
  "runner_requirements": [],
  "dependencies": [],
  "last_heartbeat": "...",
  "current_execution": "..."
}

---

56. QBUILD orchestration states

DISCOVERED
QUEUED
PROVISIONING
BUILDING
PACKAGING
SIGNING
UPLOADING
INSTALLING
LAUNCHING
TESTING
VERIFYING
COMPLETED
FAILED
BLOCKED
CANCELLED
RECOVERING

---

57. Fail-closed behavior

The existing QMOI master plan explicitly requires unknown security/remote/live-activity states to remain unknown/failure rather than becoming false passes.

Apply exactly the same principle to builds:

BUILD_UNKNOWN ≠ BUILD_PASS

ARTIFACT_UNKNOWN ≠ ARTIFACT_PASS

INSTALL_UNKNOWN ≠ INSTALL_PASS

RUNTIME_UNKNOWN ≠ RUNTIME_PASS

DEVICE_UNKNOWN ≠ DEVICE_PASS

MEMORY_SYNC_UNKNOWN ≠ MEMORY_SYNC_PASS

---

58. Artifact evidence

Every artifact gets:

{
  "application": "QMOIAIUI",
  "platform": "android",
  "architecture": "arm64-v8a",
  "source_repository": "qmoi-enhanced",
  "source_sha": "...",
  "build_id": "...",
  "workflow_id": "...",
  "artifact_name": "...",
  "artifact_size": 0,
  "sha256": "...",
  "signature": "...",
  "build_status": "PASS",
  "install_status": "PASS",
  "launch_status": "PASS",
  "runtime_status": "PASS",
  "accessibility_status": "PASS",
  "handsfree_status": "PASS",
  "memory_sync_status": "PASS"
}

---

59. Artifact provenance

The artifact must always answer:

Which source?
Which commit?
Which branch?
Which workflow?
Which builder?
Which SDK?
Which compiler?
Which dependencies?
Which signing identity?
Which tests?
Which device?
When?

---

60. QDEVICE installation protocol

1. Discover device
2. Authenticate
3. Verify device identity
4. Read capabilities
5. Check artifact compatibility
6. Verify checksum
7. Verify signature
8. Install
9. Verify installed version
10. Launch
11. Execute smoke tests
12. Execute runtime tests
13. Collect logs
14. Synchronize evidence
15. Mark status

---

61. Deployment protocol

For stores/cloud deployment:

artifact
 ↓
distribution validation
 ↓
credentials check
 ↓
metadata validation
 ↓
privacy/security validation
 ↓
submission
 ↓
provider response
 ↓
release status
 ↓
deployment verification

QMOI must distinguish:

ARTIFACT_CREATED

from:

STORE_SUBMITTED

from:

STORE_APPROVED

from:

STORE_RELEASED

---

62. No fake future-platform support

If QMOI discovers a new device:

UNKNOWN_PLATFORM

it should report:

DISCOVERED
CAPABILITY_PROFILED
ADAPTER_REQUIRED

rather than pretending it already supports it.

Once an SDK/specification exists:

ADAPTER_GENERATED
BUILD_SUPPORTED
RUNTIME_SUPPORTED

can progress independently.

---

63. Universal platform registry

Create:

platforms/
    registry.json

containing:

{
  "platforms": [
    {
      "id": "android",
      "family": "mobile",
      "status": "supported",
      "adapter": "AndroidAdapter"
    },
    {
      "id": "ios",
      "family": "mobile",
      "status": "supported",
      "adapter": "IOSAdapter"
    }
  ]
}

New platforms can be registered without rewriting the orchestrator.

---

64. Device registry

Create:

devices/
    registry.json

with:

device family
vendor
model
OS
version
architecture
capabilities
known limitations
supported artifact
test profile
accessibility profile
hands-free profile
memory profile

---

65. Capability registry

Create:

capabilities/
    universal.json

Capabilities:

voice
speech-to-text
text-to-speech
camera
microphone
GPU
NPU
biometrics
GPS
NFC
Bluetooth
Wi-Fi
cellular
haptics
eye tracking
gesture
screen reader
external display
offline storage
background execution
push notifications

---

66. QMOI memory should include device context

When QMOI receives a request:

"Continue what I was doing."

it should resolve:

identity
user
session
device
platform
last task
last application
last state
last successful checkpoint
pending remote execution
pending synchronization

---

67. Device-aware responses

For example:

Android phone:
"Voice input is available."

Wear OS:
"Voice input is available, but the full QCity interface is unavailable."

Windows:
"QALPHA IDE is available."

Web:
"Using PWA mode."

Vision device:
"Spatial interaction adapter is available."

---

68. QMOI memory namespaces

Use:

identity/
user/
conversation/
preferences/
devices/
applications/
tasks/
builds/
artifacts/
deployments/
security/
permissions/
accessibility/
handsfree/
projects/
repositories/
orchestration/
telemetry/

---

69. Memory privacy

Not every memory should replicate everywhere.

Each memory object should carry:

scope
classification
encryption
allowed_devices
allowed_apps
retention
synchronization_policy

Examples:

public preference
→ all authorized devices

private conversation
→ authorized user's devices

credential
→ never synchronize as ordinary memory

private key
→ never place in memory event stream

temporary build log
→ remote execution namespace only

---

70. Credential isolation

Especially important for:

GitHub
Apple
Google
Microsoft
signing
payment
trading
cloud

Credentials must remain in secure secret stores.

They must never become ordinary cross-device memory.

---

71. Existing memory architecture should be preserved

Do not remove:

MEMORY_INDEX.md
QMOI_REALTIME_MEMORY_INDEX.md
.qmoi_memory_index.json
ollamatracks
checkpoint.json
resumefromhere.txt
activity feeds

The existing QMOI documentation already defines these as part of resumability, memory tracking and evidence.

Instead, extend them.

---

72. New memory architecture

QMEMORY/
├── identity/
├── devices/
├── sessions/
├── events/
├── snapshots/
├── conflicts/
├── checkpoints/
├── indexes/
├── policies/
└── evidence/

---

73. Universal checkpoint

Every long operation:

build
test
deployment
sync
repository modification
device installation

must create a checkpoint.

Example:

{
  "execution_id": "...",
  "stage": "INSTALL_TESTING",
  "repository": "...",
  "commit_sha": "...",
  "target": "android-arm64",
  "artifact": "...",
  "last_completed_step": "signature_validation",
  "next_step": "install",
  "retry_count": 0
}

---

74. Recovery

If the worker dies:

WORKER FAILURE
     ↓
checkpoint discovered
     ↓
new worker
     ↓
verify previous state
     ↓
resume from checkpoint

No unnecessary rebuild where a verified artifact already exists.

---

75. Build caching

To reduce time, bandwidth and compute:

dependency cache
SDK cache
compiler cache
Gradle cache
npm cache
Python cache
Docker layers
build outputs
test results
artifact cache

But caches must never be trusted as proof.

A cached artifact still needs integrity verification.

---

76. Deterministic builds

Where possible:

same source
+
same toolchain
+
same configuration
=
same artifact

Record:

toolchain version
dependency lock
build configuration
environment fingerprint
source SHA

---

77. Remote-first mobile mode

For your low-data environment:

PHONE
  ↓
small request
  ↓
remote worker
  ↓
large computation
  ↓
small status result

Avoid transmitting:

large SDKs
source trees unnecessarily
build logs continuously
large binaries unless requested

---

78. Live status compression

Instead of sending thousands of log lines:

BUILD 74%

send:

{
  "execution": "...",
  "stage": "BUILDING",
  "progress": 74,
  "target": "android-arm64",
  "last_event": "assembleRelease",
  "error_count": 0
}

Full logs remain remote.

---

79. Existing Ollama architecture

The current automation documentation already defines:

- platform compilation
- comprehensive tests
- file-handler validation
- accessibility
- platform requirements
- signed packages
- memory maintenance
- auto-repair
- simultaneous platform builds
- checksums
- releases
- real-time memory synchronization.

The new QBUILD system should therefore become an extension of the existing autonomous agent rather than a parallel unrelated system.

---

80. Ollama should become the build decision agent, not the compiler

Correct architecture:

Ollama
   ↓
reasoning / planning / diagnosis
   ↓
QBUILD
   ↓
actual platform toolchain
   ↓
real artifact

Ollama should never fabricate a build result.

---

81. Autonomous repair

When a build fails:

BUILD FAILED
     ↓
collect error
     ↓
classify
     ↓
inspect source
     ↓
generate repair
     ↓
patch
     ↓
static validation
     ↓
rebuild

Bound it with the existing controls such as:

MAX_ITERATIONS
MAX_TASKS_PER_ITERATION
MAX_RECOVERY_ATTEMPTS

The existing automation guide explicitly uses bounded recovery and resumable state.

---

82. Never let autonomous repair bypass security

If the failure involves:

credential
certificate
private key
permissions
security policy
production signing
financial transaction

the system must stop or use an explicitly authorized safe path.

---

83. Universal testing matrix

For every:

application × platform × architecture × supported OS version

test:

build
install
launch
core functions
native integrations
network
offline
memory
accessibility
hands-free
performance
security
update
rollback

---

84. Four applications × expanded targets

The original six-platform matrix becomes:

              Android AndroidTV WearOS iOS iPadOS tvOS watchOS visionOS
QMOIAIUI          ✓       ✓        ✓     ✓    ✓      ✓      ✓      ✓
QCity             ✓       ✓        -     ✓    ✓      -      -      -
QMOI Space        ✓       ✓        ✓     ✓    ✓      ✓      ✓      ✓
QALPHA            ✓       -        -     ✓    ✓      -      -      ✓

Windows macOS Linux Web PWA ChromeOS Automotive Embedded
QMOIAIUI    ✓      ✓     ✓    ✓       ✓       ✓          ✓
QCity       ✓      ✓     ✓    ✓       ✓       -           ✓
QMOI Space  ✓      ✓     ✓    ✓       ✓       ✓           ✓
QALPHA      ✓      ✓     ✓    ✓       ✓       -           ✓

But every "✓" must be backed by actual implementation and evidence.

A "-" means:

not applicable / not currently implemented

not failure.

---

85. QMOI application capability registry

Each app should declare:

{
  "application": "QMOIAIUI",
  "capabilities": [
    "conversation",
    "voice",
    "memory",
    "handsfree",
    "accessibility",
    "cross_device_sync",
    "automation"
  ]
}

QCity:

file management
cloud storage
file analysis
cross-app integration

QMOI Space:

media playback
streaming
offline media
audio
video
device media integration

QALPHA:

coding
terminal
remote development
build orchestration
debugging
deployment

---

86. Cross-application QMOI integration

The existing QA workflow already describes QCity → QMOIAIUI and QMOI Space → QMOIAIUI workflows.

Extend this:

QCity
 ↓
QMOIAIUI analyzes file
 ↓
QMOI Space plays media
 ↓
QMOIAIUI analyzes media
 ↓
QALPHA edits/builds code
 ↓
QBUILD creates artifact
 ↓
QSTORE distributes artifact

All share the same authorized QMOI identity and memory.

---

87. QSTORE integration

Every verified artifact can enter:

QSTORE

only after:

artifact verified
signature verified
security verified
installation/runtime verified
metadata verified

QSTORE should distinguish:

development
alpha
beta
release candidate
production
deprecated
withdrawn

---

88. QSTREAM integration

QMOI Space/QSTREAM should use the same device capability layer.

For example:

TV
→ TV media interface

phone
→ touch + PiP + mobile data mode

wearable
→ remote playback controls

desktop
→ media keys + GPU acceleration

web
→ Media Session API

The existing platform matrix already describes these media-specific integrations.

---

89. Accessibility + hands-free + memory are universal layers

They should not be implemented separately in every app.

Instead:

QMOI CORE
   │
   ├── QMEMORY
   ├── QIDENTITY
   ├── QACCESSIBILITY
   ├── QHANDSFREE
   ├── QDEVICE
   └── QNETWORK
          │
          ▼
     Application adapters

This reduces duplication.

---

90. Network awareness

QMOI should know:

online
offline
metered
unmetered
Wi-Fi
cellular
VPN
high latency
low latency
unstable
restricted

Then choose:

full synchronization
delta synchronization
offline queue
compressed mode
deferred artifact download

---

91. Memory-aware network behavior

Example:

High bandwidth:
real-time synchronization

Moderate bandwidth:
batched synchronization

Low bandwidth:
compressed deltas

Very low bandwidth:
critical-state synchronization only

Offline:
local event queue

---

92. Device health awareness

QDEVICE should monitor:

battery
temperature where permitted
storage
memory pressure
network
CPU
GPU
application state
permissions
connectivity

QMOI can then avoid expensive operations on constrained devices.

---

93. Resource-aware execution

If a device has:

4 GB RAM

QMOI should not unnecessarily run:

large local compiler
large local model
large emulator

Instead:

remote execution

This aligns strongly with the remote-first architecture you are trying to use.

---

94. Universal remote execution

QMOI should be able to say:

"This task requires macOS."

→ route to macOS worker

or:

"This task requires Android device testing."

→ route to Android device worker

or:

"This task requires a physical iPhone."

→ route to authorized Apple device worker

---

95. No local toolchain requirement

The user-facing contract becomes:

LOCAL DEVICE:

Git
optional

Browser
yes

QMOI client
yes

Platform SDKs
NO

Android Studio
NO

Xcode
NO

Visual Studio
NO

Android NDK
NO

Linux build toolchain
NO

The remote builders contain the necessary toolchains.

---

96. But build tools still exist remotely

This distinction must remain explicit.

It is technically impossible to compile native platform applications without some compiler/SDK/build environment existing somewhere.

The goal is:

NO LOCAL TOOLCHAIN

not:

NO TOOLCHAIN ANYWHERE

---

97. Apple exception

Apple targets require appropriate Apple build/signing infrastructure.

Therefore:

Android phone
    ↓
remote Apple-capable build infrastructure
    ↓
iOS artifact

is possible architecturally.

But:

Android phone alone
    ↓
magically create production-signed iOS artifact

is not.

The existing QALPHA requirements correctly recognize Xcode, signing, provisioning and TestFlight/App Store Connect as Apple-specific infrastructure.

---

98. Physical-device verification

Three evidence levels:

VIRTUAL_VERIFIED

SIMULATOR_VERIFIED

PHYSICAL_DEVICE_VERIFIED

Do not confuse them.

---

99. Device farm

Eventually:

QDEVICE FARM

Android
 ├── low-end
 ├── mid-range
 ├── flagship
 ├── foldable
 ├── tablet
 └── TV

Apple
 ├── iPhone
 ├── iPad
 ├── Apple TV
 ├── Apple Watch
 └── Vision device

Windows
 ├── x64
 └── ARM64

Mac
 ├── Intel
 └── Apple Silicon

Linux
 ├── x86_64
 └── ARM64

---

100. Representative-device strategy

"All devices globally" should mean:

all supported device classes
+
representative hardware coverage
+
capability-driven compatibility
+
automatic new-device discovery

It cannot literally mean physically testing every device ever manufactured.

---

101. New device onboarding

When a new device appears:

DEVICE DETECTED
       ↓
PLATFORM IDENTIFICATION
       ↓
CAPABILITY DISCOVERY
       ↓
COMPATIBILITY CHECK
       ↓
ARTIFACT SELECTION
       ↓
INSTALL
       ↓
TEST
       ↓
REGISTER DEVICE PROFILE

---

102. New-platform onboarding

PLATFORM DETECTED
       ↓
SDK/API discovery
       ↓
adapter specification
       ↓
build worker requirements
       ↓
artifact format
       ↓
installation method
       ↓
accessibility APIs
       ↓
hands-free APIs
       ↓
memory transport
       ↓
test profile
       ↓
register platform

---

103. Universal source → universal artifact pipeline

The final canonical pipeline should therefore be:

                    QMOI SOURCE
                         │
                         ▼
                 UNIVERSAL CORE
                         │
                         ▼
                 PLATFORM ADAPTERS
                         │
                         ▼
                 TARGET DISCOVERY
                         │
                         ▼
                TARGET MATRIX
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
   MOBILE              DESKTOP            OTHER
       │                 │                 │
Android/iOS        Windows/macOS       TV/Wear/XR
iPadOS             Linux               Web/PWA
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
                 REMOTE BUILD FARM
                         │
                         ▼
                  REAL ARTIFACTS
                         │
                         ▼
                  SIGN / HASH
                         │
                         ▼
                 ARTIFACT VERIFY
                         │
                         ▼
                  DEVICE SELECT
                         │
                         ▼
                     INSTALL
                         │
                         ▼
                     LAUNCH
                         │
                         ▼
                    RUNTIME TEST
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
       ACCESSIBILITY  HANDSFREE    MEMORY
            │            │            │
            └────────────┼────────────┘
                         ▼
                     EVIDENCE
                         │
                         ▼
                  RELEASE / DEPLOY
                         │
                         ▼
                 CROSS-DEVICE SYNC

---

104. QMOI awareness loop

Every active QMOI instance should continuously maintain:

WHO AM I?
WHERE AM I?
WHICH DEVICE?
WHICH PLATFORM?
WHICH USER?
WHICH SESSION?
WHICH APPLICATION?
WHICH CAPABILITIES?
WHICH MEMORY VERSION?
WHICH TASK?
WHICH REMOTE EXECUTIONS?
WHICH PERMISSIONS?
WHICH NETWORK?
WHICH ERRORS?
WHICH RECOVERY?
WHAT CHANGED?
WHAT NEEDS SYNCHRONIZATION?

That is the practical implementation of persistent operational awareness.

---

105. QMOI presence

QMOI's avatar/presence layer should remain synchronized with:

identity
voice
style
application
device
theme
session
memory
activity

The existing repository already has avatar identity, voice selection, animation, live-window and realtime synchronization validation.

Extend this so the same QMOI identity follows the authorized user across devices.

---

106. Presence handoff

Example:

Phone:
QMOI voice conversation

User opens laptop.

Laptop:
"Continuing your QMOI conversation."

Phone:
becomes secondary

Laptop:
becomes primary

Memory:
synchronized

Avatar:
moves to active device

---

107. Multi-device simultaneous presence

QMOI should also support:

phone = voice interface
laptop = development interface
TV = display/media interface
watch = notification/control interface
server = computation interface

All can represent the same QMOI identity without each trying to become an independent conflicting QMOI.

---

108. Device roles

Define:

PRIMARY
SECONDARY
CONTROL
DISPLAY
COMPUTE
STORAGE
SENSOR
MEDIA
BUILD
TEST

A single device may have several roles.

---

109. QMOI distributed execution

A task can be split:

phone:
capture voice

server:
reasoning

GPU worker:
model inference

build worker:
compile

device:
installation/runtime

phone:
display result

This is a much more scalable model than trying to make every device perform every task locally.

---

110. Universal task routing

QMOI should choose execution location based on:

capability
latency
cost
battery
privacy
security
network
hardware
availability
authorization

---

111. QMOI should not blindly choose remote execution

Sensitive operations can require local execution.

Therefore each task has:

LOCAL_ALLOWED
REMOTE_ALLOWED
REMOTE_REQUIRED
PHYSICAL_DEVICE_REQUIRED
USER_CONFIRMATION_REQUIRED

---

112. Memory and execution security

Every task receives:

task_id
execution_id
identity
authorization
scope
device
target
memory_scope
expiration

---

113. Evidence ledger

Extend the existing "ollamatracks" architecture:

ollamatracks/
├── CURRENT_STATUS
├── TRACKING_INDEX
├── telemetry.jsonl
├── current_state.json
├── executions/
│   └── execution-id/
│       ├── execution.json
│       ├── stages.json
│       ├── repository-state.json
│       ├── git.json
│       ├── build.json
│       ├── artifacts.json
│       ├── signatures.json
│       ├── installation.json
│       ├── runtime.json
│       ├── accessibility.json
│       ├── handsfree.json
│       ├── memory.json
│       ├── device.json
│       ├── security.json
│       └── final-verification.json
└── checkpoints/

The existing master plan already establishes a structured "ollamatracks" evidence architecture and telemetry schema.

---

114. Completion engine

Only one component may produce:

FINAL_SUCCESS

The existing architecture already requires a deterministic completion engine.

Extend it:

QCOMPLETION ENGINE

source
build
artifact
signature
installation
runtime
accessibility
handsfree
memory
device
security
deployment
cross-repo

All required gates must pass.

---

115. Example final result

Instead of:

✅ Build succeeded

QMOI should produce:

QMOI BUILD VERIFIED

Application:
QMOIAIUI

Source:
qmoi-enhanced

Commit:
abc123

Targets:
Android
Windows
Web

Android:
BUILD_PASS
ARTIFACT_PASS
INSTALL_PASS
RUNTIME_PASS
ACCESSIBILITY_PASS
HANDSFREE_PASS
MEMORY_SYNC_PASS

Windows:
BUILD_PASS
ARTIFACT_PASS
INSTALL_PASS
RUNTIME_PASS
ACCESSIBILITY_PASS
HANDSFREE_PASS
MEMORY_SYNC_PASS

Web:
BUILD_PASS
DEPLOYMENT_PASS
PWA_INSTALL_PASS
RUNTIME_PASS
ACCESSIBILITY_PASS
HANDSFREE_PASS
MEMORY_SYNC_PASS

Final:
RELEASE_READY

---

116. Failure example

If Windows cannot be physically tested:

Windows:
BUILD_PASS
ARTIFACT_PASS
SIGNATURE_PASS
INSTALL_UNKNOWN
RUNTIME_UNKNOWN
PHYSICAL_DEVICE_UNKNOWN

Final:
PARTIALLY_VERIFIED

Not:

FULL_SUCCESS

---

117. Existing QMOI production lifecycle

The current master plan already defines:

DISCOVER
→ INSPECT BOTH REPOSITORIES
→ INVENTORY
→ DETERMINE CHANGES
→ PLAN
→ MODIFY
→ SELF-REVIEW
→ TEST
→ STATIC VALIDATION
→ SECURITY
→ BUILD/RUNTIME VALIDATION
→ PRODUCTION CONTRACT
→ DIFF
→ COMMIT
→ PUSH
→ VERIFY SHA
→ PR
→ CHECKS
→ REPAIR
→ MERGE
→ VERIFY
→ autosync-backup
→ synchronize other repository
→ Q.0.0.N
→ evidence
→ final verification

The new QBUILD/QDEVICE system should be inserted directly into this existing lifecycle rather than creating a competing lifecycle.

---

118. Cross-repository build flow

Alpha-Q-ai
   ↓
request QBUILD
   ↓
qmoi-enhanced
   ↓
platform implementation
   ↓
remote build
   ↓
artifact
   ↓
device verification
   ↓
evidence
   ↓
Alpha-Q-ai
   ↓
release decision

---

119. Reverse flow

qmoi-enhanced
   ↓
requires orchestration change
   ↓
Alpha-Q-ai
   ↓
orchestrator update
   ↓
validation
   ↓
merge
   ↓
sync

The existing master plan specifically requires this bidirectional capability.

---

120. Codespace independence

Once QBUILD accepts an execution:

Codespace may disconnect

and:

GitHub/remote worker continues

The existing architecture already requires remote completion to survive Codespace termination.

---

121. Reconnection

When the user opens either repo:

QMOI bootstrap
     ↓
query remote executions
     ↓
find unfinished execution
     ↓
read checkpoint
     ↓
display:
execution
stage
target
status
heartbeat
next action

This is consistent with the existing remote-state/reconnect contract.

---

122. Low-data artifact management

Never automatically download every artifact.

Default:

metadata only

User asks:

download Android artifact

Then:

download only Android artifact

User asks:

download all

Then:

show total size first

---

123. Artifact resume

Large downloads must support:

range requests
resume
checksum
partial-download detection
retry

so an interrupted 800 MB artifact does not require restarting from zero.

---

124. Remote logs

Default mobile interface:

BUILDING...
72%

Last event:
assembleRelease

Warnings:
0

Errors:
0

Advanced mode:

full logs

This preserves mobile data.

---

125. Build notifications

QMOI can notify:

build started
build completed
build failed
artifact available
installation completed
runtime test completed
release available
memory synchronized

through whichever notification mechanisms the device supports.

---

126. Device-specific notification adapters

Android → notification channels

iOS → push notifications

Windows → Toast

macOS → Notification Center

Linux → desktop notification APIs

Web → Notification API

The repository already documents several of these native notification mechanisms.

---

127. Universal update system

Every installation should know:

current version
latest compatible version
update availability
update channel
rollback version

QMOI should choose:

delta update
full update
store update
PWA update

according to platform.

---

128. Safe update

download
 ↓
checksum
 ↓
signature
 ↓
compatibility
 ↓
backup state
 ↓
install
 ↓
launch
 ↓
health check
 ↓
commit update

If health check fails:

rollback

where the platform permits rollback.

---

129. Memory migration

When the application updates:

old memory schema
      ↓
migration
      ↓
validation
      ↓
new memory schema

Never silently discard user memory.

---

130. Device migration

When a user moves from:

Android → iOS

or:

Windows → macOS

QMOI should synchronize compatible logical state while respecting platform limitations.

---

131. Capability differences

If a feature doesn't exist on another platform:

Windows Registry

should not be copied literally to:

iOS

Instead map the underlying logical requirement:

persistent application preference

to the native mechanism on that platform.

---

132. Universal abstraction principle

The universal layer describes:

WHAT QMOI needs

Platform adapters describe:

HOW the platform provides it

For example:

Universal:
persistent storage

Windows:
registry / app data

macOS:
preferences / app container

Linux:
XDG/application data

Android:
DataStore/appropriate storage

iOS:
app container/UserDefaults/CloudKit as appropriate

Web:
IndexedDB

---

133. Same principle for voice

Universal:

VOICE_INPUT

Platform:

Android speech services
iOS speech APIs
Windows speech
Web Speech API
native future platform API

---

134. Same principle for accessibility

Universal:

SCREEN_READER

Platform:

TalkBack
VoiceOver
NVDA/JAWS
AT-SPI
browser accessibility tree
future platform accessibility API

---

135. Same principle for media

Universal:

PLAY_MEDIA

Platform:

ExoPlayer
AVPlayer
Media Foundation
GStreamer/FFmpeg/etc.
Web MediaSource
future native media API

---

136. Universal API

QMOI applications should call:

qmoI.device.media.play()
qmoI.device.voice.listen()
qmoI.device.memory.save()
qmoI.device.accessibility.announce()
qmoI.device.haptics.vibrate()
qmoI.device.files.open()
qmoI.device.notifications.send()

The adapter resolves the native implementation.

---

137. New platform adapter automation

When QMOI discovers a platform it doesn't recognize:

1. collect OS metadata
2. collect architecture
3. collect SDK metadata
4. inspect available APIs
5. identify build format
6. identify package format
7. identify installation method
8. identify accessibility APIs
9. identify input APIs
10. identify persistence APIs
11. identify media APIs
12. generate adapter skeleton
13. create tests
14. build
15. validate

---

138. QMOI platform maturity levels

Use:

DISCOVERED
ADAPTER_PLANNED
ADAPTER_IMPLEMENTED
BUILD_SUPPORTED
ARTIFACT_SUPPORTED
INSTALL_SUPPORTED
RUNTIME_SUPPORTED
ACCESSIBILITY_SUPPORTED
HANDSFREE_SUPPORTED
MEMORY_SYNC_SUPPORTED
PRODUCTION_SUPPORTED

This prevents immature targets from being reported as fully supported.

---

139. Global platform inventory

QMOI should continuously maintain:

known platforms
known device families
known architectures
known browsers
known SDKs
known package formats
known accessibility mechanisms
known input mechanisms
known deployment systems

---

140. Global browser matrix

For Web/PWA:

Chrome
Edge
Firefox
Safari
Android browsers
iOS Safari
Chromium derivatives
embedded browsers
future browsers

The existing QA documentation already specifies Chrome, Firefox, Safari and Edge testing.

---

141. Accessibility universal baseline

All platforms should target:

semantic UI
keyboard accessibility where applicable
screen reader compatibility
scalable text
contrast
reduced motion
captions
alternative input
focus visibility
non-color cues
voice control

The exact platform APIs are adapter-specific.

---

142. Hands-free universal baseline

Where supported:

voice
gesture
eye gaze
switch control
head movement
remote/controller

Where unavailable:

fallback interaction

---

143. QMOI "always available" model

The practical objective should be:

QMOI is always reachable through at least one available interface.

For example:

screen available → UI

screen unavailable → voice

voice unavailable → keyboard

keyboard unavailable → touch

touch unavailable → switch/assistive input

network unavailable → local/offline mode

This is much stronger than tying QMOI to one particular device.

---

144. Offline-first core

Core capabilities that can operate offline should remain available:

cached identity
local conversations
local preferences
local task state
local commands
local file operations
offline media
offline PWA

Remote-only operations should be clearly marked:

REMOTE_REQUIRED

---

145. Remote-required tasks

Examples:

iOS production build
large model inference
large multi-platform compilation
cloud deployment
repository-wide autonomous modification
device-farm testing
large-scale media processing

---

146. QMOI should dynamically decide

Can this device do it?
       │
      YES
       ↓
Is local execution preferable?
       │
   ┌───┴───┐
  YES     NO
   │       │
 LOCAL   REMOTE

---

147. Universal execution budget

Every task can include:

max_latency
max_bandwidth
max_cost
max_energy
privacy_requirement
required_capabilities

QMOI chooses the appropriate execution environment.

---

148. Security boundary

QMOI must distinguish:

memory
credentials
tokens
private keys
signing identities
user files
build artifacts
public metadata

Only appropriate classes synchronize.

---

149. Signing

Build workers should receive signing credentials only when necessary and for the shortest possible scope.

They should never write signing keys into:

source code
memory index
logs
artifacts

---

150. Audit trail

Every sensitive build/deployment action:

who/what initiated
authorization
worker
timestamp
target
artifact
result

must be recorded.

---

151. Existing universal standards

The existing "UNIVERSALS.md" requires:

resilient automation
self-healing behavior
documentation consistency
GitHub-native execution
validation-before-merge
accountability
traceability
cross-platform parity
memory/checkpoint tracking
sync planning

and says orchestrators should expose capability/health metadata and automation must respect validation-before-action rules.

All of those should remain foundational.

---

152. New universal standards

Add:

artifact-before-release
installation-before-install-verified
runtime-before-runtime-verified
device-evidence-before-device-verified
memory-sync-before-sync-verified
accessibility-before-accessibility-verified
handsfree-before-handsfree-verified

---

153. No documentation-only completion

A markdown statement:

"QMOI supports Android TV"

does not constitute proof.

Proof requires:

source
build
artifact
installation
runtime
evidence

---

154. No validator-only completion

Similarly:

feature keyword found

does not constitute proof.

The existing agent currently uses file-based implementation detection, keyword scanning and intelligent fallbacks.

Keep those mechanisms for fast validation, but add a second tier:

STATIC_VALIDATION
+
REAL_BUILD_VALIDATION
+
RUNTIME_VALIDATION

---

155. Three-tier validation

TIER 1
Static/source validation

TIER 2
Build/package validation

TIER 3
Installation/runtime/device validation

A production release should require the applicable tiers.

---

156. Release gates

source PASS
       ↓
static PASS
       ↓
build PASS
       ↓
artifact PASS
       ↓
security PASS
       ↓
signature PASS
       ↓
install PASS
       ↓
runtime PASS
       ↓
accessibility PASS
       ↓
handsfree PASS
       ↓
memory-sync PASS
       ↓
deployment PASS
       ↓
RELEASE

---

157. Parallel builds

The current BUILD documentation already describes parallel GitHub Actions builds for Windows, macOS, Linux, iOS, Android and Web.

Expand that matrix:

Android
Android TV
Wear OS
iOS
iPadOS
tvOS
watchOS
visionOS
Windows
macOS
Linux
Web
PWA
ChromeOS

Only launch targets that have valid adapters.

---

158. Dynamic target selection

Instead of hardcoding the workflow forever:

QBUILD reads target registry
        ↓
finds enabled targets
        ↓
resolves runner
        ↓
creates build matrix

Thus adding a new platform does not require rewriting the entire orchestrator.

---

159. Builder discovery

QBUILD should maintain:

builder_id
platforms
architectures
SDK versions
availability
health
capacity
cost
location
security level

Then choose a healthy compatible worker.

---

160. Builder failover

If:

macOS builder unavailable

then:

queue
→ alternate authorized macOS builder
→ retry

Do not falsely report success.

---

161. Build queue

Use:

QUEUED
WAITING_FOR_BUILDER
RUNNING
RETRYING
BLOCKED
COMPLETE

and avoid competing builds for the same artifact/version.

---

162. Idempotency

If the same request arrives twice:

same execution ID

QBUILD returns the existing result instead of creating duplicate builds.

This aligns with the existing cross-repository idempotency contract.

---

163. Cancellation

Support:

REQUESTED
CANCELLING
CHECKPOINTED
CANCELLED

rather than leaving ambiguous states.

---

164. Remote worker isolation

Each build should run in a clean or controlled environment:

checkout exact SHA
install locked dependencies
build
test
destroy/clean worker

This prevents hidden local state from making a build appear successful.

---

165. Reproducibility

Record:

source SHA
lockfile hash
toolchain hash
build config hash
environment hash

---

166. Artifact deduplication

If:

same SHA
same target
same configuration

already exists:

reuse verified artifact

rather than rebuild unnecessarily.

---

167. Security scan before release

Existing automation already calls for secret scanning, dependency/security validation and fail-closed behavior.

Add:

artifact malware/security scan
dependency scan
SBOM generation
signature verification
provenance
permissions audit

---

168. SBOM

Each artifact should have:

software bill of materials

containing dependencies and versions.

---

169. Provenance

Each artifact should have:

source
builder
workflow
toolchain
dependencies
timestamp
signature
hash

---

170. Global QMOI status

The main dashboard should show:

QMOI GLOBAL STATUS

Identity: synchronized
Memory: synchronized
Repositories: synchronized
Orchestrators: healthy
Build workers: 8/9 healthy
Devices: 17 registered
Platforms: 13 supported
Applications: 4
Artifacts: verified
Accessibility: verified
Hands-free: verified
Remote tasks: 3
Pending builds: 2
Failures requiring attention: 0

---

171. Platform status

Each platform gets:

SOURCE
BUILD
ARTIFACT
INSTALL
RUNTIME
ACCESSIBILITY
HANDSFREE
MEMORY
DEPLOYMENT

with explicit status.

---

172. Device status

Each device gets:

online/offline
platform
version
capabilities
memory sync
QMOI instance
last heartbeat
last task

---

173. QMOI heartbeat

Each active instance sends:

instance
device
platform
version
memory cursor
current task
health
timestamp

---

174. Memory heartbeat

QMOI can detect:

DEVICE A memory cursor = 1000
DEVICE B memory cursor = 1000
DEVICE C memory cursor = 998

and synchronize only missing events.

---

175. Memory conflict dashboard

Show:

SYNCED
BEHIND
CONFLICT
BLOCKED
OFFLINE

instead of hiding synchronization problems.

---

176. Global activity stream

The existing "ollamatracks", live activity and telemetry architecture should remain the authoritative operational stream. The current master plan requires structured telemetry and live activity evidence.

Extend events with:

platform
device
artifact
memory_cursor
capability
installation
handsfree
accessibility

---

177. QMOI awareness event

Example:

{
  "event": "DEVICE_CONTEXT_CHANGED",
  "device": "android-...",
  "platform": "android",
  "network": "cellular",
  "battery": 28,
  "memory_cursor": 1234,
  "capabilities_changed": false
}

QMOI can adapt behavior automatically.

---

178. Automatic low-data mode

If QMOI detects:

metered network

it can switch:

LOW_BANDWIDTH_MODE

automatically, subject to user policy.

---

179. Low-bandwidth build mode

When enabled:

no unnecessary artifact downloads
compressed logs
metadata-only status
delta source transfer
remote compilation
cached dependencies
batched telemetry

---

180. User-facing experience

The final user experience should be as simple as:

"QMOI, build QCity everywhere."

QMOI:

Targets discovered:
Android
Android TV
Windows
macOS
Linux
Web

Additional targets:
iOS/iPadOS unavailable because QCity currently has no active Apple target.

Builds started remotely.

Then:

Android       ✓ verified
Android TV    ✓ verified
Windows       ✓ verified
macOS         ✓ verified
Linux         ✓ verified
Web           ✓ deployed
iOS           NOT_APPLICABLE

That is honest automation.

---

181. Another example

User:

"QMOI, build everything supported by this device."

QMOI detects:

Android phone
ARM64
Android version
TalkBack
voice
Bluetooth
camera
microphone

and selects:

Android ARM64 artifact

rather than giving the user a Windows ".exe".

---

182. Another example

User:

"Continue my work."

QMOI resolves:

identity
memory
last application
last device
last task
remote task
checkpoint

and resumes the correct context.

---

183. Another example

User:

"Build QMOI for the new device."

QMOI:

unknown platform detected
capability discovery started
adapter not yet available

Then automatically creates a platform onboarding task.

It does not falsely claim that the platform is already supported.

---

184. Final repository evolution

"qmoi-enhanced"

Add:

QBUILD/
QDEVICE/
QMEMORY/
QHANDSFREE/
QACCESSIBILITY/
platforms/
devices/
capabilities/
builders/
artifacts/
installation-tests/
runtime-tests/
device-tests/

and:

QILDEVICES.md
QFORALLDEVICES.md
QBUILD.md
QDEVICE.md
QMEMORY_UNIVERSAL.md
QHANDSFREE.md
QACCESSIBILITY_UNIVERSAL.md
PLATFORM_ADAPTERS.md
ARTIFACT_VERIFICATION.md
REMOTE_BUILD.md

"Alpha-Q-ai"

Add:

QBUILD_ORCHESTRATOR.md
QDEVICE_ORCHESTRATOR.md
QMEMORY_ORCHESTRATOR.md
QPLATFORM_REGISTRY.md
QBUILD_EVIDENCE.md
QDEVICE_EVIDENCE.md
UNIVERSAL_PLATFORM_CONTRACT.md

and integrate them with:

QMOIORCHESTRATOR.md
Q.0.0.N
ollamatracks
QMOI_REALTIME_MEMORY_INDEX.md
QMOI_Ollama_Autonomous_Production_Completion_Master_Plan.md

---

185. Final architecture

                         ┌───────────────────────────┐
                         │       QMOI UNIVERSAL      │
                         │           CORE            │
                         └─────────────┬─────────────┘
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            │                          │                          │
            ▼                          ▼                          ▼
       QIDENTITY                    QMEMORY                  QORCHESTRATOR
            │                          │                          │
            ├──────────────┐           │           ┌──────────────┤
            │              │           │           │              │
            ▼              ▼           ▼           ▼              ▼
       QDEVICE       QACCESSIBILITY QHANDSFREE QBUILD          QDEPLOY
            │              │           │           │              │
            └──────────────┴───────────┴───────────┴──────────────┘
                                       │
                                       ▼
                             PLATFORM REGISTRY
                                       │
       ┌───────────────────────────────┼──────────────────────────────┐
       │                               │                              │
       ▼                               ▼                              ▼
    MOBILE                          DESKTOP                         OTHER
       │                               │                              │
 Android / Android TV             Windows / macOS / Linux       TV / Wear / XR
 iOS / iPadOS                     Web / PWA                      Embedded
 Wear OS                           ChromeOS                       Automotive
       │                               │                              │
       └───────────────────────────────┼──────────────────────────────┘
                                       │
                                       ▼
                              REMOTE BUILD FARM
                                       │
             ┌─────────────────────────┼──────────────────────┐
             │                         │                      │
             ▼                         ▼                      ▼
       Linux builders           Windows builders       Apple builders
       Android builders         Web builders            specialized
             │                         │                      │
             └─────────────────────────┼──────────────────────┘
                                       │
                                       ▼
                                REAL ARTIFACTS
                                       │
                                SIGN / HASH / SBOM
                                       │
                                       ▼
                                QDEVICE FARM
                                       │
                          ┌────────────┼────────────┐
                          │            │            │
                          ▼            ▼            ▼
                      INSTALL      RUNTIME      ACCESSIBILITY
                          │            │            │
                          └────────────┼────────────┘
                                       ▼
                                  HANDSFREE
                                       │
                                       ▼
                                MEMORY SYNC
                                       │
                                       ▼
                                  EVIDENCE
                                       │
                                       ▼
                             QSTORE / DEPLOYMENT
                                       │
                                       ▼
                              GLOBAL QMOI PRESENCE

186. The resulting capability model

The ultimate QMOI model should therefore be:

ONE QMOI
│
├── ONE universal identity
├── ONE synchronized logical memory
├── ONE capability model
├── ONE accessibility model
├── ONE hands-free model
├── ONE orchestration model
├── ONE evidence model
├── ONE platform registry
├── ONE device registry
├── ONE build abstraction
└── MANY native implementations

Not:

one completely separate QMOI per device

but:

one distributed QMOI system
with native instances/adapters everywhere.

187. Final non-negotiable completion rule

QMOI must never say:

"QMOI supports every platform."

merely because a matrix contains those platforms.

It should say, for each target:

SOURCE_SUPPORTED
BUILD_SUPPORTED
ARTIFACT_VERIFIED
INSTALL_VERIFIED
RUNTIME_VERIFIED
ACCESSIBILITY_VERIFIED
HANDSFREE_VERIFIED
MEMORY_SYNC_VERIFIED
DEVICE_VERIFIED
DEPLOYMENT_VERIFIED

Only the applicable completed evidence determines the actual status.

That approach preserves the strongest part of the current repositories—their extensive platform matrices, autonomous validation, memory/checkpoint architecture, cross-repository orchestration and evidence-driven completion model—while extending them into a genuine remote multi-platform build and universal-device runtime architecture. The existing repositories already provide much of the foundation for this: "qmoi-enhanced" has the platform/application feature matrix and autonomous validator, while "Alpha-Q-ai" has the central orchestration, cross-repository execution, completion protocol and remote-state architecture.

The most important new distinction is that feature/documentation validation becomes only the first layer. QMOI's production truth becomes:

source → build → real artifact → signature → installation → runtime → accessibility → hands-free → memory synchronization → device evidence → deployment.

That is the architecture I would use as the new universal contract for both repositories.

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
