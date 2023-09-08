# Copyright (c) 2023 Aiven, Helsinki, Finland. https://aiven.io/

# Constants used for energy consumption & emission calculations
#
# The values are captured from Cloud Carbon Footprint project:
# https://github.com/cloud-carbon-footprint/cloud-carbon-footprint

from decimal import Decimal


# Default CPU utilization
CPU_DEFAULT_UTILIZATION_PCT = Decimal("50")

# CPU power consumption, min/max watts per running hour
CPU_CONSUMPTION_MIN_WATTS = {
    "ARM_NEOVERSE_N1": Decimal("1.06"),

    "AMD_EPYC_1ST_GEN": Decimal("0.85"),
    "AMD_EPYC_2ND_GEN": Decimal("0.47"),
    "AMD_EPYC_3RD_GEN": Decimal("0.43"),

    "INTEL_SANDY_BRIDGE": Decimal("2.18"),
    "INTEL_IVY_BRIDGE": Decimal("1.71"),
    "INTEL_HASWELL": Decimal("1.86"),
    "INTEL_BROADWELL": Decimal("0.71"),
    "INTEL_SKYLAKE": Decimal("0.55"),
    "INTEL_CASCADE_LAKE": Decimal("0.69"),
    "INTEL_ICE_LAKE": Decimal("0.77"),

    "INTEL_BROADWELL_CLIENT": Decimal("0.71"),
    "INTEL_SKYLAKE_CLIENT": Decimal("1.82"),

    "default": Decimal("0.74"),
}

CPU_CONSUMPTION_MAX_WATTS = {
    "ARM_NEOVERSE_N1": Decimal("1.94"),

    "AMD_EPYC_1ST_GEN": Decimal("2.6"),
    "AMD_EPYC_2ND_GEN": Decimal("1.69"),
    "AMD_EPYC_3RD_GEN": Decimal("1.95"),

    "INTEL_SANDY_BRIDGE": Decimal("8.61"),
    "INTEL_IVY_BRIDGE": Decimal("5.56"),
    "INTEL_HASWELL": Decimal("5.6"),
    "INTEL_BROADWELL": Decimal("3.69"),
    "INTEL_SKYLAKE": Decimal("4.01"),
    "INTEL_CASCADE_LAKE": Decimal("4.06"),
    "INTEL_ICE_LAKE": Decimal("3.97"),

    "INTEL_BROADWELL_CLIENT": Decimal("3.69"),
    "INTEL_SKYLAKE_CLIENT": Decimal("5.86"),

    "default": Decimal("3.5"),
}
