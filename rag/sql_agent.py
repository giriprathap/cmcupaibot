from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from rag.data_store import get_datastore
import os
from dotenv import load_dotenv

load_dotenv()

def get_sql_agent():
    """
    Creates a LangChain SQL Agent connected to the in-memory SQLite DB.
    Restricted to specific tables/views for security.
    """
    ds = get_datastore()
    if not ds.initialized:
        ds.init_db()

    # Create SQLDatabase wrapper around the existing sqlite3 connection
    # URI for memory is slightly tricky with LangChain, but we can pass the engine/connection if using SQLAlchemy.
    # However, LangChain SQLDatabase usually takes a URI.
    # Since we are using an in-memory sqlite3 connection shared across threads (check_same_thread=False),
    # we might need to use the 'creator' argument with SQLAlchemy to use the *same* raw connection, 
    # OR simpler: Dump to a file-based DB if memory is too hard to share, 
    # OR just use the text-to-sql on the pandas dataframes (PandasDataFrameAgent).
    
    # BUT, LangChain SQLDatabase prefers a SQLAlchemy engine.
    # A workaround for shared in-memory DB:
    # We will assume for this implementation we can just re-connect or use a fresh memory DB if we loaded it fast.
    # But wait, 'data_store' loads it once.
    
    # Actually, the best way for this specific codebase (which uses raw sqlite3) 
    # is to probably use a lightweight custom chain that uses `ds.query` 
    # instead of the heavy SQLDatabase which expects SQLAlchemy.
    
    # Let's write a simple Custom SQL Chain using our DS to avoid SQLAlchemy complexity with existing raw connection.
    pass

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def run_sql_agent(user_query: str):
    """
    Executes a Text-to-SQL run using the secure view.
    """
    ds = get_datastore()
    if not ds.initialized: ds.init_db()
    
    # 1. Get Schema Info (Restricted)
    # We only show the 'view_player_unified' schema
    schema_info = """
    Table: view_player_unified
    Columns:
    - player_nm (Text)
    - player_reg_id (Text)
    - mobile_no (Text)
    - gender (Text)
    - player_age (Text)
    - villagename (Text)
    - mandalname (Text)
    - districtname (Text)
    - clustername (Text)
    - sport_name (Text): e.g. Cricket, Kabaddi
    - event_name (Text)
    - venue (Text)
    - match_date (Text)
    
    Table: view_sport_rules
    Columns:
    - sport_name (Text): e.g. Hockey, Cricket
    - min_age (Integer): Minimum age allowed
    - max_age (Integer): Maximum age allowed
    - team_size (Integer)
    - is_para (Integer): 1 if para sport
    """
    
    # 2. LLM Setup
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    import datetime
    current_year = datetime.datetime.now().year
    
    # 3. Prompt
    template = f"""You are a specialized SQL expert for a Sports Chatbot.
    Your job is to answer the user's question by generating and executing a SQL query against the database.
    
    Current Year: {current_year}
    
    Database Schema:
    {{schema}}
    
    Security Rules:
    1. NEVER output a list of mobile numbers. If asked, refuse or summarize.
    2. Only SELECT columns relevant to the question.
    3. Use 'LIKE' for text matching (case-insensitive usually).
    4. Return the Final Answer based on the query result.
    
    Query Logic Guidelines:
    1. If the user provides a "Birth Year", calculate the Age (Current Year - Birth Year) implicitly.
       - Example: "Born in 2008" -> Age = {current_year} - 2008 = <age>.
       - Then query: SELECT ... WHERE <age> BETWEEN min_age AND max_age
    
    Output Formatting Rules:
    1. If the result is a LIST of items (e.g., players, matches), verify if it has > 1 row.
    2. If > 1 row, ALWAYS format the final answer as a Markdown Table.
    3. Make the table headers bold.
    4. If the result is a single number, just state it clearly in bold.
    
    Question: {{question}}
    
    First, generate the SQL query (starts with SELECT). 
    Then, I will execute it.
    Finally, summarize the answer.
    
    Output Format:
    SQL: <the sql query>
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # 4. Generate SQL
    chain_1 = prompt | llm | StrOutputParser()
    response_1 = chain_1.invoke({"schema": schema_info, "question": user_query})
    
    # Extract SQL
    raw_sql = response_1
    if "SQL:" in response_1:
        raw_sql = response_1.split("SQL:")[1]
    
    # Clean up markdown code blocks
    raw_sql = raw_sql.strip()
    if raw_sql.startswith("```sql"):
        raw_sql = raw_sql.replace("```sql", "", 1)
    if raw_sql.startswith("```"):
        raw_sql = raw_sql.replace("```", "", 1)
    if raw_sql.endswith("```"):
        raw_sql = raw_sql.replace("```", "", 1)
        
    sql_query = raw_sql.strip()
    
    print(f"🤖 AI Generated SQL: {sql_query}")
    
    # 5. Execute SQL
    try:
        # Sanity Check
        if "drop" in sql_query.lower() or "delete" in sql_query.lower() or "update" in sql_query.lower():
             return "I cannot execute modification queries."
             
        df = ds.query(sql_query)
        result_str = ""
        if df.empty:
            result_str = "No results found."
        else:
            # If result is small, return rows. If large, summarize.
            if len(df) > 10:
                result_str = f"Found {len(df)} records. Top 5: \n" + df.head(5).to_markdown()
            else:
                result_str = df.to_markdown()
                
        # 6. Final Answer Generation
        final_template = """Based on the User Question and SQL Result, provide a natural language answer.
        
        Question: {question}
        SQL Result: {result}
        
        Answer:"""
        
        final_prompt = ChatPromptTemplate.from_template(final_template)
        final_chain = final_prompt | llm | StrOutputParser()
        final_answer = final_chain.invoke({"question": user_query, "result": result_str})
        
        return final_answer
        
    except Exception as e:
        print(f"SQL Agent Error: {e}")
        return "I tried to query the database but encountered an error. Please try a simpler query."

