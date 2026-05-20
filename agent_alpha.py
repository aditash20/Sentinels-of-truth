from pydantic import BaseModel, Field
from tavily import TavilyClient

from typing import Optional, Literal
from datetime import datetime
import uuid
from dotenv import load_dotenv
from state.state_class import VerificationReport
import os

from groq import Groq


load_dotenv()

class AgentAlpha:

    def __init__(self):
        self.client = Groq(
                api_key=os.environ.get("GROQ_API_KEY"),
            )
        self.tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

    def tavily_web_search(self, user_query):

        web_search_output = self.tavily_client.search(query=user_query, search_depth="basic", max_results=10)

        return web_search_output

    def run(self, user_query, message_id: str = None):

        
        web_search_output = self.tavily_web_search(user_query=user_query)

        if web_search_output["results"] is not None:

            web_search_context = "\n\n".join([
                f"Source: {r['url']}\n{r['content']}" 
                for r in web_search_output['results']
            ])


        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"""You are Agent Alpha, a fact-checker for an Indian news agency.
        Given a claim and web search results, return a VerificationReport JSON.
        Schema: {VerificationReport.model_json_schema()}"""
                },
                {
                    "role": "user",
                    "content": f"""Claim: {user_query}\n\nEvidence:\n{web_search_context}"""
                }
            ],
            model="openai/gpt-oss-120b",
            temperature=0.1,
            response_format={"type": "json_object"} 
        )
        try:

            report = VerificationReport.model_validate_json(
                chat_completion.choices[0].message.content
            )

            return report
        
        except Exception as e:

            print(e)
            # return report

if __name__ == "__main__":

    input = "is pm narendra modi bengali"

    agent_alpha = AgentAlpha()

    output = agent_alpha.run(user_query=input)

    print(output)

