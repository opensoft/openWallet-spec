# Research and decisions

Status: draft

Use the fixed Ed25519 profile disclosed by the parent pilot. RFC 8785 provides explicit canonical serialization rather than Python dict ordering. Canonical unpadded base64url and domain separation prevent ambiguous or cross-protocol signature reuse. Current key metadata is supplied by a trusted resolver, never selected by a client proof.

Opaque signing lets a future accepted custody adapter implement the same narrow operation. The candidate does not validate remote custodian isolation or agent composition.

Primary references: [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html), [Ed25519 API](https://cryptography.io/en/50.0.1/hazmat/primitives/asymmetric/ed25519/), [rfc8785 0.1.4](https://pypi.org/project/rfc8785/0.1.4/).
