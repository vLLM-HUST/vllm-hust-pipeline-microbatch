# Sage Mate Qwen3.8-27B PP2+TP2 graph qualification

## Locked runtime

- vLLM-HUST base: `762f85b3`, package `0.28.1rc1.dev319`
- vLLM-HUST candidate: `3e57b2f75c`
- vLLM-Ascend-HUST base: `4e57439e`, package `0.25.1rc1`
- required Ascend ABI candidate: `1cf88e9e6`
- Mod: `7115254`
- image: `sha256:934701650b9d1a4b66c95bb92b2b4a9011df40924b96877764392a41ba52b807`
- accelerator/topology: Ascend 910B2 NPU0-3, PP2+TP2
- execution: `FULL_DECODE_ONLY` graph, async scheduling enabled

The original production TP4 cell is Not Applicable to this Mod because PP=1.
The four-device activation test therefore used PP2+TP2 without TP1 or eager
fallback. NPU4-7 were never selected by the test profiles.

## Functional evidence

Graph capture completed on all four ranks. Core logged the external policy as
configured and enabled. After the matched C4 run, Prometheus reported 908
policy calls, 757 admissions, 757 completions, no aborts/failures/invalid
admissions/built-in fallbacks, and enabled=1.

Five deterministic answers matched the disabled-policy baseline hashes (`42`,
`YES`, `SageMate`, `63`, `c`). Stream cancellation followed by a new request
returned `RECOVERED`. C4, C8, mixed-length, graph replay and post-test health
checks completed.

## Matched performance

Both arms use the same final image; the only difference is policy activation.

| workload | metric | disabled | balanced | delta |
| --- | ---: | ---: | ---: | ---: |
| homogeneous C4 | completion tok/s | 69.216 | 62.954 | -9.05% |
| homogeneous C4 | P50 / P95 | 5.797 / 6.088 s | 6.374 / 6.540 s | +9.95% / +7.43% |
| homogeneous C8 | completion tok/s | 123.199 | 117.810 | -4.37% |
| homogeneous C8 | P50 / P95 | 6.848 / 7.147 s | 6.980 / 7.211 s | +1.92% / +0.89% |
| fixed-work mixed C8 | completion tok/s | 132.072 | 97.296 | -26.33% |
| fixed-work mixed C8 | P50 / P95 | 6.118 / 9.613 s | 5.428 / 17.320 s | -11.29% / +80.16% |

## Decision and rollback

Qwen3.8-27B PP2+TP2 is functionally verified but fails the effectiveness gate;
it is not compatible for release. The balanced profile improves mixed P50 by
segregating work but creates severe long-request tail imbalance. Historical
PP4+TP2 coefficients are invalid for this model and topology. Requalification
requires fresh rank-local coefficients and the full matrix above.

Rollback is removal of `--batch-admission-policy` and
`--batch-admission-policy-config`. Runtime policy exceptions or invalid results
also disable the extension and restore the built-in scheduler with metrics.
