# Copyright (c) 2023 Aiven, Helsinki, Finland. https://aiven.io/
import re


def guess_cpu_type_by_instance_type_aws(*, instance_type: str) -> str | None:
    guess = None
    parts = instance_type.split(".", 1)
    family = parts[0]
    if family in {"t3"}:
        guess = "INTEL_SKYLAKE"
    elif family in {"m6i", "c6id"}:
        guess = "INTEL_ICE_LAKE"
    elif family in {"c5a", "c5ad", "m5a", "m5ad", "r5a"}:
        guess = "AMD_EPYC_2ND_GEN"
    elif family == "i3":
        guess = "INTEL_BROADWELL"
    elif family in {"t4g", "m6g", "r6g"}:
        guess = "ARM_NEOVERSE_N1"
    elif family == "m6a":
        guess = "AMD_EPYC_3RD_GEN"
    elif family in {"c5", "m5", "m5zn"}:
        guess = "INTEL_CASCADE_LAKE"
    return guess


def guess_cpu_type_by_instance_type_gcp(*, instance_type: str) -> str | None:
    guess = None
    custom_match = re.match("^([a-z0-9]+)?-?custom-([0-9]+)-([0-9]+)$", instance_type)
    if custom_match is not None:
        matches = custom_match.groups()
        family = matches[0] or "n1"
    else:
        parts = instance_type.split("-")
        family = parts[0]

    if family in {"e2", "n1"}:
        guess = "INTEL_HASWELL"
    elif family == "n2":
        guess = "INTEL_SKYLAKE"
    elif family == "n2d":
        guess = "AMD_EPYC_2ND_GEN"

    return guess


def guess_cpu_type_by_instance_type(*, provider: str, instance_type: str) -> str | None:
    guess = None
    if provider == "aws":
        guess = guess_cpu_type_by_instance_type_aws(instance_type=instance_type)
    elif provider == "gcp":
        guess = guess_cpu_type_by_instance_type_gcp(instance_type=instance_type)
    return guess
