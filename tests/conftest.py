"""Use a deterministic Qt platform for tests with simulated screen objects."""
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
