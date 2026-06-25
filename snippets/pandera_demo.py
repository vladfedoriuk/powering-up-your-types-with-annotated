from typing import Annotated
import pandas as pd
import pandera as pa
from pandera.typing import Series


class ReservationModel(pa.DataFrameModel):
    room_id: Annotated[Series[str], pa.Field(unique=True)]
    guest_count: Annotated[Series[int], pa.Field(ge=1, le=10)]
    rate: Annotated[Series[float], pa.Field(gt=0)]


# Valid DataFrame
valid_df = pd.DataFrame(
    {
        "room_id": ["101", "102", "103"],
        "guest_count": [2, 4, 1],
        "rate": [120.0, 200.0, 95.0],
    }
)

# Invalid DataFrame (violating range and uniqueness)
invalid_df = pd.DataFrame(
    {
        "room_id": ["101", "101", "103"],  # Duplicate room_id
        "guest_count": [0, 15, 1],  # guest_count <= 0 and >= 10
        "rate": [-10.0, 200.0, 95.0],  # rate <= 0
    }
)

if __name__ == "__main__":
    print("Validating valid_df...")
    ReservationModel.validate(valid_df)
    print("valid_df validated successfully!")

    try:
        print("Validating invalid_df...")
        ReservationModel.validate(invalid_df)
    except pa.errors.SchemaErrors as err:
        print("invalid_df validation failed as expected:")
        print(err.failure_cases)
