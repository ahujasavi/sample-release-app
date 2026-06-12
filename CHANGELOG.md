# Changelog

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-06-11
### Added
- Initial inventory REST API with CRUD endpoints
- `/health` endpoint for liveness probes
- `/inventory` list and per-SKU detail endpoints
- `/inventory/<sku>/adjust` for quantity updates
- Reorder-point calculation in utils
