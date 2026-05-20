STEPS TO use 

1. install relevant libraries from requirements.txt

2. set up the api keys from env file 

3. SQL setup - run the file create_db.py in the database folder

4. run uvicorn app:app --reload


The workflow and assumptions


    
    Processing pipeline:

    1. Agent Alpha checks factual correctness
       - FALSE -> DISCARD immediately

    2. Agent Beta compares against previously accepted messages only
       - SEMANTIC_DUPLICATE -> DISCARD
       - CONTRADICTION -> FLAG_REVIEW
       - NO_MATCH -> rely on Agent Alpha verdict

    3. Alpha fallback
       - TRUE -> INSERT
       - PARTIALLY_TRUE -> FLAG_REVIEW
       - UNVERIFIABLE -> FLAG_REVIEW
    
    PYDANTIC VALIDATIONS for all llm api outputs. 

Steps to improve the agents 

    1. When on a large scale the sql query to get message bodies will fail need to optimize that. 

    2. Tavily can be optimized by finding out the topic beforehand. 

    3. More autonomy can be provided to agents but it's a point of debate due to api costs. 

    4. Duplicate message check should be optimized when working on larger scale. 



    