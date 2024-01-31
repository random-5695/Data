import json  
import google.generativeai as genai
import streamlit as st
from nav import switch_page

genai.configure(api_key="AIzaSyB4v74PmXcRPT33W5aVpROQBSqawQQC6hI")  

# Set up the model  
generation_config = {  
    "temperature": 0.9,  
    "top_p": 0.1,  
    "top_k": 1,  
    "max_output_tokens": 2048,  
}  

safety_settings = [  
    {  
        "category": "HARM_CATEGORY_HARASSMENT",  
        "threshold": "BLOCK_NONE"  
    },  
    {  
        "category": "HARM_CATEGORY_HATE_SPEECH",  
        "threshold": "BLOCK_NONE"  
    },  
    {  
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",  
        "threshold": "BLOCK_NONE"  
    },  
    {  
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",  
        "threshold": "BLOCK_NONE"  
    },  
]  

model = genai.GenerativeModel(model_name="gemini-pro",  
                              generation_config=generation_config,  
                              safety_settings=safety_settings)  


#--------------------------------------------------------------------#
#----------------------  GENERATING SUMMARY  ------------------------#
#--------------------------------------------------------------------#

st.subheader("Rephrase Titles and Generate Summaries: ")

if st.button("Generate Summaries", type="primary") :

    # Load JSON data from file  
    with open("TechCrunch.json", "r", encoding="utf-8") as json_file:  
        json_data = json.load(json_file)  

    # Loop through articles and generate summaries  
    for article in json_data["articles"]:  
        article_title = article["title"]  
        article_content = article["content"]  

        # Generate summary using the generative model  
        prompt = f"{article_content}\n---\nYour task is to summarize the above article into 3-5 bullet points. Try to include the most important information which provides an overview of the article.\n---\n"  

        try:  
            response = model.generate_content(prompt)  
            summary = response.text.strip()  
            summary = summary.replace('\n\n', '\n')  

        # Handle errors if any  
        except Exception as e:  
            st.error(f"Error generating summary for article {article_title}: {e}")
            st.error(f"Blocked Reason: {response.prompt_feedback}")
            summary = "Error: Summary generation failed."  

        # Add the generated summary to the original JSON data  
        article["Summary"] = summary


    # Save the updated JSON data back to the file  
    with open("TechCrunch.json", "w", encoding="utf-8") as json_file:  
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)  

    st.info("JSON file updated with summaries.")

    #--------------------------------------------------------------------#
    #----------------------  GENERATING TITLES  -------------------------#
    #--------------------------------------------------------------------#


    # Load JSON data from file
    json_path = "TechCrunch.json"
    with open(json_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    # Loop through articles and generate titles
    for article in json_data["articles"]:
        article_title = article["title"]
        article_content = article["content"]

        # Generate summary using the generative model
        revised_title_prompt = f"Title:\n{article_title}\nContent:\n{article_content}\n---\nYour task is to give a revised title for the above article, do not include any clickbait words and represent the actual content of the article\n---\n"

        try:
            response = model.generate_content(revised_title_prompt)
            title = response.text.strip()

            # Add the generated summary as a heading to the article
            article["revised_title"] = title
        except Exception as e:
            st.error(f"Error generating title for '{article_title}': {str(e)}")

    # Update the existing JSON file with the generated summaries
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=2)

    st.info(f"Updated existing JSON file '{json_path}' with generated titles.")

else:
    st.error("Error!!")

if st.button("Export to Github", type="primary") :
    switch_page(pages/exp_github)
