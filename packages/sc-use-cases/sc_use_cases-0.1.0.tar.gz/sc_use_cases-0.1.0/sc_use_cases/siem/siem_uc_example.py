"""
example use case
"""

from typing import List
from swimlane import Swimlane
from pydantic import BaseModel


class SWInputs(BaseModel):
    swimlane_api_pat: str
    allowed_groups: List[str]


def main(context):
    inputs = SWInputs(**context.inputs)
    # creating a Swimlane instance is commonly used code. Can we create a custom Swimlane class in the __init__.py?
    swimlane = Swimlane(
        context.config["InternalSwimlaneUrl"],
        access_token=inputs.swimlane_api_pat,
        verify_ssl=False,
    )

    # getting an application is definitely commonly used code
    current_app = swimlane.apps.get(id=context.config["ApplicationId"])  # type: ignore
    current_record = current_app.records.get(id=context.config["RecordId"])

    for group in inputs.allowed_groups:
        current_record.add_restriction(swimlane.groups.get(name=group))  # type: ignore
        current_record.save()


if "sw_context" in globals():  # pragma: no cover
    sw_outputs = main(sw_context)  # type: ignore  # noqa
