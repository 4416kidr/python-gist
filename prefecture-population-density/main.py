# m/h (エムイチハーフ) というTRPGシナリオに出現する架空の都市の人口密度を現実の市区町村と比較するプログラム

import pandas as pd
import argparse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='pref.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
DF_LOG_LIMIT = 5

def log_df(level, df, n_rows, header):
    if isinstance(level, str):
        level = getattr(logging, level)
    logger.log(level, header)
    for line in df.head(n_rows).to_string().splitlines():
        logger.log(level, line)

def tokyo():
    FUNC_NAME = "tokyo"
    df_tsv_sep = pd.read_csv("tsv-files/tokyo.tsv", index_col=0, sep='\t')
    log_df("INFO", df_tsv_sep, DF_LOG_LIMIT, f"[{FUNC_NAME}] read result")
    df_tsv_sep.loc["とよあしはら"] = ["500,000", "24.00"]
    df_tsv_sep["z"] = df_tsv_sep["人口"].str.replace(",", "").astype('float64')
    df_tsv_sep["m"] = df_tsv_sep["面積"].str.replace(",", "").astype('float64')
    df_tsv_sep["人口密度"] = df_tsv_sep["z"]/df_tsv_sep["m"]
    log_df("INFO", df_tsv_sep, DF_LOG_LIMIT, f"[{FUNC_NAME}] calculate result")
    sorted_df = df_tsv_sep.sort_values("人口密度", ascending=False)
    sorted_df = sorted_df.drop(["z", "m"], axis=1)
    log_df("INFO", sorted_df, DF_LOG_LIMIT, f"[{FUNC_NAME}] density sorted result")
    print(sorted_df.head(10))

def oosaka():
    FUNC_NAME = "oosaka"
    df_tsv_sep = pd.read_csv("tsv-files/oosaka.tsv", index_col=0, sep='\t')
    log_df("INFO", df_tsv_sep, DF_LOG_LIMIT, f"[{FUNC_NAME}] read result")
    df_tsv_sep.loc["豊葦原"] = ["とよあしはら", "500,000", "24.00", str('{:,.2f}'.format(500000/24.0, 2)), ""]
    df_tsv_sep["zm"] = df_tsv_sep["人口密度"].str.replace(",", "").astype('float64')
    log_df("INFO", df_tsv_sep, DF_LOG_LIMIT, f"[{FUNC_NAME}] parse result")
    sorted_df = df_tsv_sep.sort_values("zm", ascending=False)
    sorted_df = sorted_df.drop(["読み", "施行日", "人口密度"], axis=1)
    sorted_df = sorted_df.rename(columns={"zm": "人口密度"})
    log_df("INFO", sorted_df, DF_LOG_LIMIT, f"[{FUNC_NAME}] density sorted result")
    print(sorted_df.head(10))

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--pref", type=str, choices=["tokyo", "oosaka"])
    args = argparser.parse_args()
    if args.pref == "tokyo":
        tokyo()
    elif args.pref == "oosaka":
        oosaka()
    else:
        print("Please specify prefecture name")

if __name__ == "__main__":
    main()
