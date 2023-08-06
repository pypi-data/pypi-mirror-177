import itertools
import operator
import re
from typing import Union

from a_pandas_ex_split_on_common_string import pd_add_split_on_common_string
import regex
import pandas as pd
from a_pandas_ex_plode_tool import qq_s_isnan

pd_add_split_on_common_string()


def dumpsys_to_df(dumpsysoutput: Union[bytes, str]) -> pd.DataFrame:
    regexsplitcomp = regex.compile(r"(?<!(?::))\n\n+", flags=regex.I)
    regexsub4 = regex.compile(r"^\s{5}(?!\s)", flags=regex.I)
    regexsub2 = regex.compile(r"^\s{3}(?!\s)", flags=regex.I)
    regexsearchs = regex.compile(r"^\s+", flags=regex.I)
    regexsearchsstartend = re.compile(r"^\s*$", flags=re.I)
    recom = re.compile(r"^(?:<NA>)*\s*$", flags=re.I)
    if isinstance(dumpsysoutput, bytes):
        dumpsysstring = dumpsysoutput.decode("utf-8", "replace")
    else:
        dumpsysstring = dumpsysoutput
    splitted = [x.splitlines() for x in regexsplitcomp.split(dumpsysstring)]
    splitted = [[regexsub4.sub("    ", y) for y in x] for x in splitted]
    splitted = [[regexsub2.sub("  ", y) for y in x] for x in splitted]
    splitted = [[y for y in x if not "(No recorded stats)" in y] for x in splitted]

    spaces = [[regexsearchs.search(y) for y in x] for x in splitted]
    formata = [
        [(y.span()[-1], p) if y is not None else (0, p) for y, p in zip(x, k)]
        for x, k in zip(spaces, splitted)
    ]
    asdfs = [pd.DataFrame(x) for x in formata]
    asdfs2 = []
    for df in asdfs:
        asdfs2.append(
            df.loc[~df[1].str.contains(regexsearchsstartend, na=False)].copy()
        )
    alldfs = []
    for asdfs2_ in asdfs2:
        newdf = asdfs2_.copy()
        uniind = list(sorted(asdfs2_[0].unique()))
        for ini, uni in enumerate(uniind):
            asdfs3 = (
                asdfs2_[1]
                .str.extractall(fr"^\s{{{uni}}}(?!\s)(.*)", flags=re.I)
                .reset_index()
            )
            newdf.loc[asdfs3["level_0"], f"{uni}_uni"] = asdfs3[0].__array__().copy()
            goodval = pd.NA
            iii = newdf.columns.to_list().index(f"{uni}_uni")
            counter = 0
            for key, item in newdf.iterrows():
                if not qq_s_isnan(item[f"{uni}_uni"]):
                    goodval = item[f"{uni}_uni"]

                else:
                    if item[0] >= uni:
                        newdf.iat[counter, iii] = goodval
                counter += 1
        alldfs.append(newdf.dropna(subset=[newdf.columns[2]]).copy())
    alldfsn = []
    for dfa in alldfs:
        dfa.columns = list(range(dfa.shape[1]))
        alldfsn.append(dfa.copy())
    df = pd.concat(alldfsn).drop(columns=[0, 1]).copy()
    df = df.drop_duplicates().reset_index(drop=True)
    df = df.loc[~df[3].isna()].reset_index(drop=True)
    df.columns = list(range(df.shape[1]))

    goodstuff = []
    counterxx = 0
    for name, group in df.groupby([0, 1]):
        print(f"{counterxx}", end="\r")
        if len(group) > 1:
            du2 = pd.DataFrame([3])
            group2 = group.fillna(pd.NA).copy()
            while not du2.empty:
                try:
                    dub = group2.apply(
                        lambda li_: pd.Series(
                            itertools.accumulate((str(_) for _ in li_), operator.add)
                        ),
                        axis=1,
                    )
                    du2 = dub[dub.columns[-1]].s_split_on_common_string()
                    du2 = du2.loc[(du2.aa_different.str.contains(recom))]
                    if not du2.empty:
                        group2 = group2.loc[
                            [__ for __ in group2.index if __ not in du2.index]
                        ]
                except Exception as fe:
                    break
            if not group2.empty:
                goodstuff.append(group2.copy())
        else:
            goodstuff.append(group.copy())
        counterxx += 1
    df = pd.concat(goodstuff)
    for col in df.columns:
        try:
            df.loc[:, col] = df.loc[:, col].fillna(pd.NA)
        except Exception:
            continue
    for col in df.columns:
        try:
            df.loc[:, col] = df[col].str.rstrip(": ")
        except Exception:
            continue

    df.columns = [f"aa_{x}" for x in df.columns]
    df = df.reset_index(drop=True)
    return df

def pd_add_dumpsys_to_dataframe():
    pd.Q_dumpsys_to_df = dumpsys_to_df

