from cloud_emission_estimator.emission_estimator import EmissionEstimator


def test_estimator_virtual_machine() -> None:
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


def test_estimator_volume() -> None:
    estimator = EmissionEstimator()

    test_record = {
        "class": "volume",
        "volume_gb": 10,
        "volume_type": "ssd",
        "running_hours": "12",
    }

    energy_consumption_estimate = estimator.estimate_energy_consumption_volume(utilization_record=test_record)

    assert energy_consumption_estimate > 0
