"""
Factory module for creating provider objects.
"""
import importlib
from .providers import providers_path


def get_provider(provider_name: str):
    """
    Get provider object.

    Parameters:
        provider_name (str): Name of the provider.

    Returns:
        Provider object.
    """
    if provider_name not in providers_path:
        return ValueError(message="Invalid provider name.")

    module = importlib.import_module(providers_path[provider_name][0])
    provider = getattr(module, providers_path[provider_name][1])

    return provider
