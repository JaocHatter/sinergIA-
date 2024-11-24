from typing import Dict
import pandas as pd
import os
import uuid

# TODO: SAVE RESULTS ON A DATABASE
def converter_step(state: Dict) -> Dict:
    print("CONVERTER_STEP")
    state["stage"] = "convert"
    state["next"] = "translator"
    print("total search_results: "+ str(len(state["search_results"])))
    results_df = pd.DataFrame(state["search_results"])
    data_dir = os.path.join(os.getcwd(), "generated_data")    

    # Save to CSV
    if os.path.exists(data_dir) == False:
        os.mkdir(data_dir)
    new_dir = f"research_{uuid.uuid4().hex}"
    new_dir_path = os.path.join(data_dir,new_dir)
    os.mkdir(new_dir_path)
    results_df.to_csv(os.path.join(new_dir_path,"research_results.csv"))
    
    # Save to TXT
    research_results_txt = os.path.join(new_dir_path,"research_results.txt")
    with open(research_results_txt, "w") as f:
        for result in state["search_results"]:
            f.write(f"Paper: {result['title']}\n")
            f.write(f"Year: {result['year']}\n")
            f.write(f"Authors: {', '.join(result['author'])}\n")
            f.write(f"Abstract: {result['summary']}\n")
            f.write("-" * 80 + "\n")
    state["path"] = research_results_txt
    return state