# pylint: disable=invalid-name
"""Module to compute statistics from a file with numeric data."""

import json
import sys
import time

_OUTPUT_FILE_NAME = "SalesResults.txt"


def load_json(file_path):
    """Load a JSON file and return its contents as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{file_path}'.")
        sys.exit(1)


def compute_total_sales(catalogue, sales):
    """Compute total sales cost based on the catalogue and sales record."""
    catalogue_by_title = {item['title']: item for item in catalogue}

    total_cost = 0

    for sale in sales:
        item = catalogue_by_title.get(sale['Product'])

        if item is not None:
            item_price = item.get('price')
            if item_price is None:
                print(
                    f"Warning: Item '{sale['Product']}' has no",
                    " price in catalogue. Skipping item."
                )
                continue

            quantity = sale.get('Quantity')
            if quantity is None:
                print(
                    f"Warning: Sale of item '{sale['Product']}'",
                    " has no quantity. Skipping item."
                )
                continue

            total_cost += item_price * quantity
        else:
            print(f"Warning: Item '{sale['Product']}' not found in catalogue.")

    return total_cost


def main():
    """
    Main function to parse JSON files for catalogue
    and sales from command line arguments.
    """

    start_time = time.time()

    if len(sys.argv) != 3:
        print("Usage: python computeSales.py",
              " <priceCatalogue.json> <salesRecord.json>")
        sys.exit(1)

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    catalogue = load_json(catalogue_file)
    sales = load_json(sales_file)

    total_cost = compute_total_sales(catalogue, sales)

    elapsed_time = time.time() - start_time

    print(f"Total cost: ${total_cost:,.2f}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")

    with open(_OUTPUT_FILE_NAME, 'w', encoding="utf-8") as file:
        file.write(f"Total cost: ${total_cost:,.2f}\n")
        file.write(f"Elapsed time: {elapsed_time:.6f} seconds\n")


if __name__ == "__main__":
    main()
