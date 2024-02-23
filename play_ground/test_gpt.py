import os

import yaml
from langchain_community.agent_toolkits import JsonToolkit, create_json_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools.json.tool import JsonSpec
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


def get_agent(template):
    
    prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    agent = prompt | llm | StrOutputParser()
    return agent


def create_user_story(requirement):
    template = """
    You are a experienced BA who works for Open Banking Project.
    
    You have below back ground knowledge:
    -[] The API name is Get Accounts
    -[] Only Data recipient have valid access token conatins valid scope can request this API
    -[] API has below query parameters
        Name                Type                Required       Description
        product-category    string              optional       Used to filter results on the productCategory field applicable to accounts. Any one of the valid values for this field can be supplied. If absent then all accounts returned.)
        open-status         string              optional       Used to filter results according to open/closed status. Values can be OPEN, CLOSED or ALL. If absent then ALL is assumed
        is-owned            Boolean             optional       Filters accounts based on whether they are owned by the authorised customer. True for owned accounts, false for unowned accounts and absent for all accounts
        page                PositiveInteger     optional       Page of results to request (standard pagination)。 Must less than 1000
        page-size           PositiveInteger     optional       Page size to request. Default is 25 (standard pagination). Must less than 1000
    -[] API has below headers
        Name                        Type                Required       Description
        x-v                         string              mandatory      Version of the API end point requested by the client. Must be set to a positive integer. The data holder should respond with the highest supported version between x-min-v and x-v. If the value of x-min-v is equal to or higher than the value of x-v then the x-min-v header should be treated as absent. If all versions requested are not supported then the data holder must respond with a 406 Not Acceptable. See HTTP Headers
        x-min-v                     string              mandatory      Minimum version of the API end point requested by the client. Must be set to a positive integer if provided. The data holder should respond with the highest supported version between x-min-v and x-v. If all versions requested are not supported then the data holder must respond with a 406 Not Acceptable.
        x-fapi-interaction-id       string              optional       An [RFC4122] UUID used as a correlation id. If provided, the data holder must play back this value in the x-fapi-interaction-id response header. If not provided a [RFC4122] UUID value is required to be provided in the response header to track the interaction.
        x-fapi-auth-date            string              conditional    The time when the customer last logged in to the Data Recipient Software Product as described in [FAPI-1.0-Baseline]. Required for all resource calls (customer present and unattended). Not required for unauthenticated calls.
        x-fapi-customer-ip-address  string              optional       The customer's original IP address if the customer is currently logged in to the Data Recipient Software Product. The presence of this header indicates that the API is being called in a customer present context. Not to be included for unauthenticated calls.
        x-cds-client-headers        Base64              conditional    The customer's original standard http headers Base64 encoded, including the original User Agent header, if the customer is currently logged in to the Data Recipient Software Product. Mandatory for customer present calls. Not required for unattended or unauthenticated calls.
    
    Please help me write user story from blow requirement:
    {requirement}
    
    Please list all the user story in detail with number. Must include all the positive and negative scenarios
    """
    agent = get_agent(template)
    return agent.invoke({"requirement": requirement})


def create_test_scenario(requirement):
    template = """
    You are a experienced tester who works for Open Banking Project. 
    
    Please help write BDD test scenario based on below requirement:
    {requirement}
    
    Please write anything in detail level and list the scenarios number, must include all the positive and negative scenarios. must use tables for required data to be supplied for each scenarios. must write in BDD style format for each scenarios
    """
    agent = get_agent(template)
    return agent.invoke({"requirement": requirement})


def convert_test_case(scenario):
    template = """
    You are an assistant to help me to convert the provided BDD style test scenario to cucumber feature file 

    Please generate cucumber feature file based on the following cucumber statement:
    (SET|UPDATE|DELETE) request '(|Header|Path|Query) parameter'
    TPP send '(GET|POST|PUT|DELETE)' request to '(.*)' endpoint
    TPP send '(GET|POST|PUT|DELETE)' request to '(.*)' endpoint without proxy
    TPP send '(GET|POST|PUT|DELETE)' request to '(.*)' endpoint with payload '(.*)' ( without proxy)?
    TPP receive response with status code '(\\d+)'
    retrieve access token with scope '(.*)'

    Test Scenario:
    {scenario}
    """
    agent = get_agent(template)
    return agent.invoke({"scenario": scenario})


def get_json_agent(json_path: str):

    with open(json_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    json_spec = JsonSpec(dict_=data, max_value_length=4000)
    json_toolkit = JsonToolkit(spec=json_spec)

    json_agent = create_json_agent(
        llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613"),
        toolkit=json_toolkit,
        verbose=True
    )
    return json_agent
