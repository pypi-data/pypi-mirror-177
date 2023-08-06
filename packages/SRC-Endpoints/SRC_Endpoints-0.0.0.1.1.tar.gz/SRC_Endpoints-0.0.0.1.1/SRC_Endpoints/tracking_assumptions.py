import requests
import pandas as pd
import json


def post_tracking_assumptions_to_database(dataset: pd.DataFrame, access_token: str, verbose: bool = True):
    """
    This function posts tracking assumption data to the tracking table of the database. The function firstly checks
    that the input arguments are of the correct type, followed by modifying the dataset into a list of dictionaries.
    Each dictionary is passed to the endpoint, with a status code and error message printed if appropriate, and
    verbose=True.

    :param dataset: a Pandas DataFrame containing the data to upload within a given schema. (pd.DataFrame)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: N/A
    """
    if not isinstance(dataset, pd.DataFrame):
        raise TypeError("The 'dataset' argument must be a Pandas DataFrame.")
    if not isinstance(access_token, str):
        raise TypeError("The 'access_token' must be a string type.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean argument.")
    dict_list = dataset.to_dict('records')
    url = "https://www.samsonrockapis.com/tracking/upload"
    header = {'Authorization': 'Bearer ' + access_token}
    for item in dict_list:
        response = requests.post(url, data=json.dumps(item), headers=header)
        if response.status_code in [200, 201, 202, 203, 204]:
            if verbose:
                print("Status Code: {}, data posted to tracking table.".format(response.status_code))
        elif response.status_code in [401, 403]:
            if verbose:
                print("Status Code: {}, user not authenticated for endpoint.".format(response.status_code))
        else:
            if verbose:
                print("Status Code: {}, {}.".format(response.status_code, response.text))


