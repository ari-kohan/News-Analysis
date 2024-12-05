"""
An interface to the LLM, using langchain and openai.    
"""

import getpass
import os
from typing import List
import bs4
from langchain import hub
import json

# from langchain_chroma import Chroma
# from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate


TEST_STR = "Ukraine’s top diplomat warned that the United States cannot afford to look weak in the face of increased threats from the deepening cooperation between Russia, North Korea and Iran, addressing lawmakers on Capitol Hill on Tuesday. Ukraine’s Foreign Minister Andrii Sybiha‎ was in Washington marking 1,000 days of Ukraine’s defensive war against Russia, warning against an “existential challenge” for Western democracies in confronting lawlessness from regimes in Moscow, Tehran and Pyongyang.  “Under these circumstances, the United States cannot afford to look weak. Russia, Iran, and North Korea will perceive any sign of weakness as an invitation to directly harm American interests and security,” Sybiha‎ warned during a hearing of the Helsinki Commission. The foreign minister’s remarks served as a signal to President-elect Trump, who has pledged to pursue peace through strength. But Trump’s criticism of U.S. spending on Ukraine has raised anxiety in Kyiv and among Ukraine’s supporters that his push to end the war could involve painful concessions to Russian President Vladimir Putin.  Sybiha also criticized Putin’s threats of nuclear weapons use as “blackmail,” following President Biden’s decision in recent days to green-light Ukraine using Western-provided missiles to strike targets deep inside Russia.  “Right now, we see new attempts by the Kremlin to use nuclear saber-rattling to scare the West. Their updated nuclear doctrine and public rhetoric on the use of nuclear weapons are nothing more than blackmail,” Sybiha said. “They have used it many times before when strong decisions were made. We must remain cold-headed, clear-eyed, and not give in to empty fear.”  A number of Trump allies have been highly critical of Biden's decision, saying it risks escalating the war and will make a peace deal harder to achieve. However, Republican lawmakers have been largely supportive of the move. Trump has talked about using his first days in office to end the war between Russia and Ukraine by bringing Putin and Ukrainian President Zelensky together for negotiations, but has provided little details on what a deal might look like. Zelensky has laid out a “Victory Plan” for Ukraine, with major points including NATO offering an invitation for Ukraine to join, and building up Ukraine’s military defenses to a level to deter any future, renewed Russian aggression. "
TEST_STR_2 = "Close Thank you for signing up! Subscribe to more newsletters here The latest in politics and policy. Direct to your inbox. Sign up for the Evening Report newsletter Subscribe 96<!- --> {beacon} Evening Report ©  Greg Nash Dems look beyond 2024 failures in leader search Democrats have begun their search for new leaders as they seek to reconnect with an electorate that chose President-elect Trump and relegated Democrats to minority status in both chambers of Congress.  FIRST UP — DNC BATTLE: There are several candidates and potential contenders to succeed Democratic National Committee (DNC) chairman Jaime Harrison.  Former Maryland Gov. Martin O’Malley.Minnesota Democratic-Farmer-Labor Party chair Ken Martin.Rahm Emanuel, the U.S. ambassador to Japan. Ben Wikler, chair of Wisconsin Democrats.Chuck Rocha, Democratic strategist. In the House, however, Democratic members voted Tuesday to keep their current leadership in place.  Members did not blame Rep. Hakeem Jeffries (D-N.Y.) for the party’s underwhelming performance on Election Day, as he received overwhelming support to return as House minority leader in the next Congress. Democrats also voted to keep Rep. Katherine Clark (D-Mass.) as Democratic whip, Rep. Pete Aguilar (D-Calif.) as caucus chair and Rep. Ted Lieu (D-Calif.) as the vice chair.  'WE LEARNED VERY LITTLE FROM 2016' The big question is where the party goes next after Trump cut deep into the Democratic coalition, winning support from working class voters and racial minorities on his way to a second term.  Rep. Dean Phillips (D-Minn.), who is one of only a handful who tried to challenge President Biden in a 2024 primary that was effectively squashed by party leaders, said Democrats have “learned very little from 2016.”  He said Democrats allowed themselves to be consumed by left-wing sloganeering and have become too insular, expelling anyone who doesn't pass ideological purity tests on quixotic social issues, while ignoring voter sentiments on border security for too long. “I believe Democrats have become, in many cases, a party centered on imposition and condemnation instead of invitation,” he told The Nation. And Phillips said Democrats have allowed themselves to be defined by their opposition to Trump, rather than putting out a forward-looking vision that voters find compelling.  “Condemnation is a very poor strategy for success in politics. Casting that same shadow on all of those that support him is just an absurd and destructive approach, the Minnesota Democrat said."
OPENAI_MODEL = ChatOpenAI(model="gpt-4o-mini")


SUMMARIZATION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="Summarize the following text in a few sentences"),
        HumanMessage(content="{text}"),
    ]
)

COMPARISON_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Compare the following two texts and determine if they are about the same event or not.
    The output should be formatted as json with the following format:
    {{
        same_event: true/false
    }}
    Text 1:
    {text1}
    Text 2:
    {text2}
    """
)

INFORMATION_EXTRACTION_TEMPLATE = ChatPromptTemplate.from_template(
    """.
    Extract the specified information from the provided text and format it in this json structure:
    {{
        summary: A 3-5 sentence summary of the text,
        people: A list of people mentioned in the text,
        places: A list of places mentioned in the text,
        organizations: A list of organizations mentioned in the text,
        agencies: A list of government agencies mentioned in the text,
        laws: A list of any laws mentioned in the text,
        climate: A list of any climate or climate change related information from the text
    }}
    If information relevant to one of the categories is not present in the text, store the value as an empty list []
    Text:
    {text}
    """
)


def summarize_text(text: str) -> str:
    return OPENAI_MODEL.invoke(
        SUMMARIZATION_TEMPLATE.format_messages(text=text)
    ).content


def compare_texts(text1: str, text2: str) -> str:
    # print(COMPARISON_TEMPLATE.format_messages(text1=text1, text2=text2))
    return OPENAI_MODEL.invoke(
        COMPARISON_TEMPLATE.format_messages(text1=text1, text2=text2)
    ).content

def extract_information(text: str) -> str:
    return OPENAI_MODEL.invoke(
        INFORMATION_EXTRACTION_TEMPLATE.format_messages(text=text)
    ).content


if __name__ == "__main__":
    with open("rss_feed.json", "r") as f:
        data = json.load(f)
        news = data[0]
        #print(extract_information(news["content"].replace("\n", " ")))
        print(compare_texts(TEST_STR, TEST_STR_2))