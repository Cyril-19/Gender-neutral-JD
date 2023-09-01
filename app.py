from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
openai.api_key = os.getenv("API_KEY")


def generate_description(job_title, role_description):
    instructions = f"Use gender-neutral language: Avoid using gender-specific pronouns like he, she and job titles like salesman, saleswoman. Instead, opt for inclusive terms such as 'they' and 'salesperson.'\n" \
                  "Remove gender-coded words: For example adjectives that may be associated with a specific gender, such as 'aggressive' or 'nurturing.' Use neutral descriptors, like 'results-driven' or 'collaborative.'\n" \
                  "Closely consider the education requirements and skill required listed in the {role_description}.\n" \
                  "Avoid sexist,racist and gender biased wordings and contexts\n" \
                  "Avoid words associated with being masculine, subjects perceived the role to be for a male candidate\n" \
                  "Express a commitment to equality and diversity.\n" 
    
    prompt = f"Generate an gender-neutral and inclusive job description for the position of {job_title} following the given{instructions} based on the {role_description} and examples :\n\n" \
         f"Examples:\n" \
         f"1. 'Sales Person' - [We are looking for a motivated and sales-driven individual to join our team as a Sales Person.The ideal candidate will have strong communication and interpersonal skills, as well as the ability to build relationships with customers.The Sales Person will be responsible for identifying and qualifying leads, developing proposals, and closing deals.]\n" \
         f"2. 'Server' - [We are looking for a friendly and outgoing individual to join our team as a Server.The ideal candidate will have excellent customer service skills and the ability to work under pressure. The Server will be responsible for taking orders, serving food and drinks, and providing excellent customer service.]\n" \
         f"3. 'Chairperson' - [We are looking for a highly organized and efficient individual to join our team as a Chairperson. The ideal candidate will have strong leadership and communication skills, as well as the ability to manage a team.The Chairperson will be responsible for planning and coordinating meetings, as well as ensuring that all meetings run smoothly.]\n\n" \

    
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        max_tokens=1500,  
        temperature=0.8,  
        stop=None,
        frequency_penalty=0.5,  
        presence_penalty=0.3,   
        n=2,      
        top_p=0.8  
    )
    
    return response.choices[0].text.strip()

    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_title = request.form.get("job_title")
        role_description = request.form.get("role_description")
        
        gender_neutral_description = generate_description(job_title, role_description)
        return render_template("result.html", description=gender_neutral_description)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)