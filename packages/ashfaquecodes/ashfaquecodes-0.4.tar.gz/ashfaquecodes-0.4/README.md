[![License: GNU GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/ashfaque/ashfaquecodes/blob/main/LICENSE)

## How to install
```sh
pip install ashfaquecodes
```

## Documentation
- Color the printed outputs in terminal.
    ```sh
    from ashfaquecodes import (
        , blue_print_start
        , red_print_start
        , green_print_start
        , color_print_reset
    )
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    # blue_print_start
    red_print_start()
    # green_print_start
    pp.pprint("--------------------------")
    color_print_reset()
    ```

- Get a unique list if list of non-unique elements passed in this function.
    ```sh
    from ashfaquecodes import unique_list
    _ = unique_list(non_unique_list)
    ```

- Get unique list of dictionaries if a list of duplicate dictionaries passed in this function.
    ```sh
    from ashfaquecodes import unique_list_of_dicts
    _ = unique_list_of_dicts(non_unique_list_of_dicts)
    ```

- Get a list of non-empty dictionaries if a list of empty and non-empty dictionaries passed in this function.
    ```sh
    from ashfaquecodes import remove_empty_dicts_from_list
    _ = remove_empty_dicts_from_list(list_with_empty_dicts)
    ```

- Get a sorted list of dictionaries returned according to your desired sorting key of the dictionary if a list of non-empty dictionaries passed in this function. Supports ascending and descending order.
    ```sh
    from ashfaquecodes import sort_list_of_dicts
    _ = sort_list_of_dicts(unsorted_list = unsorted_lst, key = 'dict_key_name', desc = True)
    ```

- Get execution time of your code. Can also prints the execution time in terminal if an optional parameter `print_time = True` is passed in the function.
    ```sh
    from ashfaquecodes import (
        execution_start_time
        , total_execution_time_str
    )
    execution_start_time = get_execution_start_time()
    total_execution_time_str = get_execution_end_time(execution_start_time, print_time = True)
    ```

- Custom Decorator to calculate execution time of a function which will be printed in the terminal during execution of that function.
    ```sh
    from ashfaquecodes import timer
    @timer
    def your_function(request):
        pass
    ```

## License
[GNU GPLv3](LICENSE)
