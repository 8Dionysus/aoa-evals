# Config Route

`config/` is the root compatibility route card for historical config paths.

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for root config path routing |
| entry | open when an old root config path appears or a repo-wide config payload is proposed |
| input | config payload, seed input, registry input, or old root config reference |
| output | owning mechanic part route or documented repo-wide config decision |
| owner | `config/AGENTS.md` for route law; owning mechanic or bundle for payload meaning |
| next route | Agon part config, boundary-bridge sibling canary config, or `docs/architecture/PROOF_TOPOLOGY.md` for a new repo-wide class |
| validation | `config/AGENTS.md` and the owning mechanic route card |

Active root config payloads route to the operation that owns them:

- Agon seed and registry inputs live under `mechanics/agon/parts/*/config/`.
- Boundary-bridge sibling canary config lives under
  `mechanics/boundary-bridge/parts/latest-sibling-canary/config/`.

Future repo-wide config may be introduced only when `docs/architecture/PROOF_TOPOLOGY.md`
and the relevant decision record explain why no narrower mechanic, bundle, or
generated-reader route owns it.
