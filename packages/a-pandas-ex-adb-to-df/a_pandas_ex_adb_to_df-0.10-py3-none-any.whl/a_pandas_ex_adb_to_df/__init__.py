import re
import subprocess
import pandas as pd
import regex
from flatten_everything import flatten_everything
from com.dtmilano.android.viewclient import ViewClient


def connect_to_adb(
    serialnumber: str, adb_path: str = r"C:\ProgramData\adb\adb.exe",
):
    _ = subprocess.run(
        f"{adb_path} start-server", capture_output=True, shell=False
    )
    kwargs1 = {
        "timeout": 30,
        "ignoreversioncheck": False,
        "verbose": False,
        "ignoresecuredevice": False,
        "serialno": f"{serialnumber}",
    }
    device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
    return device


def get_folder_df(
    device=None, adb_path: str = r"C:\ProgramData\adb\adb.exe"
) -> pd.DataFrame:
    if isinstance(device, str):
        device = connect_to_adb(serialnumber=device, adb_path=adb_path)

    sec = flatten_everything(
        (
            [y + "_______________________________" + x[0] for y in x]
            for x in [
                [z.strip() for z in y.splitlines() if z.strip() != ""]
                for y in regex.findall(
                    r"\n//?.*?\n\n",
                    device.shell("ls -R -s -i -H -ltr $PWD/*"),
                    regex.DOTALL | regex.IGNORECASE,
                )
            ]
        )
    )

    df = pd.DataFrame(flatten_everything(sec))
    df[0] = df[0].str.replace(
        r"(\d+\s+\d+\s+\d+),\s+(\d+)", r"\g<1>__\g<2>", regex=True, flags=re.IGNORECASE
    )
    sepa = df[0].str.split(n=9, expand=True).copy()
    df = pd.concat([df, sepa], axis=1, ignore_index=True).copy()
    df = df.loc[~df[3].isna()].copy()
    df = df.loc[df[9].str.contains(":", na=False, regex=False)]
    df = df.loc[df[7].str.contains(r"^\s*\d+\s*$")]
    fileandpath = df[10].str.split("_______________________________", expand=True)
    fileandpath[1] = fileandpath[1].str.strip(":/ ")
    fileandpath[2] = fileandpath[1] + "/" + fileandpath[0]

    df = df[[x for x in df.columns if x not in [0, 10]]].copy()
    df = pd.concat([fileandpath, df], axis=1, ignore_index=True).copy()
    df = df.loc[df[3].str.contains(r"^\s*\d+\s*$")]
    df = df.loc[df[4].str.contains(r"^\s*\d+\s*$")]

    df.columns = [
        "aa_filename",
        "aa_folder",
        "aa_fullpath",
        "aa_id",
        "aa_index",
        "aa_rights",
        "aa_links",
        "aa_owner",
        "aa_group",
        "aa_size",
        "aa_date",
        "aa_time",
    ]

    try:
        df["aa_filename"] = df["aa_filename"].astype("string")
    except Exception:
        pass
    try:
        df["aa_folder"] = df["aa_folder"].astype("category")
    except Exception:
        pass
    try:
        df["aa_fullpath"] = df["aa_fullpath"].astype("string")
    except Exception:
        pass
    try:
        df["aa_size"] = df["aa_size"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_index"] = df["aa_index"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_rights"] = df["aa_rights"].astype("category")
    except Exception:
        pass
    try:
        df["aa_links"] = df["aa_links"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_owner"] = df["aa_owner"].astype("category")
    except Exception:
        pass
    try:
        df["aa_group"] = df["aa_group"].astype("category")
    except Exception:
        pass
    try:
        df["aa_id"] = df["aa_id"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_date"] = df["aa_date"] + " " + df["aa_time"]
        df["aa_date"] = pd.to_datetime(df.aa_date)
        df = df.drop(columns=["aa_time"])
    except Exception:
        pass

    return df


def pd_add_adb_to_df():
    pd.Q_adb_to_df = get_folder_df
