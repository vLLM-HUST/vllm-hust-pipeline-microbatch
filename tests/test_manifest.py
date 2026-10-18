import json
from pathlib import Path

from vllm_hust_ext.manifest import activation_blocker, load_manifest

import vllm_hust_pipeline_microbatch


def test_policy_manifest_declares_current_gated_host_contract() -> None:
    manifest = load_manifest(
        Path(vllm_hust_pipeline_microbatch.__file__).with_name(
            "vllm-hust-extension-v0.2.json"
        )
    )
    assert manifest.bundle_id == "org.vllm-hust.pipeline-microbatch"
    assert activation_blocker(manifest) is None
    assert manifest.bundle_version == "0.2.1.dev1"
    assert manifest.host.version_range == ">=0.31.1.post1.dev19,<0.31.1.post1.dev20"
    assert manifest.protocols[0].name == "vllm.batch-admission-policy"
    assert manifest.components[0].contracts == ("vllm.batch-admission-policy.v1",)

    payload = json.loads(
        Path(vllm_hust_pipeline_microbatch.__file__)
        .with_name("vllm-hust-extension-v0.2.json")
        .read_text(encoding="utf-8")
    )
    qualification = payload["activation"]["additional_config"][
        "_manager_runtime_qualification"
    ]
    assert qualification["pipeline_parallel_size"] == 2
    assert qualification["tensor_parallel_size"] == 1
    assert qualification["host_commit"] == "f7bc2a5eebc505f28abfbf318734225e4c30c64c"
    assert "functional_status" not in qualification
    assert "recovery_status" not in qualification
    assert "status" not in qualification
    assert manifest.host.api_range == "==1.0"
