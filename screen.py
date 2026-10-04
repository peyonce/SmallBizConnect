from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp


class WelcomeScreen(Screen):
    """Layout defined in smallbizconnect.kv."""

    def go_to_dashboard(self):
        self.manager.current = "dashboard"


class DashboardScreen(Screen):
    """Layout defined in smallbizconnect.kv. Grabs widgets by id."""

    @property
    def data(self):
        return self.manager.business_data

    def on_pre_enter(self, *args):
        self._refresh_totals()

    def handle_add_sale(self):
        amount = self._read_amount()
        if amount is None:
            return
        self.data.add_sale(amount)
        self._refresh_totals()

    def handle_add_expense(self):
        amount = self._read_amount()
        if amount is None:
            return
        self.data.add_expense(amount)
        self._refresh_totals()

    def handle_view_history(self):
        self.manager.current = "history"

    def handle_reset_day(self):
        self.data.reset_day()
        self._refresh_totals()

    def _read_amount(self):
        raw = self.ids.amount_input.text.strip()

        if not raw:
            self._show_error("Please enter an amount.")
            return None

        try:
            value = float(raw)
        except ValueError:
            self._show_error(f"'{raw}' is not a valid number.")
            return None

        if value <= 0:
            self._show_error("Amount must be greater than zero.")
            return None

        return value

    def _show_error(self, message):
        content = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
        )

        label = Label(
            text=message,
            font_size=dp(16),
            color=(0.15, 0.15, 0.20, 1),
        )

        ok_button = Button(
            text="OK",
            background_normal="",
            background_color=(0.20, 0.45, 0.85, 1),
            color=(1, 1, 1, 1),
            font_size=dp(15),
            size_hint_y=None,
            height=dp(44),
        )

        content.add_widget(label)
        content.add_widget(ok_button)

        popup = Popup(
            title="Input error",
            content=content,
            size_hint=(0.8, 0.3),
            auto_dismiss=True,
        )

        ok_button.bind(on_release=popup.dismiss)
        popup.open()

    def _refresh_totals(self):
        self.ids.sales_value.text    = f"R{self.data.today_sales:.2f}"
        self.ids.expenses_value.text = f"R{self.data.today_expenses:.2f}"
        self.ids.profit_value.text   = f"R{self.data.profit:.2f}"
        self.ids.amount_input.text   = ""


class HistoryScreen(Screen):
    """Shows all transactions grouped by day, with delete and export."""

    @property
    def data(self):
        return self.manager.business_data

    def on_pre_enter(self, *args):
        self.refresh_list()

    def refresh_list(self):
        container = self.ids.list_layout
        container.clear_widgets()

        groups = self.data.get_grouped_by_date()

        if not groups:
            container.add_widget(
                Label(
                    text="No transactions yet.",
                    font_size=dp(16),
                    color=(0.45, 0.45, 0.50, 1),
                    size_hint_y=None,
                    height=dp(40),
                )
            )
            return

        for label, records in groups:
            container.add_widget(
                Label(
                    text=label,
                    font_size=dp(18),
                    bold=True,
                    color=(0.20, 0.45, 0.85, 1),
                    size_hint_y=None,
                    height=dp(36),
                    halign="left",
                    valign="middle",
                )
            )

            for t in records:
                if t["type"] == "sale":
                    color  = (0.20, 0.60, 0.30, 1)
                    prefix = "Sale"
                else:
                    color  = (0.80, 0.30, 0.30, 1)
                    prefix = "Expense"

                row = BoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=dp(50),
                    padding=[dp(10), 0],
                    spacing=dp(4),
                )

                time_label = Label(
                    text=t["time"],
                    font_size=dp(16),
                    color=(0.45, 0.45, 0.50, 1),
                    size_hint_x=0.35,
                    halign="left",
                )
                time_label.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

                type_label = Label(
                    text=prefix,
                    font_size=dp(16),
                    color=color,
                    size_hint_x=0.35,
                    halign="left",
                )
                type_label.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

                amount_label = Label(
                    text=f"R{t['amount']:.2f}",
                    font_size=dp(16),
                    bold=True,
                    color=color,
                    size_hint_x=0.25,
                    halign="right",
                )
                amount_label.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

                delete_button = Button(
                    text="X",
                    font_size=dp(18),
                    bold=True,
                    size_hint_x=None,
                    width=dp(40),
                    background_normal="",
                    background_color=(0.80, 0.30, 0.30, 1),
                    color=(1, 1, 1, 1),
                )
                delete_button.bind(
                    on_release=lambda btn, tid=t["id"], info=t: self.handle_delete(tid, info)
                )

                row.add_widget(time_label)
                row.add_widget(type_label)
                row.add_widget(amount_label)
                row.add_widget(delete_button)

                from kivy.graphics import Color, Rectangle
                with row.canvas.before:
                    Color(1, 1, 1, 1)
                    bg = Rectangle(pos=row.pos, size=row.size)

                def update_bg(instance, value, bg=bg):
                    bg.pos = instance.pos
                    bg.size = instance.size

                row.bind(pos=update_bg, size=update_bg)

                container.add_widget(row)

    def handle_delete(self, transaction_id, transaction):
        kind   = transaction["type"]
        amount = transaction["amount"]

        content = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
        )

        message = Label(
            text=f"Delete this {kind} of R{amount:.2f}?",
            font_size=dp(16),
            color=(0.15, 0.15, 0.20, 1),
        )

        buttons = BoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(48),
        )

        cancel_button = Button(
            text="Cancel",
            background_normal="",
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=dp(15),
        )

        delete_button = Button(
            text="Delete",
            background_normal="",
            background_color=(0.80, 0.30, 0.30, 1),
            color=(1, 1, 1, 1),
            font_size=dp(15),
        )

        buttons.add_widget(cancel_button)
        buttons.add_widget(delete_button)

        content.add_widget(message)
        content.add_widget(buttons)

        popup = Popup(
            title="Confirm Delete",
            content=content,
            size_hint=(0.8, 0.35),
            auto_dismiss=False,
        )

        cancel_button.bind(on_release=popup.dismiss)

        def do_delete(btn):
            popup.dismiss()
            self._confirm_delete(transaction_id)

        delete_button.bind(on_release=do_delete)

        popup.open()

    def _confirm_delete(self, transaction_id):
        self.data.delete_transaction(transaction_id)
        self.refresh_list()

    # ------------------------------------------------------------------
    # Export to CSV
    # ------------------------------------------------------------------
    def handle_export(self):
        """Write all transactions to CSV, then show a confirmation popup."""
        path  = self.data.export_to_csv()
        count = len(self.data.transactions)

        content = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
        )

        message = Label(
            text=f"Exported {count} records to\ntransactions.csv",
            font_size=dp(15),
            color=(0.15, 0.15, 0.20, 1),
            halign="center",
        )
        message.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        ok_button = Button(
            text="OK",
            background_normal="",
            background_color=(0.20, 0.45, 0.85, 1),
            color=(1, 1, 1, 1),
            font_size=dp(15),
            size_hint_y=None,
            height=dp(44),
        )

        content.add_widget(message)
        content.add_widget(ok_button)

        popup = Popup(
            title="Export Complete",
            content=content,
            size_hint=(0.8, 0.35),
            auto_dismiss=True,
        )

        ok_button.bind(on_release=popup.dismiss)
        popup.open()

    def go_back(self):
        self.manager.current = "dashboard"
