"""Utilities for deriving data source and feature view schemas. Shared by backend and local schema derivation."""
import datetime
from typing import Callable
from typing import Optional

import pyspark
from pyspark.sql import types as pyspark_types
from typeguard import typechecked

from tecton_proto.common import spark_schema_pb2
from tecton_spark import data_source_helper
from tecton_spark import spark_schema_wrapper


@typechecked
def get_hive_table_schema(
    spark: pyspark.sql.SparkSession,
    database: str,
    table: str,
    post_processor: Optional[Callable],
    timestamp_field: str,
    timestamp_format: str,
) -> spark_schema_pb2.SparkSchema:
    df = data_source_helper._get_raw_hive_table_dataframe(spark, database, table)
    if post_processor is not None:
        df = post_processor(df)
    if timestamp_field:
        ts_format = None
        if timestamp_format:
            ts_format = timestamp_format
        df = data_source_helper.apply_timestamp_column(df, timestamp_field, ts_format)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_kinesis_schema(
    spark: pyspark.sql.SparkSession, stream_name: str, post_processor: Callable
) -> spark_schema_pb2.SparkSchema:
    """Compute the Kinesis schema using mock Kinesis data.

    Creates a mocked DataFrame for this stream, without actually creating a stream reader.
    This method returns a message in the Kinesis message format (below) with mocked contents.

    |-- approximateArrivalTimestamp: timestamp
    |-- data: binary
    |-- partitionKey: string
    |-- sequenceNumber: string
    |-- streamName: string
    """
    row = pyspark.Row(
        data=bytearray("no_data", "utf-8"),
        streamName=stream_name,
        partitionKey="0",
        sequenceNumber="0",
        approximateArrivalTimestamp=datetime.datetime.fromtimestamp(0),
    )
    df = spark.createDataFrame([row])

    df = post_processor(df)

    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


# https://docs.databricks.com/spark/latest/structured-streaming/kafka.html
KAFKA_SCHEMA = pyspark_types.StructType(
    [
        pyspark_types.StructField("key", pyspark_types.BinaryType(), True),
        pyspark_types.StructField("value", pyspark_types.BinaryType(), True),
        pyspark_types.StructField("topic", pyspark_types.StringType(), True),
        pyspark_types.StructField("partition", pyspark_types.IntegerType(), True),
        pyspark_types.StructField("offset", pyspark_types.LongType(), True),
        pyspark_types.StructField("timestamp", pyspark_types.TimestampType(), True),
        pyspark_types.StructField("timestampType", pyspark_types.IntegerType(), True),
    ]
)


@typechecked
def get_kafka_schema(spark: pyspark.sql.SparkSession, post_processor: Callable) -> spark_schema_pb2.SparkSchema:
    """Compute the Kafka schema using mock Kafka data."""
    df = spark.createDataFrame([], KAFKA_SCHEMA)
    df = post_processor(df)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_stream_data_source_function_schema(
    spark: pyspark.sql.SparkSession, data_source_fn: Callable
) -> spark_schema_pb2.SparkSchema:
    """Compute the Kafka schema using mock Kafka data."""
    df = data_source_fn(spark=spark)
    assert (
        isinstance(df, pyspark.sql.dataframe.DataFrame) and df.isStreaming
    ), "Data Source Function must return a streaming DataFrame"
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)
