# Threat Lineage Model

To maintain explainability, the Threat System utilizes a Lineage model.
Each `ThreatDetection` must point to its originating `ThreatSignal`.
When multiple events correlate, they form an unalterable chronological hash chain identical to the governance audit layer.

* Parent Hash Tracking guarantees missing events highlight database tampering.
* Deterministic reasoning hashes allow mathematical reproduction of why a threat was triggered.
