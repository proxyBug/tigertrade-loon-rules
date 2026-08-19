# Changelog

All notable changes to this project are documented here.

## [0.1.0] - 2026-08-20

### Added

- Moomoo / Futu standalone rules for Loon, Surge, Shadowrocket, Clash/mihomo, Quantumult X, and sing-box.
- Combined Tiger Trade + Moomoo subscriptions for all six clients.
- Eight current TigerFintech domains cross-checked against the August 2026 blackmatrix7 ruleset.
- Current v2fly Futu domain coverage plus the verified `moomoo.ca`, `moomoobull.com`, and `fututrustee.com` domains.
- Deterministic repository tests and GitHub Actions validation.
- Read-only `python3 scripts/generate.py --check` drift detection.
- MIT license, third-party provenance notice, and evidence-based maintenance documentation.

### Changed

- Generated-file dates now come from source metadata instead of the machine clock.
- README claims and usage examples were rewritten around reproducible evidence and exact rule counts.
- Broad keyword matching was replaced with explicit domain suffixes to prevent unrelated hosts such as `moomooi.com` from matching.

### Removed

- `futu.inc` and `nniuvip.com` from the proposed Moomoo rules because both lacked current DNS and corroborating high-confidence sources during the 2026-08-20 audit.
