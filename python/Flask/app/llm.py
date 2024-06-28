def llm_selector(llm_name):
    # thid function is factory method that returns an instance of an LLM class
    # based on the llm_name parameter
    if llm_name == "llm1":
        return LLM1()
    elif llm_name == "llm2":
        return LLM2()
    else:
        return None
