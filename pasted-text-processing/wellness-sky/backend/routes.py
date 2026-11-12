"""Compatibility import for deployments that expect a routes module."""

from .main import app

__all__ = ["app"]
