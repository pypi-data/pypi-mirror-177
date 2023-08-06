import csv
import json
import os
import pathlib
import typing

import httpx
import typer

from neosctl import util
from neosctl.auth import ensure_login
from neosctl.schema import DataProductCreate
from neosctl.schema import FieldDataType
from neosctl.schema import FieldDefinition
from neosctl.util import process_response


app = typer.Typer()


def product_url(ctx: typer.Context) -> str:
    return "{}/product".format(ctx.obj.get_gateway_api_url().rstrip("/"))


special_delimiters = {
    r"\t": "\t",
}


@app.command(name="template")
def template(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
    filepath: str = typer.Option(..., "--filepath", "-f", help="Filepath of the csv template"),
    output_dir: str = typer.Option(..., "--output-dir", "-o", help="Output directory for the json template"),
    delimiter: str = typer.Option(",", "--delimiter", "-d", help="csv delimiter"),
    quotechar: typing.Optional[str] = typer.Option(None, "--quote-char", "-q", help="csv quote char"),
):
    """Generate a data product schema template from a csv.

    Given a csv with a header row, generate a template field schema.
    """
    fp = util.get_file_location(filepath)

    delimiter = special_delimiters.get(delimiter, delimiter)

    kwargs = {k: v for k, v in [("delimiter", delimiter), ("quotechar", quotechar)] if v is not None}

    with fp.open() as f:
        reader = csv.DictReader(f, **kwargs)
        fields = reader.fieldnames

    output = []
    for field in fields:
        output.append(
            FieldDefinition(
                name=field,
                description=None,
                type="STRING",
                primary=False,
                optional=False,
                data_type=FieldDataType(
                    meta={},
                    type="TEXT",
                ),
            ).dict(),
        )

    fp = pathlib.Path(output_dir) / "{}.json".format(name)
    with fp.open("w") as f:
        json.dump(output, f, indent=4)


@app.command(name="create")
def create_from_json(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
    engine: str = typer.Option(..., "--engine", "-e", help="Storage engine"),
    filepath: str = typer.Option(..., "--filepath", "-f", help="Filepath of the table schema json payload"),
):
    """Create a data product.
    """
    @ensure_login
    def _request(ctx: typer.Context, dpc: DataProductCreate) -> httpx.Response:
        return util.post(
            ctx,
            "{dp_url}/{name}".format(dp_url=product_url(ctx), name=name),
            json=dpc.dict(exclude_none=True),
        )

    fp = util.get_file_location(filepath)
    fields = util.load_json_file(fp, "schema")

    dpc = DataProductCreate(engine=engine, fields=fields)

    r = _request(ctx, dpc)
    process_response(r)


@app.command()
def list(ctx: typer.Context):
    """List data products.
    """
    @ensure_login
    def _request(ctx: typer.Context):
        return util.get(ctx, product_url(ctx))

    r = _request(ctx)
    process_response(r)


@app.command()
def delete_data(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Delete data from a data product.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            "{dp_url}/{name}/data".format(dp_url=product_url(ctx), name=name),
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def delete(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Delete a data product.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            "{dp_url}/{name}".format(dp_url=product_url(ctx), name=name),
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def publish(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Publish a data product.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.post(
            ctx,
            "{dp_url}/{name}/publish".format(dp_url=product_url(ctx), name=name),
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def unpublish(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Unpublish a product.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            "{dp_url}/{name}/publish".format(dp_url=product_url(ctx), name=name),
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="schema")
def get_schema(
    ctx: typer.Context,
    product_name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Get data product schema.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            "{dp_url}/{name}/schema".format(dp_url=product_url(ctx), name=product_name),
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def preview(
    ctx: typer.Context,
    product_name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Preview data product data.

    Get the first 25 rows of a data product's data.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            "{product_url}/{name}".format(
                product_url=product_url(ctx),
                name=product_name,
            ),
        )

    r = _request(ctx)
    process_response(r)
