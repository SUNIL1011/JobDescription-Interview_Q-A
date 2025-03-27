from typing_extensions import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict
import os
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from IPython.display import Markdown
import streamlit as st
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
class State(TypedDict):
    input: str
    userstory : str
    product_owner_review: str
    product_owner_feedback : str
    revise_user_stories :str
    create_design_document :str
    revise_design_document :str
    generated_code :str
    review_generated_code : str
    security_reviewed_code : str
    bug_fixed_code : str
    write_test_cases : str
    fix_security_code : str
    review_test_cases : str
    quality_assurance_testing : str
    fix_test_case_after_review : str
    
    



llm=ChatGroq(model="qwen-2.5-32b")
#llm = ChatOpenAI(model="gpt-4o")
workflow = StateGraph(State)

def User_Input_Requirement(state: State):
    """LLM call to create an initial user requirement"""

    msg = llm.invoke(f"Create an initial user requirement {state['input']}")
    return {"userstory": msg.content}



def Create_User_Stories(state: State):
    """LLM call to create user stories"""

    msg = llm.invoke(f"Create user stories based on  {state['userstory']}")
    return {"product_owner_review": msg.content}


def Product_Owner_Review(state: State):
    """LLM call to decide if the review if the user stories is good or bad"""

    msg = llm.invoke(f"Review user stories based on  {state['product_owner_review']}")
    return {"product_owner_feedback": msg.content}

def Check_Owner_Review(state: State):
    """Gate function to check if the product owner review is good"""

    # Simple check - does the feedback contain "bad" or "needs improvement"
    if "bad" in state["product_owner_feedback"] or "needs improvement" in state["product_owner_feedback"]:
        return "Fail"
    return "Pass"

def Revise_User_Stories(state: State):
    """LLM call to decide if the review the user stories is good or bad"""

    msg = llm.invoke(f"Revise user stories based on  {state['product_owner_feedback']}")
    return {"revise_user_stories": msg.content}

def Create_Design_Document(state: State):
    """LLM call to create a design document"""

    msg = llm.invoke(f"Review user stories based on  {state['product_owner_feedback']}")
    return {"create_design_document": msg.content}

def Revise_Design_Document(state: State):
    """LLM call to revise design document"""

    msg = llm.invoke(f"Review user stories based on  {state['create_design_document']}")
    return {"revise_design_document": msg.content}

def Check_Revised_Design_Document(state: State):
    """Gate function to check if the reviewed design document is good"""

    # Simple check - does the feedback contain "bad" or "needs improvement"
    if "bad" in state["revise_design_document"] or "needs improvement" in state["revise_design_document"]:
        return "Fail"
    return "Pass"

def Generate_Code(state: State):
    """LLM call to create the code"""

    msg = llm.invoke(f"Create a code based on the revised design document {state['revise_design_document']}")
    return {"generated_code": msg.content}

def Code_Review(state: State):
    """LLM call to create the code"""

    msg = llm.invoke(f"Review the code based on the generated code {state['generated_code']}")
    return {"review_generated_code": msg.content}

def Check_Code_Review(state: State):
    """Gate function to check if the reviewed code is good"""

    # Simple check - does the feedback contain "bad" or "needs improvement"
    if "bad" in state["review_generated_code"] or "needs improvement" in state["review_generated_code"]:
        return "Fail"
    return "Pass"

def Security_Review(state: State):
    """LLM call to create the code"""

    msg = llm.invoke(f"Create a code based on the revised design document {state['review_generated_code']}")
    return {"security_reviewed_code": msg.content}

def Bug_Fixes(state: State):
    """LLM call to decide if the code needs bug fixes"""

    msg = llm.invoke(f"Provide bug fixes to code as per the code review {state['review_generated_code']}")
    return {"bug_fixed_code": msg.content}

def Check_Security_Review(state: State):
    """Gate function to check if the security of the reviewed code is good"""

    # Simple check - does the feedback contain "bad" or "needs improvement"
    if "bad" in state["security_reviewed_code"] or "needs improvement" in state["security_reviewed_code"]:
        return "Fail"
    return "Pass"

def Write_Test_Cases(state: State):
    """LLM call to decide if the code needs bug fixes"""

    msg = llm.invoke(f"Provide test cases to the security reviewed code based on the {state['security_reviewed_code']}")
    return {"write_test_cases": msg.content}

def Fix_Code_Review_After_Security(state: State):
    """LLM call to decide if the code needs bug fixes"""

    msg = llm.invoke(f"Fix the code as per the security reviewed code based on the {state['security_reviewed_code']}")
    return {"fix_security_code": msg.content}

def Review_Test_Cases(state: State):
    """LLM call to create the code"""

    msg = llm.invoke(f" Review the test cases based on the {state['security_reviewed_code']}")
    return {"review_test_cases": msg.content}

