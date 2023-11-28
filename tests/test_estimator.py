from cloud_emission_estimator.emission_estimator import EmissionEstimator
from decimal import Decimal
import cloud_emission_estimator


def test_estimator_component_virtual_machine() -> None:
    estimator = EmissionEstimator()

    test_record = {
        "class": "virtual_machine",
        "cpu_count": 16,
        "cpu_type": "INTEL_ICE_LAKE",
        "running_hours": "12",
        "memory_gb": "16",
    }

    energy_consumption_estimate_cpu = estimator.estimate_energy_consumption_cpu(utilization_record=test_record)
    energy_consumption_estimate_mem = estimator.estimate_energy_consumption_memory(utilization_record=test_record)

    assert energy_consumption_estimate_cpu > 0
    assert energy_consumption_estimate_cpu > 0

    energy_consumption_estimate_total = estimator.estimate_energy_consumption_for_utilization_record(utilization_record=test_record)

    assert (energy_consumption_estimate_cpu + energy_consumption_estimate_mem) == energy_consumption_estimate_total


def test_estimator_component_volume() -> None:
    estimator = EmissionEstimator()

    test_record = {
        "class": "volume",
        "volume_gb": 10,
        "volume_type": "ssd",
        "running_hours": "12",
    }

    energy_consumption_estimate = estimator.estimate_energy_consumption_volume(utilization_record=test_record)

    assert energy_consumption_estimate > 0


def test_estimator_zero_records() -> None:
    report = cloud_emission_estimator.estimate_emissions(utilization_records=[])
    assert report == {"total":{"energy_kwh":Decimal("0.00")}}


def test_estimator_sample_records() -> None:
    sample_records = [
        {
            "class": "virtual_machine",
            "cpu_count": 16,
            "cpu_type": "ARM_NEOVERSE_N1",
            "running_hours": "24",
            "memory_gb": "128",
            "provider": "aws",
            "region": "eu-west-1",
        },
        {
            "class": "volume",
            "volume_gb": 1024,
            "volume_type": "ssd",
            "running_hours": "24",
            "provider": "aws",
            "region": "eu-west-1",
        },
    ]

    report = cloud_emission_estimator.estimate_emissions(utilization_records=sample_records)
    assert report["total"]["energy_kwh"] > 0


def test_estimator_sample_records_grouping() -> None:
    sample_records = [
        {
            "class": "virtual_machine",
            "cpu_count": 16,
            "cpu_type": "INTEL_ICE_LAKE",
            "running_hours": "24",
            "memory_gb": "128",
            "provider": "gcp",
            "region": "europe-west-4",
            "group": "compute",
        },
        {
            "class": "volume",
            "volume_gb": 1024,
            "volume_type": "ssd",
            "running_hours": "24",
            "provider": "gcp",
            "region": "europe-west-4",
            "group": "storage",
        },
    ]

    report = cloud_emission_estimator.estimate_emissions(utilization_records=sample_records)
    groups = report.get("groups")
    assert groups is not None
    assert len(groups) == 2

    found = set()
    for group in groups:
        group_name = group.get("group_name")
        assert group_name
        assert group["energy_kwh"] > 0
        found.add(group_name)

    assert found == {"compute", "storage"}


def test_cgi_lookups() -> None:
    estimator = EmissionEstimator()

    gci_a = estimator.lookup_gci_by_provider_and_region(provider="aws", region="us-east-1")
    gci_b = estimator.lookup_gci_by_provider_and_region(provider="aws", region="eu-north-1")

    assert gci_a != gci_b

    gci_a = estimator.lookup_gci_by_provider_and_region(provider="gcp", region="us-east1")
    gci_b = estimator.lookup_gci_by_provider_and_region(provider="gcp", region="europe-north1")

    assert gci_a != gci_b


def test_gci_impact_between_regions() -> None:
    sample_records_aws_us = [
        {
            "class": "virtual_machine",
            "cpu_count": 16,
            "cpu_type": "ARM_NEOVERSE_N1",
            "running_hours": "7300",
            "memory_gb": "128",
            "provider": "aws",
            "region": "us-east-1",
        },
        {
            "class": "volume",
            "volume_gb": 1024,
            "volume_type": "ssd",
            "running_hours": "7300",
            "provider": "aws",
            "region": "us-east-1",
        },
    ]
    sample_records_aws_eu = [
        {
            "class": "virtual_machine",
            "cpu_count": 16,
            "cpu_type": "ARM_NEOVERSE_N1",
            "running_hours": "7300",
            "memory_gb": "128",
            "provider": "aws",
            "region": "eu-north-1",
        },
        {
            "class": "volume",
            "volume_gb": 1024,
            "volume_type": "ssd",
            "running_hours": "7300",
            "provider": "aws",
            "region": "eu-north-1",
        },
    ]

    report_us = cloud_emission_estimator.estimate_emissions(utilization_records=sample_records_aws_us)
    report_eu = cloud_emission_estimator.estimate_emissions(utilization_records=sample_records_aws_eu)
    assert report_us["total"]["energy_kwh"] == report_eu["total"]["energy_kwh"]
    assert report_us["total"]["co2eq_mtons"] != report_eu["total"]["co2eq_mtons"]
