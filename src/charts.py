from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def radar_mock_px() -> None:
    data = Path("../data/data.csv").resolve()
    df = read_data(data, company="Acme")
    fig = px.line_polar(df, r='Answer', theta='Question', line_close=True)
    fig.update_traces(fill='toself')
    fig.show()


def radar_mock_go(show_all: bool = False) -> None:
    data = Path("../data/data.csv").resolve()
    df = read_data(data)
    categories = df["Question_text"].unique().tolist()
    acme_values = df.loc[df["Company"] == "Acme", "Answer"].values
    skunk_values = df.loc[df["Company"] == "Skunk Works", "Answer"].values
    print(skunk_values)
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=acme_values,
        theta=categories,
        fill="toself",
        name="Acme"
    ))

    if show_all:
        fig.add_trace(go.Scatterpolar(
            r=skunk_values,
            theta=categories,
            fill="toself",
            name="Skunk Works"
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3]
            )
        ),
        showlegend=False
    )
    fig.show()


def read_data(csv_file: Path, company: str = None) -> pd.DataFrame:
    df = pd.read_csv(csv_file)
    if company:
        df = df[df["Company"] == company]
    return df


if __name__ == "__main__":
    radar_mock_go(show_all=False)
