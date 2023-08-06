from enum import Enum
import attr
from typing import Sequence, List, Dict, Any, Union

from aws_feature_store.inputs import Config


class FeatureTypeEnum(Enum):
    """Enum of feature types.

    The data type of a feature can be Fractional, Integral or String.
    """

    FRACTIONAL = "Fractional"
    INTEGRAL = "Integral"
    STRING = "String"


@attr.s
class FeatureDefinition:
    """Feature definition.

    This instantiates a Feature Definition object where FeatureDefinition is a subclass of Config.

    Attributes:
        feature_name (str): The name of the feature
        feature_type (FeatureTypeEnum): The type of the feature
    """

    feature_name: str = attr.ib()
    feature_type: FeatureTypeEnum = attr.ib()

    def to_dict(self) -> Dict[str, Any]:
        """Construct a dictionary based on each attribute."""
        return Config.construct_dict(
            FeatureName=self.feature_name, FeatureType=self.feature_type.value
        )