"""Run fetcher pipeline, the CLI command."""

from typing import Optional

import typer

from dbnomics_fetcher_ops.services.run_fetcher_pipeline import run_fetcher_pipeline

__all__ = ["run_command"]


def run_command(
    debug_gitlab: bool = typer.Option(False, help="Show logging debug messages of Python GitLab"),
    gitlab_private_token: str = typer.Option(..., envvar="GITLAB_PRIVATE_TOKEN"),
    json_data_from_git: bool = typer.Option(False, envvar="JSON_DATA_FROM_GIT"),
    json_data_pipeline_id: Optional[int] = typer.Option(None, envvar="JSON_DATA_PIPELINE_ID"),
    provider_slug: str = typer.Option(..., envvar="PROVIDER_SLUG"),
    source_data_from_git: bool = typer.Option(False, envvar="SOURCE_DATA_FROM_GIT"),
    source_data_pipeline_id: Optional[int] = typer.Option(None, envvar="SOURCE_DATA_PIPELINE_ID"),
    start_from: Optional[str] = typer.Option(None, envvar="START_FROM"),
):
    """Run a pipeline for a fetcher, with options."""
    from ..app_args import app_args

    assert app_args is not None

    run_fetcher_pipeline(
        provider_slug,
        debug_gitlab=debug_gitlab,
        dry_run=app_args.dry_run,
        fetcher_metadata=app_args.fetcher_metadata,
        gitlab_private_token=gitlab_private_token,
        json_data_from_git=json_data_from_git,
        json_data_pipeline_id=json_data_pipeline_id,
        source_data_from_git=source_data_from_git,
        source_data_pipeline_id=source_data_pipeline_id,
        start_from=start_from,
    )
