# RelayDiscipline

## Product
A reliability layer for human and AI-agent handoffs. Teams define relay protocols; operators submit handoff packets; GenLayer validators decide whether the packet is complete, safe to accept, and correctly routed.

## Why GenLayer
Handoff quality is semantic: a packet may contain all required fields yet omit the actual risk, hidden dependency, or recovery context. GenLayer validators judge meaning and operational sufficiency without a centralized supervisor.

## Intelligent Contract
- Entities: relay networks, protocols, packets, recipients, acceptance decisions.
- Core write: `inspect_handoff(packet_id)`.
- Consensus output: READY, READY_WITH_ACK, REROUTE, INCOMPLETE, REJECT; missing obligations; risk level; recommended recipient class.
- Deterministic rules: sender ownership, protocol version pinning, packet immutability, bounded dependencies, expiry, pagination.
- Validation: exact decision agreement plus overlap on missing-obligation codes.

## Frontend
- Composition: horizontal relay topology with packets physically moving between stations; expandable protocol oscilloscope below.
- Palette: graphite, phosphor green, warning yellow, pale cyan.
- Type: square technical sans with narrow mono annotations.
- Motion: packet transfer, relay switching, line energizing, checksum flicker.
- Skeleton: empty topology nodes connect sequentially, then packet metadata resolves.
- Empty state: disconnected stations waiting for the first protocol.
- Transaction progress: a packet travels through wallet, ingress, validator junction, and destination.

## Non-overlap
No incident timeline, proposal board, document archive, or card lanes. The defining interaction is spatial packet routing across a live topology.
