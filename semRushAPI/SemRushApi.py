import pandas as pd
import requests
import time
from io import StringIO
import os


def semRushApi(url):
    st=time.time()
    #return 0
    print('Started executing SemRushApi.py')
    #new_path = "DigiScore\\test1.csv"
    new_path = "test1.csv"

    api_key = '8bdbff61b7aa7c84bd0a8be0ffb526c9'

    response=requests.get('http://www.semrush.com/users/countapiunits.html?key=8bdbff61b7aa7c84bd0a8be0ffb526c9')
    print(response)
    print(response.text)
    apiUnitsBeforeExecution = response.text
    apiUnitsBeforeExecution=int(apiUnitsBeforeExecution)
    print('API_Units_Before_Execution:',apiUnitsBeforeExecution)

    def get_domain_info(domain):
        try:
            domain_overview_url = "https://api.semrush.com/?type=domain_ranks&key={}&export_columns=Db,Dn,Dt,Rk,Or,Ot,Oc,Ad,At,Ac,Sh,Sv,FKn,FPn,Sr&domain={}&database=fr".format(api_key, domain)

            response = requests.get(domain_overview_url)

            if response.status_code != 200:
                print(f'Error with status code: {response.status_code}')
                return None
            print(response.text)

            data = pd.read_csv(StringIO(response.text), sep=';')  # Specify delimiter

            # Assuming the first row of the DataFrame is the relevant data
            data_dict = data.iloc[0].to_dict()
            print('--------------------------------------------------------------------------------------------')
            print(data_dict)
            print('--------------------------------------------------------------------------------------------')

            # Check if each key exists in the dictionary before unpacking
            Db = data_dict.get('Database', None)
            Dn = data_dict.get('Domain', None)
            Dt = data_dict.get('Date', None)
            Rk = data_dict.get('Rank', None)
            Or = data_dict.get('Organic Keywords', None)
            Ot = data_dict.get('Organic Traffic', None)
            Oc = data_dict.get('Organic Cost', None)
            Ad = data_dict.get('Adwords Keywords', None)
            At = data_dict.get('Adwords Traffic', None)
            Ac = data_dict.get('Adwords Cost', None)
            Sh = data_dict.get('PLA keywords', None)
            Sv = data_dict.get('PLA uniques', None)
            FKn = data_dict.get('SERP Features Positions', None)
            FPn = data_dict.get('SERP Features Positions Branded', None)
            Sr = data_dict.get('SERP Features Traffic', None)
            #Srb = data_dict.get('SERP Features Traffic Branded', None)
            #St = data_dict.get('SERP Features Traffic Cost', None)

            #return Db, Dn, Dt, Rk, Or, Ot, Oc, Ad, At, Ac, Sh, Sv, FKn, FPn, Sr, Srb, St

        except Exception as e:
            print(f'An error occurred: {e}')
            Db = None
            Dn = None
            Dt = None
            Rk = None
            Or = None
            Ot = None
            Oc = None
            Ad = None
            At = None
            Ac = None
            Sh = None
            Sv = None
            FKn = None
            FPn = None
            Sr = None
            #Srb = None
            #St = None

        return Db, Dn, Dt, Rk, Or, Ot, Oc, Ad, At, Ac, Sh, Sv, FKn, FPn, Sr, #Srb, St


    def getTopKeywords_1_3_10(domain):
        try:
            response=requests.get(f'https://api.semrush.com/?type=subdomain_rank&key={api_key}&export_columns=X0,X1&subdomain={domain}&database=fr')
            print(response)
            print(response.text)

            data = pd.read_csv(StringIO(response.text), sep=';')  # Specify delimiter

            # Assuming the first row of the DataFrame is the relevant data
            data_dict = data.iloc[0].to_dict()
            print('--------------------------------------------------------------------------------------------')
            print(data_dict)
            print('--------------------------------------------------------------------------------------------')

            # Check if each key exists in the dictionary before unpacking
            X0 = data_dict.get('X0', None)
            X1 = data_dict.get('X1', None)

            #return X0,X1

        except Exception as e:
            print(f'An error occurred: {e}')
            X0=None
            X1=None

        return X0,X1

    def main():
        domains = [url]

        # Initialize an empty DataFrame with None values
        data = pd.DataFrame({
            'Database': [None],
            'Domain': [None],
            'Date': [None],
            'Rank': [None],
            'Organic Keywords': [None],
            'Organic Traffic': [None],
            'Organic Cost': [None],
            'Adwords Keywords': [None],
            'Adwords Traffic': [None],
            'Adwords Cost': [None],
            'PLA Keywords': [None],
            'PLA Uniques': [None],
            'SERP Features Positions': [None],
            'SERP Features Positions Branded': [None],
            'SERP Features Traffic': [None],
            #'SERP Features Traffic Branded': [None],
            #'SERP Features Traffic Cost': [None],
            'Number of Keywords 1-3' : [None],
            'Number of Keywords 3-10' : [None]
        })

        for domain in domains:
            try:
                print(f"Processing domain: {domain}")
                Db, Dn, Dt, Rk, Or, Ot, Oc, Ad, At, Ac, Sh, Sv, FKn, FPn, Sr = get_domain_info(domain)
                X0, X1=getTopKeywords_1_3_10(domain)
                data = pd.DataFrame({
                    'Database': [Db],
                    'Domain': [Dn],
                    'Date': [Dt],
                    'Rank': [Rk],
                    'Organic Keywords': [Or],
                    'Organic Traffic': [Ot],
                    'Organic Cost': [Oc],
                    'Adwords Keywords': [Ad],
                    'Adwords Traffic': [At],
                    'Adwords Cost': [Ac],
                    'PLA Keywords': [Sh],
                    'PLA Uniques': [Sv],
                    'SERP Features Positions': [FKn],
                    'SERP Features Positions Branded': [FPn],
                    'SERP Features Traffic': [Sr],
                    #'SERP Features Traffic Branded': [Srb],
                    #'SERP Features Traffic Cost': [St],
                    'Number of Keywords 1-3' : [X0],
                    'Number of Keywords 3-10' : [X1]
                })
                print(f"Finished processing domain: {domain}")

            except Exception as e:
                print(f"An error occurred while processing domain {domain}: {e}")

        try:
            # Transpose DataFrame
            data_transposed = data.transpose().reset_index()

            # Rename columns
            data_transposed.columns = ['SemRushDataType', 'SemRushData']
            data_dict = data.to_dict()
            # Read the existing CSV file into a DataFrame
            df = pd.read_csv(new_path)
            '''with open(new_path, 'r') as f:
                lines = f.readlines()

            # Print each line number and the number of fields in that line
            for i, line in enumerate(lines):
                print(f"Line {i+1}: {len(line.split(','))} fields")'''


            # Read the existing CSV file into a DataFrame
            df = pd.read_csv(new_path)

            # Create a DataFrame with the new data
            new_data_list = [{'SemRush API Data Type': k, 'SemRush API Data': v[0]} for k, v in data_dict.items()]
            new_data = pd.DataFrame(new_data_list)

            # Make sure new_data has the same number of rows as df, filling with NaN if necessary
            new_data = new_data.reindex(df.index)

            # Concatenate the existing DataFrame with the new DataFrame
            df = pd.concat([df, new_data], axis=1)

            # Write the updated DataFrame back to the CSV file
            df.to_csv(new_path, index=False)
            print(df)

        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df = None

        try:
            #API units balance
            response=requests.get('http://www.semrush.com/users/countapiunits.html?key=8bdbff61b7aa7c84bd0a8be0ffb526c9')
            print(response)
            print(response.text)
            apiUnitsAfterExecution = response.text
            apiUnitsAfterExecution=int(apiUnitsAfterExecution)
            apiUnitsSpent = apiUnitsAfterExecution-apiUnitsBeforeExecution
            print('API_Units_Left:',apiUnitsAfterExecution)
            print('API_Units_Spent:',apiUnitsSpent)
        except Exception as e:
            print("An error occured:",e)

    main()
        # At the end of the function, add:
    et=time.time()
    semRushApi_time=et-st
    print('Total execution time of SemRushApi.py is:',semRushApi_time,'seconds')
    return semRushApi_time


