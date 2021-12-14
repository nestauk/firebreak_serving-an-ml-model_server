import uvicorn
from fastapi import FastAPI
import load_data_utils as load_data
import transition_utils as trans_utils
import pandas as pd
from pydantic import BaseModel

# 2. Create the app object
app = FastAPI()
data = load_data.Data()
skill_type = None

class JobDetails(BaseModel):
    job_name: str

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, stranger'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/extract_details')
def get_transitions(job: JobDetails):
    job_name = job.job_name
    job_i = data.occ_title_to_id(job_name)
    similarity_measure = "combined" #@param ['combined', 'essential_skills', 'optional_skills', 'work_activities', 'work_context']
    number_of_matches =  20 #@param {type:"integer"}

# For this purpose, we're using a helper function `find_most_similar()` that simply finds the
# row in the similarity matrix that corresponds to your occupation, and sorts the table 
# of all occupations according to the similarity values in this row.
    transitions = trans_utils.find_most_similar(
        job_i, # Origin occupation for which we're searching the other most similar other occupations
        similarity_measure=similarity_measure, # Type of similarity measure to use
        n=number_of_matches, # Number of most similar occupations to show
        destination_ids='report', # Pool of admissible destination occupations (try also 'all')
        transpose=False, # If job_i describes a jobseeker, set to False; if job_i describes a vacancy, set to True
        ).round(2)
    dicts = transitions[1:6].to_dict("records")
    for transition in dicts:
        transition["name"] = transition["preferred_label"]
        transition["skills"] = trans_utils.show_skills_overlap(
            job_i=job_i, # Origin occupation ID
            job_j=transition["id"], # Destination occupation ID
            skills_match='optional',
            verbose=False)[["origin_skill","destination_skill","similarity"]].to_dict("records")
        transition.pop("preferred_label", None)
        transition.pop("id", None)
    return dicts

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=80)
