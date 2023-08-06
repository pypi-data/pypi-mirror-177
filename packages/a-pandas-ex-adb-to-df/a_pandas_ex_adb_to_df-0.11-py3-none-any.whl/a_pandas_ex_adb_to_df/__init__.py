import os
import re
import subprocess
import pandas as pd
import regex
from flatten_everything import flatten_everything
from com.dtmilano.android.viewclient import ViewClient
from flexible_partial import FlexiblePartial

pulledfilecompiled = regex.compile(r"1\s+file\s+pulled", flags=regex.IGNORECASE)


def connect_to_adb(
    serialnumber: str, adb_path: str = r"C:\ProgramData\adb\adb.exe",
):
    _ = subprocess.run(f"{adb_path} start-server", capture_output=True, shell=False)
    kwargs1 = {
        "timeout": 30,
        "ignoreversioncheck": False,
        "verbose": True,
        "ignoresecuredevice": False,
        "serialno": f"{serialnumber}",
    }
    device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
    return device


def remove_file(fullpath_on_device,device):
    print(f'Deleting {fullpath_on_device}                         ', end='\r')
    return device.shell(f'''rm -f "{fullpath_on_device}"''')

def pull_adb_file(save_in_folder, folder_on_device, fullpath_on_device, adb_path,serialnumber):
    print(save_in_folder, folder_on_device, fullpath_on_device, adb_path)
    savepath_folder = (
        os.path.join(save_in_folder, folder_on_device)
        .replace("/", os.sep)
        .replace("\\", os.sep)
    )

    savepath = (
        os.path.join(save_in_folder, fullpath_on_device)
        .replace("/", os.sep)
        .replace("\\", os.sep)
    )
    if not os.path.exists(savepath_folder):
        os.makedirs(savepath_folder)
    ps = subprocess.run(
        f'"{adb_path}" -s {serialnumber} pull "{fullpath_on_device}" "{savepath}"',
        capture_output=True,
        shell=True,
    )
    output=ps.stdout.decode("utf-8", "replace")
    print(output)
    if pulledfilecompiled.search(output) is not None:
        return True
    else:
        return False


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

    df.aa_fullpath = df.aa_fullpath.astype("string").str.replace(
        r"\\(\s+)", r"\g<1>", regex=True, flags=regex.IGNORECASE
    )
    df.aa_folder = df.aa_folder.astype("string").str.replace(
        r"\\(\s+)", r"\g<1>", regex=True, flags=regex.IGNORECASE
    )
    df.aa_filename = df.aa_filename.astype("string").str.replace(
        r"\\(\s+)", r"\g<1>", regex=True, flags=regex.IGNORECASE
    )

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

    df["ff_pull_file"] = df.apply(
        lambda x: FlexiblePartial(
            pull_adb_file,
            True,
            folder_on_device=x.aa_folder,
            fullpath_on_device=x.aa_fullpath,
            adb_path=adb_path,
            serialnumber=device.__dict__['serialno']
        ),
        axis=1,
    )
    df["ff_remove_file"] = df.apply(
        lambda x: FlexiblePartial(
            remove_file,
            True,
            fullpath_on_device=x.aa_fullpath,
            device=device
        ),
        axis=1,
    )
    return df


def pd_add_adb_to_df():
    pd.Q_adb_to_df = get_folder_df
