# ReMarkable sync API: Complete reverse engineering guide

The ReMarkable cloud API has been thoroughly reverse-engineered by the open-source community, with mature libraries available in Go, Python, TypeScript, and PHP. Building a sync connector for Otso is feasible using existing implementations as reference—the most critical consideration is supporting both legacy and newer **sync15** protocols, as ReMarkable has been migrating users to the new system since 2023.

## Authentication uses a two-tier JWT token system

ReMarkable implements device registration through **8-character one-time codes** generated at `my.remarkable.com/connect/desktop`. The authentication flow produces two token types that must be managed separately.

**Device Token** is obtained by exchanging the one-time code and never expires:
```http
POST https://my.remarkable.com/token/json/2/device/new
Content-Type: application/json

{
    "code": "apwngead",
    "deviceDesc": "desktop-macos",
    "deviceID": "d4605307-a145-48d2-b60a-3be2c46035ef"
}
```

Valid `deviceDesc` values include `desktop-windows`, `desktop-macos`, `mobile-android`, `mobile-ios`, `browser-chrome`, and `remarkable`. The response returns the device token as plain text.

**User Token** is short-lived (expires within **24 hours**) and must be refreshed at session start:
```http
POST https://my.remarkable.com/token/json/2/user/new
Authorization: Bearer {device_token}
```

All subsequent API calls use Bearer authentication with the user token. Tokens are standard JWTs with Auth0 user IDs prefixed as `auth0|5a68dc51cb30df1234567890`.

## API endpoints require dynamic service discovery

Before accessing storage or notifications, hosts must be discovered through the service manager at `service-manager-production-dot-remarkable-production.appspot.com`:

```http
GET /service/json/1/document-storage?environment=production&group=auth0|{user_id}&apiVer=2
```

This returns the storage host, typically `document-storage-production-dot-remarkable-production.appspot.com`. The discovery request is **unauthenticated**—the group parameter has no observed effect.

**Core storage endpoints** on the discovered host:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/document-storage/json/2/docs` | GET | List all documents |
| `/document-storage/json/2/docs?doc={ID}&withBlob=true` | GET | Get item with download URL |
| `/document-storage/json/2/upload/request` | PUT | Request upload URL |
| `/document-storage/json/2/upload/update-status` | PUT | Update metadata post-upload |
| `/document-storage/json/2/delete` | PUT | Delete document/folder |

Documents are stored as ZIP archives on Google Cloud Storage with signed URLs (`BlobURLGet`/`BlobURLPut`) that expire within hours.

## Document metadata follows a specific JSON structure

Each document returns metadata with a notable API quirk—the field `VissibleName` contains an intentional typo:

```json
{
    "ID": "0631045c-e3a9-45a0-8446-abcdef012345",
    "Version": 4,
    "BlobURLGet": "https://storage.googleapis.com/remarkable-production-document-storage/...",
    "BlobURLGetExpires": "2020-12-20T07:07:56.628Z",
    "ModifiedClient": "2020-12-12T22:16:39.539539Z",
    "Type": "DocumentType",
    "VissibleName": "My Notebook",
    "CurrentPage": 0,
    "Bookmarked": false,
    "Parent": "ec53580c-3579-4fe7-a096-012345abcdef"
}
```

**Document types** are `DocumentType` (notebooks, PDFs, EPUBs) and `CollectionType` (folders). Special IDs include empty string `""` for root and `"trash"` for deleted items.

## Real-time sync uses WebSocket notifications

The notifications API provides real-time change events via WebSocket at the discovered notifications host:

```
wss://{notifications-host}/notifications/ws/json/1
Authorization: Bearer {user_token}
```

Events include `DocAdded` (create/update) and `DocDeleted` with metadata including `sourceDeviceID` to filter self-triggered events:

```json
{
  "message": {
    "attributes": {
      "event": "DocAdded",
      "id": "b083f079-c45e-4b1f-81ea-32c36a672142",
      "sourceDeviceDesc": "remarkable",
      "type": "DocumentType",
      "vissibleName": "My Notebook"
    },
    "publishTime": "2020-12-21T10:09:59.016Z"
  }
}
```

## The sync15 protocol migration creates compatibility challenges

ReMarkable has progressively migrated users from the legacy sync protocol (1.0/1.5) to **sync15**, which uses different endpoints at `internal.cloud.remarkable.com/sync/v2/`. This migration has caused significant issues for third-party tools—some users are on legacy protocols while others are forced to sync15.

The **ddvk/rmfakecloud** self-hosted cloud implementation supports all protocol versions and serves as the authoritative reference for sync15 behavior. Key differences include hash-based content addressing using SHA256 and a `.tree` file tracking sync state.

## Binary .rm file format has evolved through multiple versions

Notebook stroke data is stored in `.rm` binary files with little-endian byte order. **Version 6** (firmware 3.0+, 2022) is current:

| Version | Era | Key Features |
|---------|-----|--------------|
| v3/v5 | Pre-2022 | Simple binary, strokes only |
| v6 | 2022+ | Block-based, typed text, CRDT, PDF highlights |

**Legacy format structure** (v3/v5) begins with a 43-byte header `"reMarkable .lines file, version=5"` followed by layer counts, line metadata (brush type, color, base size), and point data (X, Y, speed, direction, width, pressure as float32 values).

Pen types are encoded as integers: **0** (Brush), **2** (Ballpoint), **4** (Fineliner), **5** (Highlighter), **6** (Eraser), **21** (Calligraphy). Display resolution is **1404×1872 pixels** with coordinates mapping directly.

**Version 6** introduces a tagged block structure supporting typed text with CRDT sequences for collaborative editing, bold/italic formatting, and `GlyphRange` for PDF highlight extraction. The **rmscene** Python library at `github.com/ricklupton/rmscene` provides the most complete v6 parser.

## ZIP archive structure mirrors the device filesystem

Cloud-synced documents are ZIP archives containing:
```
├── {UUID}/
│   ├── {page-uuid}-metadata.json
│   └── {page-uuid}.rm
├── {UUID}.content          # Page list, settings JSON
├── {UUID}.metadata         # Document metadata JSON
├── {UUID}.pagedata         # Template names, one per line
├── {UUID}.pdf              # Original PDF if applicable
└── {UUID}.thumbnails/
    └── {page-uuid}.jpg     # 280×374 thumbnails
