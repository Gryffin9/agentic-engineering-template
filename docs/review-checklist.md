# Review Checklist

Use this checklist before accepting an agent-produced change.

- The diff matches the task contract.
- For the executable example, the supplied changed-file manifest covers the real diff and the contract's allowlist was reviewed independently.
- No unrelated refactors or formatting churn are included.
- Public APIs, schemas, and configuration changes are intentional.
- Validation commands were run and reported.
- Tests cover the new or changed behavior where practical.
- Documentation was updated if behavior changed.
- No secrets, private data, prompts, or proprietary details were added.
- Error handling and failure modes are understandable.
- The human reviewer can explain the change after reading it.
- A passing automated gate has not been mistaken for human approval or merge authorization.
