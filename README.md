# Relay Discipline

### Semantic Handoff Protocol / `RD-PRIMARY`

Systems rarely fail because nobody sent the handoff. They fail because the packet looked complete while the dangerous dependency stayed implicit.

Relay Discipline turns custody transfer into a visible network route. A packet leaves its origin, crosses ingress, pauses at a five-validator junction, and reaches its destination only with a decision that the receiving operator can inspect.

**Enter the live relay:** https://relay-discipline.pages.dev

```text
◇ ORIGIN ═════ ◇ INGRESS ═════ ◇ JUNCTION ═════ ◇ DESTINATION
  intent         checksum       5 validators      custody
```

## Packet anatomy

A relay packet is not a message blob. It is a pinned protocol instance containing independently fetched evidence and a recipient attestation:

```json
{
  "protocol": "ops-handoff-v1",
  "recipient_class": "PAYMENTS",
  "objective": "What responsibility is moving?",
  "risks": ["What can break after transfer?"],
  "dependencies": ["What must remain available?"],
  "recovery": "How is custody safely reversed?",
  "evidence_urls": ["Public, independently checkable operational record"],
  "recipient_attestation_url": "Public recipient acceptance record"
}
```

Once sealed, the packet cannot be edited into a safer-looking version.

## Junction decision codes

| Gate | Meaning |
|---|---|
| `READY` | Complete, correctly routed, and safe to transfer |
| `READY_WITH_ACK` | Transfer is viable but the destination must acknowledge a condition |
| `REROUTE` | Packet belongs to another recipient class |
| `INCOMPLETE` | A required operational obligation is missing |
| `REJECT` | The proposed transfer is unsafe or invalid |

Consensus judges every outcome-driving field: protocol obligations, recipient class, objective, risks, dependencies, recovery, independently fetched evidence snapshots, and recipient attestation. The contract downgrades `READY` when obligations are missing, routing disagrees, or high-risk recovery is absent.

Bradbury workflow verification: packet submission `0xe7d92647ff2947ed577ed41f59f96dbac861fa53c51c3c990449bc3173d7cff9`; validator inspection `0x004e023ca89dde21b73275f82559a877402b4c82184c43aacaf77b78a41012eb`.

## Deployed route

**Bradbury Testnet · Chain `4221`**

```text
Contract   0x1d50D59fc9a795632De38B4Fa4C9633E9EC07A1D
Protocol   ops-handoff-v1
Deployer   0xCAFA30BF94D4fb01146588a1b7901BD85E7DbD0f
Live App   https://relay-discipline.pages.dev
Explorer   https://explorer-bradbury.genlayer.com/
```

The deployment script creates the contract and initializes the operational protocol as two sequential on-chain transactions.

## Use the relay

```bash
cd frontend
npm install
npm run dev -- -p 3102
```

Open `http://localhost:3102`, connect a wallet, and follow the route:

1. **Build handoff** — review the custody manifest.
2. **Seal packet on-chain** — one wallet approval creates the immutable packet.
3. **Request validator inspection** — a second deliberate approval starts consensus.
4. **Read the junction decision** — gate, missing obligations, risk, route, and rationale appear in the decision rail.

The two transactions are intentionally separate. A network error never causes an automatic resubmission, and a pending packet is stored under a contract-specific recovery key so switching deployments cannot duplicate it.

## Protocol surface

| Read path | Write path |
|---|---|
| `get_protocol` | `create_protocol` |
| `get_packet` | `submit_packet` |
| `get_decision` | `inspect_handoff` |
| `get_packets_page` | — |
| `get_summary` | — |

## Adversarial checks

The test suite is designed around unsafe handoffs, not only the happy path:

- incomplete obligations cannot pass as ready;
- a recipient mismatch forces rerouting;
- the same packet cannot be inspected twice;
- packet pagination and proof formatting remain stable;
- protocol and packet identifiers cannot be duplicated.

Run it with:

```bash
python -m pytest -q
```

Build the production topology with:

```bash
cd frontend && npm run build
```

## Components

```text
contracts/contract.py     protocol registry + semantic junction
scripts/deploy.py         deploy + protocol seed
tests/direct/             adversarial relay scenarios
frontend/app/page.tsx     animated routing surface
frontend/lib/chain.ts     Bradbury wallet transport
```

Relay Discipline is a protocol instrument, not a ticket board. Its central object is the transfer packet, its central moment is the validator junction, and its success condition is accountable custody.
