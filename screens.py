from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp

from data import BusinessData


# ---------------------------------------------------------------------
# Shared visual constants (keep small — move to a styles.py if it grows)
# ---------------------------------------------------------------------
COLOR_PRIMARY = (0.20, 0.45, 0.85, 1)
FONT_TITLE = 32
FONT_SUBTITLE = 18
FONT_HEADING = 26
FONT_BODY = 18
BUTTON_HEIGHT = dp(55)


# =====================================================================
# WELCOME SCREEN
# =====================================================================
class WelcomeScreen(Screen):
    """First screen the user sees."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(40),
            spacing=dp(20),
        )

        title = Label(
            text="SmallBizConnect",
            font_size=FONT_TITLE,
            bold=True,
            color=COLOR_PRIMARY,
        )

        subtitle = Label(
            text="Manage your business with confidence",
            font_size=FONT_SUBTITLE,
        )

        get_started_button = Button(
            text="Get Started",
            font_size=FONT_BODY,
            size_hint=(1, None),
            height=BUTTON_HEIGHT,
            background_color=COLOR_PRIMARY,
        )
        get_started_button.bind(on_press=self.go_to_dashboard)

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(get_started_button)

        self.add_widget(layout)

    def go_to_dashboard(self, instance):
        self.manager.current = "dashboard"


# =====================================================================
# DASHBOARD SCREEN
# =====================================================================
class DashboardScreen(Screen):
    """Shows today's totals and lets the user add sales / expenses."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create our data object. Later we could pass this in
        # from main.py so it's shared across screens.
        self.data = BusinessData()

        # ---- Layout ----
        layout = BoxLayout(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(15),
        )

        # ---- Title / greeting ----
        title = Label(
            text="SmallBizConnect",
            font_size=FONT_HEADING,
            bold=True,
            color=COLOR_PRIMARY,
            size_hint_y=None,
            height=dp(60),
        )

        welcome = Label(
            text="Welcome back!",
            font_size=FONT_SUBTITLE,
            size_hint_y=None,
            height=dp(40),
        )

        # ---- Live totals (we keep references so we can update them) ----
        self.sales_label = Label(
            text="Today's Sales\nR0.00",
            font_size=FONT_BODY,
        )
        self.expenses_label = Label(
            text="Today's Expenses\nR0.00",
            font_size=FONT_BODY,
        )
        self.profit_label = Label(
            text="Today's Profit\nR0.00",
            font_size=FONT_BODY,
        )

        # ---- Amount input (shared by both buttons) ----
        self.amount_input = TextInput(
            hint_text="Enter amount (e.g. 50)",
            input_filter="float",       # only digits + one dot
            multiline=False,
            font_size=FONT_BODY,
            size_hint_y=None,
            height=dp(50),
        )

        # ---- Action buttons ----
        add_sale_button = Button(
            text="Add Sale",
            size_hint_y=None,
            height=BUTTON_HEIGHT,
        )
        add_sale_button.bind(on_press=self.handle_add_sale)

        add_expense_button = Button(
            text="Add Expense",
            size_hint_y=None,
            height=BUTTON_HEIGHT,
        )
        add_expense_button.bind(on_press=self.handle_add_expense)

        # ---- Add everything to the layout (order = top → bottom) ----
        layout.add_widget(title)
        layout.add_widget(welcome)
        layout.add_widget(self.sales_label)
        layout.add_widget(self.expenses_label)
        layout.add_widget(self.profit_label)
        layout.add_widget(self.amount_input)
        layout.add_widget(add_sale_button)
        layout.add_widget(add_expense_button)

        self.add_widget(layout)

    # ---------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------
    def handle_add_sale(self, instance):
        amount = self._read_amount()
        if amount is None:
            return
        self.data.add_sale(amount)
        self._refresh_totals()

    def handle_add_expense(self, instance):
        amount = self._read_amount()
        if amount is None:
            return
        self.data.add_expense(amount)
        self._refresh_totals()

    # ---------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------
    def _read_amount(self):
        """Return the typed amount as a float, or None if invalid."""
        raw = self.amount_input.text.strip()
        if not raw:
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    def _refresh_totals(self):
        """Redraw all three labels from the current data."""
        self.sales_label.text = f"Today's Sales\nR{self.data.today_sales:.2f}"
        self.expenses_label.text = f"Today's Expenses\nR{self.data.today_expenses:.2f}"
        self.profit_label.text = f"Today's Profit\nR{self.data.profit:.2f}"
        self.amount_input.text = ""   # clear the input for the next entry