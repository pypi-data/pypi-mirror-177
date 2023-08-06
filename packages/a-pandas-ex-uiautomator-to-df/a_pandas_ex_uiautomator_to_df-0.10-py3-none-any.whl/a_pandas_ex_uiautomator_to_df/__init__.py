import pandas as pd
from a_pandas_ex_string_to_dtypes import pd_add_string_to_dtypes
from a_pandas_ex_xml2df import pd_add_read_xml_files
from aa_pandas_ex_df_to_string import pd_add_to_string
import numpy as np

pd_add_string_to_dtypes()
pd_add_to_string()


pd_add_read_xml_files()


def dataframe_from_uiautomator_window_dump(dumpstring):

    if isinstance(dumpstring, bytes):
        dumpstring = dumpstring.decode("utf-8", "replace")
    if not dumpstring.strip().startswith("<?xml"):
        dumpstring = "\n".join(dumpstring.splitlines()[1:])

    df = pd.Q_Xml2df(dumpstring).reset_index()
    df2 = df.ds_to_string()
    allgooddataf = []
    for col in df2.columns:
        if "level_" in col:
            if col in ["level_0"]:
                continue

            gutframe = (df2.loc[~df2[col].str.contains("^node$|<NA>")]).copy()
            dropcols = []
            sortcols = []
            indexcols = []

            for col2 in gutframe.columns:
                if "level_" in col2:
                    vca = gutframe[col2].value_counts()
                    if len(vca) == 1:
                        if str(vca.index[0]).strip() in ["node", "<NA>"]:
                            dropcols.append(col2)
                            continue
                    if gutframe[(gutframe[col2].str.contains("text"))].empty:
                        if not "<NA>" in [str(x) for x in vca.index.to_list()]:
                            sortcols.append(col2)
                    else:
                        indexcols.append(col2)
            gutframe = gutframe.drop(columns=dropcols)
            if (len(gutframe) > 30) and len(sortcols) == 1:
                continue
            if sortcols:
                for name, group in gutframe.groupby(sortcols):
                    group2 = group.copy()
                    for col3 in group.columns:
                        tstlist = list(set(group[col3].astype("string").to_list()))
                        if tstlist[0] == "<NA>" and len(tstlist) == 1:
                            group2 = group2.drop(columns=col3)
                    sortcols_level_add = []
                    sortcols_hirac_add = []
                    for name1, groupxx in group2.groupby(sortcols):
                        if len(groupxx) != 17:
                            continue
                        groupxx2 = groupxx.copy()
                        groupxx4 = (
                            groupxx2.drop(columns=sortcols + ["aa_all_keys"])
                            .set_index(indexcols[0])
                            .T.copy()
                        )
                        for ini, _ in enumerate(sortcols):
                            sortcols_level_add.append(int(_[6:]))
                            sortcols_hirac_add.append((groupxx2[_].iloc[0]))
                        for ini, ll in enumerate(sortcols_level_add):
                            groupxx4[f"position_{ini}"] = ll
                        for ini, ll in enumerate(sortcols_hirac_add):
                            groupxx4[f"position_{ini}_h"] = ll
                        groupxx2["aa_all_keys"] = df.loc[groupxx2.index, "aa_all_keys"]
                        groupxx2["aa_all_keys"] = groupxx2["aa_all_keys"].apply(
                            lambda x: x[:-1]
                        )
                        groupxx4.loc[:, "keys_hierarchy"] = str(
                            groupxx2["aa_all_keys"].iloc[0]
                        )
                        allgooddataf.append(groupxx4.copy())

    df = (
        pd.concat(allgooddataf, ignore_index=True)
        .reset_index(drop=True)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    coords_ = (
        df.bounds.str.extractall(r"(\d+)\W+(\d+)\W+(\d+)\W+(\d+)")
        .reset_index(drop=True)
        .rename(columns={0: "start_x", 1: "start_y", 2: "end_x", 3: "end_y"})
        .astype(np.uint16)
        .copy()
    )
    df = pd.concat([coords_, df], axis=1).copy()
    df.loc[:, "aa_width"] = df.end_x - df.start_x
    df.loc[:, "aa_height"] = df.end_y - df.start_y
    df["aa_center_x"] = df["start_x"] + (df["aa_width"] // 2)
    df["aa_center_y"] = df["start_y"] + (df["aa_height"] // 2)
    for col in df.columns:
        try:
            df.loc[:, col] = df.loc[:, col].str.replace("^false$", "False", regex=True)
            df.loc[:, col] = df.loc[:, col].str.replace("^true$", "True", regex=True)
        except Exception:
            pass

    for col in df.columns:
        if col == "bounds":
            continue
        try:
            try:
                df.loc[:, col] = df.loc[:, col].ds_string_to_best_dtype()
            except Exception:
                pass

            df.loc[:, col] = df.loc[:, col].ds_reduce_memory_size(verbose=False)
        except Exception:
            pass
    df.bounds = list(zip(df.start_x, df.start_y, df.end_x, df.end_y))
    df = df.rename(
        columns={
            "start_x": "aa_start_x",
            "start_y": "aa_start_y",
            "end_x": "aa_end_x",
            "end_y": "aa_end_y",
        }
    )
    df = df.filter(list(sorted(df.columns))).copy()
    return df


def pd_add_uiautomator_to_df():
    pd.Q_uiautomator_to_df = dataframe_from_uiautomator_window_dump
