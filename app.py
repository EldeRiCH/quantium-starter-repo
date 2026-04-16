import pandas as pd
from dash import Dash, dcc, html, callback, Output, Input
import plotly.express as px

df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])

app = Dash(__name__)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        "fontFamily": "'Segoe UI', sans-serif",
        "padding": "30px",
    },
    children=[
        html.Div(
            style={"textAlign": "center", "marginBottom": "30px"},
            children=[
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={
                        "color": "#e94560",
                        "fontSize": "2.5rem",
                        "fontWeight": "700",
                        "letterSpacing": "2px",
                        "margin": "0 0 8px 0",
                    },
                ),
                html.P(
                    "Soul Foods · Pink Morsel Sales Analysis",
                    style={"color": "#a0a0b0", "fontSize": "0.95rem", "margin": 0},
                ),
            ],
        ),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "marginBottom": "24px",
            },
            children=[
                html.Div(
                    style={
                        "background": "rgba(255,255,255,0.05)",
                        "borderRadius": "12px",
                        "padding": "14px 28px",
                        "display": "inline-flex",
                        "alignItems": "center",
                        "gap": "12px",
                        "border": "1px solid rgba(255,255,255,0.1)",
                    },
                    children=[
                        html.Span(
                            "Region:",
                            style={
                                "color": "#a0a0b0",
                                "fontWeight": "600",
                                "marginRight": "8px",
                            },
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
                            style={"color": "#e0e0f0"},
                            inputStyle={"marginRight": "4px", "accentColor": "#e94560"},
                            labelStyle={"marginRight": "20px", "cursor": "pointer"},
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            style={
                "background": "rgba(255,255,255,0.04)",
                "borderRadius": "16px",
                "padding": "20px",
                "border": "1px solid rgba(255,255,255,0.08)",
                "boxShadow": "0 8px 32px rgba(0,0,0,0.4)",
            },
            children=[dcc.Graph(id="sales-chart")],
        ),
    ],
)


@callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]
    grouped = filtered.groupby("date", as_index=False)["sales"].sum().sort_values("date")

    fig = px.line(
        grouped,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Total Sales ($)"},
    )
    fig.update_traces(line=dict(color="#e94560", width=2))
    fig.add_vline(
        x=pd.Timestamp("2021-01-15").timestamp() * 1000,
        line_dash="dash",
        line_color="#f5a623",
        annotation_text="Price Increase (Jan 15, 2021)",
        annotation_font_color="#f5a623",
        annotation_position="top left",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="#c0c0d0"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode="x unified",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
