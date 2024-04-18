import logging
import os
from typing import Optional
from pydantic import BaseModel
import boto3

TABLE_NAME = "lemonstreet"


class DynamoBase(BaseModel):
    pk: Optional[str] = None
    sk: Optional[str] = None


def dynamodb():
    return boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name="us-east-2",
    )


def table():
    return dynamodb().Table(TABLE_NAME)


def dynamo_save(item: DynamoBase):
    if item.pk is None:
        raise ValueError("Missing PK")
    if item.sk is None:
        raise ValueError("Missing SK")
    table().put_item(Item=item.model_dump())


def dynamo_load(pk, sk):
    response = table().get_item(Key={"pk": pk, "sk": sk})
    if response.get("Item") is None:
        raise "Not Found: PK=" + pk + " SK=" + sk
    return response.get("Item")


def dynamo_prefix_query(pk: str, sk_prefix):
    response = table().query(
        KeyConditionExpression="pk = :pk_value and begins_with(sk, :sk_prefix)",
        ExpressionAttributeValues={":pk_value": pk, ":sk_prefix": sk_prefix},
    )
    items = response.get("Items", [])
    return items


def dynamo_prefix_delete(pk: str, sk_prefix: str):
    t = table()

    response = t.query(
        KeyConditionExpression="pk = :pk_value and begins_with(sk, :sk_prefix)",
        ExpressionAttributeValues={":pk_value": pk, ":sk_prefix": sk_prefix},
    )

    # Delete Each
    for item in response.get("Items", []):
        item_pk = item["pk"]
        item_sk = item["sk"]
        logging.debug(f"Deleting record: PK={item_pk}, SK={item_sk}")
        t.delete_item(
            Key={
                "pk": item_pk,
                "sk": item_sk,
            }
        )
