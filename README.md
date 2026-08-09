# Relay Discipline

Relay Discipline is a semantic custody-handoff network for human teams and autonomous agents. Operators seal a transfer packet containing its objective, destination, known risks, dependencies, recovery procedure, and supporting evidence. GenLayer validators decide whether custody can move safely or whether the packet needs acknowledgement, rerouting, completion, or rejection.

## Why GenLayer

A handoff can contain every required field and still hide the dependency that makes it unsafe. Relay Discipline combines semantic validator review with deterministic enforcement. Consensus interprets operational meaning; the contract enforces immutable packets, protocol pinning, sender ownership, required obligations, recipient consistency, and safe decision backstops.

## Transfer path

```text
Origin → Ingress → Validator Junction → Destination
```

1. Connect a wallet on GenLayer Bradbury Testnet.
2. Build and seal one handoff packet on-chain.
3. Start validator inspection with a separate explicit action.
4. Receive `READY`, `READY_WITH_ACK`, `REROUTE`, `INCOMPLETE`, or `REJECT`.
5. Review missing obligations, risk, recommended destination, confidence, and rationale.

## Contract

- Network: GenLayer Bradbury Testnet (`4221`)
- Address: `0xB8a401d77631EC7A2182D5cAb06d03dc649fB7D7`
- Seeded protocol: `ops-handoff-v1`
- Core methods: `create_protocol`, `submit_packet`, `inspect_handoff`, `get_protocol`, `get_packet`, `get_decision`, `get_packets_page`, `get_summary`
- Explorer: https://explorer-bradbury.genlayer.com/

The deployed protocol requires a clear objective, known risks, recovery path, and bounded dependencies. A validator result cannot remain `READY` when required obligations are missing, the recommended recipient conflicts with the packet, or high-risk recovery context is absent.

## Run locally

```bash
cd frontend
npm install
npm run dev -- -p 3102
```

Open http://localhost:3102 and connect Rabby or MetaMask. The interface switches to Bradbury automatically and keeps pending packet recovery scoped to the deployed contract.

## Tests

```bash
python -m pytest -q
cd frontend
npm run build
```

The suite covers the full relay lifecycle, pagination, proof format, duplicate inspection, missing-obligation enforcement, and recipient mismatch rerouting.

## Structure

```text
contracts/   Intelligent Contract and deterministic backstops
frontend/    Next.js topology interface
scripts/     Deployment and protocol initialization
tests/       Lifecycle and adversarial contract tests
```

## Transaction discipline

Sealing and inspection are intentionally separate wallet actions. The frontend never auto-resubmits a write, prevents duplicate clicks while consensus is active, and resumes a pending packet without creating a second transaction.

