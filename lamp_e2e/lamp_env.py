"""One place to set up LAMP for a domain: path setup, runtime patches, and (for domains that are not
in LAMP's repo, e.g. robomimic Square / ToolHang) registering a domain config module in memory, so
LAMP's own `Config.declare_config` can import it without any file being added to the LAMP repo."""
import os
import sys
import types

from _lamp_path import setup

ROBOT = {"Packing": "MagneticGripper", "Square": "Panda", "ToolHang": "Panda"}


def _register_extra_domain(domain):
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.join(here, "robomimic") not in sys.path:
        sys.path.insert(0, os.path.join(here, "robomimic"))
    import domains  # lamp_e2e/robomimic/domains.py
    if domain not in domains.CONFIGS:
        return False
    mod = types.ModuleType("domain_configs.{}Config".format(domain))
    for k, v in domains.CONFIGS[domain]().items():
        setattr(mod, k, v)
    import domain_configs  # LAMP's package, so the submodule import resolves
    sys.modules[mod.__name__] = mod
    setattr(domain_configs, "{}Config".format(domain), mod)
    return True


def domain_from_argv(default="Packing"):
    """Read --domain from the command line before anything else is imported (LAMP's Config is global)."""
    if "--domain" in sys.argv:
        return sys.argv[sys.argv.index("--domain") + 1]
    return default


def out_dir(domain):
    here = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(here, "out") if domain == "Packing" else os.path.join(here, "out", domain)
    os.makedirs(d, exist_ok=True)
    return d


def declare(domain):
    setup()
    _register_extra_domain(domain)
    from Config import Config
    Config.declare_config(domain, ROBOT.get(domain))
    import py3_patches
    py3_patches.apply()
    return Config
