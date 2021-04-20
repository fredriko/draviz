from collections import OrderedDict
from pathlib import Path
from typing import List, Dict, Tuple

import pandas as pd
import plotly.graph_objects as go


def get_answer_string(answer: int, answer_map: Dict[int, str]) -> str:
    return answer_map.get(answer, "Undefined")


def create_radar_plot(data_file: Path, company_names: List[str], language: str = "en",
                      enumerate_questions: bool = True) -> None:
    df, answers_list = read_data(data_file, language=language)
    question_column = "Question_text"
    if enumerate_questions:
        question_column = "Question_text_enum"

    categories = df[question_column].unique().tolist()

    answers_per_company: List[Tuple[List[str], List[str]]] = []

    for company_name in company_names:
        company_answers_int = df.loc[df["Company"] == company_name, "Answer"].values
        company_answers_str = df.loc[df["Company"] == company_name, "Answer_text"].values
        answers_per_company.append((company_answers_int, company_answers_str))

    fig = go.Figure()

    for index, answers in enumerate(answers_per_company):
        fig.add_trace(go.Scatterpolar(
            r=answers[0],
            theta=categories,
            fill="toself",
            name=company_names[index],
            text=answers[1],
            hoverinfo="text"
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                tickmode="array",
                tickvals=[0, 1, 2, 3],
                ticktext=answers_list,
                range=[0,3]
            ),
            angularaxis=dict(
                direction="clockwise"
            )
        ),
        showlegend=False,
        font=dict(size=24)
    )

    config = {
        'toImageButtonOptions': {
            'format': 'png',  # one of png, svg, jpeg, webp
            'filename': 'custom_image',
            'height': 1000,
            'width': 1800,
            'scale': 1,  # Multiply title/legend/axis/canvas sizes by this factor,
        }
    }
    fig.show(config=config)


def create_parallel_plot(data_file: Path, language: str = "en", enumerate_questions: bool = True) -> None:
    df, answers_list = read_data(data_file, language=language)

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


def read_data(csv_file: Path, company: str = None, language: str = "en") -> Tuple[pd.DataFrame, List[str]]:
    df = pd.read_csv(csv_file)
    df_questions = pd.read_csv(Path(f"../data/questions_{language}.csv"))
    df = df[df["Applicable"] != False]
    if company:
        df = df[df["Company"] == company]
    df = pd.merge(df, df_questions, how="inner", on="Question")
    df["Question_text_enum"] = df["Question"].astype(str) + ": " + df["Question_text"]

    dd = OrderedDict()
    if language == "en":
        dd: Dict[int, str] = {
            0: "Don't know",
            1: "No",
            2: "Partially",
            3: "Yes"
        }
    else:
        dd: Dict[int, str] = {
            0: "Vet inte",
            1: "Nej",
            2: "Delvis",
            3: "Ja"
        }
    df["Answer_text"] = df["Answer"].apply(lambda x: dd.get(x, "Undefined"))
    return df, list(dd.values())


if __name__ == "__main__":
    #data_file = Path("../data/data-nv.csv")
    data_file = Path("../data/data.csv")
    language = "en"
    #company_names = ["Projektstart"]
    #company_names = ["Mitten av projektet"]
    #company_names = ["Projektstart", "Mitten av projektet"]
    company_names = ["Acme"]
    create_radar_plot(data_file, company_names, language=language, enumerate_questions=True)
    #create_parallel_plot(data_file, language=language)
