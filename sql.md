SQL Notes by Vamp 9/17/18

## What is SQL?
- **S**tructured **Q**uery **L**anguage
- a universal standard language specification for performing CRUD operations on relational databases
  - data operations that apply to any application that persists data
  - **C**reate: new data
  - **R**ead: existing data
  - **U**pdate: existing data
  - **D**elete: existing data

## What is a SQL dialect
- SQL is the specification that describes a standard for interacting with relational databases
- SQL dialects are implementations (usable systems) of the specification
- a SQL dialect encompasses what is known as a DBMS
  - **D**ata**b**ase **M**anagement **S**ystem
- SQL dialects can be thought of like human language dialects
  - shared core but with unique nuances in each dialect
  - like Southern English vs NorthEastern
    - different slangs and meanings but both are English at their core
- each dialect may have its own definitions of data types and operations

### Common Open Source SQL Dialects
- PostgreSQL
  - psql, postgres
  - open source SQL dialect
  - massive community and support
  - widely used across the industry
  - advanced features such as JSONB / indexing that are not found in other SQL dialects
- MySQL
  - "open source" with paid proprietary versions
  - owned and distributed by Oracle
  - large community and support
  - widely used across the industry
- SQLite
  - open source
  - lightweight DBMS used for prototyping / local development
  - stores records in a text file as a CSV
    - **C**omma **S**eparated **V**alue
  - minimal features
  - **should not be used in a production application**

