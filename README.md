# Pipeline Microbatch Scheduling for vLLM-HUST

Owner-led research carrier for calibrated pipeline-parallel microbatch scheduling. The work crosses scheduler, executor, communication, KV, worker, and benchmark boundaries and requires neutral host contracts.

**Status: rank-local cost prediction and deterministic microbatch assignment are installable and tested; vLLM scheduler/worker attachment remains blocked until `HOST_CONTRACT.md` is implemented.**

Technical ownership belongs to @xsun2001. Source extraction must preserve exact authorship, license, tests, constraints, and evidence before activation is considered.

See [MAINTAINERS.md](MAINTAINERS.md) and [PROVENANCE.md](PROVENANCE.md).

## Extension framework

Extension ID: `org.vllm-hust.pipeline-microbatch`

This repository follows the vLLM-HUST Extension Template. The current package
is deliberately `import_only`: it can be built, installed, discovered, and
inspected, but Extension Manager must refuse enablement until the maintainers
land a real host contract, implementation, compatibility evidence, and tests.

```bash
python -m pip install "vllm-hust-ext @ git+https://github.com/vLLM-HUST/extension-manager.git@main"
python -m pip install -e ".[test]"
vllm-hust-ext extension inspect org.vllm-hust.pipeline-microbatch
vllm-hust-ext extension check org.vllm-hust.pipeline-microbatch
pytest -q
```

The static Manifest 0.2 descriptor lives inside the Python distribution under
`src/`. Installation alone changes no vLLM behavior.
