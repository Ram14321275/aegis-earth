# Cyber Defense Topology

Aegis Earth enforces defense-in-depth across the platform globally.

1. **Zero-Trust Identity**: Every service interaction requires explicit lineage validation. No perimeter implicit trust exists.
2. **Attestation Edge**: Field nodes must periodically present short-lived nonces mixed with cryptographic signatures.
3. **Detection Core**: Scans inbound signals across the WebSocket and REST fabrics (e.g. anomaly detection, nonce reuse).
4. **Containment Periphery**: Quarantines endpoints logically instead of destructive IP bans, allowing instant forensic analysis without service degradation for legitimate users.
