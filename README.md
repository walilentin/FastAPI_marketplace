## Creating Roles in the Database

Before creating users, it is necessary to create two roles in the database: "User" and "Administrator". This can be done using SQL queries or appropriate ORM commands for your FastAPI application.

### SQL Queries

```sql
-- Creating the "User" role
INSERT INTO role (id, name, permissions) VALUES (1, 'User', '{"basic_permissions": true}');

-- Creating the "Admin" role
INSERT INTO role (id, name, permissions) VALUES (2, 'Admin', '{"admin_permissions": true}');

