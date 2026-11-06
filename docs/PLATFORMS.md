# Platform adoption

The **policy** is shared across platforms. Actual verification commands must match each product and toolchain.

| App type | Typical checks to add beyond the four baseline categories | Where to run |
| --- | --- | --- |
| Windows desktop | Compiler, unit/UI tests, installer/signing, MSIX/packaging | Windows runner and real PC |
| macOS desktop | Xcode/Swift, entitlements, notarization, accessibility | macOS runner and real Mac |
| Linux desktop | Build, package, integration tests, distro compatibility | Linux runner/containers and actual desktop |
| Android | Gradle unit tests, lint, static analysis, build variant, schema/migrations, UI/instrumented tests | Configured Android SDK runner + physical device |
| iOS | Xcode build/test, provisioning, privacy manifest, device UX | macOS + simulator/physical iPhone |
| Web | Typecheck, lint, unit/integration/end-to-end tests, accessibility, production build | Linux/Windows/macOS as appropriate + browsers |
| PWA / installable web app | Web tests plus service worker/cache, install experience and offline behavior | Real target browsers/devices |
| Browser extension | Unit tests, manifest permissions, browser integration, policy review, packaging | Target browser and optional extension store |
| Portable app / executable | Build, package integrity, malware/trust/signing review, clean-machine run | Each target operating system |
| Non-installable script or static tool | Runtime dependencies, clear launch instructions, unit tests, expected output | Target OS/browser/runtime |
| API/backend | Unit/integration tests, contracts, DB migration, permission tests, load tests | Isolated CI services/staging |
| Cross-platform | Shared-core tests **and** per-target builds | Matrix of actual targets |

`examples/` contains **starting points**, not validated universal commands. It now includes iOS/Xcode, browser extension, and portable Python in addition to Android, Windows, macOS, Linux, and web examples. Copy the relevant sample, replace names, SDK destinations and commands, **create any app-specific script referenced**, then dry-run. A Flutter/React Native/Electron/MAUI project often needs **multiple** platform verification jobs; one generic green check does not prove all targets.

## Separate gates

1. **Focused checks** — fast, relevant tests for a small edit.
2. **Full project checks** — broader unit/integration/static analysis and builds at owner-approved checkpoints.
3. **Release checks** — signed artifacts, migrations/backups, install/update/restore, privacy, security, accessibility, and target-device review.

Do not collapse these into a single “verified” label.

## Portability and publication decisions

- **iOS is supported by the instructions**, but a runnable iOS app requires an iOS-capable stack and Mac/Xcode-based builds. Personal-device testing and App Store distribution have different account requirements. Verify these at project start via [Apple's Xcode requirements](https://developer.apple.com/xcode/system-requirements/) and [Apple Developer membership guidance](https://developer.apple.com/help/account/membership/programs-overview).
- **Cross-platform source is conditional.** Flutter supports mobile, web and desktop platforms, but individual features or plugins may need platform code and tests. Check [Flutter supported platforms](https://docs.flutter.dev/reference/supported-platforms) and the actual app needs before choosing a stack.
- **Extensions are not ordinary websites.** Check current manifest version, API permissions and publishing rules via [Chrome Extensions](https://developer.chrome.com/docs/extensions) and the target browser's official documentation.
- **Installable PWA vs ordinary website:** Verify actual browser installation/offline behavior via [web.dev](https://web.dev/learn/pwa/installation). A website can be valuable without installability.
- **Portable or personal-only software** may not need app-store registration, a domain or public hosting. Still document runtime requirements and test it on clean target environments.

Never hard-code a “latest SDK” assumption in this starter kit. Record the **official link and date checked** in each project's `FEASIBILITY.md`; update before releasing.
