from google import genai


def get_response(prompt: str, model: str = "gemini-2.0-flash", API_KEY=None) -> str:
    """
    Generate a response from given model
    
    Args:
        prompt: prompt for model
        model: which model to use
        API_KEY: optional api key for model specific api
        
    Returns:
        Response from LLM
    """

    if 'gemini' in model:
        return generate_gemini_response(prompt, API_KEY)
    else:
        print("Unsupported model")


def generate_gemini_response(prompt: str, API_KEY: str, model: str = "gemini-2.0-flash") -> str:
    """
    Generate a response from gemini
    
    Args:
        prompt: prompt for gemini
        API_KEY: google ai api key
        model: which version of gemini to use
        
    Returns:
        Response from gemini
    """

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text

