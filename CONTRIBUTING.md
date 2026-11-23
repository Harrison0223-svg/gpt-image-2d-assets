# Contributing

Keep each topic branch focused. Include a reproducible synthetic fixture, expected and actual results, and exact test commands. Do not include private data, secrets, or unlicensed assets. Add a regression test for changes in behavior. Disclose material AI assistance and review the diff yourself before submitting.

## Offline checks

With Python and Pillow installed, run from the repository root:

    python gpt-image-2d-assets/scripts/test_asset_tools.py
    python gpt-image-2d-assets/scripts/test_motion_review.py

Preserve source pixel data. Automated checks complement visual review; they do not certify animation quality.
