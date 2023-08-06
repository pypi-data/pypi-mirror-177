import argparse
import logging
import sys

from gaarf.io import writer, reader  # type: ignore
from gaarf.simulation import generate_fake_data , FakeSpecification
from .utils import GaarfConfigBuilder, ConfigSaver, initialize_runtime_parameters


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="+")
    parser.add_argument("-c", "--config", dest="gaarf_config", default=None)
    parser.add_argument("--account", dest="customer_id")
    parser.add_argument("--output", dest="save", default="csv")
    parser.add_argument("--input", dest="input", default="file")
    parser.add_argument("--api-version", dest="api_version", default=10)
    parser.add_argument("--log",
                        "--loglevel",
                        dest="loglevel",
                        default="info")
    parser.add_argument("--customer-ids-query",
                        dest="customer_ids_query",
                        default=None)
    parser.add_argument("--customer-ids-query-file",
                        dest="customer_ids_query_file",
                        default=None)
    parser.add_argument("--save-config",
                        dest="save_config",
                        action="store_true")
    parser.add_argument("--no-save-config",
                        dest="save_config",
                        action="store_false")
    parser.add_argument("--config-destination",
                        dest="save_config_dest",
                        default="config.yaml")
    parser.set_defaults(save_config=False)
    args = parser.parse_known_args()
    main_args = args[0]

    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
        stream=sys.stdout,
        level=main_args.loglevel.upper(),
        datefmt="%Y-%m-%d %H:%M:%S")
    logging.getLogger("google.ads.googleads.client").setLevel(logging.WARNING)
    logging.getLogger("smart_open.smart_open_lib").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    config = GaarfConfigBuilder(args).build()
    logger.debug("config: %s", config)

    if main_args.save_config and not main_args.gaarf_config:
        ConfigSaver(main_args.save_config_dest).save(config)

    config = initialize_runtime_parameters(config)
    logger.debug("initialized config: %s", config)

    writer_client = writer.WriterFactory().create_writer(
        config.output, **config.writer_params)
    reader_factory = reader.ReaderFactory()
    reader_client = reader_factory.create_reader(main_args.input)

    for query in main_args.query:
        report = generate_fake_data(reader_client.read(query))
        writer_client.write(report, query)


if __name__ == "__main__":
    main()

