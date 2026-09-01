# Pipeline microbatch host contract proposal

The extracted rank-local cost model and assignment functions are host-independent.
Runtime activation requires:

1. `vllm.pipeline.batch-queue.v1`: explicit ownership of a bounded microbatch
   queue without adding fields directly to core scheduler output classes;
2. `vllm.scheduler.request-work.v1`: immutable request/context snapshots;
3. `vllm.pipeline.in-flight.v1`: rank-safe in-flight IDs and completion receipts;
4. `vllm.pipeline.profile.v1`: default-off timestamps with rank-specific output
   paths and an evidence label.

The provider must reject asynchronous scheduling and unsupported connectors or
parallel modes. Synthetic cost models may be used only for smoke tests and must
never be reported as measured performance. Historical CSV/PNG artifacts remain
provenance evidence, not current compatibility receipts.
