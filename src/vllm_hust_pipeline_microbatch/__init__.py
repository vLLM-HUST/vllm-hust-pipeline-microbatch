"""Pipeline microbatch cost/planning contracts and inert runtime metadata."""

from .planner import (
    MicroBatchCostModel,
    MicroBatchSnapshot,
    RequestWork,
    assign_lowest_cost,
    balanced_assignment,
    worst_rank_cost,
)


class VllmHustPipelineMicrobatchContractProposal:
    """Metadata-only proposal; this class performs no runtime activation."""


__all__ = [
    "MicroBatchCostModel",
    "MicroBatchSnapshot",
    "RequestWork",
    "VllmHustPipelineMicrobatchContractProposal",
    "assign_lowest_cost",
    "balanced_assignment",
    "worst_rank_cost",
]
