import uvicorn
from fastapi import FastAPI
import load_data_utils as load_data
import transition_utils as trans_utils
import pandas as pd
from pydantic import BaseModel
from operator import itemgetter


app = FastAPI()
data = load_data.Data()
skill_type = None


class JobDetails(BaseModel):
    job_name: str


@app.get('/')
def index():
    return {'message': 'Hello, stranger'}


@app.get('/extract_details')
def get_transitions(job: JobDetails):
    job_name = job.job_name
    job_i = data.occ_title_to_id(job_name)
    job_i_skills = data.occupation_skills(job_i, skill_importance=skill_type).to_dict('records')
    skill_ids = []
    for skill in job_i_skills:
        skill_ids.append(skill["skill_id"])

    transitions = trans_utils.find_most_similar(
        job_i, # Origin occupation for which we're searching the other most similar other occupations
        similarity_measure="combined", # Type of similarity measure to use
        n=20, # Number of most similar occupations to show
        destination_ids='report', # Pool of admissible destination occupations (try also 'all')
        transpose=False, # If job_i describes a jobseeker, set to False; if job_i describes a vacancy, set to True
        ).round(2)
    dicts = transitions[1:6].to_dict("records")
    for transition in dicts:
        transition["name"] = transition["preferred_label"]
        skills = data.occupation_skills(transition["id"], skill_importance=skill_type).to_dict('records')
        transition["temp_skills"] = []
        for skill in skills:
            if skill["skill_id"] in skill_ids:
                skill_dict = {
                    "origin_skill":skill["preferred_label"],
                    "destination_skill":skill["preferred_label"],
                    "similarity":1
                }
            if skill["skill_id"] not in skill_ids:
                skill_dict = {
                    "origin_skill":skill["preferred_label"],
                    "destination_skill":skill["preferred_label"],
                    "similarity":0
                }
            transition["temp_skills"].append(skill_dict)
        transition["skills"] = sorted(transition["temp_skills"], key=itemgetter("similarity"), reverse=True)

        # transition["skills"] = trans_utils.show_skills_overlap(
        #     job_i=job_i, # Origin occupation ID
        #     job_j=transition["id"], # Destination occupation ID
        #     skills_match='optional',
        #     verbose=False)[["origin_skill","destination_skill","similarity"]].to_dict("records")
        # This code above is super slow so i've bashed in some horrible code for now.

        transition.pop("preferred_label", None)
        transition.pop("tempt_skills", None)
        transition.pop("id", None)
    return dicts


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=80)
