Example
- explore One-to-Many and Many-to-Many relationships across Users, Games, Game Studios, and (User) Owned Games
- design and create the following Tables
  - `users`
  - `games`
  - `game_studios`
  - `owned_games`

# Building the MySQL Database

## Planning Relationships

### User and Owned Games
- a User can own **many** Games
- A Game can be owned by **many** Users
  - **Many-to-Many (m2m) relationship**
  - use a **junction / associative table** called `owned_games`
    - an **associative table** contains **two** Foreign Keys and serves only as a bridge between User and Game to manage the Many-to-Many relationship

### Game and Game Studio
- a Game Studio can have **many** Games
- a Game **belongs to one** Game Studio
  - **One-to-Many relationship**
  - the Game **belongs to** a Game Studio so it holds the Foreign Key `game_studio_id`


## Create and use the Database (MySQL)
- create
```sql
CREATE DATABASE user_games;
```
- switch to the database to interact with it
```sql
use user_games;
```

## User Table
- Table: `users`
- Columns
  - id: `int`
    - constraints: primary key, auto-increment, unique
  - username: `varchar(20)`
    - constraints: unique

### SQL
```sql
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(20) UNIQUE
);
```
- using `describe users` command to view the _shape_ of the Table
  - the _shape_ is defined by the Column data types and constraints
```
+----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| id       | int(11)     | NO   | PRI | NULL    | auto_increment |
| username | varchar(20) | YES  | UNI | NULL    |                |
+----------+-------------+------+-----+---------+----------------+
```
- forgot to add the `NOT NULL` constraint to the `username` Column
  - use the `ALTER TABLE` command to modify the Column
  - general form
  ```sql
  ALTER TABLE [table name]
  CHANGE COLUMN [column name]
  [new column name] [data type] [constraint(s)];
  ```
  - adding `NOT NULL` constraint to `username` column
  ```sql
  ALTER TABLE users
  CHANGE COLUMN username
  username VARCHAR(20) NOT NULL UNIQUE;
  ```
- use the `describe` command to confirm the change
```sql
+----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| id       | int(11)     | NO   | PRI | NULL    | auto_increment |
| username | varchar(20) | NO   | UNI | NULL    |                |
+----------+-------------+------+-----+---------+----------------+
```
## Game Studio Table
- because the Game Studio is needed for defining the Foreign Key on the Game Table it must be created first
- Table: `game_studios`
- Columns
  - id: `int`
    - constraints: primary key, auto-increment, unique
  - title: `varchar(30)`
    - constraints: unique 
- Relationships
  - Game Studio **has many** Games
### SQL
```sql
CREATE TABLE game_studios (
  id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  title VARCHAR(30) UNIQUE NOT NULL
);
```
- `describe game_studios;`
```sql
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| title | varchar(30) | NO   | UNI | NULL    |                |
+-------+-------------+------+-----+---------+----------------+
```

## Game Table
- because the Game and User Tables are needed to define the `owned_games` Table they must both be created first
- Table: `games`
- Columns
  - id: `int`
    - constraints: primary key, auto-increment, unique
  - title: `varchar(30)`
    - constraints: unique
  - game_studio_id: `int`
    - constraints: Foreign Key for `game_studio` referencing the `id` column of `game_studios`
- Relationships
  - Game **belongs to** Game Studio

### SQL
```sql
CREATE TABLE games (
  id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  title VARCHAR(30) UNIQUE NOT NULL,
  game_studio_id INT NOT NULL,
  FOREIGN KEY (game_studio_id) REFERENCES game_studios(id)
);
```
- `describe games;`
```sql
+----------------+-------------+------+-----+---------+----------------+
| Field          | Type        | Null | Key | Default | Extra          |
+----------------+-------------+------+-----+---------+----------------+
| id             | int(11)     | NO   | PRI | NULL    | auto_increment |
| title          | varchar(30) | NO   | UNI | NULL    |                |
| game_studio_id | int(11)     | NO   | MUL | NULL    |                |
+----------------+-------------+------+-----+---------+----------------+
```

## Owned Games Table
- this is an example of an **associative / junction** table
- it serves as a middle reference point to manage Many-to-Many relationships
- notice that it contains **two** Foreign Keys (one for User and one for Game)
  - the two Foreign Keys **together** form what is called a **composite index**
  - a **composite index** is considered unique **as a pair**
- Table: `owned_games`
- Columns
  - user_id: `int`
    - constraints: Foreign Key for `user` referencing the `id` column of `users` 
  - game_id: `int`
    - constraints: Foreign Key for `game` referencing the `id` column of `games`
