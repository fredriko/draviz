from collections import OrderedDict
from typing import Dict

import plotly.graph_objects as go
import streamlit as st


def create_plot(answers: Dict[str, int], answer_dict: Dict[int, str]) -> None:
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[v for k, v in answers.items() if v != 4],
        theta=[k for k, v in answers.items() if v != 4],
        fill="toself",
        # name=phase,
        text=[k for k, v in answers.items() if v != 4],
        hoverinfo="text"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                tickmode="array",
                tickvals=[0, 1, 2, 3],
                ticktext=list(answer_dict.values()),
                range=[0, 3]
            ),
            angularaxis=dict(
                direction="clockwise"
            )
        ),
        showlegend=False,
        font=dict(size=16)
    )

    st.plotly_chart(fig)


def main():
    st.title("Data Readiness Assessment")

    langs: Dict[str, str] = {
        'English': 'en',
        'Svenska': 'sv'
    }
    lang_select = st.selectbox('Please choose language', list(langs.keys()))
    language = langs[lang_select]

    dd = OrderedDict()
    if language == "en":
        dd: Dict[int, str] = {
            0: "Don't know",
            1: "No",
            2: "Partially",
            3: "Yes",
            4: "Not relevant"
        }
    else:
        dd: Dict[int, str] = {
            0: "Vet inte",
            1: "Nej",
            2: "Delvis",
            3: "Ja",
            4: "Inte relevant"
        }

    qq = OrderedDict()
    if language == "en":
        qq: Dict[str, str] = {
            "Programmatic access to data": "Do you have programmatic access to the data?",
            "Licenses in order": "Are your licenses in order?",
            "Lawful access to data": "Do you have lawful access to the data?",
            "Ethics assessment of data": "Has there been an ethics assessment of the data?",
            "Converted to suitable format": "Is the data converted to an appropriate format?",
            "Characteristics known": "Are the characteristics of the data known?",
            "Validated data": "Is the data validated?",
            "Stakeholders agree on business need": "Do stakeholders agree on the objective of the current use case?",
            "Purpose of data clear": "Is the purpose of using the data clear to all stakeholders?",
            "Sufficient data for the use case": "Is the data sufficient for the current use case?",
            "Evaluation steps clear": "Are the steps required to evaluate a potential solution clear?",
            "Data acquisition over time": "Is your organization prepared to handle more data like this beyond the scope of the project",
            "Data secured": "Is the data secured?",
            "Risk free sharing": "Is it safe to share the data with others?",
            "Allowed to share": "Are you allowed to share the data with others?"
        }
    else:
        qq: Dict[str, str] = {
            "Programmatisk åtkomst": "Har ni programmatisk åtkomst till datan?",
            "Licenser i ordning": "Är era licenser i ordning?",
            "Laglig rätt till åtkomst": "Har ni laglig rätt till dataåtkomst?",
            "Etikprövad data": "Har ni genomfört en etikprövning av datan?",
            "Konverterad till lämpligt format": "Är datan konverterad till ett lämpligt format?",
            "Känd karaktäristik": "Är datans karaktäkistik känd?",
            "Validerad data": "Är datan validerad?",
            "Parter överens om affärsbehov": "Är parterna överens om målet för aktuellt användningsfall?",
            "Syftet med data klart": "Är syftet med att använda datan tydlig för alla parter?",
            "Tillräckligt med data": "Finns det tillräckligt med data för aktuellt användningsfall?",
            "Utvärdering av lösning klar": "Är stegen för att utvärdera en möjlig lösning tydliga?",
            "Organisationen hanterar datainsamling": "Är er organisation beredd på att hantera mer liknande data bortom projektets omfattning?",
            "Datasäkerhet hanterad": "Är datan säker?",
            "Riskfri delning av data": "Är det säkert att dela datan med andra?",
            "Tillåten att dela data": "Har ni tillåtelse att dela datan med andra?"
        }

    answers = OrderedDict()
    for (k, v) in qq.items():
        ans_val = st.radio(v, dd.values())
        answers[k] = [k for k, v in dd.items() if v == ans_val][0]

    create_plot(answers, dd)


if __name__ == "__main__":
    main()
