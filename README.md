# Cloud Emission Estimator

Cloud Emission Estimator is a Python based tool for calculating energy usage and carbon emissions based on cloud resource consumption.

This tool is derived from [Cloud Carbon Footprint](https://github.com/cloud-carbon-footprint/cloud-carbon-footprint/).

## Usage

You can run the commandline tool with an included sample as follows:

```
$ python3 -m cloud_emission_estimator --input doc/samples/data_sample_service_april_2023.json
```

Or call the module programmatically as:

```python
import cloud_emission_estimator

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

print(cloud_emission_estimator.estimate_emissions(utilization_records=sample_records))
```

## License

Licensed under the Apache License, Version 2.0: <http://www.apache.org/licenses/LICENSE-2.0>
