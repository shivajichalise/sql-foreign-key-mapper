# SQL Foreign Key Mapper

## Overview

SQL Foreign Key Mapper is a Python script designed to extract foreign key relationships from a SQL dump file and generate SQL queries to add foreign key constraints between related tables. The script processes the SQL dump file, generates the necessary `INSERT` statements for a foreign key mapping table, and constructs SQL queries to modify the schema, ensuring proper foreign key constraints.

## Features

- **Parse SQL Dump**: Extracts `CREATE TABLE` statements from an SQL dump.
- **Foreign Key Detection**: Allows users to manually identify foreign key columns in each table and provides an option to specify their parent tables and columns.
- **Generate Foreign Key Mappings**: Saves the foreign key mappings in a file (`foreign_key_mappings.sql`).
- **Generate ALTER Statements**: Generates SQL `ALTER` statements to modify columns to `BIGINT UNSIGNED` and add foreign key constraints to the relevant tables.
- **Populating Data**: After generating the foreign key mapping, the data is populated into the `foreign_key_mapping` table in the database.

## Requirements

- Python 3.x
- A MySQL or MariaDB database to run the generated SQL commands.
- The input SQL dump file must contain valid `CREATE TABLE` statements with proper table and column definitions.

## Usage Instructions

1. **Run the Script**:
   - Clone or download this repository.
   - Install Python if you haven't already.
   - Ensure that the SQL dump file (e.g., `dump.sql`) is available in the same directory or specify its path when prompted.

2. **Generate Foreign Key Mappings**:
   - The script will prompt you to confirm if a column is a foreign key, and if so, request the parent table and column name.
   - The foreign key mappings will be saved in `foreign_key_mappings.sql`.

3. **Populate Data to the Foreign Key Mapping Table**:
   - After the `foreign_key_mappings.sql` file is generated, you need to run the generated SQL to insert the foreign key mappings into the `foreign_key_mapping` table in your database.

4. **Generate ALTER Statements**:
   - After populating the foreign key mappings, run the following SQL query in your database:

   ```sql
   SELECT CONCAT(
       'ALTER TABLE ', parent_table_name, ' ',
       'CHANGE ', parent_column_name, ' ', parent_column_name, ' BIGINT UNSIGNED;',
   
       'ALTER TABLE ', child_table_name, ' ',
       'CHANGE ', child_column_name, ' ', child_column_name, ' BIGINT UNSIGNED, ',
       'ADD CONSTRAINT fk_', child_table_name, '_', child_column_name, ' ',
       'FOREIGN KEY (', child_column_name, ') ',
       'REFERENCES ', parent_table_name, '(', parent_column_name, ') ',
       'ON DELETE CASCADE ',
       'ON UPDATE CASCADE;'
   ) AS sql_command
   FROM foreign_key_mapping;
   ```

	•	This will generate the necessary ALTER statements to modify columns to BIGINT UNSIGNED and set up foreign key constraints.

5.	Execute the ALTER Statements:
	•	Once you have the ALTER SQL queries generated, you can run them directly in your MySQL/MariaDB database to apply the changes.

Important Notes
	•	This script works only for integer foreign key columns (i.e., columns with types like BIGINT, INT, TINYINT, etc.).
	•	The foreign_key_mapping table must already exist in your database with the following structure:

```sql
CREATE TABLE `foreign_key_mapping` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `child_table_name` VARCHAR(255),
    `child_column_name` VARCHAR(255),
    `parent_table_name` VARCHAR(255),
    `parent_column_name` VARCHAR(255)
);
```

•	Make sure that both the child and parent tables exist before running the ALTER statements, as this script assumes that the database schema is already in place.

### Steps After Generating the Mappings:
1. Run the script to populate the `foreign_key_mapping` table with the correct foreign key information.
2. Execute the SQL query mentioned above to generate the `ALTER` statements that modify the columns to `BIGINT UNSIGNED` and add the foreign key constraints.
3. Execute the generated `ALTER` SQL statements in your database to apply the changes.
