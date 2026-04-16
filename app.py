import pandas as pd
from dash import Dash, dcc, html, callback, Output, Input
import plotly.express as px

df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])

PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")

app = Dash(__name__)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(160deg, #0d0d1a 0%, #111827 60%, #0f2027 100%)",
        "fontFamily": "'Segoe UI', Helvetica, sans-serif",
        "padding": "36px 48px",
    },
    children=[
        # Header
        html.Div(
            style={"textAlign": "center", "marginBottom": "36px"},
            children=[
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={
                        "color": "#ff4d6d",
                        "fontSize": "2.8rem",
                        "fontWeight": "800",
                        "letterSpacing": "3px",
                        "margin": "0 0 6px 0",
                        "textShadow": "0 0 30px rgba(255,77,109,0.4)",
                    },
                ),
                html.P(
                    "Soul Foods · Pink Morsel Sales Analysis",
                    style={"color": "#6b7280", "fontSize": "0.9rem", "margin": 0, "letterSpacing": "1px"},
                ),
            ],
        ),

        # Stats row
        html.Div(
            id="stats-row",
            style={
                "display": "flex",
                "justifyContent": "center",
                "gap": "20px",
                "marginBottom": "28px",
            },
        ),

        # Controls row
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "marginBottom": "20px",
            },
            children=[
                html.Div(
                    style={
                        "background": "rgba(255,255,255,0.04)",
                        "borderRadius": "14px",
                        "padding": "14px 32px",
                        "display": "inline-flex",
                        "alignItems": "center",
                        "gap": "16px",
                        "border": "1px solid rgba(255,255,255,0.08)",
                        "boxShadow": "0 4px 20px rgba(0,0,0,0.3)",
                    },
                    children=[
                        html.Span(
                            "Filter by Region",
                            style={"color": "#9ca3af", "fontWeight": "600", "fontSize": "0.85rem", "letterSpacing": "1px"},
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": " All", "value": "all"},
                                {"label": " North", "value": "north"},
                                {"label": " East", "value": "east"},
                                {"label": " South", "value": "south"},
                                {"label": " West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            style={"color": "#e5e7eb"},
                            inputStyle={"marginRight": "5px", "accentColor": "#ff4d6d", "cursor": "pointer"},
                            labelStyle={"marginRight": "22px", "cursor": "pointer", "fontSize": "0.9rem"},
                        ),
                    ],
                )
            ],
        ),

        # Chart
        html.Div(
            style={
                "background": "rgba(255,255,255,0.03)",
                "borderRadius": "18px",
                "padding": "24px",
                "border": "1px solid rgba(255,255,255,0.07)",
                "boxShadow": "0 12px 48px rgba(0,0,0,0.5)",
            },
            children=[
                dcc.Graph(
                    id="sales-chart",
                    config={
                        "scrollZoom": True,
                        "displayModeBar": True,
                        "modeBarButtonsToRemove": ["select2d", "lasso2d"],
                        "displaylogo": False,
                    },
                    style={"height": "520px"},
                )
            ],
        ),

        html.P(
            "Tip: scroll to zoom · click and drag to pan · double-click to reset",
            style={"textAlign": "center", "color": "#374151", "fontSize": "0.78rem", "marginTop": "12px"},
        ),
    ],
)


def make_stat_card(label, value, color):
    return html.Div(
        style={
            "background": "rgba(255,255,255,0.04)",
            "borderRadius": "12px",
            "padding": "16px 28px",
            "border": f"1px solid {color}40",
            "boxShadow": f"0 4px 20px {color}20",
            "textAlign": "center",
            "minWidth": "160px",
        },
        children=[
            html.P(label, style={"color": "#6b7280", "fontSize": "0.75rem", "margin": "0 0 4px", "letterSpacing": "1px"}),
            html.P(value, style={"color": color, "fontSize": "1.4rem", "fontWeight": "700", "margin": 0}),
        ],
    )


@callback(
    Output("sales-chart", "figure"),
    Output("stats-row", "children"),
    Input("region-filter", "value"),
)
def update_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]
    grouped = filtered.groupby("date", as_index=False)["sales"].sum().sort_values("date")

    before = grouped[grouped["date"] < PRICE_INCREASE_DATE]["sales"].mean()
    after = grouped[grouped["date"] >= PRICE_INCREASE_DATE]["sales"].mean()
    change_pct = ((after - before) / before) * 100

    stats = [
        make_stat_card("AVG SALES BEFORE", f"${before:,.0f}", "#60a5fa"),
        make_stat_card("AVG SALES AFTER", f"${after:,.0f}", "#34d399"),
        make_stat_card("CHANGE", f"+{change_pct:.1f}%" if change_pct >= 0 else f"{change_pct:.1f}%", "#34d399" if change_pct >= 0 else "#f87171"),
    ]

    fig = px.line(
        grouped,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Total Sales ($)"},
    )
    fig.update_traces(
        line=dict(color="#ff4d6d", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(255,77,109,0.07)",
    )
    fig.add_vline(
        x=PRICE_INCREASE_DATE.timestamp() * 1000,
        line_dash="dash",
        line_color="#fbbf24",
        line_width=2,
        annotation_text="Price Increase · Jan 15, 2021",
        annotation_font_color="#fbbf24",
        annotation_font_size=12,
        annotation_position="top left",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="#9ca3af", size=12),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            zerolinecolor="rgba(0,0,0,0)",
            rangeslider=dict(visible=True, bgcolor="rgba(255,255,255,0.03)", bordercolor="rgba(255,255,255,0.1)"),
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=20, b=10),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1f2937", bordercolor="#374151", font_color="#e5e7eb"),
        dragmode="pan",
    )
    return fig, stats


if __name__ == "__main__":
    app.run(debug=True)
