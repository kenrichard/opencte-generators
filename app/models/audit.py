""" Data Model - Audit Log for Generation """

from decimal import Decimal
from datetime import datetime
import json
from typing import Optional
from app.utils.db_dynamo import (
    DynamoBase,
    dynamo_save,
)


class Audit(DynamoBase):
    """Audit Data Model"""

    ts: str
    course_key: Optional[str] = None
    unit_key: Optional[str] = None
    lesson_key: Optional[str] = None
    user_key: Optional[str] = None
    customer_key: Optional[str] = None
    section_key: Optional[str] = None
    prompt: Optional[str] = None
    event: Optional[str] = None
    description: Optional[str] = None
    completion: Optional[str] = None
    completion_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    input_cost: Optional[Decimal] = None
    output_cost: Optional[Decimal] = None
    total_cost: Optional[Decimal] = None


def audit_pk():
    return "AUDIT"


def audit_sk(ts):
    return "AUDIT~" + ts


def audit_completion(prompt, description, keys, model, completion):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    usage = completion.usage
    completion_tokens = (
        usage.completion_tokens if hasattr(usage, "completion_tokens") else 0
    )
    prompt_tokens = usage.prompt_tokens if hasattr(usage, "prompt_tokens") else 0
    total_tokens = usage.total_tokens if hasattr(usage, "total_tokens") else 0

    if model == "gpt-4-turbo-preview" or model == "gpt-4-1106-preview":
        # Input $0.01 / 1K tokens
        # Output $0.03 / 1K tokens
        input_cost = 0.01 * float(prompt_tokens) / 1000.0
        output_cost = 0.03 * float(completion_tokens) / 1000.0
        total_cost = input_cost + output_cost
    elif model == "gpt-3.5-turbo-1106":
        # Input $0.0010 / 1K tokens
        # Output $0.0020 / 1K tokens
        input_cost = 0.0010 * float(prompt_tokens) / 1000.0
        output_cost = 0.0020 * float(completion_tokens) / 1000.0
        total_cost = input_cost + output_cost
    elif model == "text-embedding-ada-002":
        # Embeddings $0.0001 / 1K tokens
        input_cost = 0.0010 * float(prompt_tokens) / 1000.0
        output_cost = 0
        total_cost = input_cost + output_cost
    else:
        print("Cannot Calculate Costs:")

    if description != "Search":
        print("Total Tokens=" + str(total_tokens) + " $" + str(total_cost))

    audit = Audit(
        pk=audit_pk(),
        sk=audit_sk(ts),
        ts=ts,
        course_key=keys.get("course_key"),
        unit_key=keys.get("unit_key"),
        lesson_key=keys.get("lesson_key"),
        prompt=prompt,
        description=description,
        completion=json.dumps(completion, default=vars),
        completion_tokens=completion_tokens,
        prompt_tokens=prompt_tokens,
        total_tokens=total_tokens,
        input_cost=to_decimal(input_cost),
        output_cost=to_decimal(output_cost),
        total_cost=to_decimal(total_cost),
    )
    dynamo_save(audit)


def to_decimal(f: float):
    return Decimal(str(f)).quantize(Decimal("0.000"))
