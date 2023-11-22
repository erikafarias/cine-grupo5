def stock_snacks() -> tuple[list, list, list, dict]:

        '''
        Los nombres y los precios por separado
        '''

        endpoint: str = f'{URL}/snacks'
        response = requests.get(endpoint, headers=AUTH)
        response.raise_for_status()

        stock_of_snacks: [dict] = response.json()
        list_names_snacks: list = []
        for elemento in stock_of_snacks:
            list_names_snacks.append(elemento)

        list_prices_snacks: list = []
        for elemento in list_names_snacks:
            list_prices_snacks.append(stock_of_snacks[elemento])

        list_ult:list = []
        n:int = 0

        for element in list_names_snacks:
            text: str = f"{element} >> ${list_prices_snacks[n]}"
            n+=1
            list_ult.append(text)

        return list_names_snacks, list_prices_snacks, list_ult, stock_of_snacks