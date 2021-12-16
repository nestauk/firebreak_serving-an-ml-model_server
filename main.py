from typing import Optional
from enum import Enum
import uvicorn

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

import mapping_career_causeways.transitions_utils as trans_utils
import mapping_career_causeways.load_data_utils as load_data

app = FastAPI()
data = load_data.Data()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            transition["description"] = data.occ_lookup[str(transition["destination_id"])]["group_description"]
            transition["major_occupation_category"] = data.occ_lookup[str(transition["destination_id"])]["group_name"]
            transition["qualification"] = data.occ_lookup[str(transition["destination_id"])]["qualification"]
            transition["skills"] = trans_utils.show_skills_overlap(
                job_i=origin_id, # Origin occupation ID
                job_j=transition["destination_id"], # Destination occupation ID
                skills_match='optional',
                verbose=False)[["origin_skill","destination_skill","similarity"]].to_dict("records")
        return top_transitions
    else:
        return "job title not found! Try another."

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)