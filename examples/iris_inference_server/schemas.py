from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict
from pydantic import field_validator
from typing import List

# data validation steps using pydantic
class IrisRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sepal_length: float = Field(alias="sepal length (cm)")
    sepal_width: float = Field(alias="sepal width (cm)")
    petal_length: float = Field(alias="petal length (cm)")
    petal_width: float = Field(alias="petal width (cm)")

    def get_feature_values(self) -> List[float]:
        """
        Get the feature values as a list.
        """
        return [
            self.sepal_length,
            self.sepal_width,
            self.petal_length,
            self.petal_width,
        ]

    def get_feature_names(self) -> List[str]:
        """
        Get the feature names as a list.
        """
        return [
            "sepal length (cm)",
            "sepal width (cm)",
            "petal length (cm)",
            "petal width (cm)",
        ]


class IrisResponse(BaseModel):
    """Schema for the iris prediction response."""
    species: int = Field(description="Predicted species of the iris flower")
    confidence: float = Field(description="Confidence score of the prediction")

    # mapping integer to species name
    # The validator runs automatically during model creation, 
    # ensuring the data is always validated and transformed correctly in one place.
    # You don’t have to write the mapping logic in the router
    # You don’t risk forgetting validation in other routes
    # You don’t duplicate mapping code everywhere
    
    # Without the validator
    # You have to remember to call map_int_to_species()
    # in every place you create IrisResponse.

    @field_validator("species")
    @classmethod
    def map_int_to_species(cls, species_id: int) -> str:
        species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}

        if species_id not in species_map:
            raise ValueError(f"Invalid species_id: {species_id}. Must be 0, 1, or 2.")
        return species_map.get(species_id)
