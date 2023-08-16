# Copyright (c) 2023 Aiven, Helsinki, Finland. https://aiven.io/

# Constants used for energy consumption & emission calculations
#
# The values are captured from Cloud Carbon Footprint project:
# https://github.com/cloud-carbon-footprint/cloud-carbon-footprint

from decimal import Decimal


CARBON_INTENSITY_GRAMS_PER_KWH = {
    "aws": {
        "af-south-1": Decimal("900.6"),
        "ap-east-1": Decimal("710"),
        "ap-northeast-1": Decimal("465.8"),
        "ap-northeast-2": Decimal("415.6"),
        "ap-northeast-3": Decimal("465.8"),
        "ap-south-1": Decimal("708.2"),
        "ap-southeast-1": Decimal("408"),
        "ap-southeast-2": Decimal("760"),
        "ap-southeast-3": Decimal("717.7"),
        "ca-central-1": Decimal("120"),
        "eu-central-1": Decimal("311"),
        "eu-south-1": Decimal("213.4"),
        "eu-west-1": Decimal("278.6"),
        "eu-west-2": Decimal("225"),
        "eu-west-3": Decimal("51.1"),
        "eu-north-1": Decimal("8.8"),
        "me-central-1": Decimal("404.1"),
        "me-south-1": Decimal("505.9"),
        "sa-east-1": Decimal("61.7"),
        "us-east-1": Decimal("379.069"),
        "us-east-2": Decimal("410.608"),
        "us-west-1": Decimal("322.167"),
        "us-west-2": Decimal("322.167"),
        "default": Decimal("392.78188"),  # Average of the above regions
    },

    "gcp": {
        # Google Cloud Platform numbers are sourced from here:
        #  https://cloud.google.com/sustainability/region-carbon
        # note: we don't account for CFE% just yet
        "asia-east1": Decimal("453"),
        "asia-east2": Decimal("360"),
        "asia-northeast1": Decimal("463"),
        "asia-northeast2": Decimal("383"),
        "asia-northeast3": Decimal("425"),
        "asia-south1": Decimal("555"),
        "asia-south2": Decimal("632"),
        "asia-southeast1": Decimal("372"),
        "asia-southeast2": Decimal("580"),
        "australia-southeast1": Decimal("538"),
        "australia-southeast2": Decimal("490"),
        "europe-central2": Decimal("738"),
        "europe-north1": Decimal("112"),
        "europe-southwest1": Decimal("160"),
        "europe-west1": Decimal("123"),
        "europe-west2": Decimal("166"),
        "europe-west3": Decimal("413"),
        "europe-west4": Decimal("317"),
        "europe-west6": Decimal("118"),
        "europe-west8": Decimal("323"),
        "europe-west9": Decimal("71"),
        "europe-west12": Decimal("323"),
        "me-west1": Decimal("476"),
        "northamerica-northeast1": Decimal("0"),
        "northamerica-northeast2": Decimal("36"),
        "southamerica-east1": Decimal("65"),
        "southamerica-west1": Decimal("165"),
        "us-central1": Decimal("445"),
        "us-east1": Decimal("532"),
        "us-east4": Decimal("354"),
        "us-east5": Decimal("354"),
        "us-south1": Decimal("342"),
        "us-west1": Decimal("67"),
        "us-west2": Decimal("202"),
        "us-west3": Decimal("606"),
        "us-west4": Decimal("396"),
        "default": Decimal("337.638"),  # Average of the above regions
    },

    "default": {
        "default": Decimal("436.00"),
    },
}
