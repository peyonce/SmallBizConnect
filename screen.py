import webbrowser
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp

class WelcomeScreen(Screen):
    def go_to_dashboard(self):
        self.manager.current = "dashboard"

class DashboardScreen(Screen):
    @property
    def data(self):
        return self.manager.business_data

    def on_pre_enter(self, *args):
        self._refresh_totals()

    def handle_add_sale(self):
        amount = self._read_amount()
        if amount is None: return
        self.data.add_sale(amount)
        self._refresh_totals()

    def handle_add_expense(self):
        amount = self._read_amount()
        if amount is None: return
        self.data.add_expense(amount)
        self._refresh_totals()

    def handle_view_history(self):
        self.manager.current = "history"
        
    def handle_view_tools(self):
        self.manager.current = "tools"

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
        content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        content.add_widget(Label(text=message, font_size=dp(16)))
        ok = Button(text="OK", size_hint_y=None, height=dp(44), background_color=(0.20, 0.45, 0.85, 1))
        content.add_widget(ok)
        popup = Popup(title="Input error", content=content, size_hint=(0.8, 0.3))
        ok.bind(on_release=popup.dismiss)
        popup.open()

    def _refresh_totals(self):
        self.ids.sales_value.text    = f"R{self.data.today_sales:.2f}"
        self.ids.expenses_value.text = f"R{self.data.today_expenses:.2f}"
        self.ids.profit_value.text   = f"R{self.data.profit:.2f}"
        self.ids.amount_input.text   = ""

class HistoryScreen(Screen):
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
            container.add_widget(Label(text="No transactions yet.", font_size=dp(16), size_hint_y=None, height=dp(40)))
            return

        for label, records in groups:
            container.add_widget(Label(text=label, font_size=dp(18), bold=True, color=(0.20, 0.45, 0.85, 1), size_hint_y=None, height=dp(36), halign="left", valign="middle"))
            for t in records:
                color = (0.20, 0.60, 0.30, 1) if t["type"] == "sale" else (0.80, 0.30, 0.30, 1)
                row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50), padding=[dp(10), 0], spacing=dp(4))
                
                time_lbl = Label(text=t["time"], font_size=dp(16), color=(0.45, 0.45, 0.50, 1), size_hint_x=0.35)
                type_lbl = Label(text=t["type"].title(), font_size=dp(16), color=color, size_hint_x=0.35)
                amt_lbl = Label(text=f"R{t['amount']:.2f}", font_size=dp(16), bold=True, color=color, size_hint_x=0.25, halign="right")
                del_btn = Button(text="X", font_size=dp(18), bold=True, size_hint_x=None, width=dp(40), background_color=(0.80, 0.30, 0.30, 1))
                
                del_btn.bind(on_release=lambda btn, tid=t["id"], info=t: self.handle_delete(tid, info))
                
                row.add_widget(time_lbl)
                row.add_widget(type_lbl)
                row.add_widget(amt_lbl)
                row.add_widget(del_btn)
                
                from kivy.graphics import Color, Rectangle
                with row.canvas.before:
                    Color(1, 1, 1, 1)
                    bg = Rectangle(pos=row.pos, size=row.size)
                row.bind(pos=lambda inst, val, bg=bg: setattr(bg, 'pos', inst.pos), size=lambda inst, val, bg=bg: setattr(bg, 'size', inst.size))
                container.add_widget(row)

    def handle_delete(self, tid, t):
        content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        content.add_widget(Label(text=f"Delete this {t['type']} of R{t['amount']:.2f}?"))
        btns = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(48))
        cancel = Button(text="Cancel", background_color=(0.6, 0.6, 0.6, 1))
        delete = Button(text="Delete", background_color=(0.80, 0.30, 0.30, 1))
        btns.add_widget(cancel)
        btns.add_widget(delete)
        content.add_widget(btns)
        
        popup = Popup(title="Confirm Delete", content=content, size_hint=(0.8, 0.35))
        cancel.bind(on_release=popup.dismiss)
        delete.bind(on_release=lambda x: (self.data.delete_transaction(tid), self.refresh_list(), popup.dismiss()))
        popup.open()

    def handle_export(self):
        path = self.data.export_to_csv()
        count = len(self.data.transactions)
        content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        content.add_widget(Label(text=f"Exported {count} records to\ntransactions.csv"))
        ok = Button(text="OK", size_hint_y=None, height=dp(44), background_color=(0.20, 0.45, 0.85, 1))
        content.add_widget(ok)
        popup = Popup(title="Export Complete", content=content, size_hint=(0.8, 0.35))
        ok.bind(on_release=popup.dismiss)
        popup.open()

    def go_back(self):
        self.manager.current = "dashboard"

class ToolsScreen(Screen):
    def open_link(self, url):
        webbrowser.open(url)

    def go_back(self):
        self.manager.current = "dashboard"
