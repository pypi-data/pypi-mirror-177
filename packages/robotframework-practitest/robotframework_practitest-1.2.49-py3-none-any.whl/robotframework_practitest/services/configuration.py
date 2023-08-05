WAIT_FOR_TEST_CREATED = 300


class VariableItem:
    def __init__(self, name, mandatory=True, default=None):
        self.Name = name
        self.Default = default
        self.Mandatory = mandatory

    @property
    def as_tuple(self):
        return self.Name, self.Mandatory, self.Default


PRACTI_TEST_VARIABLES = [
    VariableItem('PT_ENABLED', False, False),
    VariableItem('PT_DEBUG', False, False),
    VariableItem('PT_PROJECT_NAME'),
    VariableItem('PT_USER_NAME'),
    VariableItem('PT_USER_NAME_EMAIL'),
    VariableItem('PT_USER_TOKEN'),
    VariableItem('PT_ENDPOINT', False),
    VariableItem('PT_TEST_SET_LEVEL', False, 0),
    VariableItem('PT_TEST_NAME_LEVEL', False, 1),
    VariableItem('PT_EXTERNAL_RUN_ID', False),
    VariableItem('TAG_MAPPING'),
    VariableItem('PT_TEST_FIELDS'),
    VariableItem('PT_TEST_SET_FIELDS'),
    VariableItem('PT_RETENTION_TIMEOUT', False, 300),
    VariableItem('PT_LOG_TO_FILE', False, True),
    VariableItem('PT_LOG_TO_STDOUT', False, False),
]


def get_default_value(name):
    for var in [v for v in PRACTI_TEST_VARIABLES if v.Name == name]:
        return var.Default
    raise AttributeError(f"Variable '{name}' is unknown")
