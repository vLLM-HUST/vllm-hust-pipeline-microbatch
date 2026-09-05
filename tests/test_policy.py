from dataclasses import dataclass
from types import SimpleNamespace

import pytest

from vllm_hust_pipeline_microbatch.policy import (
    PipelineMicrobatchConfig,
    PipelineMicrobatchPolicy,
)


@dataclass(frozen=True)
class FakeRequest:
    request_id: str
    context_length: int


@dataclass(frozen=True)
class FakeContext:
    requests: tuple[FakeRequest, ...]
    in_flight_batch_ids: frozenset[str]


def _vllm_config(
    *,
    pp: int = 2,
    tp: int = 2,
    model: str = "Qwen/Qwen3.8-27B",
    profile: dict | None = None,
):
    if profile is None:
        profile = {
            "mode": "balanced",
            "model_ids": ["Qwen/Qwen3.8-27B"],
            "pipeline_parallel_size": 2,
            "tensor_parallel_size": 2,
            "microbatch_count": 2,
        }
    return SimpleNamespace(
        additional_config={"pipeline_microbatch": profile},
        parallel_config=SimpleNamespace(
            pipeline_parallel_size=pp, tensor_parallel_size=tp
        ),
        model_config=SimpleNamespace(model=model),
        max_concurrent_batches=pp,
    )


def test_configuration_rejects_tp4_and_profile_mismatch() -> None:
    with pytest.raises(ValueError, match="pipeline_parallel_size > 1"):
        PipelineMicrobatchConfig.from_vllm_config(_vllm_config(pp=1, tp=4))

    with pytest.raises(ValueError, match="topology mismatch"):
        PipelineMicrobatchConfig.from_vllm_config(_vllm_config(pp=2, tp=1))

    with pytest.raises(ValueError, match="does not cover model"):
        PipelineMicrobatchConfig.from_vllm_config(_vllm_config(model="other/model"))


def test_balanced_policy_assigns_and_rotates_batches() -> None:
    policy = PipelineMicrobatchPolicy.from_vllm_config(_vllm_config())
    requests = (
        FakeRequest("r0", 10),
        FakeRequest("r1", 20),
        FakeRequest("r2", 30),
    )

    first = policy.admit_batch(FakeContext(requests, frozenset()))
    assert first is not None
    assert first.batch_id == "pipeline-microbatch-0"
    assert first.request_ids == ("r0", "r2")

    second = policy.admit_batch(FakeContext(requests, frozenset({first.batch_id})))
    assert second is not None
    assert second.batch_id == "pipeline-microbatch-1"
    assert second.request_ids == ("r1",)


def test_policy_reclaims_cancelled_requests_and_recovers() -> None:
    policy = PipelineMicrobatchPolicy.from_vllm_config(_vllm_config())
    requests = (FakeRequest("r0", 10), FakeRequest("r1", 20))
    first = policy.admit_batch(FakeContext(requests, frozenset()))
    assert first is not None
    policy.on_batch_complete(first.batch_id)
    policy.on_batch_abort(first.batch_id)

    remaining = (FakeRequest("r1", 21),)
    recovered = policy.admit_batch(FakeContext(remaining, frozenset()))
    assert recovered is not None
    assert recovered.request_ids == ("r1",)
    assert policy.export_stats()["cancellations_reclaimed"] == 1
    assert policy.export_stats()["aborts"] == 1


def test_calibrated_mode_requires_every_pipeline_rank() -> None:
    profile = {
        "mode": "calibrated",
        "model_ids": ["Qwen/Qwen3.8-27B"],
        "pipeline_parallel_size": 2,
        "tensor_parallel_size": 2,
        "microbatch_count": 2,
        "cost_models": [
            {
                "p0": 0,
                "p1": 1,
                "p2": 0,
                "p3": 1,
                "p4": 0,
                "p5": 0,
                "pp_rank": 0,
                "layer_num": 24,
            }
        ],
    }
    with pytest.raises(ValueError, match="every PP rank"):
        PipelineMicrobatchConfig.from_vllm_config(_vllm_config(profile=profile))
