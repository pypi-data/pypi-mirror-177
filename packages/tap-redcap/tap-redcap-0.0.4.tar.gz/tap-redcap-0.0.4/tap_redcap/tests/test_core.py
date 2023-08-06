"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_standard_tap_tests

from tap_redcap.tap import TapRedCap

SAMPLE_CONFIG = {
    "token": "",
    "content": "record",
    "action": "export",
    "format": "json",
    "type": "eav",
    "forms": ["demographics_form"],
    "events": "",
    "rawOrLabel": "label",
    "rawOrLabelHeaders": "label",
    "exportCheckboxLabel": "true",
    "exportSurveyFields": "true",
    "returnFormat": "json",
    "exportDataAccessGroups": "true",
    "base_url": "https://redcap.chop.edu/api/",
    "api_timeout": 1500
    # TODO: Initialize minimal tap config
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(
        TapRedCap,
        config=SAMPLE_CONFIG
    )
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your tap.
