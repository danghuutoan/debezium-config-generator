from ensurepip import bootstrap
import os
import yaml
import json
from debezium import DebeziumConfig
from jinja2 import Template
from db import DatabaseIdentity
from kafka import KafkaConfig
from schemaRegistry import SchemaRegistryConfig
from sink import Sink

from source import Source
from user import UserIdentity
import argparse


def read_conf(path):
    conf = None
    with open(path, "r") as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return conf


def read_template(path):
    template = None
    with open(path) as file:
        template = Template(file.read())

    return template


def parse_source_conf(conf: dict):
    dbname = conf["dbname"]
    host = conf["host"]
    port = conf["port"]
    db_type = conf["db_type"]
    schema = conf["schema"]
    include_tables = conf["tables"]["include"]
    exclude_tables = conf["tables"]["exclude"]

    source_user = UserIdentity(name=conf["username"], password=conf["password"])
    source_database = DatabaseIdentity(
        host=host,
        port=port,
        name=dbname,
        type=db_type,
        user=source_user,
    )
    return Source(
        database=source_database,
        schema=schema,
        include_tables=include_tables,
        exclude_tables=exclude_tables,
    )


def parse_sink_conf(conf: dict):
    dbname = conf["dbname"]
    host = conf["host"]
    port = conf["port"]
    db_type = conf["db_type"]

    source_user = UserIdentity(name=conf["username"], password=conf["password"])

    source_database = DatabaseIdentity(
        host=host, port=port, name=dbname, type=db_type, user=source_user
    )
    return Sink(database=source_database)


def generate_sink_config(debezium_conf: DebeziumConfig):
    template = read_template("templates/sink.json.jinja2")
    json_config = template.render(
        topics=debezium_conf.sink.topics,
        host=debezium_conf.sink.database.host,
        port=debezium_conf.sink.database.port,
        username=debezium_conf.sink.database.user.name,
        password=debezium_conf.sink.database.user.password,
        database_name=debezium_conf.sink.database.name,
        bootstrap_servers=debezium_conf.kafka.bootstrap_servers,
        schema_registry_url=debezium_conf.schema_registry.urls,
        db_type=debezium_conf.sink.database.type,
    )

    with open(
        f"{output_dir}/{sink.database.name}_sink.json", "w", encoding="utf-8"
    ) as f:
        f.write(json_config)

    return json_config


def generate_source_config(debezium_conf: DebeziumConfig):
    template = read_template("templates/source.json.jinja2")
    json_config = template.render(
        include_tables=debezium_conf.source.include_tables,
        exclude_tables=debezium_conf.source.exclude_tables,
        schema=debezium_conf.source.schema,
        host=debezium_conf.source.database.host,
        port=debezium_conf.source.database.port,
        username=debezium_conf.source.database.user.name,
        password=debezium_conf.source.database.user.password,
        database_name=debezium_conf.source.database.name,
        bootstrap_servers=debezium_conf.kafka.bootstrap_servers,
        schema_registry_url=debezium_conf.schema_registry.urls,
        db_type=debezium_conf.source.database.type,
        sink_database_name=debezium_conf.sink.database.name
    )

    with open(
        f"{output_dir}/{sink.database.name}_source.json", "w", encoding="utf-8"
    ) as f:
        f.write(json_config)

    return json_config


if __name__ == "__main__":
    output_dir = None
    # Initialize parser
    parser = argparse.ArgumentParser()
    # Adding optional argument
    parser.add_argument("-o", "--Output", help="Show Output", const=1, nargs='?', type=str, default='output')
    # Read arguments from command line
    args = parser.parse_args()


    print("Displaying Output as: % s" % args.Output)
    output_dir = args.Output
    os.makedirs(output_dir, exist_ok=True)

    
    conf = read_conf("conf.yaml")
    projects = conf["projects"]
    debezium_url = conf["debezium"]["url"]
    kafka_conf = KafkaConfig(bootstrap_servers=conf["kafka"]["bootstrap_servers"])
    schema_registry_conf = SchemaRegistryConfig(urls=conf["schema_registry"]["url"])
    for db in projects:
        sink = parse_sink_conf(db["project"]["sink"])
        source = parse_source_conf(db["project"]["source"])
        for table in source.include_tables:
            sink.topics.append(f"{source.schema}.{table}")

        debezium_config = DebeziumConfig(
            url=debezium_url,
            sink=sink,
            source=source,
            kafka=kafka_conf,
            schema_registry=schema_registry_conf,
        )

        json_config = generate_sink_config(debezium_conf=debezium_config)
        json_config = generate_source_config(debezium_conf=debezium_config)
        print(json_config)