#semRushApi('https://www.esg.fr/')



##########################################################################################################################################
#COMPETITORS FUNCTION
##########################################################################################################################################



def semRushApiCompetitor(url,competitor_num):
    st=time.time()
    #return 0
    print('Started executing SemRushApiCompetitor.py')
    #new_path = f"DigiScore\\DataML\\Competitors\\seoCompetitor_{competitor_num}.csv"
    #new_path = f"DataML\\Competitors\\seoCompetitor_{competitor_num}.csv"
    new_path = os.path.join('DataML', 'Competitors', f'seoCompetitor_{competitor_num}.csv')


    api_key = '8bdbff61b7aa7c84bd0a8be0ffb526c9'

    response=requests.get('http://www.semrush.com/users/countapiunits.html?key=8bdbff61b7aa7c84bd0a8be0ffb526c9')
    print(response)
    print(response.text)
    apiUnitsBeforeExecution = response.text
    apiUnitsBeforeExecution=int(apiUnitsBeforeExecution)
    print('API_Units_Before_Execution:',apiUnitsBeforeExecution)

    def get_domain_info(domain):
        try:
            domain_overview_url = "https://api.semrush.com/?type=domain_ranks&key={}&export_columns=Db,Dn,Dt,Rk,Or,Ot,Oc,Ad,At,Ac,Sh,Sv,FKn,FPn,Sr&domain={}&database=fr".format(api_key, domain)

            response = requests.get(domain_overview_url)

            if response.status_code != 200:
                print(f'Error with status code: {response.status_code}')
                return None
            print(response.text)

            data = pd.read_csv(StringIO(response.text), sep=';')  # Specify delimiter

            # Assuming the first row of the DataFrame is the relevant data
            data_dict = data.iloc[0].to_dict()
            print('--------------------------------------------------------------------------------------------')
            print(data_dict)
            print('--------------------------------------------------------------------------------------------')

            # Check if each key exists in the dictionary before unpacking
            Db = data_dict.get('Database', None)
            Dn = data_dict.get('Domain', None)
            Dt = data_dict.get('Date', None)
            Rk = data_dict.get('Rank', None)
            Or = data_dict.get('Organic Keywords', None)
            Ot = data_dict.get('Organic Traffic', None)
            Oc = data_dict.get('Organic Cost', None)
            Ad = data_dict.get('Adwords Keywords', None)
            At = data_dict.get('Adwords Traffic', None)
            Ac = data_dict.get('Adwords Cost', None)
            Sh = data_dict.get('PLA keywords', None)
            Sv = data_dict.get('PLA uniques', None)
            FKn = data_dict.get('SERP Features Positions', None)
            FPn = data_dict.get('SERP Features Positions Branded', None)
            Sr = data_dict.get('SERP Features Traffic', None)
            #Srb = data_dict.get('SERP Features Traffic Branded', None)
            #St = data_dict.get('SERP Features Traffic Cost', None)

            #return Db, Dn, Dt, Rk, Or, Ot, Oc, Ad, At, Ac, Sh, Sv, FKn, FPn, Sr, Srb, St

        except Exception as e:
            print(f'An error occurred: {e}')
            Db = None
            Dn = None
            Dt = None
            Rk = None
            Or = None
            Ot = None
            Oc = None
            Ad = None
            At = None
            Ac = None
            Sh = None
            Sv = None
            FKn = None
            FPn = None
            Sr = None
            #Srb = None
            #St = None

        return Db, Dn, Dt, Rk, Or, Ot, Oc, Ad, At, Ac, Sh, Sv, FKn, FPn, Sr, #Srb, St


    def getTopKeywords_1_3_10(domain):
        try:
            response=requests.get(f'https://api.semrush.com/?type=subdomain_rank&key={api_key}&export_columns=X0,X1&subdomain={domain}&database=fr')
            print(response)
            print(response.text)

            data = pd.read_csv(StringIO(response.text), sep=';')  # Specify delimiter

            # Assuming the first row of the DataFrame is the relevant data
            data_dict = data.iloc[0].to_dict()
            print('--------------------------------------------------------------------------------------------')
            print(data_dict)
            print('--------------------------------------------------------------------------------------------')

            # Check if each key exists in the dictionary before unpacking
            X0 = data_dict.get('X0', None)
            X1 = data_dict.get('X1', None)

            #return X0,X1

        except Exception as e:
            print(f'An error occurred: {e}')
            X0=None
            X1=None

        return X0,X1

    def main():
        domains = [url]

        # Initialize an empty DataFrame with None values
        data = pd.DataFrame({
            'Database': [None],
            'Domain': [None],
            'Date': [None],
            'Rank': [None],
            'Organic Keywords': [None],
            'Organic Traffic': [None],
            'Organic Cost': [None],
            'Adwords Keywords': [None],
            'Adwords Traffic': [None],
            'Adwords Cost': [None],
            'PLA Keywords': [None],
            'PLA Uniques': [None],
            'SERP Features Positions': [None],
            'SERP Features Positions Branded': [None],
            'SERP Features Traffic': [None],
            #'SERP Features Traffic Branded': [None],
            #'SERP Features Traffic Cost': [None],
            'Number of Keywords 1-3' : [None],
            'Number of Keywords 3-10' : [None]
        })

        for domain in domains:
            try:
                print(f"Processing domain: {domain}")
                Db, Dn, Dt, Rk, Or, Ot, Oc, Ad, At, Ac, Sh, Sv, FKn, FPn, Sr = get_domain_info(domain)
                X0, X1=getTopKeywords_1_3_10(domain)
                data = pd.DataFrame({
                    'Database': [Db],
                    'Domain': [Dn],
                    'Date': [Dt],
                    'Rank': [Rk],
                    'Organic Keywords': [Or],
                    'Organic Traffic': [Ot],
                    'Organic Cost': [Oc],
                    'Adwords Keywords': [Ad],
                    'Adwords Traffic': [At],
                    'Adwords Cost': [Ac],
                    'PLA Keywords': [Sh],
                    'PLA Uniques': [Sv],
                    'SERP Features Positions': [FKn],
                    'SERP Features Positions Branded': [FPn],
                    'SERP Features Traffic': [Sr],
                    #'SERP Features Traffic Branded': [Srb],
                    #'SERP Features Traffic Cost': [St],
                    'Number of Keywords 1-3' : [X0],
                    'Number of Keywords 3-10' : [X1]
                })
                print(f"Finished processing domain: {domain}")

            except Exception as e:
                print(f"An error occurred while processing domain {domain}: {e}")

        try:
            # Transpose DataFrame
            data_transposed = data.transpose().reset_index()

            # Rename columns
            data_transposed.columns = ['SemRushDataType', 'SemRushData']
            data_dict = data.to_dict()
            # Read the existing CSV file into a DataFrame
            df = pd.read_csv(new_path)
            '''with open(new_path, 'r') as f:
                lines = f.readlines()

            # Print each line number and the number of fields in that line
            for i, line in enumerate(lines):
                print(f"Line {i+1}: {len(line.split(','))} fields")'''


            # Read the existing CSV file into a DataFrame
            df = pd.read_csv(new_path)

            # Create a DataFrame with the new data
            new_data_list = [{f'SemRush API Data Type: Competitor_{competitor_num}': k, f'SemRush API Data: Competitor_{competitor_num}': v[0]} for k, v in data_dict.items()]
            new_data = pd.DataFrame(new_data_list)

            # Make sure new_data has the same number of rows as df, filling with NaN if necessary
            new_data = new_data.reindex(df.index)

            # Concatenate the existing DataFrame with the new DataFrame
            df = pd.concat([df, new_data], axis=1)

            # Write the updated DataFrame back to the CSV file
            df.to_csv(new_path, index=False)
            print(df)

        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df = None

        try:
            #API units balance
            response=requests.get('http://www.semrush.com/users/countapiunits.html?key=8bdbff61b7aa7c84bd0a8be0ffb526c9')
            print(response)
            print(response.text)
            apiUnitsAfterExecution = response.text
            apiUnitsAfterExecution=int(apiUnitsAfterExecution)
            apiUnitsSpent = apiUnitsAfterExecution-apiUnitsBeforeExecution
            print('API_Units_Left:',apiUnitsAfterExecution)
            print('API_Units_Spent:',apiUnitsSpent)
        except Exception as e:
            print("An error occured:",e)

    main()
        # At the end of the function, add:
    et=time.time()
    semRushApiCompertitor_time=et-st
    print('Total execution time of SemRushApiCompetitor.py is:',semRushApiCompertitor_time,'seconds')
    return semRushApiCompertitor_time


#semRushApiCompetitor('https://www.esg.fr/',1)