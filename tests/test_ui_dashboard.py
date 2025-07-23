# --- REPLACE THE ENTIRE CONTENTS OF THIS FILE ---

import requests
import uuid
from playwright.sync_api import Page
from tests.pages.dashboard_page import DashboardPage

def test_dashboard_title(page: Page):
    dashboard = DashboardPage(page)
    dashboard.navigate()
    dashboard.check_title()

def test_new_result_appears_in_table(page: Page):
    # 1. ARRANGE: Create unique test data and post it via the API
    unique_test_name = f"test_end_to_end_{uuid.uuid4()}"
    test_payload = {
        "test_name": unique_test_name,
        "status": "fail",
        "duration_ms": 777,
        "test_suite": "end_to_end_tests"
    }
    response = requests.post("http://127.0.0.1:8000/api/results", json=test_payload)
    assert response.status_code == 201

    # 2. ACT: Navigate to the page
    dashboard = DashboardPage(page)
    dashboard.navigate()

    # 3. ASSERT: Check for the outcome
    # All the complex logic is now hidden inside this one method call.
    dashboard.check_for_test_result(unique_test_name)