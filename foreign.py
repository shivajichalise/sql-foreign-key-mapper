import os
import re

def process_sql_dump(file_path="sagun_sir.sql", output_file="foreign_key_mappings.sql"):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist in the current directory.")
        return

    # Read the SQL dump file
    with open(file_path, "r") as file:
        sql_dump = file.read()

    # Find all CREATE TABLE statements
    create_table_statements = re.findall(
        r"CREATE TABLE IF NOT EXISTS `(\w+)` \((.*?)PRIMARY KEY", sql_dump, re.S
    )

    if not create_table_statements:
        print("No CREATE TABLE statements found in the dump.")
        return

    # Open the output file to append the generated INSERT statements
    with open(output_file, "a") as output:
        for table_name, table_content in create_table_statements:
            print(f"\nProcessing table: {table_name}")
            print("-" * 40)

            # Extract columns between CREATE TABLE and PRIMARY KEY, ignoring specific columns
            columns = re.findall(r"`(\w+)`\s+([\w()]+)", table_content)
            columns = [
                (column_name, column_type)
                for column_name, column_type in columns
                if column_name not in {"id", "created_at", "updated_at"}
            ]

            if not columns:
                print(f"No relevant columns found for table `{table_name}`.")
                continue

            # Collect foreign key mappings
            foreign_key_mappings = []

            for column_name, column_type in columns:
                print(f"\nColumn: `{column_name}`\nType: {column_type}")
                print("-" * 40)
                is_foreign_key = input(
                    f"Is `{column_name}` a foreign key? (y/n): ").strip().lower()
                if is_foreign_key == "y":
                    parent_table = input(
                        f"Enter the PARENT TABLE for `{column_name}`: ").strip()
                    parent_column = input(
                        f"Enter the RELATION COLUMN for `{column_name}`: ").strip()
                    foreign_key_mappings.append((table_name, column_name, parent_table, parent_column))
                print("\n" + "-" * 40)

            # Write INSERT statements to the output file
            for child_table, child_column, parent_table, parent_column in foreign_key_mappings:
                insert_query = (
                    f"INSERT INTO `foreign_key_mapping` "
                    f"(`child_table_name`, `child_column_name`, `parent_table_name`, `parent_column_name`) VALUES "
                    f"('{child_table}', '{child_column}', '{parent_table}', '{parent_column}');\n"
                )
                output.write(insert_query)
                print(f"Generated and saved: {insert_query.strip()}")

    print("\nProcessing completed. Check the output file for results.")

# Run the script
if __name__ == "__main__":
    # Default file and output paths
    default_input_file = "dump.sql"
    default_output_file = "foreign_key_mappings.sql"

    print("\nWelcome to the SQL Dump Processor!")
    print("-" * 40)

    # Check if the default file exists
    if os.path.exists(default_input_file):
        print(f"Using default SQL dump file: {default_input_file}")
    else:
        default_input_file = input("Enter the path to your SQL dump file: ").strip()

    # Use the default output file
    print(f"Generated INSERT queries will be saved in: {default_output_file}\n")
    print("-" * 40)

    process_sql_dump(default_input_file, default_output_file)
