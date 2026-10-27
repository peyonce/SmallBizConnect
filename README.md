 SmallBizConnect

A small-business tracker built with Python + Kivy. Designed for young founders and township businesses to log sales, track expenses, manage cash flow, and reach formal markets.

[SmallBizConnect logo](assets/logo.png)
 

SmallBizConnect directly addresses the "Youth entrepreneurship and small-business growth" problem statement. We cover multiple focus areas required by the brief:

- **Bookkeeping:** Track daily sales/expenses, see live profit, and export a full transaction history to CSV.
- **Business Registration:** Built-in "Business Tools" screen links directly to CIPC to help young founders formalize their business.
- **Funding Readiness:** Generate a clean CSV bank report that can be used to apply for funding, loans, or grants.
- **Fraud Protection:** Built-in links to SARS scam alerts to help rural businesses avoid digital fraud.

# Features

- **Dashboard:** Today's sales, expenses, and profit at a glance.
- **Add transactions:** Record sales and expenses with one tap.
- **Input validation:** Friendly popups when you enter bad data.
- **Transaction history:** Every record grouped by Today / Yesterday / date.
- **Delete with confirmation:** Mistakes are safe to fix.
- **Export to CSV:** Open in Excel, Google Sheets, or Numbers.
- **Business Growth Tools:** Quick access to registration, funding prep, and fraud protection.
- **Persistent storage:** Your data survives app restarts (JSON).
- **Custom branding:** Poppins font, custom logo.

## Tech Stack

- **Python 3.9+**
- **Kivy 2.3+** — cross-platform UI framework
- **JSON** — for data persistence
- **CSV** — for exporting transactions
- **Pillow** — for logo generation

## Getting Started

### Install

```bash
pip install kivy Pillow
python3 main.py

Usage
Tap Get Started on the welcome screen.

Enter an amount and tap Add Sale or Add Expense.

Tap View History to see all records grouped by day.

Tap the red X on any row to delete it (with confirmation).

Tap Export to CSV to write everything to transactions.csv.

Tap Business Tools to access registration, funding, and fraud resources.

Roadmap
☑ Bookkeeping (Sales, Expenses, Profit)
☑ CSV Export (Funding Readiness)
☑ Business Tools Screen (Registration & Fraud Links)
□ Android build (.apk) for mobile access
□ Cloud sync for multiple devices
License
MIT — free to use, modify, and share.

Author
Built by Nthabiseng Phiri.
 