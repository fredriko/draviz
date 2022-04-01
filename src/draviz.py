"""
This program generates radar charts for displaying the answers to questions about data readiness.
"""
import argparse
import pathlib
from collections import OrderedDict
from pathlib import Path
from typing import List, Dict, Tuple

import pandas as pd
import plotly.graph_objects as go


def get_answer_string(answer: int, answer_map: Dict[int, str]) -> str:
    return answer_map.get(answer, "Undefined")


def create_radar_plot(questions_file: Path, answers_file: Path, phases: List[str], language: str = "en",
                      enumerate_questions: bool = True) -> None:
    df, answers_list = read_data(questions_file, answers_file, language=language)
    question_column = "Question_text"
    if enumerate_questions:
        question_column = "Question_text_enum"

    categories = df[question_column].unique().tolist()

    answers_per_phase: List[Tuple[List[str], List[str]]] = []

    for phase in phases:
        phase_answers_int = df.loc[df["Phase"] == phase, "Answer"].values
        phase_answers_str = df.loc[df["Phase"] == phase, "Answer_text"].values
        answers_per_phase.append((phase_answers_int, phase_answers_str))

    fig = go.Figure()

    for index, answers in enumerate(answers_per_phase):
        fig.add_trace(go.Scatterpolar(
            r=answers[0],
            theta=categories,
            fill="toself",
            name=phases[index],
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
                range=[0, 3]
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


def read_data(questions_file: Path, answers_file: Path, company: str = None, language: str = "en") -> Tuple[
    pd.DataFrame, List[str]]:
    df = pd.read_csv(answers_file)
    df_questions = pd.read_csv(questions_file)
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
    df["Answer_text"] = df["Answer"].apply(lambda x: dd.get(int(x), "Undefined"))
    return df, list(dd.values())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-q", "--questions",
                        type=pathlib.Path,
                        help="A CSV file containing the questions about data readiness.",
                        required=True)
    parser.add_argument("-a", "--answers",
                        type=pathlib.Path,
                        help="A CSV file containing the answers to the questions about data readiness.",
                        required=True)
    parser.add_argument("-l", "--language",
                        type=str,
                        help="ISO 639-1 code of the language used for marking labelling the axes in the radar chart.",
                        choices=["en", "sv"],
                        default="en")
    parser.add_argument("-p", "--phases",
                        type=str,
                        help="A comma separated list of the phases to include in the radar chart. The phases available "
                             "depend on the values in the 'Phases' column of the file answer file specified.",
                        required=True)

    args = parser.parse_args()
    questions = args.questions
    answers = args.answers
    language = args.language
    phases = args.phases
    if phases is not None:
        phases = phases.split(",")

    create_radar_plot(questions, answers, phases, language=language, enumerate_questions=True)


if __name__ == "__main__":
    main()
