# Pipeline microbatch host contract

The extracted rank-local cost model and assignment functions are host-independent.
Runtime activation uses `vllm.batch-admission-policy` API 1.1:

1. Core owns the bounded future queue and opaque in-flight batch receipts.
2. Scheduler exposes immutable request-work snapshots; the policy returns only
   a batch ID and eligible request IDs.
3. Scheduler retains Request, RequestQueue, KV cache and SchedulerOutput
   ownership and validates every policy result.
4. Completion and abort receipts close policy lifecycle state; exceptions or
   invalid results disable the policy and restore built-in scheduling.
5. Requestless connector/finished-request maintenance bypasses policy admission
   and continues through the built-in empty step.

The policy rejects PP1, topology/model mismatches, and incomplete calibrated
profiles. Synthetic or balanced profiles may be used for smoke tests only and
must never be reported as measured performance. Historical CSV/PNG artifacts
remain provenance evidence, not current compatibility receipts.
