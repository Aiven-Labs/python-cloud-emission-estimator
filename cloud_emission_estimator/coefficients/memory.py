# Copyright (c) 2023 Aiven, Helsinki, Finland. https://aiven.io/

# Constants used for energy consumption & emission calculations
#
# The values are captured from Cloud Carbon Footprint project:
# https://github.com/cloud-carbon-footprint/cloud-carbon-footprint

from decimal import Decimal


MEMORY_CONSUMPTION_WATTS_PER_GB_HOUR = Decimal("0.392")
