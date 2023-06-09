from tests.testing_env.test_database_connection import get_database_connection
from repositories.user_repository import UserRepository
from repositories.trip_repository import TripRepository
from repositories.expense_repository import ExpenseRepository

test_user_repository = UserRepository(get_database_connection())
test_trip_repository = TripRepository(get_database_connection())
test_expense_repository = ExpenseRepository(get_database_connection())
