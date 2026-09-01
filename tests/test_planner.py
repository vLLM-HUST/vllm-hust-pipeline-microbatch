from vllm_hust_pipeline_microbatch import (
    MicroBatchCostModel,
    MicroBatchSnapshot,
    RequestWork,
    assign_lowest_cost,
    balanced_assignment,
    worst_rank_cost,
)


def _model(rank: int, context_cost: float) -> MicroBatchCostModel:
    return MicroBatchCostModel(0, 1, 0, context_cost, 0, 0, rank, 8)


def test_cost_uses_slowest_pipeline_rank() -> None:
    batch = MicroBatchSnapshot(0, (RequestWork("a", 10),))
    assert worst_rank_cost(batch, (_model(0, 1), _model(1, 2))) == 21


def test_lowest_cost_assignment_is_deterministic() -> None:
    batches = (
        MicroBatchSnapshot(0, (RequestWork("a", 10),)),
        MicroBatchSnapshot(1),
    )
    assigned = assign_lowest_cost(RequestWork("b", 4), batches, (_model(0, 1),))
    assert assigned[1].requests[0].request_id == "b"


def test_balanced_assignment_differs_by_at_most_one() -> None:
    requests = tuple(RequestWork(str(index), 1) for index in range(7))
    batches = balanced_assignment(requests, 3)
    sizes = [batch.request_num for batch in batches]
    assert sizes == [3, 2, 2]
