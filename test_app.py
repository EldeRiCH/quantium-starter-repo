import pytest
from dash import html, dcc
import app as dash_app


def find_components(component, component_type):
    """Recursively collect all components of a given type from the layout tree."""
    found = []
    if isinstance(component, component_type):
        found.append(component)
    children = getattr(component, "children", None)
    if isinstance(children, list):
        for child in children:
            found.extend(find_components(child, component_type))
    elif children is not None:
        found.extend(find_components(children, component_type))
    return found


def test_header_is_present():
    headers = find_components(dash_app.app.layout, html.H1)
    assert len(headers) > 0, "No H1 header found in layout"
    assert any("Pink Morsel" in str(h.children) for h in headers), \
        "Header does not contain expected title text"


def test_visualisation_is_present():
    graphs = find_components(dash_app.app.layout, dcc.Graph)
    assert len(graphs) > 0, "No Graph component found in layout"
    assert any(g.id == "sales-chart" for g in graphs), \
        "Expected sales-chart Graph not found"


def test_region_picker_is_present():
    radio_items = find_components(dash_app.app.layout, dcc.RadioItems)
    assert len(radio_items) > 0, "No RadioItems component found in layout"
    picker = next((r for r in radio_items if r.id == "region-filter"), None)
    assert picker is not None, "Expected region-filter RadioItems not found"
    values = [opt["value"] for opt in picker.options]
    assert set(values) == {"all", "north", "east", "south", "west"}, \
        f"Unexpected region options: {values}"
