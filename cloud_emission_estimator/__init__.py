# Copyright (c) 2023 Aiven, Helsinki, Finland. https://aiven.io/
from cloud_emission_estimator.emission_estimator import EmissionEstimator


def estimate_emissions(*, utilization_records: list[dict]) -> dict:
    estimator = EmissionEstimator()
    return estimator.estimate_emissions(utilization_records=utilization_records)
