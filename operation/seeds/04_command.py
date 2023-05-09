import pandas as pd
import ruamel.yaml
import glob
from settings import Session
from models import Technique, Command
from sqlalchemy import exc

def get_commands_by_df(file: str):
    yaml = ruamel.yaml.YAML()
    with open(file) as f:
        content = yaml.load(f)
    commands = list()
    for el in content["atomic_tests"]:
        try:
            command = el["executor"]["command"]
        except:
            command = None
        commands.append(command)
    df_commands = pd.DataFrame(commands, columns=["Commands"])
    return df_commands

# atomicのDFを生成
file_lst = glob.glob("/resources/atomics/*")
df_atomics = pd.DataFrame(columns=["Commands", "technique_external_id"])
for file in file_lst:
    technique_external_id = file.split(".yaml")[0].split("atomics/")[1]
    df_tmp = get_commands_by_df(file)
    df_tmp["technique_external_id"] = technique_external_id
    df_atomics = pd.concat([df_atomics, df_tmp], axis=0)
df_atomics = df_atomics.sort_values("technique_external_id")

for row in df_atomics.itertuples():
    record = Command()
    record.command = row[1]
    record.technique_id = Technique.get_id_by_external_id(row[2])
    Session.add(record)
    
Session.commit()
Session.close()
print("Command table created.")