import streamlit as st
import openai
import re
import requests


# Define the allowlist of characters
ALLOWLIST_PATTERN = re.compile(r"^[a-zA-Z0-9\s.,;:!?\-]+$")


def fetch(input, pattern, model):
    # Set the system and user URLs
    base_url = f"https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns/{pattern}/"
    system_url = f"{base_url}/system.md"
    user_url = f"{base_url}/user.md"

    # Fetch the prompt content
    system_content = fetch_content_from_url(system_url)
    user_file_content = fetch_content_from_url(user_url)

    # Build the API call
    system_message = {"role": "system", "content": system_content}
    user_message = {"role": "user", "content": user_file_content + "\n" + input}
    messages = [system_message, user_message]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0,
        top_p=1,
        frequency_penalty=0.1,
        presence_penalty=0.1,
    )
    return response.choices[0].message.content


def sanitize_content(content):
    """Sanitize the content by removing characters that do not match the ALLOWLIST_PATTERN.

    Args:
        content (str): The content to be sanitized.

    Returns:
        str: The sanitized content.
    """

    return "".join(char for char in content if ALLOWLIST_PATTERN.match(char))


# Pull the URL content's from the GitHub repo
def fetch_content_from_url(url):
    """Fetches content from the given URL.

    Args:
        url (str): The URL from which to fetch content.

    Returns:
        str: The sanitized content fetched from the URL.

    Raises:
        requests.RequestException: If an error occurs while making the request to the URL.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
        sanitized_content = sanitize_content(response.text)
        return sanitized_content
    except requests.RequestException as e:
        return str(e)


st.title("My fabric")
selected_model = st.selectbox(
    "Model",
    (
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo-preview",
    ),
)
selected_pattern = st.selectbox(
    "Pattern",
    (
        "agility_story",
        "ai",
        "analyze_claims",
        "analyze_incident",
        "analyze_paper",
        "analyze_prose",
        "analyze_prose_json",
        "analyze_spiritual_text",
        "analyze_tech_impact",
        "analyze_threat_report",
        "analyze_threat_report_trends",
        "check_agreement",
        "clean_text",
        "compare_and_contrast",
        "create_aphorisms",
        "create_command",
        "create_keynote",
        "create_logo",
        "create_markmap_visualization",
        "create_mermaid_visualization",
        "create_npc",
        "create_threat_model",
        "create_video_chapters",
        "create_visualization",
        "explain_code",
        "explain_docs",
        "extract_algorithm_update_recommendations",
        "extract_article_wisdom",
        "extract_ideas",
        "extract_patterns",
        "extract_poc",
        "extract_predictions",
        "extract_recommendations",
        "extract_references",
        "extract_sponsors",
        "extract_videoid",
        "extract_wisdom",
        "find_hidden_message",
        "improve_prompt",
        "improve_writing",
        "label_and_rate",
        "philocapsulate",
        "provide_guidance",
        "rate_content",
        "rate_value",
        "summarize",
        "summarize_git_changes",
        "summarize_micro",
        "summarize_newsletter",
        "summarize_pull-requests",
        "summarize_rpg_session",
        "write_essay",
        "write_micro_essay",
        "write_pull-request",
        "write_semgrep_rule",
    ),
)

input_text = st.text_area("Input text")

selected_model
selected_pattern

submitted = st.button(f"Run: {selected_pattern}")

results = st.container(border=True)

if submitted:
    response = fetch(input_text, selected_pattern, selected_model)
    results.write(response)
