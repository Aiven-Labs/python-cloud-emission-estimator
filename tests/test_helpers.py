from cloud_emission_estimator.helpers import guess_cpu_type_by_instance_type


def test_helpers_guess_cpu_type() -> None:
    assert guess_cpu_type_by_instance_type(provider="", instance_type="") is None
    assert guess_cpu_type_by_instance_type(provider="aws", instance_type="m6g.xlarge") == "ARM_NEOVERSE_N1"
    assert guess_cpu_type_by_instance_type(provider="gcp", instance_type="n2-standard-8") == "INTEL_SKYLAKE"
    assert guess_cpu_type_by_instance_type(provider="gcp", instance_type="n2d-custom-16-32768") == "AMD_EPYC_2ND_GEN"