- Relationships
  - User (owner) **has many** Games **through Owned Games**
  - Game **has many** Users (owners) **through Owned Games**
    - that is to say that a User can own many Games and a Game can be owned by many Users

### SQL
```sql
CREATE TABLE owned_games (
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  game_id INT NOT NULL,
  FOREIGN KEY (game_id) REFERENCES games(id)
);
```
- `describe owned_games;`
```sql
+---------+---------+------+-----+---------+-------+
| Field   | Type    | Null | Key | Default | Extra |
+---------+---------+------+-----+---------+-------+
| user_id | int(11) | NO   | MUL | NULL    |       |
| game_id | int(11) | NO   | MUL | NULL    |       |
+---------+---------+------+-----+---------+-------+
```

# Using the MySQL Database

## Create (`INSERT`) data for the Tables

### create a User
```sql
INSERT INTO users (username) VALUES ('the-vampiire');
```
- query for all rows and columns in the `users` table to confirm and view the user ID value (for use in `owned_games`)
```sql
SELECT * FROM users;
```
```sql
+----+--------------+
| id | username     |
+----+--------------+
|  1 | the-vampiire |
+----+--------------+
```

### create a Game Studio
```sql
INSERT INTO game_studios (title) VALUES ('Bungie');
```
```sql
SELECT * FROM game_studios;
```
```sql
+----+--------+
| id | title  |
+----+--------+
|  1 | Bungie |
+----+--------+
```

### create a Game
- use the `id` of the `game_studios` entry for the Foreign Key value of `game_studio_id`
```sql
INSERT INTO games (title, game_studio_id) VALUES ('Destiny 2', 1);
```
```sql
SELECT * FROM games;
```
```sql
+----+-----------+----------------+
| id | title     | game_studio_id |
+----+-----------+----------------+
|  1 | Destiny 2 |              1 |
+----+-----------+----------------+
```

### create an Owned Game
- use the `id` of `users` and `games` entries for the Foreign Key values of `user_id` and `game_id`
```sql
INSERT INTO owned_games (user_id, game_id) VALUES (1, 1);
```
```sql
SELECT * FROM owned_games;
```
```sql
+---------+---------+
| user_id | game_id |
+---------+---------+
|       1 |       1 |
+---------+---------+
```

## Read (`SELECT`) data from the Tables

### query for just the `title` of the Game Studio
```sql
SELECT title FROM game_studios;
```

### query for all of the Games that **belong to** the Game Studio
- we will be getting data across two tables for this query
- we will use a `JOIN` statement to bundle the data from both related tables
  - the `JOIN` statement requires an `ON` field to know what is being matched
  - in this case we are **joining on**
    - the `game_studio_id` Foreign Key of the `games` table
    - with the `id` Primary Key of the `game_studios` table
```sql
SELECT * FROM games
  INNER JOIN game_studios
  ON game_studio_id = game_studios.id;
```
```sql
+----+-----------+----------------+------+--------+
| id | title     | game_studio_id | id   | title  |
+----+-----------+----------------+------+--------+
|  1 | Destiny 2 |              1 |    1 | Bungie |
+----+-----------+----------------+------+--------+
```
- notice how all of the columns from _both tables_ is returned because we used the wildcard `*` selector instead of specifying specific columns
- also notice how the `id` and `title` columns are ambiguous since their names are shared across both tables
  - to remedy this you can use an **alias** which will rename the columns for the purpose of the query results (does not affect the actual table)
```sql
SELECT
  games.id AS 'Game ID',
  games.title AS 'Game Title',
  game_studio_id,
  game_studios.id AS 'Studio ID',
  game_studios.title AS 'Studio Title'
  FROM games
  INNER JOIN game_studios ON game_studios.id = game_studio_id;
```
```sql
+---------+------------+----------------+-----------+--------------+
| Game ID | Game Title | game_studio_id | Studio ID | Studio Title |
+---------+------------+----------------+-----------+--------------+
|       1 | Destiny 2  |              1 |         1 | Bungie       |
+---------+------------+----------------+-----------+--------------+
```

### query for all the Games the User owns
- using the user `id` value of `1`
- requires two joins
  - one join across the **associative table** `owned_games` which manages the Many-to-Many relationship
  - one join across the `users` table (for specifying the user id)
```sql
SELECT games.id, games.title FROM games
INNER JOIN owned_games
INNER JOIN users
  ON owned_games.user_id = users.id
WHERE user_id = 1;
```
```sql
+----+-----------+
| id | title     |
+----+-----------+
|  1 | Destiny 2 |
+----+-----------+
```