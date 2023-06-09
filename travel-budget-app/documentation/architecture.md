# Architectural description

## Structure
The packing structure of the application is as follows: </br>
<img src="pictures/subfolders-structure.png"> </br>
- the package `ui` is responsible for the user interface
- the package `services` is responsible for the application logic
- the package `respositories` is responsible for permanent storage of the data
- the package `entities` contains classes that that reflect the data objects of the application
- the package `errors` is responsible for handling errors

## User interface
User interface contains the following views:
- login 
- create user
- main menu
- trips list
- create a new trip
- trip view and expenses list
- add an expense
- trip's statistics
- user's statistics
Each view is implemented in its own class. User only sees one view at a time. UI is almost entirely separated from the application logic; it calls the `services` and `errors` packages. 

In the cases of `UserStats` and `TripStats` classes, the statistics data is calculated inside those classes.  

## Application logic
The logical data model of the application consists of the classes `User`, `Trip`, and `Expense`, which describe users, their trips, and expenses of the trips.

```mermaid
classDiagram
    
    Expense "*" --> "1" Trip
    Trip "*" --> "1" User
    class User{
        username
        password
    }
    class Trip{
        trip_id
        trip_name
        username
        duration
    }
    class Expense{
        expense_id
        description
        trip_id
        amount
        category
    }
```

The diagram below describes the relationship between classes in the program: 
1. for `User`: </br>
<img src="pictures/user-service-diagram.png"> </br>
2. for `Trip`: </br>
<img src="pictures/trip-service-diagram.png"> </br>
3. for `Expense`: </br>
<img src="pictures/expense-service-diagram.png"> </br>

## Permanent storage of data
Classes `UserRepository`, `TripRepository`, `ExpenseRepository` from the package *repositories* are responsible for permanent storage of the data. They use the `sqlite3` package to create and manage the database.

## Files
The application stores user, trip, and expense data in the `database.sqlite` file in the corresponding tables. The database is initialized in the [init_database.py](https://github.com/gabikakol/software-dev-exercises/blob/main/travel-budget-app/src/init_database.py) file. The configuration file [.env](https://github.com/gabikakol/software-dev-exercises/blob/main/travel-budget-app/.env) places at the root of the application defines the name of the database file.

# Main functionalities
Below, main functionalities of the application are described using sequence diagrams. 

## User login
When the user enters valid username and password, the application logs the user in the following way: 

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant UserService
  participant UserRepository
  
  User->>UI: "login" button clicked
  UI->>UserService: login("gabi", "123")
  UserService->>UserRepository: find_user("gabi")
  UserRepository-->>UserService: user
  UserService-->>UI: user
  UI->UI: user_menu()
```

## Creating a new user
When the user enters a unique username and two valid, identical passwords, the application creates a new user in the following way:

```mermaid
sequenceDiagram

  actor User
  participant UI
  participant UserService
  participant UserRepository
  participant billie
  
  User->>UI: "create user" button clicked
  UI->>UserService: new_user("billie", "abc123", "abc123")
  UserService->>UserRepository: find_user("billie")
  UserRepository-->>UserService: None
  UserService->>user: User("billie", "abc123")
  UserService->>UserRepository: create_user(billie)
  UserRepository-->>UserService: user
  UserService-->>UI: user
  UI->>UI: user_menu()
```

## Creating a trip
When the user enters a valid trip name and duration, the application creates a new trip in the following way:

```mermaid
sequenceDiagram
  actor Trip
  participant UI
  participant TripService
  participant TripRepository
  participant trip
  Trip->>UI: "save" button clicked
  UI->>TripService: new_trip("snowboarding trip to Ruka", "8")
  TripService->>trip: Trip(None, "snowboarding trip to Ruka", "gabi", "8")
  TripService->>TripRepository: create_trip(trip)
  TripRepository-->>TripService: trip
  TripService-->>UI: trip
  UI->>UI: trips_list()
```

## Adding an expense
When the user enters a valid expense description, cost, and chooses a category, the application creates a new expense in the following way:

```mermaid
sequenceDiagram

  actor Expense
  participant UI
  participant ExpenseService
  participant ExpenseRepository
  participant expense
  
  Expense->>UI: "save" button clicked
  UI->>ExpenseService: add_expense("sunday lunch", "hj213asd", "16.34", "restaurants")
  ExpenseService->>expense: Expense(None, "sunday lunch", "hj213asd", "16.34", "restaurants")
  ExpenseService->>ExpenseRepository: create_expense(expense)
  ExpenseRepository-->>ExpenseService: expense
  ExpenseService-->>UI: expense
  UI->>UI: trip_view()
```

## Viewing statistics
The application shows 2 types of statistics, each in a separate window. User statistics are the general statistics based an all user's trips and expenses, whereas trip statistics are only based on the data of the particular trip. 

### User statistics
User statistics are calculated in the `UserStats` class from the UI package. The data is retrieved from the database using the following classes and functions:

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant UserService
    participant TripRepository
    participant ExpenseRepository
    
    User->>UI: "user statistics" button clicked
    UI->>UserService: get.username()
    UserService-->>UI: self.username
    UI->>TripRepository: find_all_trips()
    TripRepository-->>UI: self.trips
    UI->>ExpenseRepository: find_all_expenses()
    ExpenseRepository-->>UI: self.expenses
```

### Trip statistics
User statistics are calculated in the `TripStats` class from the UI package. The data is retrieved from the database using the following classes and functions:
```mermaid
sequenceDiagram
    actor Trip
    participant UI
    participant TripService
    participant TripRepository
    participant ExpenseRepository
    
    User->>UI: "trip statistics" button clicked
    UI->>UserService: get.trip_name()
    UserService-->>UI: self.trip_name
    UI->>UserService: get.trip_id()
    UserService-->>UI: self.trip_id
    UI->>TripRepository: find_trip(self.trip_id)
    TripRepository-->>UI: self.current_trip
    UI->>ExpenseRepository: find_all_expenses()
    ExpenseRepository-->>UI: self.trip_expenses
```

## Weaknesses left in the program's structure
The main weakness is user interface. There is a lot of work to be done on the UI design, especially for viewing list of the trips, trip's expenses, and statistics. So far, these are only listed one by one. The list of the trips should have a scroll bar (for cases when user adds big number of trips), and the trip's expenses and statistics should be displayed in a table. 
