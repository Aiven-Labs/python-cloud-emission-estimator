# Copyright (c) 2023 Aiven, Helsinki, Finland. https://aiven.io/

# Constants used for energy consumption & emission calculations
#
# The values are captured from Cloud Carbon Footprint project:
# https://github.com/cloud-carbon-footprint/cloud-carbon-footprint

from decimal import Decimal


POWER_USAGE_EFFECTIVINESS = {
    "aws": {
        "default": Decimal("1.135"),
    },

    "google": {
        "asia-east1": Decimal("1.12"),
        "asia-southeast1": Decimal("1.13"),
        "australia-southeast1": Decimal("1.10"),
        "europe-north1": Decimal("1.09"),
        "europe-west1": Decimal("1.09"),
        "europe-west4": Decimal("1.07"),
        "us-central1": Decimal("1.11"),
        "us-central2": Decimal("1.11"),
        "us-east4": Decimal("1.08"),
        "default": Decimal("1.1"),  # PUE fleet wide average
    },

    "default": {
        "default": Decimal("1.58"),
    },
}
