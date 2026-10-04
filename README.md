# SmallBizConnect

A small-business tracker built with Python + Kivy.
Log sales and expenses, see today's totals, review your history,
and export everything to a spreadsheet.


## Features

- **Dashboard** — today's sales, expenses, and profit at a glance
- **Add transactions** — record sales and expenses with one tap
- **Input validation** — friendly popups when you enter bad data
- **Transaction history** — every record grouped by Today / Yesterday / date
- **Delete with confirmation** — mistakes are safe to fix
- **Export to CSV** — open in Excel, Google Sheets, or Numbers
- **Persistent storage** — your data survives app restarts (JSON)
- **Custom branding** — Poppins font, custom logo

## Tech Stack

- **Python 3.9+**
- **Kivy 2.3+** — cross-platform UI framework
- **JSON** — for data persistence
- **CSV** — for exporting transactions
- **Pillow** — for logo generation

## Getting Started

### Install

    pip install kivy Pillow

### Run

    python3 main.py

## Usage

1. Tap **Get Started** on the welcome screen
2. Enter an amount and tap **Add Sale** or **Add Expense**
3. Tap **View History** to see all records grouped by day
4. Tap the red **X** on any row to delete it (with confirmation)
5. Tap **Export to CSV** to write everything to transactions.csv

## Roadmap

- [ ] Edit an existing transaction
- [ ] Monthly summary screen
- [ ] Search / filter history
- [ ] Charts of daily profit
- [ ] Android build (.apk)

## License

MIT — free to use, modify, and share.

## Author

Built by Nthabiseng Phiri.
