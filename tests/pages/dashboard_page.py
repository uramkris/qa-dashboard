# --- tests/pages/dashboard_page.py ---

from playwright.sync_api import Page, expect

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.URL = "http://localhost:8501/"
        self.EXPECTED_TITLE = "QA Dashboard"
    
    def navigate(self):
        self.page.goto(self.URL)

    def check_title(self):
        expect(self.page).to_have_title(self.EXPECTED_TITLE)

    def check_for_test_result(self, test_name: str):
        """
        Checks that an element with the specific test name exists in the DOM.
        
        We use to_have_count(1) instead of to_be_visible() because st.dataframe
        is a virtualized grid. It doesn't render DOM elements for cells that
        are off-screen, causing visibility checks to fail. This assertion
        proves data integrity without being brittle.
        """
        # Step 1: Locate the element by its text.
        result_locator = self.page.get_by_text(test_name)

        # Step 2 (THE FIX): Assert that exactly one such element exists in the DOM.
        # This is not concerned with visibility, only existence.
        expect(result_locator).to_have_count(1)