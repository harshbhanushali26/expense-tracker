from rich.console import Group, Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from rich.columns import Columns
from rich.rule import Rule


from datetime import datetime, date



console = Console()


def print_success(message):
    console.print(f"✅ [green]{message}[/green]")


def print_warning(message):
    console.print(f"⚠️  [yellow]{message}[/yellow]")


def print_error(message):
    console.print(f"❌ [red]{message}[/red]")


def print_section_title(title, icon="📌", color="cyan"):
    console.print(f"\n[bold {color}]{icon} {title} [/bold {color}]\n")


def print_header():
    title = Align.center("\n💸  [bold white on dark_green] PERSONAL EXPENSE TRACKER [/bold white on dark_green]\n[yellow]Your Daily Finance Companion[/yellow]\n")
    console.print(Panel(title, style="bold cyan", border_style="cyan", box=box.ROUNDED))


def print_main_menu():
    console.print(Panel( Align.center("📋 [bold cyan]Track & Manage Expenses[/bold cyan]"), border_style="magenta", box=box.ROUNDED))
    table = Table(title = "📟 Expense Tracker Console", box=box.SQUARE, expand = False,
        pad_edge=True,   # Adds spacing to edges
        show_lines=False 
        )
    
    table.add_column("Options", justify="center", style="bold yellow", width=8)
    table.add_column("Actions",  style="bold white",  width=40)

    table.add_row("1", "➕ Add Transaction")
    table.add_row("2", "✏️ Update Transaction")
    table.add_row("3", "🗑️ Delete Transaction")
    table.add_row("4", "📋 View All Transactions")
    table.add_row("5", "🔍 Filter Transactions")
    table.add_row("6", "📆 Daily Summary")
    table.add_row("7", "📅 Monthly Summary")
    table.add_row("8", "📊 Category Breakdown")
    # table.add_row("9", "📤 Export (PDF)")
    table.add_row("0", "❌ Exit")
    
    console.print(table)
    
    
