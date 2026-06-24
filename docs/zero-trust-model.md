# Zero Trust Model

The Zero Trust architecture in Aegis Earth relies heavily on **Replay Protection** and **Cryptographic Identity**.

## Monotonic Continuity
We track request counters persistently per internal identity. 

## Nonce Tracking
We hold ephemeral cache tables locking nonce values. A nonce presented twice immediately signals an attack and triggers containment.

## Sovereign Boundaries
Even authenticated traffic is audited for sovereign boundary drift (e.g. US-only keys communicating with EU datacenters triggers immediate alerts).
