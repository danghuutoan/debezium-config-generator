import yaml
from jinja2 import Template
from db import DatabaseIdentity
from sink import Sink

from source import Source
from user import UserIdentity


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
    tables = conf["tables"]

    source_user = UserIdentity(
        name=conf["username"], password=conf["password"]
    )
    source_database = DatabaseIdentity(
        host=host, port=port, name=dbname, type=db_type, user=source_user,
    )
    return Source(database=source_database, schema=schema, tables=tables,)


def parse_sink_conf(conf: dict):
    dbname = conf["dbname"]
    host = conf["host"]
    port = conf["port"]
    db_type = conf["db_type"]

    source_user = UserIdentity(
        name=conf["username"], password=conf["password"]
    )

    source_database = DatabaseIdentity(
        host=host, port=port, name=dbname, type=db_type, user=source_user
    )
    return Sink(database=source_database)


if __name__ == "__main__":
    template = read_template("templates/sink.json.jinja")
    conf = read_conf("conf.yaml")
    database_conf = conf["projects"]
    debezium_conf = conf["debezium"]
    kafka_conf = conf["kafka"]
    schema_registry_conf = conf["schema_registry"]
    for db in database_conf:
        sink = parse_sink_conf(db["project"]["sink"])
        source = parse_source_conf(db["project"]["source"])
        json_config = template.render(
            tables=source.tables,
            schema=source.schema,
            host=sink.database.host,
            port=sink.database.port,
            username=sink.database.user.name,
            password=sink.database.user.password,
            database_name=sink.database.name,
            bootstrap_servers=kafka_conf["bootstrap_servers"],
            schema_registry_url=schema_registry_conf["url"],
            db_type=sink.database.type,
        )

        print(json_config)
