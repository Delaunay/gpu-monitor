import gpusmi.plugins
from gpusmi.core import discover_plugins


def test_plugins():
    plugins = discover_plugins(gpusmi.plugins)

    assert len(plugins) == 1
