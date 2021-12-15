# Preprocessing

Various notebooks for preparing the ESCO occupational and skills data for downstream analysis.

**`Assign_ONET_to_all_ESCO_occupations.ipynb`**  
Extend the [crosswalk](https://github.com/nestauk/mapping-career-causeways/tree/main/supplementary_online_data/ONET_ESCO_crosswalk) between ESCO and O\*NET frameworks to cover the full set of ESCO occupations.

**`ESCO_occupation_hierarchy.ipynb`**  
Reconstruct the 'broader' (parent) and 'narrower' (children) occupational relationships using ESCO API.

**`ESCO_skills_hierarchy.ipynb`**  
Reconstruct the [ESCO skills pillar hierarchy](https://ec.europa.eu/esco/portal/escopedia/Skills_pillar) using ESCO API.

**`Extract_ISCO_category_titles.ipynb`**  
Obtain titles for each ISCO major, sub-major, minor and unit group.

**`Generate_SBERT_embeddings.ipynb`**  
Use `sentence_transformers` package for generating Sentence-BERT embeddings of skills descriptions. For much faster calculations, one can also use [this Google Colab notebook](https://colab.research.google.com/drive/1EfEXjdu4MYZMmr7X2gymFamxpw_J23me?usp=sharing), with the GPU enabled.
