# Copyright (c) 2023 Aiven, Helsinki, Finland. https://aiven.io/

# Estimate cloud based emissions based on a collected set of utilization records
#
# This tool is derives from Cloud Carbon Footpring, https://github.com/cloud-carbon-footprint/cloud-carbon-footprint/

from cloud_emission_estimator.coefficients.cpu import CPU_CONSUMPTION_MIN_WATTS, CPU_CONSUMPTION_MAX_WATTS, CPU_DEFAULT_UTILIZATION_PCT
from cloud_emission_estimator.coefficients.memory import MEMORY_CONSUMPTION_WATTS_PER_GB
from cloud_emission_estimator.coefficients.pue import POWER_USAGE_EFFECTIVINESS
from cloud_emission_estimator.coefficients.volume import VOLUME_CONSUMPTION_WATTS_PER_GB
from cloud_emission_estimator.coefficients.gci import CARBON_INTENSITY_GRAMS_PER_KWH
from cloud_emission_estimator.helpers import guess_cpu_type_by_instance_type
from decimal import Decimal
from functools import cache
from typing import Any, Dict, List

import logging


class EmissionEstimator:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)

    @cache
    def lookup_pue_by_provider_and_region(self, *, provider: str, region: str) -> Decimal:
        pue = POWER_USAGE_EFFECTIVINESS["default"]["default"]

        if provider in POWER_USAGE_EFFECTIVINESS:
            if region and region in POWER_USAGE_EFFECTIVINESS[provider]:
                pue = POWER_USAGE_EFFECTIVINESS[provider][region]
            elif "default" in POWER_USAGE_EFFECTIVINESS[provider]:
                pue = POWER_USAGE_EFFECTIVINESS[provider]["default"]
        elif provider:
            self.log.warning("No PUE information found for provider %r", provider)

        return pue

    @cache
    def lookup_volume_consumption_by_provider_region_and_type(self, *, provider: str, region: str, volume_type: str = "ssd") -> Decimal:
        per_gb_consumption = VOLUME_CONSUMPTION_WATTS_PER_GB["default"][volume_type]["default"]

        if provider in VOLUME_CONSUMPTION_WATTS_PER_GB:
            if region and region in VOLUME_CONSUMPTION_WATTS_PER_GB[provider][volume_type]:
                per_gb_consumption = VOLUME_CONSUMPTION_WATTS_PER_GB[provider][volume_type][region]
            elif "default" in VOLUME_CONSUMPTION_WATTS_PER_GB[provider][volume_type]:
                per_gb_consumption = VOLUME_CONSUMPTION_WATTS_PER_GB[provider][volume_type]["default"]
        elif provider:
            self.log.warning("No volume consumption factors found for provider %r", provider)

        return per_gb_consumption

    def lookup_pue(self, *, utilization_record: Dict[str, Any]) -> Decimal:
        provider = utilization_record.get("provider")
        region = utilization_record.get("region")

        return self.lookup_pue_by_provider_and_region(provider=provider, region=region)

    @cache
    def lookup_gci_by_provider_and_region(self, *, provider: str, region: str) -> Decimal:
        grams_per_kwh = CARBON_INTENSITY_GRAMS_PER_KWH["default"]["default"]

        if provider in CARBON_INTENSITY_GRAMS_PER_KWH:
            if region and region in CARBON_INTENSITY_GRAMS_PER_KWH[provider]:
                grams_per_kwh = CARBON_INTENSITY_GRAMS_PER_KWH[provider][region]
            elif "default" in CARBON_INTENSITY_GRAMS_PER_KWH[provider]:
                grams_per_kwh = CARBON_INTENSITY_GRAMS_PER_KWH[provider]["default"]
        elif provider:
            self.log.warning("No carbon intensity figures found for provider %r", provider)

        return grams_per_kwh

    def lookup_gci(self, *, utilization_record: Dict[str, Any]) -> Decimal | None:
        provider = utilization_record.get("provider")
        region = utilization_record.get("region")

        if provider:
            return self.lookup_gci_by_provider_and_region(provider=provider, region=region)
        else:
            return None

    def estimate_energy_consumption_cpu(self, *, utilization_record: Dict[str, Any]) -> Decimal:
        # Energy consumption estimate for CPU consumption
        # Result in Watt-hours
        #
        # Calculated as:
        #  scaled watts based on cpu utilization *
        #  number of cpus *
        #  running hours *
        #  power usage effeciviness

        min_watts = CPU_CONSUMPTION_MIN_WATTS["default"]
        max_watts = CPU_CONSUMPTION_MAX_WATTS["default"]

        cpu_type = utilization_record.get("cpu_type")
        if not cpu_type:
            instance_type = utilization_record.get("instance_type")
            provider = utilization_record.get("provider")
            if provider and instance_type:
                cpu_type = guess_cpu_type_by_instance_type(provider=provider, instance_type=instance_type)

        if cpu_type:
            min_watts = CPU_CONSUMPTION_MIN_WATTS.get(cpu_type, min_watts)
            max_watts = CPU_CONSUMPTION_MAX_WATTS.get(cpu_type, max_watts)

        cpu_utilization = Decimal(utilization_record.get("cpu_utilization_pct", CPU_DEFAULT_UTILIZATION_PCT))

        pue = self.lookup_pue(utilization_record=utilization_record)

        return (
            (min_watts + (max_watts - min_watts) * cpu_utilization / 100) *
            Decimal(utilization_record.get("cpu_count", 1)) *
            Decimal(utilization_record["running_hours"]) *
            pue
        )

    def estimate_energy_consumption_memory(self, *, utilization_record: Dict[str, Any]) -> Decimal:
        # Energy consumption estimate for memory usage
        # Result in Watt-hours
        pue = self.lookup_pue(utilization_record=utilization_record)
        return (
            Decimal(utilization_record["memory_gb"]) *
            MEMORY_CONSUMPTION_WATTS_PER_GB *
            Decimal(utilization_record["running_hours"]) *
            pue
        )

    def estimate_energy_consumption_volume(self, *, utilization_record: Dict[str, Any]) -> Decimal:
        # Energy consumption estimate for memory usage
        # Result in Watt-hours
        pue = self.lookup_pue(utilization_record=utilization_record)

        provider = utilization_record.get("provider")
        region = utilization_record.get("region")
        volume_type = utilization_record.get("volume_type", "ssd")
        per_gb_consumption = self.lookup_volume_consumption_by_provider_region_and_type(
            provider=provider,
            region=region,
            volume_type=volume_type,
        )

        return (
            Decimal(utilization_record["volume_gb"]) *
            per_gb_consumption *
            Decimal(utilization_record["running_hours"]) *
            pue
        )

    def estimate_energy_consumption_for_utilization_record(self, *, utilization_record: Dict[str, Any]) -> Decimal:
        # Energy consumption estimate for a single record
        # Result in Watt-hours
        record_class = utilization_record.get("class")

        energy_estimate = Decimal(0)
        if record_class == "virtual_machine":
            energy_estimate = self.estimate_energy_consumption_cpu(utilization_record=utilization_record)
            energy_estimate += self.estimate_energy_consumption_memory(utilization_record=utilization_record)
        elif record_class == "volume":
            energy_estimate = self.estimate_energy_consumption_volume(utilization_record=utilization_record)

        return energy_estimate

    def estimate_emissions(self, *, utilization_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        buckets = {
            "total": {
                "energy_wh": Decimal(0),
                "co2eq_grams": Decimal(0),
            }
        }

        for utilization_record in utilization_records:
            group_name = utilization_record.get("group")
            if group_name:
                if group_name == "total":
                    group_name = None
                elif group_name not in buckets:
                    buckets[group_name] = {
                        "energy_wh": Decimal(0),
                        "co2eq_grams": Decimal(0),
                    }
            energy_estimate = self.estimate_energy_consumption_for_utilization_record(utilization_record=utilization_record)
            buckets["total"]["energy_wh"] += energy_estimate
            if group_name:
                buckets[group_name]["energy_wh"] += energy_estimate

            grid_carbon_intensity = self.lookup_gci(utilization_record=utilization_record)
            if grid_carbon_intensity:
                buckets["total"]["co2eq_grams"] += energy_estimate / 1000 * grid_carbon_intensity
                if group_name:
                    buckets[group_name]["co2eq_grams"] += energy_estimate / 1000 * grid_carbon_intensity

        report: Dict[str, Any] = {
            "groups": []
        }

        # convert units, energy usage into kWh and co2 emissions into metric tons co2eq
        for group_name, result_record in buckets.items():
            group_record: Dict[str, Decimal | str] = {}

            energy_wh = result_record["energy_wh"]
            energy_kwh = energy_wh / 1000
            group_record["energy_kwh"] = energy_kwh.quantize(Decimal("0.00"))

            co2eq_grams = result_record["co2eq_grams"]
            if co2eq_grams > 0:
                co2eq_kg = co2eq_grams / 1000
                group_record["co2eq_kg"] = co2eq_kg.quantize(Decimal("0.00"))

            if group_name == "total":
                report["total"] = group_record
            else:
                group_record["group_name"] = group_name
                report["groups"].append(group_record)

        if not report["groups"]:
            report.pop("groups")

        return report
