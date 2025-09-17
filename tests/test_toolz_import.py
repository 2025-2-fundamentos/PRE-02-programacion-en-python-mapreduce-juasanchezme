"""Smoke test to verify toolz is installed and importable.

This ensures the environment is set up correctly and that IDE warnings like
"Import 'toolz.itertoolz' could not be resolved" no longer apply when using
the project's virtual environment.
"""


def test_toolz_import_resolves():
    import toolz  # noqa: F401  # ensure top-level package import works
    from toolz.itertoolz import concat, pluck

    # Basic sanity checks that the imported symbols are callables
    assert callable(concat)
    assert callable(pluck)
