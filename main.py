from typing import Optional
from enum import Enum
import uvicorn

from fastapi import FastAPI, Query

import mapping_career_causeways.transitions_utils as trans_utils
import mapping_career_causeways.load_data_utils as load_data

#instantiate 
app = FastAPI()
data = load_data.Data()

class SkillImportance(str, Enum):
    essential = "Essential"
    optional = "Optional"

@app.get("/")
def root():
    return {"Howdy:" "Brothers"}

@app.get("/transition/{job_title}")
def get_job_title_data(job_title: str, top_n_jobs: Optional[int] = 5, skills_importance: Optional[SkillImportance] = None):

    if job_title in list(set(data.occ.preferred_label.tolist())):
        origin_id = data.occ[data.occ.preferred_label == job_title].iloc[0]['id']
        transititions = trans_utils.get_transitions(origin_ids=[origin_id], less_information=True)
        top_transitions = transititions[['destination_id', 'destination_label', 'similarity']][:top_n_jobs].to_dict('records')
       
        for transition in top_transitions:
            skills_list = data.occupation_skills(transition['destination_id'], skill_importance=skills_importance)['preferred_label'].to_list()
            transition['skills'] = list(set(skills_list))

        return top_transitions
    else:
        return "job title not found! Try another."

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)