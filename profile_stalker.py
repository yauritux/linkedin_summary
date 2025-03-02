import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary


def summarize_linkedin(name: str) -> Summary:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    summary_template = """
        given the Linkedin information {information} about a person from I want you to create:
        1. grab the photo image url
        2. a short summary
        3. two interesting facts about them
        
        Use information from Linkedin and output the summary and facts in the following format:
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", streaming=True)
    # llm = ChatOllama(model="qwen2:latest")
    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data})
    print(res)
    return res


if __name__ == "__main__":
    print("Profile Stalker")
    print(os.environ["OPENAI_API_KEY"])

    os.environ["LANGCHAIN_TRACING_V2"] = "false"

    import sys

    if len(sys.argv) > 1:
        name = sys.argv[1]
        response = summarize_linkedin(name)
        if hasattr(response, "summary") and hasattr(response, "facts"):
            print("Summary:\n")
            print(response.summary)
            print("\nFacts:\n")
            print(response.facts)
        else:
            print(response)
    else:
        print("Please provide a name as a command-line argument.")
