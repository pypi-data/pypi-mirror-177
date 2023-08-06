"""Top-level package for Pyramid Resume Template Default."""

__author__ = """Steve Locke"""
__email__ = "steve@locke.codes"
__version__ = "0.1.0"

from pathlib import Path


def includeme(config):
    config.include("pyramid_jinja2")
    config.add_jinja2_extension("jinja2.ext.with_")
    config.add_jinja2_search_path("pyramid_resume_template_default:templates")
    config.add_static_view("pyramid_resume_template_default_static", "pyramid_resume_template_default:static/")
    config.add_request_method(
        lambda _: Path(config.registry.settings["resume.default_content"]), "content_path", reify=True
    )
    config.add_request_method(lambda _: "pyramid_resume_template_default", "theme", reify=True)
    config.add_request_method(lambda _: "favicon.ico", "favicon", reify=True)
