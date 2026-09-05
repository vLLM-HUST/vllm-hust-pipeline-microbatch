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
    assert manifest.bundle_version == "0.2.0"
    assert manifest.host.version_range == ">=0.28.1rc1.dev319,<0.29"
    assert manifest.protocols[0].name == "vllm.batch-admission-policy"
    assert manifest.components[0].contracts == ("vllm.batch-admission-policy.v1",)