### Comparison between MySQL and PostgreSQL
- [comparison article](https://www.2ndquadrant.com/en/postgresql/postgresql-vs-mysql/)

# Relational Database core philosophies

## Tables
- a database is organized by **Tables** that describe the _shape_ of the data they hold using **Columns**
- each table has its own unique name that should adequately identify the data it holds
  - table names are always pluralized
- each table should **only contain columns specific to that data**
  - use **relationships** to relate data across tables
  - more on managing relationships further down
  - Ex: a User table (`users`) and an Address table (`addresses`)
    - `users` contains core details about the User like name, age
    - `addresses` contains information specifically about an Address like city, state
      - Addresses are _related_ to Users but are stored in separate tables because their data is distinct from one another
      - a state does not describe a User much like an age does not describe an address so they belong in their own tables

### Relationship with OOP
- a Table is like a Class definition
- a blueprint to describe in general terms some attributes (columns) of the data it holds

## Columns
- each Table organizes and defines the data it holds by its Columns
- each Table **must have a Primary Key** Column which is used as a unique identifier for each Row within the Table
  - typically the `id` column of the Table but may be given any name
  - typically _auto-incremented_ but may have other mechanisms for guaranteeing uniqueness
  - **must be unique so that data does not overlap or conflict**
- a Column definition requires:
  - a name
  - a data type
    - used for efficiently storing data depending on its type
    - most types are shared but each dialect may have its own definition of data types
- a Column definition may also include constraints
  - unique
  - auto-incrementing
  - a relationship with another Table
  - requiring the data be stored in a specific format
  - allowing the data to be `null` (absence of data)

### Relationship with OOP
- a Column is like a Property defined in a Class
- an Object Instance (Row) will have properties that hold the values stored in the Column associated with that Row
  - these properties will have the same name as the Column

## Rows
- each **Row** within a Table holds the data associated with one record / entry
  - the row contains values for each column described by its containing Table

### Relationship with OOP
- a Row is to its Table like an Object Instance is to its Class
- each Row is represented by an Object Instance within the code
- the properties of the Object are the Column names for its associated Table
- the value of a property of the Object will be the value stored in the Column for that Row

# Relationships
- **Relationships** describe connections between data in different Tables
- allows Tables to only manage and store data specific to a single purpose while still connecting related data
- uses the concept of a **Foreign Key** to relate data across Tables

## Keywords:

### primary key:
  - a column describing a unique identifier that can be used for looking up distinct rows (entries) in a table
  - primary keys are indexed meaning they are able to be queried (looked up) rapidly

### foreign key:
  - a column describing a unique identifier that references a row in another table to describe a relationship
  - a foreign key suggests ownership by the row it identifies in the referenced table

### one-to-one (o2o):
- one row in one table corresponds to one row in another table
	- number of rows in each are equal
	- primary keys in each table are the same
  - Used for (rare):
    - extending / separating information involving a single unit that are not often used
    - reducing the data load of an often used table by factoring out information that is less commonly accessed but still related

### one-to-many (o2m)
- one row in one table corresponds to many rows in another table
- often the primary table has less rows than the referencing table
- primary key of the owning table is used to relate data as the foreign key in the owned table
  - the owned table will have a primary key (as all tables do) in addition to a foreign key column which corresponds to the primary key of the owning table

- Perspective terminology:
  - one row has many rows in another table
  - many rows belong to one row

- Used for (common):
  - expressing ownership relationships
  - relating independent entities that share a common identity
	
- Examples:
  - author (owner, primary) -> books (owned by, foreign key == primary of owner)
      - user (owner, primary) -> addresses (owned by, foreign key == user.id)

## Ownership
- when describing relationships between Tables it is best to think in terms of ownership
  - one Table _owns_ the data stored in a second Table
  - the second Table's data _belongs to_ the data stored in the first Table
- in relationships there will always be a **Parent** (owning) Table that has related data stored in a **Child** (owned) Table
  - `users` table has addresses information about each User stored in a related `addresses` Table
  - the User _owns_ the Address(es)
  - the User _has_ many Addresses
  - the Addresses _belongs to_ a User
- this relationship is managed by using **Primary** and **Foreign** keys across the related Tables

## Foreign Keys
- a Foreign Key is an identifier that relates data in one Table to related data in another Table
- every Table must have a Primary Key that uniquely identifies each row it contains
- any Table that is _owned by_ another Table must **also include a Foreign Key relating the two Tables**
  - this Foreign Key is used as a relation between the Tables
- the Foreign Key is considered _foreign_ because it exists _in addition to_ the Primary Key for that Table
- **the Foreign Key on the _owned_ Table is the Primary Key of the _owning_ Table**
  - `users` Table has a Primary Key stored in the column `id`
  - `addresses` Table has a Primary Key stored in the column `id`
  - `addresses` _also has_ a Foreign Key relating the Address to the User stored in a column called `user_id`
    - **because the Address _belongs to_ / _is owned by_ the User the `user_id` Column is defined in the `addresses` Table
    - think of it like a pet dog with a collar. the dog is owned by the person so they hold the identifier while the person (owner) does not

# ORMs
- **O**bject **R**elational **M**ap / Mapper/ Mapping
  - maps (translates, represents) Tables as Classes and Rows as Object Instances of those classes
- a library or framework that translates object-oriented code into database operations and data representations
- allows developers to work in their native language rather than writing raw database operations
- allows database data to exist as Objects within the codebase rather than raw, less manageable, data
- provides methods and functions that expose database CRUD logic / operations
- provides security and fallback mechanisms that, when used correctly, prevent common attack vectors and data-loss

## Common SQL-based ORMs
- Python: [SQLAlchemy](https://www.sqlalchemy.org/)
- JavaScript: [Sequelize](http://docs.sequelizejs.com/)

# SQL basic CRUD operations
- `[]` is used to show where your own values should go
  - **do not include the `[]` brackets in your query**

## General
- `WHERE` is used to describe a match condition(s)
- `AND` can be used to chain multiple `WHERE` conditions that must **all be met**
- `OR` can be used to chain multiple `WHERE` conditions that **at least one must be met**
- any _string_ must be in single `'` quotes
- any numeric value should be written as a number
- all SQL statements **must end in a `;`**
  - this is critical. missing the `;` will cause statements to bleed into each other creating unexpected behavior

## Create: `INSERT`
  - inserting a new Row with all values listed in order from left ro right Column names
  - general form
    ```sql
    INSERT INTO [table name] VALUES ([all values]);
    ```

## READ: `SELECT`
  - general form
  - querying for all rows and columns
  ```sql
  SELECT * FROM [table name];
  ```
  - querying for all rows with specific columns
  ```sql
  SELECT [column_name 1], [column_name 2] FROM [table name];
  ```
  - querying for all columns from specific rows that match some column value
  ```sql
  SELECT * FROM [table name] WHERE [column_name] = ['value'];
  ```
  - querying for all columns from specific rows with several matching column values
  ```sql
  SELECT * FROM [table name] WHERE [column_name 1] = 'value' AND [column_name 2] = 'value';
  ```
  - always try to use the Primary Key column for identifying an individual row
  ```sql
  SELECT * FROM [table name] WHERE id = 1;
  ```

UPDATE: `UPDATE` 
  - general form
  ```sql
  UPDATE [table name] SET ([columns, ]) VALUES ([values, ]);
  ```
  - update one column across many rows (no `WHERE` clause)
  ```sql
  UPDATE [table name] SET [column_name 1] = 'value';
  ```
  - update one column for one row
  ```sql
  UPDATE [table name] SET [column_name 1] = 'value' WHERE id = 1;
  ```

DELETE: `DELETE`
  - general form
  ```sql
  DELETE FROM [table name];
  ```
  - delete row(s) that match a condition
  ```sql
  DELETE FROM [table name] WHERE [condition];
  ```
