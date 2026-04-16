import pandas as pd
import pytest
from io import StringIO

SAMPLE_CSV = """product,price,quantity,date,region
pink morsel,$3.00,100,2021-01-10,north
pink morsel,$4.50,200,2021-01-20,south
pink morsel,$3.00,50,2020-12-01,east
not a morsel,$2.00,999,2021-01-10,north
"""


def run_process(csv_text):
    df = pd.read_csv(StringIO(csv_text))
    df = df[df["product"] == "pink morsel"].copy()
    df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
    df["sales"] = df["quantity"] * df["price"]
    return df[["sales", "date", "region"]].reset_index(drop=True)


def test_filters_non_pink_morsel_rows():
    result = run_process(SAMPLE_CSV)
    assert len(result) == 3


def test_output_columns():
    result = run_process(SAMPLE_CSV)
    assert list(result.columns) == ["sales", "date", "region"]


def test_sales_calculation():
    result = run_process(SAMPLE_CSV)
    assert result.loc[0, "sales"] == pytest.approx(300.0)
    assert result.loc[1, "sales"] == pytest.approx(900.0)


def test_date_and_region_preserved():
    result = run_process(SAMPLE_CSV)
    assert result.loc[0, "date"] == "2021-01-10"
    assert result.loc[0, "region"] == "north"


def test_output_file_has_correct_columns(tmp_path):
    out = tmp_path / "output.csv"
    df = run_process(SAMPLE_CSV)
    df.to_csv(out, index=False)
    loaded = pd.read_csv(out)
    assert list(loaded.columns) == ["sales", "date", "region"]