def get_all_tracking_assumptions(access_token: str, verbose: bool = True):
    """
    This function enables the user to collect all tracking information held in the database. The function firstly checks
    that the arguments are of the correct type, followed by attempting to collect the requested information from the
    database. If the information is available, it is returned as a Pandas DataFrame, otherwise, empty data shall be
    returned, with an appropriate status code printed if verbose=True.

    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not isinstance(access_token, str):
        raise TypeError("The 'access_token' argument must be a string type.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/tracking"
    header = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        if verbose:
            print("Status Code: {}".format(response.status_code))
        return pd.read_json(response.text)
    elif response.status_code == 404:
        if verbose:
            print("Status Code: {}, cannot find tracking data.".format(response.status_code))
        return pd.DataFrame()
    elif response.status_code in [401, 403]:
        if verbose:
            print("Status Code: {}, user not properly authenticated for endpoint.".format(response.status_code))
        return pd.DataFrame()
    else:
        if verbose:
            print("Status Code: {}, {}.".format(response.status_code, response.text))
        return pd.DataFrame()


def get_index_tracking_assumption_history(index: str, access_token: str, verbose: bool = True):
    """
    This function enables the user to collect all tracking information held in the database relating to a specific index.
    The function firstly checks that the arguments are of the correct type, followed by attempting to collect the
    requested information from the database. If the information is available, it is returned as a Pandas DataFrame,
    otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

    :param index: the index for which the user would like to return data. (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [index, access_token]):
        raise TypeError("The 'index' and 'access_token' arguments must be string types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    index_values = ['AEX', 'AMX', 'AMZ', 'AMZI', 'AS51', 'ASX', 'BEL20', 'CAC', 'CPQ', 'DAX', 'DJASD', 'DJCASD',
                    'DJDVY', 'DJEMDIV', 'DJEPCSD', 'DJINET', 'DJSHMB', 'DJSMDQT', 'DJUSDIVT', 'EPRA-EUROPE',
                    'FTSEMIB', 'FUDP', 'GDM', 'GDXJ', 'GEIS-AWCHINA', 'GEIS-AWDEVEUR', 'GEIS-AWEMEUR',
                    'GEIS-AWEXCHINA', 'GEIS-AWJAPAN', 'GEIS-AWLATAM', 'GEIS-AWMEA', 'GEIS-AWNAM',
                    'GEIS-GSCCHINA', 'GEIS-GSCDEVEUR', 'GEIS-GSCEMEUR', 'GEIS-GSCEXCHINA', 'GEIS-GSCJAPAN',
                    'GEIS-GSCLATAM', 'GEIS-GSCMEA', 'GEIS-GSCNAM', 'HSCEI', 'HUR', 'IBEX', 'KOSPI2', 'MCMOT',
                    'MCX', 'MDAX', 'MEXBOL', 'MOAT', 'MSCI-DM-SC-ASIAEXJAP', 'MSCI-DM-SC-CAN', 'MSCI-DM-SC-EMEA',
                    'MSCI-DM-SC-JAPAN', 'MSCI-DM-SC-USA', 'MSCI-DM-STD-ASIAEXJAP', 'MSCI-DM-STD-CAN',
                    'MSCI-DM-STD-EMEA', 'MSCI-DM-STD-JAPAN', 'MSCI-DM-STD-USA', 'MSCI-EM-SC-AMERICAS',
                    'MSCI-EM-SC-ASIA', 'MSCI-EM-SC-EMEA', 'MSCI-EM-STD-AMERICAS', 'MSCI-EM-STD-ASIA',
                    'MSCI-EM-STD-EMEA', 'MSCI-MINVOL-EUROPE', 'MSCI-MINVOL-USA', 'MSCI-MINVOL-EM',
                    'MSCI-SRI-ASIAEXJAP', 'MSCI-SRI-CANADA', 'MSCI-SRI-EMEA', 'MSCI-SRI-JAPAN', 'MSCI-SRI-USA',
                    'MSCI-ESG-ASIAEXJAP', 'MSCI-ESG-CANADA', 'MSCI-ESG-EMEA', 'MSCI-ESG-JAPAN', 'MSCI-ESG-USA',
                    'NBI', 'NDX', 'OMX', 'RIY', 'RTY', 'SD3E', 'SD3P', 'SDAX', 'SMI', 'SMIM', 'SPEUHDA',
                    'SPGTAQD', 'SPGTCED', 'SPGTIND', 'SPI', 'SPTSX', 'SPTSX60', 'SPTXDV', 'SX5E', 'SX5P',
                    'SXXP', 'TecDAX', 'TOP40', 'TW50', 'UKX', 'XIN9I', 'EPRA-ASIA', 'EPRA-NAM', 'IXAROBK',
                    'IXBRHLTK', 'MID', 'SML', 'SPX', 'STXTDSV', 'TWDP', 'NIKKEI', 'TOPIX', 'CRSP', 'TA-125',
                    'TA-35', 'HSI', 'KLCI', 'STI', 'MUNR', 'BLOSSOM', 'OMX30', 'FBLSSRTR', 'MDYF', 'FR10',
                    'FREM', 'MCVAT', 'ENDP']
    if index not in index_values:
        raise ValueError("The 'index' value must be one of {}".format(index_values))
    url = "https://www.samsonrockapis.com/tracking&index={}".format(index)
    header = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        if verbose:
            print("Status Code: {}".format(response.status_code))
        return pd.read_json(response.text)
    elif response.status_code == 404:
        if verbose:
            print("Status Code: {}, cannot find tracking data for {}.".format(response.status_code,
                                                                                  index))
        return pd.DataFrame()
    elif response.status_code in [401, 403]:
        if verbose:
            print("Status Code: {}, user not properly authenticated for endpoint.".format(response.status_code))
        return pd.DataFrame()
    else:
        if verbose:
            print("Status Code: {}, {}.".format(response.status_code, response.text))
        return pd.DataFrame()


