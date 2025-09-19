import pandas as pd
import os, json, re
import google.generativeai as genai

foley_df = pd.read_excel('Foley_Comp2_879.xlsx')
foley_df = foley_df.head()

# --- Load API key from environment variable ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# get a list of valid models
# models = genai.list_models()
# for m in models:
#     print(m.name, m.supported_generation_methods)

# --- Gemini model ---
model = genai.GenerativeModel("gemini-2.5-flash")

# --- Function to parse a single name ---
def parse_name_with_gemini(name: str):
    """
    Send the name string to Gemini and parse first, middle, last, org_flag.
    """
    
    print(f"Parsing: {name}")  # shows progress

    prompt = f"""
    You are a name parsing assistant. Parse the input string into an array of people.
    There could be just one person, multiple people, or nonsense entities (such as businesses, ie LLC)
    In the case of a business, make make the first name BUSINESS, the last name the name of the business, and "org_flag": True
    The names are not guaranteed to be in any order, some are Last,First while others are First M.I. Last, etc. For example:
    "Draper Jared Clark, Draper Leilani Lyn" is two people - Jared and Leilani Lyn, but
    " Johnston Margaret Alice Beauch" is only one person
    Use your judgment to correctly parse the entries into appropriate fields:
    Each person should be an object with keys:
    - first (string or empty)
    - middle (string or empty)
    - last (string or empty)
    - org_flag (true if this is a business/organization)

    Do not include any explanation or commentary. Return **only valid JSON**. Example format:
    [
        {{"first": "John", "middle": "A.", "last": "Smith", "org_flag": false}},
        {{"first": "Jane", "middle": "", "last": "Doe", "org_flag": false}}
    ]

    Input: "{name}"
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        match = re.search(r"\[.*\]", text, re.S)  # find array
        if match:
            data_list = json.loads(match.group(0))  # list of people
        else:
            # fallback if no JSON found
            data_list = [{"first": "", "middle": "", "last": "", "org_flag": True}]
        return data_list
    except Exception as e:
        print(f"Error parsing {name}: {e}")
        return [{"first": "", "middle": "", "last": "", "org_flag": True}]

# --- Function to build mailing name for multiple owners ---
def build_mailing_name(row):
    mailing_names = []

    # row["parsed"] is list of people returned by Gemini
    for person in row["parsed"]:
        if person["org_flag"]:
            # If it's a business/organization, keep original string
            mailing_names.append(row["Owner Name(s)"])
        else:
            # Build "First Middle Last" (or just First Last)
            parts = [person["first"].strip()]
            if person["middle"].strip():
                parts.append(person["middle"].strip())
            if person["last"].strip():
                parts.append(person["last"].strip())
            mailing_names.append(" ".join(parts).strip())

    # Join multiple people with & if more than one
    return " & ".join(mailing_names)

# --- Parse names ---
foley_df["parsed"] = foley_df["Owner Name(s)"].apply(parse_name_with_gemini)

# --- Build mailing name ---
foley_df["mailing name"] = foley_df.apply(build_mailing_name, axis=1)

# --- Optional: drop parsed dict column ---
# foley_df = foley_df.drop(columns=["parsed"])

print(foley_df.head())   

'''

import pandas as pd
import os, json, re
import openai

foley_df = pd.read_excel('Foley_Comp2_879.xlsx')
foley_df = foley_df.head()

# --- Load API key ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Function to parse a single name ---
def parse_name_with_openai(name: str):
    """
    Send the name string to OpenAI and parse first, middle, last, org_flag.
    """
    print(f"Parsing: {name}")  # shows progress

    prompt = f"""
    You are a name parsing assistant. Parse the input string into an array of people.
    There could be just one person, multiple people, or nonsense entities (such as businesses, ie LLC)
    In the case of a business, make the first name BUSINESS, the last name the name of the business, and "org_flag": True
    The names are not guaranteed to be in any order, some are Last,First while others are First M.I. Last, etc
    Use your judgment to correctly parse the entries into appropriate fields:
    Each person should be an object with keys:
    - first (string or empty)
    - middle (string or empty)
    - last (string or empty)
    - org_flag (true if this is a business/organization)

    Do not include any explanation or commentary. Return **only valid JSON**. Example format:
    [
        {{"first": "John", "middle": "A.", "last": "Smith", "org_flag": false}},
        {{"first": "Jane", "middle": "", "last": "Doe", "org_flag": false}}
    ]

    Input: "{name}"
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        text = response.choices[0].message.content.strip()

        # Extract JSON
        match = re.search(r"\[.*\]", text, re.S)
        if match:
            data_list = json.loads(match.group(0))
        else:
            data_list = [{"first": "", "middle": "", "last": "", "org_flag": True}]
        return data_list
    except Exception as e:
        print(f"Error parsing {name}: {e}")
        return [{"first": "", "middle": "", "last": "", "org_flag": True}]
    
# --- Function to build mailing name for multiple owners ---
def build_mailing_name(row):
    mailing_names = []

    # row["parsed"] is list of people returned by Gemini
    for person in row["parsed"]:
        if person["org_flag"]:
            # If it's a business/organization, keep original string
            mailing_names.append(row["Owner Name(s)"])
        else:
            # Build "First Middle Last" (or just First Last)
            parts = [person["first"].strip()]
            if person["middle"].strip():
                parts.append(person["middle"].strip())
            if person["last"].strip():
                parts.append(person["last"].strip())
            mailing_names.append(" ".join(parts).strip())

    # Join multiple people with & if more than one
    return " & ".join(mailing_names)

foley_df["parsed"] = foley_df["Owner Name(s)"].apply(parse_name_with_openai)
foley_df["mailing name"] = foley_df.apply(build_mailing_name, axis=1)
print(foley_df.head())


'''