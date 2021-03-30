from pathlib import Path
from typing import List

import pandas as pd
import plotly.graph_objects as go

"""
TODO
 * Sort on q<NUM> to have questions listed in order (both plot types)
 * Have numeric values on radial axis be labels indicating "yes", "no", etc. instead. (radar plot)
"""


def create_radar_plot(data_file: Path, company_names: List[str], language: str = "en",
                      enumerate_questions: bool = True) -> None:
    df = read_data(data_file, language=language)
    question_column = "Question_text"
    if enumerate_questions:
        question_column = "Question_text_enum"

    categories = df[question_column].unique().tolist()

    answers_per_company: List[List[str]] = []

    for company_name in company_names:
        company_answers = df.loc[df["Company"] == company_name, "Answer"].values
        answers_per_company.append(company_answers)

    fig = go.Figure()

    for index, answers in enumerate(answers_per_company):
        fig.add_trace(go.Scatterpolar(
            r=answers,
            theta=categories,
            fill="toself",
            name=company_names[index]
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


def create_parallel_plot(data_file: Path, language: str = "en", enumerate_questions: bool = True) -> None:
    df = read_data(data_file, language=language)

    question_column = "Question_text"
    if enumerate_questions:
        question_column = "Question_text_enum"

    qs = df[question_column].unique().tolist()
    df["aux"] = df.groupby(question_column).cumcount()
    df = df.pivot(index="aux", columns=question_column, values="Answer")

    dims = [dict(range=[0, 3], label=v, values=df[v]) for v in qs]

    # Missing a column with the company names; it should be used instead of the index for coloring and labelling.
    fig = go.Figure(data=go.Parcoords(
        line=dict(color=df.index,
                  colorscale=[[0, 'purple'], [0.5, 'lightseagreen'], [1, 'gold']]),
        dimensions=dims))

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    fig.show()


def read_data(csv_file: Path, company: str = None, language: str = "en") -> pd.DataFrame:
    df = pd.read_csv(csv_file)
    df_questions = pd.read_csv(Path(f"../data/questions_{language}.csv"))
    df = df[df["Applicable"] != False]
    if company:
        df = df[df["Company"] == company]
    df = pd.merge(df, df_questions, how="inner", on="Question")
    df["Question_text_enum"] = df['Question'].astype(str) + ": " + df['Question_text']
    return df


if __name__ == "__main__":
    data_file = Path("../data/data-nv.csv")
    language = "sv"
    company_names = ["NV start", "NV mid"]
    create_radar_plot(data_file, company_names, language=language, enumerate_questions=True)
