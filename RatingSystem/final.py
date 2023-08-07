import time
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def weightRatingSystem():
    st=time.time()
    print("Started executing WeightRatingSystem.py")
    #return 0
    def mainCompanySeoFileProcessing():

        main_company_file = 'test1.csv'

        df=pd.read_csv(main_company_file)

        # Create a boolean mask to identify rows to delete
        #mask = df['Website Data Type'].isin(['Website Panel', 'Competitors Panel', 'Marketing Channel Distribution Panel', 'Keywords Panel','Category Name','First Competitor','Second Competitor','Third Competitor','Fourth Competitor','Fifth Competitor'])

        # Use the boolean mask to select the rows and columns you want to modify
        #df.loc[mask, 'Website Data Type':'Website Data'] = None

        web_rows_to_delete = ['Website Panel', 'Company Name', 'Competitors Panel', 'Marketing Channel Distribution Panel', 'Keywords Panel','Category Name','First Competitor','Second Competitor','Third Competitor','Fourth Competitor','Fifth Competitor']
        # Delete the rows
        df.loc[df['Website Data Type'].isin(web_rows_to_delete), 'Website Data Type':'Website Data'] = np.nan

        #df['Website Data'] = df['Website Data'].apply(lambda x: float(x.replace('%', '')) / 100 if '%' in str(x) else x)

        # Function to process strings
        def process_string(x):
            str_x = str(x)
            # Check if x is a percentage
            if '%' in str_x:
                return float(str_x.replace('%', '')) / 100
            # Check if x starts with a number and is in 'K' or 'M' format
            elif str_x[0].isdigit():
                if 'K' in str_x:
                    return float(str_x.replace('K', '')) * 1_000
                elif 'M' in str_x:
                    return float(str_x.replace('M', '')) * 1_000_000
                elif ':' in str_x:  # Check if x is in 'HH:MM:SS' or 'MM:SS' format
                    time_parts = list(map(int, str_x.split(':')))
                    if len(time_parts) == 3:  # 'HH:MM:SS' format
                        hours, minutes, seconds = time_parts
                        return float(hours * 3600 + minutes * 60 + seconds)
                    elif len(time_parts) == 2:  # 'MM:SS' format
                        minutes, seconds = time_parts
                        return float(minutes * 60 + seconds)
                else:  # Convert other numeric strings to float
                    return float(str_x)
            # If x is neither a percentage nor in 'K' or 'M' format or a time, leave it as it is
            return x

        # Apply the function to each value in the 'Website Data' column
        df['Website Data'] = df['Website Data'].apply(process_string)

        # Function to convert numbers to float
        def convert_to_float(x):
            try:
                return float(x)
            except ValueError:
                return x

        # Apply the function to each value in the 'SemRush API Data' column
        #df['SemRush API Data'] = df['SemRush API Data'].apply(convert_to_float)

        # Identify the rows you want to delete
        rows_to_delete = ['Database', 'Domain', 'Date']  # Replace these with the names of the rows you want to delete

        # Delete the rows
        df.loc[df['SemRush API Data Type'].isin(rows_to_delete), 'SemRush API Data Type':'SemRush API Data'] = np.nan
        # Split the DataFrame into two
        mainCompanyWebDataDF = df[['Website Data Type', 'Website Data']].copy()
        mainCompanySemRushDF = df[['SemRush API Data Type', 'SemRush API Data']].copy()
        # Drop rows where all values are missing
        mainCompanyWebDataDF.dropna(how='all', inplace=True)
        mainCompanySemRushDF.dropna(how='all', inplace=True)

        # Append the second DataFrame to the first
        #df_final = df1.append(df2, ignore_index=True)

        #df.to_csv('RatingSystem\\normalMainCompany.csv',index=False)
        #mainCompanyWebDataDF.to_csv('RatingSystem\\WebDataMainCompany.csv',index=False)
        #mainCompanySemRushDF.to_csv('RatingSystem\\semRushDataMainCompany.csv',index=False)
        #print(df)

        # Rename the columns in the second DataFrame
        mainCompanySemRushDF.columns = ['Website Data Type', 'Website Data']


        # Append the second DataFrame to the first

        df_final = pd.concat([mainCompanyWebDataDF, mainCompanySemRushDF], ignore_index=True)

        # Sort the DataFrame based on the 'Website Data Type' column
        df_final = df_final.sort_values('Website Data Type')
        df_final.to_csv('RatingSystem\\regularDataWebSeo\\allDataMainCompany.csv',index=False)

        #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            #print(df)
        return df_final

    #########################################################################


    def competitorsSeoFileProcessing():

        competitor_files = ['DataML\\Competitors\\seoCompetitor_1.csv',
                            'DataML\\Competitors\\seoCompetitor_2.csv',
                            'DataML\\Competitors\\seoCompetitor_3.csv',
                            'DataML\\Competitors\\seoCompetitor_4.csv',
                            'DataML\\Competitors\\seoCompetitor_5.csv']

        # Function to process strings
        def process_string(x):
            str_x = str(x)
            # Check if x is a percentage
            if '%' in str_x:
                return float(str_x.replace('%', '')) / 100
            # Check if x starts with a number and is in 'K' or 'M' format
            elif str_x[0].isdigit():
                if 'K' in str_x:
                    return float(str_x.replace('K', '')) * 1_000
                elif 'M' in str_x:
                    return float(str_x.replace('M', '')) * 1_000_000
                elif ':' in str_x:  # Check if x is in 'HH:MM:SS' or 'MM:SS' format
                    time_parts = list(map(int, str_x.split(':')))
                    if len(time_parts) == 3:  # 'HH:MM:SS' format
                        hours, minutes, seconds = time_parts
                        return float(hours * 3600 + minutes * 60 + seconds)
                    elif len(time_parts) == 2:  # 'MM:SS' format
                        minutes, seconds = time_parts
                        return float(minutes * 60 + seconds)
                else:  # Convert other numeric strings to float
                    return float(str_x)
            # If x is neither a percentage nor in 'K' or 'M' format or a time, leave it as it is
            return x

        # Function to convert numbers to float
        def convert_to_float(x):
            try:
                return float(x)
            except ValueError:
                return x


        # Create an empty list to store the final DataFrames
        final_dfs = []
        for i, file in enumerate(competitor_files, 1):  # 'i' starts from 1
            df = pd.read_csv(file)

            # Create a boolean mask to identify rows to delete
            #mask = df['Website Data Type'].isin(['Website Panel', 'Competitors Panel', 'Marketing Channel Distribution Panel', 'Keywords Panel','Category Name','First Competitor','Second Competitor','Third Competitor','Fourth Competitor','Fifth Competitor'])

            # Use the boolean mask to select the rows and columns you want to modify
            #df.loc[mask, 'Website Data Type':'Website Data'] = None

            web_rows_to_delete = ['Website Panel','Category Name', 'Company Name',
                                'Keywords Panel: Competitor_1','Marketing Channel Distribution Panel: Competitor_1',
                                'Keywords Panel: Competitor_2','Marketing Channel Distribution Panel: Competitor_2',
                                'Keywords Panel: Competitor_3','Marketing Channel Distribution Panel: Competitor_3',
                                'Keywords Panel: Competitor_4','Marketing Channel Distribution Panel: Competitor_4',
                                'Keywords Panel: Competitor_5','Marketing Channel Distribution Panel: Competitor_5']
            # Delete the rows
            df.loc[df['Website Data Type'].isin(web_rows_to_delete), 'Website Data Type':'Website Data'] = np.nan

            #df['Website Data'] = df['Website Data'].apply(lambda x: float(x.replace('%', '')) / 100 if '%' in str(x) else x)


            # Apply the function to each value in the 'Website Data' column
            df['Website Data'] = df['Website Data'].apply(process_string)

            # Apply the function to each value in the 'SemRush API Data' column
            df[f'SemRush API Data: Competitor_{i}'] = df[f'SemRush API Data: Competitor_{i}'].apply(convert_to_float)

            # Identify the rows you want to delete
            rows_to_delete = ['Database', 'Domain', 'Date']  # Replace these with the names of the rows you want to delete

            # Delete the rows
            df.loc[df[f'SemRush API Data Type: Competitor_{i}'].isin(rows_to_delete), f'SemRush API Data Type: Competitor_{i}':f'SemRush API Data: Competitor_{i}'] = np.nan
            # Split the DataFrame into two
            competitorWebDataDF = df[['Website Data Type', 'Website Data']].copy()
            competitorSemRushDF = df[[f'SemRush API Data Type: Competitor_{i}', f'SemRush API Data: Competitor_{i}']].copy()
            # Drop rows where all values are missing
            competitorWebDataDF.dropna(how='all', inplace=True)
            competitorSemRushDF.dropna(how='all', inplace=True)

            # Append the second DataFrame to the first
            #df_final = df1.append(df2, ignore_index=True)

            #df.to_csv(f'normalCompetitor{i}.csv',index=False)
            #competitorWebDataDF.to_csv(f'RatingSystem\\webDataCompetitor_{i}.csv',index=False)
            #competitorSemRushDF.to_csv(f'RatingSystem\\semRushDataCompetitor_{i}.csv',index=False)
            #print(df)

            # Rename the columns in the second DataFrame
            competitorSemRushDF.columns = ['Website Data Type', 'Website Data']


            # Append the second DataFrame to the first

            df_final = pd.concat([competitorWebDataDF, competitorSemRushDF], ignore_index=True)

            # Sort the DataFrame based on the 'Website Data Type' column
            df_final = df_final.sort_values('Website Data Type')
            df_final.to_csv(f'RatingSystem\\regularDataWebSeo\\allDataCompetitor_{i}.csv',index=False)

            # Append the final DataFrame for this iteration to the list
            final_dfs.append(df_final)

            #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                #print(df)
        # Return the list of final DataFrames
        return final_dfs

    #########################################################################


    df_main = mainCompanySeoFileProcessing()
    final_dataframes = competitorsSeoFileProcessing()
    df_comp1 = final_dataframes[0]
    df_comp2 = final_dataframes[1]
    df_comp3 = final_dataframes[2]
    df_comp4 = final_dataframes[3]
    df_comp5 = final_dataframes[4]

    #########################################################################


    dataframes = {}  # A dictionary to hold your new DataFrames

    for data_type in df_main['Website Data Type'].unique():
        # Create a new DataFrame for this data_type
        df_new = pd.DataFrame()

        # Add data from the main company
        df_main_tmp = df_main[df_main['Website Data Type'] == data_type].copy()
        df_main_tmp['Source'] = 'Main'
        df_new = pd.concat([df_new, df_main_tmp], ignore_index=True)

        # Add data from each competitor
        for i, df_comp in enumerate([df_comp1, df_comp2, df_comp3, df_comp4, df_comp5]):
            df_comp_tmp = df_comp[df_comp['Website Data Type'] == data_type].copy()
            df_comp_tmp['Source'] = f'Competitor {i+1}'
            df_new = pd.concat([df_new, df_comp_tmp], ignore_index=True)
            #print(df_new)
            #df_new.to_csv('Merged.csv',index=False)

        # Store the new DataFrame in the dictionary
        dataframes[data_type] = df_new
        #print(dataframes)

        scaler = MinMaxScaler()  # Initialize a scaler

    # Apply MinMaxScaler to each DataFrame
    for data_type, df in dataframes.items():
        df['Website Data'] = scaler.fit_transform(df[['Website Data']])
        dataframes[data_type] = df

    #print(len(dataframes))
    #dataframes['SERP Features Traffic Branded']['Website Data'][2]=5.0
    #dataframes['SERP Features Traffic Branded']['Website Data'][3]=4.5
    #dataframes['SERP Features Traffic Branded']['Website Data'][4]=4.3
    #print(dataframes['Bounce Rate'])
    #print(dataframes['SERP Features Positions Branded'])

    #########################################################################


    # Initialize DataFrames for each source
    df_main = pd.DataFrame()
    df_comp1 = pd.DataFrame()
    df_comp2 = pd.DataFrame()
    df_comp3 = pd.DataFrame()
    df_comp4 = pd.DataFrame()
    df_comp5 = pd.DataFrame()

    # Consolidate the data for each source
    for df in dataframes.values():
        df_main = pd.concat([df_main, df[df['Source'] == 'Main']], ignore_index=True)
        df_comp1 = pd.concat([df_comp1, df[df['Source'] == 'Competitor 1']], ignore_index=True)
        df_comp2 = pd.concat([df_comp2, df[df['Source'] == 'Competitor 2']], ignore_index=True)
        df_comp3 = pd.concat([df_comp3, df[df['Source'] == 'Competitor 3']], ignore_index=True)
        df_comp4 = pd.concat([df_comp4, df[df['Source'] == 'Competitor 4']], ignore_index=True)
        df_comp5 = pd.concat([df_comp5, df[df['Source'] == 'Competitor 5']], ignore_index=True)
    #print(df_comp5)


    #########################################################################


    # Write each DataFrame to a CSV file
    df_main.to_csv('RatingSystem\\finalDataWebSeo\\main.csv', index=False)
    df_comp1.to_csv('RatingSystem\\finalDataWebSeo\\comp1.csv', index=False)
    df_comp1.to_csv('RatingSystem\\finalDataWebSeo\\comp2.csv', index=False)
    df_comp3.to_csv('RatingSystem\\finalDataWebSeo\\comp3.csv', index=False)
    df_comp4.to_csv('RatingSystem\\finalDataWebSeo\\comp4.csv', index=False)
    df_comp5.to_csv('RatingSystem\\finalDataWebSeo\\comp5.csv', index=False)

    #########################################################################


    def mainCompanySocialMediaFileProcessing():
        socialMediaFile = 'test.csv'

        df=pd.read_csv(socialMediaFile)
        df.replace('Not Available', np.nan, inplace=True)

        # Function to process strings
        def process_string(x):
            str_x = str(x)
            # Check if x is a percentage
            if '%' in str_x:
                return float(str_x.replace('%', '')) / 100
            # Check if x starts with a number and is in 'K' or 'M' format
            elif str_x[0].isdigit():
                if 'K' in str_x:
                    return float(str_x.replace('K', '')) * 1_000
                elif 'M' in str_x:
                    return float(str_x.replace('M', '')) * 1_000_000
                elif ':' in str_x:  # Check if x is in 'HH:MM:SS' or 'MM:SS' format
                    time_parts = list(map(int, str_x.split(':')))
                    if len(time_parts) == 3:  # 'HH:MM:SS' format
                        hours, minutes, seconds = time_parts
                        return float(hours * 3600 + minutes * 60 + seconds)
                    elif len(time_parts) == 2:  # 'MM:SS' format
                        minutes, seconds = time_parts
                        return float(minutes * 60 + seconds)
                else:  # Convert other numeric strings to float
                    return float(str_x)
            # If x is neither a percentage nor in 'K' or 'M' format or a time, leave it as it is
            return x



        # Specify columns to drop
        columns_to_drop = ['Social Platform Link', 'Social Platform Username', ]

        # Drop the columns
        df = df.drop(columns=columns_to_drop)

        # First, let's melt the DataFrame to a long format
        df_melted = df.melt(id_vars=['Social Platform Name'], var_name='Social Data Type', value_name='Social Data')

        # Then, rename 'Social Platform Name' to 'Source'
        df_melted = df_melted.rename(columns={'Social Platform Name': 'Social Platform'})

        # Apply the function to each value in the 'Website Data' column
        df_melted['Social Data'] = df_melted['Social Data'].apply(process_string)
        df_melted = df_melted[~((df_melted['Social Platform'] == 'Linkedin') & (df_melted['Social Data Type'] == 'Followers Count')  & df_melted['Social Data'].isna())]
        df_melted.replace('Linkedin', 'LinkedIn', inplace=True)
        df_melted = df_melted[~((df_melted['Social Platform'] == 'Facebook') & (df_melted['Social Data Type'] == 'Average Comments per 5 posts'))]
        # Drop rows where all values are missing
        df_melted.dropna(how='all', inplace=True)

        # Function to convert numbers to float
        def convert_to_float(x):
            try:
                return float(x)
            except ValueError:
                return x
        # Add the platform name as a prefix to each value in the 'Social Data Type' column
        df_melted['Social Data Type'] = df_melted.apply(lambda row: f"{row['Social Data Type']} {row['Social Platform']}", axis=1)

        # Save your processed DataFrame to a new CSV file
        df_melted.to_csv('RatingSystem\\regularDataSocial\\processed_social_media_Main.csv', index=False)
        #df.to_csv('Actual\\testsss\\DataNormalRating\\regularData\\social.csv')
        return df_melted

    def competitorsSocialMediaFileProcessing():
        competitor_files = ['DataML\\Competitors\\socialCompetitor_1.csv',
                            'DataML\\Competitors\\socialCompetitor_2.csv',
                            'DataML\\Competitors\\socialCompetitor_3.csv',
                            'DataML\\Competitors\\socialCompetitor_4.csv',
                            'DataML\\Competitors\\socialCompetitor_5.csv'
                            ]


        # Function to process strings
        def process_string(x):
            str_x = str(x)
            # Check if x is a percentage
            if '%' in str_x:
                return float(str_x.replace('%', '')) / 100
            # Check if x starts with a number and is in 'K' or 'M' format
            elif str_x[0].isdigit():
                if 'K' in str_x:
                    return float(str_x.replace('K', '')) * 1_000
                elif 'M' in str_x:
                    return float(str_x.replace('M', '')) * 1_000_000
                elif ':' in str_x:  # Check if x is in 'HH:MM:SS' or 'MM:SS' format
                    time_parts = list(map(int, str_x.split(':')))
                    if len(time_parts) == 3:  # 'HH:MM:SS' format
                        hours, minutes, seconds = time_parts
                        return float(hours * 3600 + minutes * 60 + seconds)
                    elif len(time_parts) == 2:  # 'MM:SS' format
                        minutes, seconds = time_parts
                        return float(minutes * 60 + seconds)
                else:  # Convert other numeric strings to float
                    return float(str_x)
            # If x is neither a percentage nor in 'K' or 'M' format or a time, leave it as it is
            return x

        # Create an empty list to store the final DataFrames
        final_dfs = []
        for i, file in enumerate(competitor_files, 1):  # 'i' starts from 1
            df = pd.read_csv(file)
            df.replace('Not Available', np.nan, inplace=True)

            # Specify columns to drop
            columns_to_drop = ['Social Platform Link', 'Social Platform Username']

            # Drop the columns
            df = df.drop(columns=columns_to_drop)

            # First, let's melt the DataFrame to a long format
            df_melted = df.melt(id_vars=['Social Platform Name'], var_name='Social Data Type', value_name='Social Data')

            # Then, rename 'Social Platform Name' to 'Source'
            df_melted = df_melted.rename(columns={'Social Platform Name': 'Social Platform'})
            # Apply the function to each value in the 'Website Data' column
            df_melted['Social Data'] = df_melted['Social Data'].apply(process_string)
            df_melted = df_melted[~((df_melted['Social Platform'] == 'Linkedin') & (df_melted['Social Data Type'] == 'Followers Count')  & df_melted['Social Data'].isna())]
            df_melted.replace('Linkedin', 'LinkedIn', inplace=True)
            df_melted = df_melted[~((df_melted['Social Platform'] == 'Facebook') & (df_melted['Social Data Type'] == 'Average Comments per 5 posts'))]
            # Drop rows where all values are missing
            df_melted.dropna(how='all', inplace=True)
            # Append the final DataFrame for this iteration to the list

            # Add the platform name as a prefix to each value in the 'Social Data Type' column
            df_melted['Social Data Type'] = df_melted.apply(lambda row: f"{row['Social Data Type']} {row['Social Platform']}", axis=1)


            # Save your processed DataFrame to a new CSV file
            df_melted.to_csv(f'RatingSystem\\regularDataSocial\\processed_social_media_Competior_{i}.csv', index=False)
            final_dfs.append(df_melted)


        #df.to_csv('Actual\\testsss\\DataNormalRating\\regularData\\social.csv')
        return final_dfs

    #########################################################################


    df_main_social=mainCompanySocialMediaFileProcessing()
    final_dataframes_social = competitorsSocialMediaFileProcessing()
    df_social_comp1 = final_dataframes_social[0]
    df_social_comp2 = final_dataframes_social[1]
    df_social_comp3 = final_dataframes_social[2]
    df_social_comp4 = final_dataframes_social[3]
    df_social_comp5 = final_dataframes_social[4]
    #print(df_social_comp1)

    #########################################################################

    dataframes_social = {}  # A dictionary to hold your new DataFrames

    for data_type in df_main_social['Social Data Type'].unique():
        # Create a new DataFrame for this data_type
        df_new = pd.DataFrame()

        # Add data from the main company
        df_main_tmp = df_main_social[df_main_social['Social Data Type'] == data_type].copy()
        df_main_tmp['Source'] = 'Main'
        df_new = pd.concat([df_new, df_main_tmp], ignore_index=True)

        # Add data from each competitor
        for i, df_social_comp in enumerate([df_social_comp1, df_social_comp2, df_social_comp3, df_social_comp4, df_social_comp5]):
            df_comp_tmp = df_social_comp[df_social_comp['Social Data Type'] == data_type].copy()
            df_comp_tmp['Source'] = f'Competitor {i+1}'
            df_new = pd.concat([df_new, df_comp_tmp], ignore_index=True)

        # Store the new DataFrame in the dictionary
        dataframes_social[data_type] = df_new

    # Apply MinMaxScaler to each DataFrame
    for data_type, df in dataframes_social.items():
        scaler = MinMaxScaler()  # Initialize a new scaler for each D/ataFrame
        df['Social Data'] = scaler.fit_transform(df[['Social Data']])
        dataframes_social[data_type] = df

    #print(len(dataframes_social))
    #print(dataframes_social)
    #print(dataframes_social['Followers Count Instagram'])
    #print(dataframes_social['Average Likes per 5 posts LinkedIn'])


    #########################################################################


    # Initialize DataFrames for each source
    df_social_main = pd.DataFrame()
    df_social_comp1 = pd.DataFrame()
    df_social_comp2 = pd.DataFrame()
    df_social_comp3 = pd.DataFrame()
    df_social_comp4 = pd.DataFrame()
    df_social_comp5 = pd.DataFrame()

    # Consolidate the data for each source
    for df in dataframes_social.values():
        df_social_main = pd.concat([df_social_main, df[df['Source'] == 'Main']], ignore_index=True)
        df_social_comp1 = pd.concat([df_social_comp1, df[df['Source'] == 'Competitor 1']], ignore_index=True)
        df_social_comp2 = pd.concat([df_social_comp2, df[df['Source'] == 'Competitor 2']], ignore_index=True)
        df_social_comp3 = pd.concat([df_social_comp3, df[df['Source'] == 'Competitor 3']], ignore_index=True)
        df_social_comp4 = pd.concat([df_social_comp4, df[df['Source'] == 'Competitor 4']], ignore_index=True)
        df_social_comp5 = pd.concat([df_social_comp5, df[df['Source'] == 'Competitor 5']], ignore_index=True)
    #print(df_social_comp3)

    #########################################################################

    # Write each DataFrame to a CSV file
    df_social_main.to_csv('RatingSystem\\finalDataSocial\\social_main.csv', index=False)
    df_social_comp1.to_csv('RatingSystem\\finalDataSocial\\social_comp1.csv', index=False)
    df_social_comp2.to_csv('RatingSystem\\finalDataSocial\\social_comp2.csv', index=False)
    df_social_comp3.to_csv('RatingSystem\\finalDataSocial\\social_comp3.csv', index=False)
    df_social_comp4.to_csv('RatingSystem\\finalDataSocial\\social_comp4.csv', index=False)
    df_social_comp5.to_csv('RatingSystem\\finalDataSocial\\social_comp5.csv', index=False)


    #########################################################################

    # Load main and competitors data
    dataframes = {
        'Main': pd.read_csv('RatingSystem\\finalDataWebSeo\\main.csv'),
        'First Competitor': pd.read_csv('RatingSystem\\finalDataWebSeo\\comp1.csv'),
        'Second Competitor': pd.read_csv('RatingSystem\\finalDataWebSeo\\comp2.csv'),
        'Third Competitor': pd.read_csv('RatingSystem\\finalDataWebSeo\\comp3.csv'),
        'Fourth Competitor': pd.read_csv('RatingSystem\\finalDataWebSeo\\comp4.csv'),
        'Fifth Competitor': pd.read_csv('RatingSystem\\finalDataWebSeo\\comp5.csv')
    }

    # Load social media data for main and competitors
    social_dataframes = {
        'Main': pd.read_csv('RatingSystem\\finalDataSocial\\social_main.csv'),
        'First Competitor': pd.read_csv('RatingSystem\\finalDataSocial\\social_comp1.csv'),
        'Second Competitor': pd.read_csv('RatingSystem\\finalDataSocial\\social_comp2.csv'),
        'Third Competitor': pd.read_csv('RatingSystem\\finalDataSocial\\social_comp3.csv'),
        'Fourth Competitor': pd.read_csv('RatingSystem\\finalDataSocial\\social_comp4.csv'),
        'Fifth Competitor': pd.read_csv('RatingSystem\\finalDataSocial\\social_comp5.csv')
    }

    weights_df = pd.read_csv('RatingSystem\\allWeightsFiles\\weights.csv')
    weights_df['Platform'] = weights_df['Platform'].str.capitalize()

    category_weights_df = pd.read_csv('RatingSystem\\allWeightsFiles\\category_weights.csv')
    category_weights_df.set_index('Category', inplace=True)
    category_weights_df.index.name = 'Category'

    platform_weights_df = pd.read_csv("RatingSystem\\allWeightsFiles\\platform_weights.csv")
    platform_weights_df.set_index('Platform', inplace=True)
    platform_weights_df.index.name = 'Platform'

    competitor_weights_df = weights_df[weights_df['Category'] == 'Competitor Analysis'].copy()
    competitor_weights_df.set_index('Metric', inplace=True)
    competitor_weights_df = competitor_weights_df[['Weight']]
    competitor_weights_df.index.name = 'Competitor'

    def distribute_nan_weights(df, weights_df):
        nan_metrics = df['Website Data Type'][df['Website Data'].isna()]
        
        for metric in nan_metrics:
            if metric not in weights_df['Metric'].values:
                continue
                
            category = weights_df.loc[weights_df['Metric'] == metric, 'Category'].values[0]
            total_weight = weights_df.loc[weights_df['Category'] == category, 'Weight'].sum()
            nan_weight = weights_df.loc[weights_df['Metric'] == metric, 'Weight'].values[0]

            weights_to_distribute = nan_weight / (total_weight - nan_weight)
            valid_metrics = weights_df.loc[(weights_df['Category'] == category) & (weights_df['Metric'] != metric), 'Metric']
            
            for valid_metric in valid_metrics:
                weights_df.loc[weights_df['Metric'] == valid_metric, 'Weight'] += weights_to_distribute / len(valid_metrics)

            weights_df.loc[weights_df['Metric'] == metric, 'Weight'] = 0

    def calculate_scores(df, weights_df, category_weights_df):
        distribute_nan_weights(df, weights_df)

        weighted_metrics = df.set_index('Website Data Type')['Website Data'].mul(weights_df.set_index('Metric')['Weight'])
        category_sums = weighted_metrics.groupby(weights_df.set_index('Metric')['Category']).sum()

        weighted_categories = category_sums.mul(category_weights_df['Category Weight'])

        return weighted_categories if isinstance(weighted_categories, pd.Series) else pd.Series()

    def calculate_social_metrics(social_media_df, weights_df):
        social_media_df.columns = ['Platform', 'Metric', 'Value', 'Source']
        merged = pd.merge(social_media_df, weights_df, left_on=['Metric', 'Platform'], right_on=['Metric', 'Platform'], how='left')
        merged['Weight'].fillna(0, inplace=True)
        merged['Score'] = merged['Value'] * merged['Weight']

        grouped = merged.groupby(['Platform', 'Metric']).sum().reset_index()

        return grouped

    def calculate_social_platforms(social_media_df, platform_weights_df):
        social_media_df = calculate_social_metrics(social_media_df, weights_df)
        social_media_df = pd.merge(social_media_df, platform_weights_df, on='Platform', how='left')
        social_media_df['Platform Weight'].fillna(1, inplace=True)
        social_media_df['Score'] = social_media_df['Score'] * social_media_df['Platform Weight']
        
        return social_media_df['Score'].sum()

    def calculate_social_scores(social_dataframes, weights_df, platform_weights_df):
        social_scores = {}
        for name, df in social_dataframes.items():
            social_scores[name] = calculate_social_platforms(df, platform_weights_df)

        return social_scores

    def calculate_final_scores(dataframes, weights_df, category_weights_df, social_dataframes, platform_weights_df, competitor_weights_df):
        final_scores = {}
        for name, df in dataframes.items():
            scores = calculate_scores(df, weights_df, category_weights_df)
            final_scores[name] = scores

        social_scores = calculate_social_scores(social_dataframes, weights_df, platform_weights_df)

        for name in final_scores:
            social_media_weight = category_weights_df.loc[category_weights_df.index == 'Social Media Performance', 'Category Weight'].values[0]
            final_scores[name]['Social Media Performance'] = social_scores[name] * social_media_weight

            # Recalculate the final score after adding Social Media Performance score
            final_scores[name]['Final Score'] = final_scores[name].sum()

        # Update the main company's Competitor Analysis score to be the weighted sum of the competitors' scores
        competitor_analysis_score = sum(final_scores[competitor]['Final Score'] * competitor_weights_df.loc[competitor, 'Weight'] for competitor in final_scores if competitor != 'Main')
        competitor_analysis_score /= sum(competitor_weights_df['Weight'])
        competitor_analysis_weight = category_weights_df.loc[category_weights_df.index == 'Competitor Analysis', 'Category Weight'].values[0]
        final_scores['Main']['Competitor Analysis'] = competitor_analysis_score * competitor_analysis_weight

        # Recalculate the final score for main company after updating Competitor Analysis score
        final_scores['Main']['Final Score'] = final_scores['Main'].drop('Final Score').sum()

        return final_scores


    final_scores = calculate_final_scores(dataframes, weights_df, category_weights_df, social_dataframes, platform_weights_df, competitor_weights_df)

    # Create DataFrame and set the index name
    final_scores_df = pd.DataFrame(final_scores).T
    final_scores_df.index.name = 'Subjects'
    # Round every value to 4 decimal places
    final_scores_df = final_scores_df.round(4)
    final_scores_df.to_csv("RatingSystem\\final_scores.csv")
    print(final_scores_df)

    et=time.time()
    total_time=et-st
    print(total_time)
    print("Total executing time of WeightRatingSystem.py:",total_time ,"seconds")

    return total_time

#weightRatingSystem()