# Copyright (c) 2023 Aiven, Helsinki, Finland. https://aiven.io/

# Constants used for energy consumption & emission calculations
#
# The values are captured from Cloud Carbon Footprint project:
# https://github.com/cloud-carbon-footprint/cloud-carbon-footprint

from decimal import Decimal


VOLUME_CONSUMPTION_WATTS_PER_GB_SSD_DEFAULT = Decimal("0.000392")

VOLUME_CONSUMPTION_WATTS_PER_GB = {
    "aws": {
        "ssd": {
            "default": VOLUME_CONSUMPTION_WATTS_PER_GB_SSD_DEFAULT * 2,  # Replication factor 2
        },
    },
    "gcp": {
        "ssd": {
            "default": VOLUME_CONSUMPTION_WATTS_PER_GB_SSD_DEFAULT * 2,  # Replication factor 2
        }
    },
    "default": {
        "ssd": {
            "default": VOLUME_CONSUMPTION_WATTS_PER_GB_SSD_DEFAULT,
        }
    }
}
