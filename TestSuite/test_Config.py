from MyConfig.Config_base import Configuration
from datetime import datetime
import os
import tempfile
import pytest

# CREATE THE CONFIGURATION FILE
configuration = Configuration().configuration


@pytest.mark.parametrize("test_input, expected", [
    ('LOG_FILE', "AutoML_(?Timestamp).log"),
])
def test_logger(test_input, expected):
    timer = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file = expected.replace('(?Timestamp)', timer)

    full_log = os.path.join(
        tempfile.gettempdir(),
        "AutoML",
        log_file

    )

    assert configuration[test_input] == full_log


@pytest.mark.parametrize("test_input, expected", [
    ('cc', "sugaanth.mohan@gmail.com"),
    ('from', "AutoMLNotifier@gmail.com"),
    ('host', "localhost"),
    ('subject_prefix', "AutoML - (?Status) | (?Subject)"),
    ('to', "sugaanth.mohan@gmail.com"),
])
def test_email_notifier(test_input, expected):
    assert configuration['EMAIL_NOTIFIER'][test_input] == expected


@pytest.mark.parametrize("test_input, expected", [
    ('generations', 3),
    ('n_jobs', -1),
    ('population_size', 20),
    ('scoring', 'r2'),
    ('use_dask', True),
    ('verbosity', 2),
    ('warm_start', False),
])
def test_automl_base_configuration(test_input, expected):
    assert configuration['AUTOML_CONFIGURATIONS'][test_input] == expected
