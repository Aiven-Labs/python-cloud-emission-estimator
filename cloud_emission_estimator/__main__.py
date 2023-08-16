# Copyright (c) 2023 Aiven, Helsinki, Finland. https://aiven.io/
from cloud_emission_estimator.emission_estimator import EmissionEstimator
from decimal import Decimal

import argparse
import json
import logging


class json_encoder(json.JSONEncoder):
    def default(self, obj: object) -> object:
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input file with utilization records")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    log = logging.getLogger(__name__)

    with open(args.input) as fh:
        utilization_records = json.load(fh)
        log.info("Read %r records in total", len(utilization_records))

    estimator = EmissionEstimator()
    report = estimator.estimate_emissions(utilization_records=utilization_records)

    print(json.dumps(report, indent=4, cls=json_encoder))
