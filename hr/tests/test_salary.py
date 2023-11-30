import datetime
from unittest.mock import (
    MagicMock,
    patch,
)

from django.test import (
    Client,
    TestCase,
)
from django.urls import reverse

from hr.calculate_salary import CalculateMonthRateSalary, WorkDayEnum
from hr.pydantic_models import WorkingDays
from hr.tests.factories import (
    EmployeeFactory,
    PositionFactory,
)


DAYS_DICT = {
    'day_1': 'WORKING_DAY',
    'day_2': 'WORKING_DAY',
    'day_3': 'WORKING_DAY',
    'day_4': 'WEEKEND',
    'day_5': 'WEEKEND',
    'day_6': 'WORKING_DAY',
    'day_7': 'WORKING_DAY',
    'day_8': 'WORKING_DAY',
    'day_9': 'WORKING_DAY',
    'day_10': 'WORKING_DAY',
    'day_11': 'WEEKEND',
    'day_12': 'WEEKEND',
    'day_13': 'WORKING_DAY',
    'day_14': 'WORKING_DAY',
    'day_15': 'WORKING_DAY',
    'day_16': 'WORKING_DAY',
    'day_17': 'WORKING_DAY',
    'day_18': 'WEEKEND',
    'day_19': 'WEEKEND',
    'day_20': 'WORKING_DAY',
    'day_21': 'WORKING_DAY',
    'day_22': 'WORKING_DAY',
    'day_23': 'WORKING_DAY',
    'day_24': 'WORKING_DAY',
    'day_25': 'WEEKEND',
    'day_26': 'WEEKEND',
    'day_27': 'WORKING_DAY',
    'day_28': 'WORKING_DAY',
    'day_29': 'WORKING_DAY',
    'day_30': 'WORKING_DAY',
}


class SalaryCalculatorViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.url = reverse('hr:salary_calculator')
        self.position = PositionFactory(monthly_rate=10000)

    @patch('hr.views.CalculateMonthRateSalary.get_days_count')
    @patch('hr.views.CalculateMonthRateSalary.calculate_salary')
    def test_salary_calculation(self, mock_calculate_salary, mock_get_days_count):
        mock_get_days_count.return_value = MagicMock(working=20, sick=0, vacation=0)
        mock_calculate_salary.return_value = 9999
        self.client.force_login(self.admin_user)
        employee = EmployeeFactory(position=self.position)
        salary_data = dict({'employee': employee.id}, **DAYS_DICT)
        response = self.client.post(self.url, salary_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('calculated_salary', response.context)

    def test_access_by_non_admin(self):
        non_admin_user = EmployeeFactory(is_staff=False, is_superuser=False)
        self.client.force_login(non_admin_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)


class TestCalculateMonthRateSalary(TestCase):
    def setUp(self):
        self.employee = EmployeeFactory()
        self.salary = 10000
        self.position = PositionFactory(monthly_rate=self.salary)
        self.employee.position = self.position
        self.calculator = CalculateMonthRateSalary(self.employee)

    def test_calculate_base_work_days(self):
        self.assertEqual(self.calculator._calculate_base_work_days(DAYS_DICT), 22)

    def test_calculate_daily_salary(self):
        base_working_days = 20
        expected_daily_salary = 500  # 10000 / 20
        self.assertEqual(self.calculator._calculate_daily_salary(base_working_days), expected_daily_salary)

    def test_calculate_monthly_salary(self):
        working_days = WorkingDays(working=20, sick=0, vacation=0)
        expected_salary = 10000  # 20 * 500
        self.assertEqual(self.calculator.calculate_salary(working_days), expected_salary)

    @patch('hr.calculate_salary.CalculateMonthRateSalary._calculate_working_monthly_salary')
    @patch('hr.calculate_salary.CalculateMonthRateSalary._calculate_sick_monthly_salary')
    @patch('hr.calculate_salary.CalculateMonthRateSalary._calculate_vacation_monthly_salary')
    def test_calculate_salary_with_leave(self, mock_vacation, mock_sick, mock_working):
        mock_working.return_value = 8000
        mock_sick.return_value = 1200
        mock_vacation.return_value = 800
        working_days = WorkingDays(working=16, sick=2, vacation=1)
        expected_salary = 10000  # 8000 + 1200 + 800
        self.assertEqual(self.calculator.calculate_salary(working_days), expected_salary)

    @patch('hr.models.MonthlySalary.objects.update_or_create')
    def test_save_salary(self, mock_update_or_create):
        self.calculator.save_salary(salary=10000, date=datetime.date.today())
        mock_update_or_create.assert_called_once()

    @patch('hr.calculate_salary.CalculateMonthRateSalary._calculate_monthly_vacation_days')
    @patch('hr.calculate_salary.CalculateMonthRateSalary._calculate_monthly_sick_days')
    @patch('hr.calculate_salary.CalculateMonthRateSalary._calculate_monthly_working_days')
    def test_get_days_count(self, mock_working_days, mock_sick_days, mock_vacation_days):
        mock_working_days.return_value = 20
        mock_sick_days.return_value = 4
        mock_vacation_days.return_value = 2

        result = self.calculator.get_days_count(DAYS_DICT)
        expected_working_days = WorkingDays(working=20, sick=4, vacation=2)

        self.assertEqual(result, expected_working_days)

    def test__calculate_monthly_working_days(self):
        result = self.calculator._calculate_monthly_working_days(DAYS_DICT)
        expected_result = len(
            {day: work_type for day, work_type in DAYS_DICT.items() if work_type == WorkDayEnum.WORKING_DAY.name},
        )

        self.assertEqual(result, expected_result)