def Check_Test_Cases(state: State):
    """Gate function to check if the review of test cases is good"""

    # Simple check - does the feedback contain "bad" or "needs improvement"
    if "bad" in state["review_test_cases"] or "needs improvement" in state["review_test_cases"]:
        return "Fail"
    return "Pass"

def QA_Testing(state: State):
    """LLM call to do the quality assurance testing"""

    msg = llm.invoke(f"Conduct a quality assuarance testing based on  {state['review_test_cases']}")
    return {"quality_assurance_testing": msg.content}

def Fix_Test_Cases_After_Review(state: State):
    """LLM call to decide if the code needs bug fixes"""

    msg = llm.invoke(f"Provide fixes to the code after the review based on the {state['review_test_cases']}")
    return {"fix_test_case_after_review": msg.content}






# Add nodes
workflow.add_node("User_Input_Requirement", User_Input_Requirement)
workflow.add_node("Create_User_Stories", Create_User_Stories)
workflow.add_node("Product_Owner_Review", Product_Owner_Review)
workflow.add_node("Create_Design_Document", Create_Design_Document)
workflow.add_node("Revise_User_Stories", Revise_User_Stories)
workflow.add_node("Revise_Design_Document", Revise_Design_Document)
workflow.add_node("Generate_Code",Generate_Code)
workflow.add_node("Code_Review",Code_Review)
workflow.add_node("Security_Review",Security_Review)
workflow.add_node("Bug_Fixes",Bug_Fixes)
workflow.add_node("Write_Test_Cases",Write_Test_Cases)
workflow.add_node("Fix_Code_Review_After_Security",Fix_Code_Review_After_Security)
workflow.add_node("Review_Test_Cases",Review_Test_Cases)
workflow.add_node("QA_Testing",QA_Testing)
workflow.add_node("Fix_Test_Cases_After_Review",Fix_Test_Cases_After_Review)

# Add edges to connect nodes
workflow.add_edge(START, "User_Input_Requirement")
workflow.add_edge("User_Input_Requirement", "Create_User_Stories")
workflow.add_edge("Create_User_Stories", "Product_Owner_Review")
workflow.add_conditional_edges("Product_Owner_Review",Check_Owner_Review,{"Fail":"Revise_User_Stories","Pass":"Create_Design_Document"})
workflow.add_edge("Revise_User_Stories", "Create_User_Stories")
workflow.add_edge("Create_Design_Document", "Revise_Design_Document")
workflow.add_conditional_edges("Revise_Design_Document",Check_Revised_Design_Document,{"Fail":"Create_Design_Document","Pass":"Generate_Code"})
workflow.add_edge("Generate_Code", "Code_Review")
workflow.add_conditional_edges("Code_Review",Check_Code_Review,{"Fail":"Bug_Fixes","Pass":"Security_Review"})
workflow.add_edge("Bug_Fixes", "Generate_Code")
workflow.add_conditional_edges("Security_Review",Check_Security_Review,{"Fail":"Fix_Code_Review_After_Security","Pass":"Write_Test_Cases"})
workflow.add_edge("Fix_Code_Review_After_Security", "Generate_Code")
workflow.add_edge("Write_Test_Cases","Review_Test_Cases")
workflow.add_conditional_edges("Review_Test_Cases",Check_Security_Review,{"Fail":"Fix_Test_Cases_After_Review","Pass":"QA_Testing"})
workflow.add_edge("Fix_Test_Cases_After_Review","Write_Test_Cases")
workflow.add_edge("QA_Testing",END)

workflow = workflow.compile()
workflow.get_graph().draw_mermaid_png(output_file_path="langgraph_SDLC.png")

st.title("🤖 LLM Based SDLC WORKFLOW ")
st.subheader(
    "LLM-based SDLC WORKFLOW"
)

# Sidebar setting
st.sidebar.title("App Workflow")
st.sidebar.image("langgraph_SDLC.png")





query = st.text_input("What is your use case")

if st.button("START WORKFLOW"):
    if query:
        # Invoke LLM Workflow
        state = workflow.invoke({"input": query})
        with st.spinner("Processing your WORKFLOW... 🎭"):
            state = workflow.invoke({"input": query})
        st.write(state["input"])

        with st.expander("📌 INPUT "):
            st.write(state["input"])
        
        with st.expander("📌 USER STORY"):
            st.write(state["userstory"])
        
        
        
        with st.expander("📌 CODE"):
            st.write(state["generated_code"])
        

        st.download_button("📥 Dowload code", state["generated_code"], file_name="generated_code.txt")
        st.markdown("### 🔗 Powered by LangGraph with Prompt Chaining Workflow 🚀")
        st.write("This AI-driven app analyzes and improves business pitches using advanced prompt chaining techniques.")









