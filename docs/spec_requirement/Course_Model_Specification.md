Course Model Specification

#1.Objective

The Course Model acts as the bridge between the application and the database.

Its responsibilities are limited to:

*Executing SQL queries
*Reading course records
*Writing course records
*Updating course records
*Deleting course records
*Returning query results
*Managing database connections
*Providing course lookup methods
*Providing statistical database queries

The model must never:

*Validate user input
*Check business rules
*Generate HTML
*Handle HTTP requests
*Perform authentication
*Perform authorization
*Call AI modules
*Generate reports


#2.Model Responsibilities

The Course Model is responsible for:

#1.Create

*Insert a new course into the database.

#2.Read

Retrieve:

*All courses
*Single course by ID
*Single course by name
*Active courses
*Inactive courses
*Courses by status

#3.Update

Modify existing course information.
Update only:
*Course Name
*Technology Stack
*Duration
*Description
*Status
*Updated By
*Updated At

#4.Delete
Remove a course record from the database.

#5.Search
Search courses using:

*Course Name
*Technology Stack
*Description

#6.Filter
Retrieve courses based on:

*Status
*Technology
*Minimum Duration
*Maximum Duration

#7.Statistics

Provide database queries for:

*Total Courses
*Active Courses
*Inactive Courses
*verage Course Duration

#8.Lookup

Provide helper methods for:

*Course Exists
*Course by Name

#3.Model Responsibilities Matrix

Operation        Responsibility 
Insert Course    Yes            
Update Course    Yes            
Delete Course   Yes            
Retrieve Course Yes            
Search Course   Yes            
Filter Course   Yes            
Lookup Course   Yes            
Statistics      Yes            
Validation      No             
Business Rules  No             
HTML            No             
AI              No             
Reports         No             

#4. Required Database Operations

The model supports the following operations.
#Course CRUD
*Create Course
*Get Course by ID
*Get Course by Name
*Get All Courses
*Update Course
*Delete Course

#Lookup Operations

*Check Course Exists
*Get Active Courses
*Get Inactive Courses
*Get Courses by Status

#Search Operations

*Search by Course Name
*Search by Technology Stack
*Search by Description

#Filter Operations

*Filter by Status
*Filter by Technology
*Filter by Minimum Duration
*Filter by Maximum Duration

#Statistics

*Count Courses
*Get Course Statistics

#5.Model Scope
##The Course Model SHALL
*Read data
*Write data
*Update data
*Delete data
*Execute SQL
*Return query results
*Perform lookup operations
*Provide statistics

##The Course Model SHALL NOT
*Validate form input
*Check business rules
*Generate HTML
*Handle HTTP requests
*Perform authentication
*Perform authorization
*Call AI modules
*Generate reports
*Perform scheduling

#6.CRUD Responsibilities
#Create
Purpose:Insert a new course into the Course table.

#Table Used
Course

#Columns Inserted
*course_name
*technology_stack
*duration_hours
*description
*status
*created_by

#Return
*New Course ID
*Database Error

#Read
Retrieve:
#Single Course Using: id
#Course by Name Using:course_name
#All Courses :Return every course ordered by course name.

#Active Courses Condition: status = 'Active'
#Inactive Courses Condition:status = 'Inactive'

#Update

Allow updating:
*course_name
*technology_stack
*duration_hours
*description
*status
*updated_at
*updated_by

Never update:
*id
*created_at
*created_by

#Delete
Delete course using: id Only database deletion.

Business validation happens in the Service Layer.

#7.Lookup Operations
The model supports the following lookup methods.
#Course Exists
Checks whether a course with the given course name already exists.
Supports:
*Create
 Update
Uses: exclude_id to ignore the current record during updates.
Returns:
*True
*False

#Get Course by Name
Retrieve a single course using its unique course name.
Returns:
*Course object
*None

#8. Search Operations
The model supports searching by:
Search Field     Description   
course_name      Partial Match 
technology_stack Partial Match 
description      Partial Match 

Search should be case-insensitive where supported by SQLite.

#9. Filter Operations
Supported filters:
#Status
*Active
*Inactive

#Technology
Examples:
*Python
*Java
*React
*AI

#Duration
Examples:
*Less than 20 Hours
*Between 20–40 Hours
*Greater than 40 Hours

#10.Sorting

Current Version:Sorting is supported for
*course_name

Future versions may support:
*duration_hours
*status
*created_at
*updated_at

Order:
*ASC
*DESC

#11.Pagination

Current Version:Pagination is not implemented.
Future Enhancement
Support:
*Page Number
*Page Size
*Offset
*Limit
Default page size should be configurable.

#12. Statistics Queries
The model provides queries for:

#Total Courses
Returns:COUNT(*)

##Active Courses
Returns:COUNT(status='Active')

#Inactive Courses
Returns:COUNT(status='Inactive')

#Average Duration
Returns:Average duration in hours.

#13. Data Mapping
Database Column   Model Property   
id               id               
course_name      course_name      
technology_stack technology_stack 
duration_hours   duration_hours   
description      description      
status           status           
created_at       created_at       
updated_at       updated_at       
created_by       created_by       
updated_by       updated_by       

#14. Input Requirements

The model expects validated data from the Service Layer.
Expected fields:
*course_name
*technology_stack
*duration_hours
*description
*status
*created_by
*updated_by
The model assumes validation has already been completed.

#15. Output Specification

#On Success
Returns:
*Course ID
*Course Object
*List of Course Objects
*Success Status
*Statistics Dictionary

#On Failure
Returns:
*None
*False
*Empty List

May propagate:
*Database Connection Error
*SQL Execution Error
*Constraint Violation

#16. Error Handling
The model should handle:
*Database connection failures
*SQL syntax errors
*Constraint violations
*Duplicate course names
*Missing records
*Transaction failures
The model reports these errors to the Service Layer without converting them into user-friendly messages.

#17. Security Requirements

The Course Model must:
*Use parameterized SQL queries.
*Prevent SQL Injection.
*Use centralized database connections.
*Avoid exposing database internals.
*Return only required data.

#18. Performance Requirements

The model should:
*Minimize database calls.
*Use indexes on searchable fields.
*Retrieve only necessary records.
*Optimize search queries.
*Optimize filter queries.
*Return ordered results efficiently.

#19.Dependencies

The Course Model depends on:
*SQLite3
*Database Connection Module
*Course Table
It must not depend on:
*Routes
*Services
*Templates
*Frontend
*AI Modules

#20.Request Flow
text Browser Routes Course Service Course Mode SQLite Database

#21.Deliverables
The Course Model provides:
*Database CRUD operations
*Lookup operations
*Search operations
*Filter operations
*Statistics queries
*Duplicate course detection
*Database error handling
*Secure SQL execution
*Performance optimization through indexing
*Clean data access abstraction

