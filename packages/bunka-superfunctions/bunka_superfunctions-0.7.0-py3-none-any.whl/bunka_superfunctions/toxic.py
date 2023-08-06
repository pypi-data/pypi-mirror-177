from detoxify import Detoxify
import warnings
from tqdm import tqdm
import pandas as pd

warnings.simplefilter(action='ignore', category=FutureWarning)
toxic_model = Detoxify('multilingual')

# 20 minutes for around 20,000 sentences
def get_toxic_comments(df:pd.DataFrame, text_col:str, index_col:str, thresh:int = 0.5):

    df_tox = pd.DataFrame()

    pbar = tqdm(total = len(df))

    for id, text in zip(df[index_col].to_list(), df[text_col].to_list()):

        res = toxic_model.predict(text)
        res = pd.DataFrame(res, index = [0])

        res[index_col] = id
        res[text_col]=text
        df_tox = df_tox.append(res)

        pbar.update(1)

    df_tox = df_tox.reset_index(drop=True)
    df_tox = df_tox.sort_values('toxicity', ascending=False)
    
    df_tox['label'] = 0
    df_tox['label'][df_tox['toxicity']>thresh] = 1
    
    return df_tox