```

The `.content` file maps page UUIDs to PDF page numbers for annotated documents. PDF annotations are stored as overlay strokes in separate `.rm` files, not embedded in the PDF.

## Production-ready libraries exist across languages

**Recommended for Otso integration** based on maintenance status and feature completeness:

- **erikbrinkman/rmapi-js** (TypeScript) — Active, 56 stars, NPM package, supports registration, CRUD operations, custom EPUB settings. Best choice for JavaScript/TypeScript stacks.

- **rschroll/rmcl** (Python) — Active, async support via trio, automatic token refresh, file-tree abstraction. Use with **rmscene** for v6 format parsing.

- **ddvk/rmfakecloud** (Go) — Active (v0.0.26, Oct 2025), 1000+ stars, supports all sync protocols. Authoritative reference for protocol behavior even if not used directly.

The previously dominant **juruen/rmapi** (Go, ~1000 stars) and **splitbrain/ReMarkableAPI** (PHP, 422 stars) are now archived but contain valuable documentation—splitbrain's wiki remains the most comprehensive API reference.

## Known limitations and best practices

**No official rate limits** are documented, but community tools recommend exponential backoff for 429/503 responses. Google Cloud Platform infrastructure underlies the storage layer.

**Version conflicts** return errors when the supplied version isn't exactly server version +1. Always fetch current version before updates. Token expiration returns 401 with "Token is expired" message—refresh the user token and retry.

**Critical hosts** your connector may need to reach:
- `my.remarkable.com` — Authentication
- `service-manager-production-dot-remarkable-production.appspot.com` — Service discovery  
- `document-storage-production-dot-remarkable-production.appspot.com` — Storage API
- `internal.cloud.remarkable.com` — Sync v2 endpoints
- `*-notifications-production.cloud.remarkable.engineering` — WebSocket notifications

## Conclusion

Building the Otso connector is well-supported by community work. Start with **rmapi-js** or **rmcl** as your base library, implement the two-tier authentication flow with automatic token refresh, and handle both legacy and sync15 protocols for maximum compatibility. The WebSocket notifications API enables efficient real-time sync without polling. For parsing notebook content, use **rmscene** for v6 format or **lines-are-rusty** for legacy formats. The **ddvk/rmfakecloud** codebase serves as the definitive reference when official documentation is lacking.