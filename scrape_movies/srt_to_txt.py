import re
import numpy as np
import zipfile
import pandas as pd
import glob

for folder in ['friendship/', 'hate_speech/', 'racism/']:
    for filename in glob.glob('movie_subtitles_zips/' + folder + '*.zip'):
        print(filename)
        movie = []
        print("opening file")
        archive = zipfile.ZipFile(filename, 'r')
        files = zipfile.ZipFile.namelist(archive)
        for file in files:
            srt_filename = re.findall(r'.*\.srt', file)
            if len(srt_filename) > 0:
                srt_filename = srt_filename[0]
                break
        if srt_filename:
            movie_data = archive.read(srt_filename)
            movie_data = movie_data.decode('ISO-8859-1').strip().replace('\r', '').split('\n')

            print("Processing file")
            df = pd.DataFrame(movie_data, columns=['dialog'])
            print(df.head())
            print(df.columns)


            def cleansing(df, n, x):
                def remove_blank_lines(df):
                    df.replace("", np.nan, inplace=True)
                    df = df.dropna()
                    return df

                def remove_brackets(df):
                    df = df.replace(r'^-?\(.*\)$', '', regex=True)
                    df = df.replace(r'\(.*?\)', '', regex=True)
                    return df

                def strip_all_values(df):
                    df = df.apply(lambda x: x.str.strip())
                    return df

                def remove_specialchars(df):
                    df = df.replace(r'[\=\-\{\}\[\]\^\#]', '', regex=True)
                    df = df.replace(r'\\... ', '', regex=True)
                    df = df.replace(r'<.*?>', '', regex=True)
                    return df

                def remove_nonchar_lines(df):
                    df = df.drop(df[df.dialog.str.contains(r'^\d?\d?\d?\d|\d\d:\d\d:\d\d,.*', regex=True)].index)
                    return df

                def remove_first_n_lines(df, n):
                    df = df.iloc[n:]
                    return df

                df = remove_blank_lines(df)
                df = strip_all_values(df)
                df = remove_brackets(df)
                df = remove_nonchar_lines(df)
                df = remove_specialchars(df)
                df = remove_blank_lines(df)
                df = remove_first_n_lines(df, n)
                df = remove_blank_lines(df)

                return df


            df_movie = cleansing(df, 1, 0)

            movie_txt = df_movie.dialog.values.tolist()

            sent = ''
            new_l = []
            for t in movie_txt:
                if t[-1] not in ['.', '?', '!']:
                    sent += t + ' '
                else:
                    sent += t
                    new_l.append(sent)
                    sent = ''

            df_movie_updated = pd.DataFrame(columns=['dialog'])
            df_movie_updated['dialog'] = new_l
            df_movie_updated.head()

            print("converting to csv")
            df_movie_updated.to_csv(
                'movie_subtitles_text/' + folder + re.findall(r'movie_subtitles_zips\/.*\\(.*)\.zip', filename)[
                    0] + '_conv.csv')