def print_txn_table(txns: dict):
    table = Table(title="[bold white]📋 Transaction Overview [/bold white]",show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Date", style="green")
    table.add_column("Type", style="bold white")
    table.add_column("Amount", justify="right", style="bold yellow")
    table.add_column("Category", style="bold white")
    table.add_column("Description", style="yellow")
    
    for txn in txns:
        table.add_row(txn.id, txn.date, txn.type, str(txn.amount), txn.category, txn.description or "-")

    console.print(table)
    

def display_summary(summary, title, is_today=False, period_label="day"):
    today_text = " [Today]" if is_today else ""

    table = Table(
        title=f"[bold bright_cyan]{title}{today_text}[/]",
        show_edge=True,
        header_style="bold bright_cyan",
        box=box.SIMPLE_HEAVY,
        style="white"
    )

    # Add columns
    table.add_column("Income", justify="right")
    table.add_column("Expense", justify="right")
    table.add_column("Carry Forward", justify="right")
    table.add_column("Balance", justify="right")

    # Add data row
    table.add_row(
        f"{summary['income']:,.2f}",
        f"{summary['expense']:,.2f}",
        f"{summary['carry_forward']:,.2f}",
        f"[bold green]{summary['balance']:,.2f}[/]" if summary["balance"] > 0
        else f"[bold red]{summary['balance']:,.2f}[/]"
    )

    table_panel = Panel.fit(table, style="bright_blue")

    # Expense breakdown panel (optional)
    category_breakdown_panel = None
    if summary['breakdown']:
        breakdown_text = "\n".join(
            f" - {cat}: ₹{amt:,.2f}" for cat, amt in summary['breakdown'].items()
        )
        category_breakdown_panel = Panel(
            breakdown_text,
            title="📊 [bold bright_magenta]Expense Breakdown[/]",
            border_style="bright_magenta",
            style="white"
        )

    # Footer messages
    balance_summary = ""
    if summary["balance"] > 0:
        balance_summary = f"[bold green]✅ You saved ₹{summary['balance']:,.2f} this {period_label}![/]"
    elif summary["balance"] < 0:
        balance_summary = f"[bold red]⚠️ You overspent by ₹{-summary['balance']:,.2f} this {period_label}![/]"

    footer_msg = Group(
        f"[red]📌 Transactions: {summary['num_expense']} expenses, {summary['num_income']} income[/]",
        f"[red]📌 Total Transactions: {summary['num_expense'] + summary['num_income']}[/]",
        balance_summary
    )

    # Assemble final panel content
    panel_items = [table_panel]
    if category_breakdown_panel:
        panel_items.append(category_breakdown_panel)
    panel_items.append(footer_msg)

    summary_panel = Panel.fit(
        Align.center(Group(*panel_items)),
        title="📊 [bold green3]Summary[/]",
        border_style="green3",
        padding=(1, 2)
    )
    
    console.print(summary_panel)
 

# ====================================== Dashboard =================================== # 
        
def get_today_panel(today_summary, user_name):
        today_panel = Panel.fit(
        f"""📅 [b]Today: {date.today()}[/b]
├─ Income: ₹{today_summary['income']:.2f}
├─ Expense: ₹{today_summary['expense']:.2f}
└─ Balance: ₹{today_summary['balance']:.2f} 
✅ Saved ₹{today_summary['balance']:.2f} today!""",
        title=f"📊 Welcome back, {user_name}!",
        border_style="cyan",
        padding=(1, 2)
    )
        return today_panel
       
      
def get_monthly_panel(month_summary):
        month_panel = Panel.fit(
        f"""🗓️  [b]This Month: {date.today():%B %Y}[/b]
├─ Total Income: ₹{month_summary['income']:.2f}
├─ Total Expense: ₹{month_summary['expense']:.2f}
├─ Carry Forward: ₹{month_summary['carry_forward']:.2f}
└─ Net Savings: ₹{month_summary['balance']:.2f}""",
        border_style="green",
        padding=(1, 2)
    )
        return month_panel


def get_category_panel(top_categories):
    category_table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
    category_table.add_column("🔥 Category", justify="left")
    category_table.add_column("Amount (₹)", justify="right")
    for name, amt in top_categories:
        category_table.add_row(name, f"{amt:.2f}")

    category_panel = Panel.fit(
        category_table,
        title="Top Spending Categories",
        border_style="red",
        padding=(1, 2)
    )
    return category_panel
        
    
def get_footer_panel(month_summary):
    footer_panel = Panel.fit(
        f"📌 Transactions this month: {month_summary['num_income'] + month_summary['num_expense']}\n🕒 LastView: [dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/]",
        border_style="yellow"
    )
    return footer_panel
    
    
def show_dashboard(today_summary, month_summary, top_categories, user_name):
    today_panel = get_today_panel(today_summary, user_name)
    month_panel = get_monthly_panel(month_summary)
    category_panel = get_category_panel(top_categories)
    footer_panel = get_footer_panel(month_summary)
    
    row_1 = Columns([today_panel, month_panel, category_panel], equal=True, expand=True)
    row_2 = Columns([footer_panel], align="center", expand=True)
    
    dashboard = Panel(
        Group(row_1, Rule(style="dim"), row_2),
        title="📊 Monthly Summary",
        border_style="bold blue",
        padding=(1, 2)
    )
    
    console.print(dashboard)
    

# ===================== MENU DISPLAY FUNCTIONS ===================== #

def show_main_menu():   
    table = Table.grid(padding=(0, 2))
    table.add_column("Option", style="bold yellow")
    table.add_column("Action", style="white")

    table.add_row("1", "⚙️  Manage Transactions")
    table.add_row("2", "📊  Analysis")
    table.add_row("3", "📋  Manage Categories")
    table.add_row("0", "🚪 Exit")

    console.print(Panel.fit(table, title="📟 Expense Tracker Console", border_style="cyan", padding=(1, 2)))


def show_transaction_menu(): 
    table = Table.grid(padding=(0, 2))
    table.add_column("Option", style="bold yellow", justify="center")
    table.add_column("Action", style="white")

    table.add_row("1", "➕ Add Transaction")
    table.add_row("2", "✏️ Update Transaction")
    table.add_row("3", "🗑️ Delete Transaction")
    table.add_row("0", "🔙 Back")

    console.print(Panel.fit(table, title="⚙️ Manage Transactions", border_style="cyan", padding=(1, 2)))


def show_analysis_menu(): 
    table = Table.grid(padding=(0, 2))
    table.add_column("Option", style="bold yellow", justify="center")
    table.add_column("Action", style="white")
    table.add_row("1", "📆  Daily Summary")
    table.add_row("2", "📅  Monthly Summary")
    table.add_row("3", "📊  Category Breakdown")
    table.add_row("4", "📋  View Transactions")
    table.add_row("0", "🔙  Back to Main Menu")

    console.print(Panel.fit(table, title="📊  Analysis", border_style="cyan", padding=(1, 2)))


def show_category_menu():
    table = Table.grid(padding=(0, 2))
    table.add_column("Option", style="bold yellow", justify="center")
    table.add_column("Action", style="white")
    table.add_row("1", "➕  Add Category")
    table.add_row("2", "📋  View Catgories")
    table.add_row("0", "🔙  Back to Main Menu")

    console.print(Panel.fit(table, title="📋  Manage Categories", border_style="cyan", padding=(1, 2)))
    