def get_most_recent_index_tracking_assumption(index: str, access_token: str, verbose: bool = True):
    """
    This function enables the user to collect the most recent tracking assumption information from the database relating
    to a specific index review. The function firstly checks that the arguments are of the correct type, followed by
    attempting to collect the requested information from the database. If the information is available, it is returned
    as a Pandas DataFrame, otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

    :param index: the index for which the user would like to return data. (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [index, access_token]):
        raise TypeError("The 'index' and 'access_token' arguments must be string types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    index_values = ['AEX', 'AMX', 'AMZ', 'AMZI', 'AS51', 'ASX', 'BEL20', 'CAC', 'CPQ', 'DAX', 'DJASD', 'DJCASD',
                    'DJDVY', 'DJEMDIV', 'DJEPCSD', 'DJINET', 'DJSHMB', 'DJSMDQT', 'DJUSDIVT', 'EPRA-EUROPE',
                    'FTSEMIB', 'FUDP', 'GDM', 'GDXJ', 'GEIS-AWCHINA', 'GEIS-AWDEVEUR', 'GEIS-AWEMEUR',
                    'GEIS-AWEXCHINA', 'GEIS-AWJAPAN', 'GEIS-AWLATAM', 'GEIS-AWMEA', 'GEIS-AWNAM',
                    'GEIS-GSCCHINA', 'GEIS-GSCDEVEUR', 'GEIS-GSCEMEUR', 'GEIS-GSCEXCHINA', 'GEIS-GSCJAPAN',
                    'GEIS-GSCLATAM', 'GEIS-GSCMEA', 'GEIS-GSCNAM', 'HSCEI', 'HUR', 'IBEX', 'KOSPI2', 'MCMOT',
                    'MCX', 'MDAX', 'MEXBOL', 'MOAT', 'MSCI-DM-SC-ASIAEXJAP', 'MSCI-DM-SC-CAN', 'MSCI-DM-SC-EMEA',
                    'MSCI-DM-SC-JAPAN', 'MSCI-DM-SC-USA', 'MSCI-DM-STD-ASIAEXJAP', 'MSCI-DM-STD-CAN',
                    'MSCI-DM-STD-EMEA', 'MSCI-DM-STD-JAPAN', 'MSCI-DM-STD-USA', 'MSCI-EM-SC-AMERICAS',
                    'MSCI-EM-SC-ASIA', 'MSCI-EM-SC-EMEA', 'MSCI-EM-STD-AMERICAS', 'MSCI-EM-STD-ASIA',
                    'MSCI-EM-STD-EMEA', 'MSCI-MINVOL-EUROPE', 'MSCI-MINVOL-USA', 'MSCI-MINVOL-EM',
                    'MSCI-SRI-ASIAEXJAP', 'MSCI-SRI-CANADA', 'MSCI-SRI-EMEA', 'MSCI-SRI-JAPAN', 'MSCI-SRI-USA',
                    'MSCI-ESG-ASIAEXJAP', 'MSCI-ESG-CANADA', 'MSCI-ESG-EMEA', 'MSCI-ESG-JAPAN', 'MSCI-ESG-USA',
                    'NBI', 'NDX', 'OMX', 'RIY', 'RTY', 'SD3E', 'SD3P', 'SDAX', 'SMI', 'SMIM', 'SPEUHDA',
                    'SPGTAQD', 'SPGTCED', 'SPGTIND', 'SPI', 'SPTSX', 'SPTSX60', 'SPTXDV', 'SX5E', 'SX5P',
                    'SXXP', 'TecDAX', 'TOP40', 'TW50', 'UKX', 'XIN9I', 'EPRA-ASIA', 'EPRA-NAM', 'IXAROBK',
                    'IXBRHLTK', 'MID', 'SML', 'SPX', 'STXTDSV', 'TWDP', 'NIKKEI', 'TOPIX', 'CRSP', 'TA-125',
                    'TA-35', 'HSI', 'KLCI', 'STI', 'MUNR', 'BLOSSOM', 'OMX30', 'FBLSSRTR', 'MDYF', 'FR10',
                    'FREM', 'MCVAT', 'ENDP']
    if index not in index_values:
        raise ValueError("The 'index' value must be one of {}".format(index_values))
    url = "https://www.samsonrockapis.com/tracking&index={}&latest".format(index)
    header = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        if verbose:
            print("Status Code: {}".format(response.status_code))
        return pd.json_normalize(json.loads(response.text))
    elif response.status_code == 404:
        if verbose:
            print("Status Code: {}, no tracking data available for {}".format(response.status_code, index))
        return pd.DataFrame()
    elif response.status_code == 401:
        if verbose:
            print("Status Code: {}, user not properly authenticated for endpoint.".format(response.status_code))
        return pd.DataFrame()
    else:
        if verbose:
            print("Status Code: {}, {}.".format(response.status_code, response.text))
        return pd.DataFrame()
