"""Put the LAMP repo root on sys.path and chdir there (LAMP resolves paths relative to Config.py)."""
import os
import sys

LAMP_ROOT = os.environ.get("LAMP_ROOT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lamp"))
LAMP_ROOT = os.path.abspath(LAMP_ROOT)


def setup():
    # LAMP's Discretizer imports torch only for an unused GPU helper (get_discretized_pose_tensor).
    # Stub it only while Discretizer is imported, then remove it so scipy/sklearn don't see a fake torch.
    if LAMP_ROOT not in sys.path:
        sys.path.insert(0, LAMP_ROOT)
    os.chdir(LAMP_ROOT)
    try:
        import torch  # noqa
    except ImportError:
        # torch is only used by LAMP's unused *_tensor helpers. The dummy Tensor class keeps
        # scipy's array-API checks (is_torch_array) working against the stub.
        import types
        stub = types.ModuleType("torch")

        class Tensor(object):
            pass

        stub.Tensor = Tensor
        sys.modules["torch"] = stub
    return LAMP_ROOT
