import requests
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter.font import Font

class CurrencyConverter:
    def __init__(self):
        self.window = Tk()
        self.window.title("Currency Converter")
        self.window.geometry("400x600")
        self.window.resizable(False, False)
        
        # Updated color scheme
        self.colors = {
            'bg': '#0A0F2C',        # Dark blue background
            'input_bg': '#FFFFFF',  # White input background
            'text': '#FFFFFF',      # White text
            'button': '#00B4D8',    # Bright blue button
            'result': '#FFFFFF'     # White result text
        }
        
        # Define currencies dictionary without flags
        self.currencies = {
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'JPY': 'Japanese Yen',
            'GBP': 'British Pound',
            'CNY': 'Chinese Yuan',
            'AUD': 'Australian Dollar',
            'CAD': 'Canadian Dollar',
            'CHF': 'Swiss Franc',
            'HKD': 'Hong Kong Dollar',
            'NGN': 'Nigerian Naira',
            'SGD': 'Singapore Dollar'
        }
        
        self.window.configure(bg=self.colors['bg'])
        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = Label(
            self.window,
            text="Currency Converter",
            font=("Arial", 24),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title_label.pack(pady=(40, 20))
        
        # Result display (moved to top like in image)
        self.result_label = Label(
            self.window,
            text="$ 0.00",
            font=("Arial", 48, "bold"),  # Increased font size
            bg=self.colors['bg'],
            fg=self.colors['result']
        )
        self.result_label.pack(pady=(0, 10))
        
        self.sub_result_label = Label(
            self.window,
            text="Converted Currency (USD)",
            font=("Arial", 12),
            bg=self.colors['bg'],
            fg='#8E8E8E'
        )
        self.sub_result_label.pack(pady=(0, 30))
        # Main container for inputs
        main_frame = Frame(self.window, bg=self.colors['bg'])
        main_frame.pack(fill='x', padx=20)
        
        # Amount input
        Label(
            main_frame,
            text="AMOUNT",
            font=("Arial", 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        self.amount_entry = Entry(
            main_frame,
            font=("Arial", 16),
            bg=self.colors['input_bg'],
            fg='#000000',
            relief='flat'
        )
        self.amount_entry.pack(fill='x', pady=(5, 20))
        
        # Currency selection frame
        currency_frame = Frame(main_frame, bg=self.colors['bg'])
        currency_frame.pack(fill='x', pady=10)
        
        # Style for comboboxes
        style = ttk.Style()
        style.configure(
            "Currency.TCombobox",
            background=self.colors['input_bg'],
            fieldbackground=self.colors['input_bg'],
            foreground='#000000',
            arrowcolor=self.colors['text']
        )
        
        # From currency with flag
        from_frame = Frame(currency_frame, bg=self.colors['bg'])
        from_frame.pack(side=LEFT, fill='x', expand=True, padx=(0, 10))
        
        self.from_currency = ttk.Combobox(
            from_frame,
            values=[f"{code} - {self.currencies[code]}" for code in self.currencies.keys()],
            style="Currency.TCombobox",
            state='readonly',
            font=("Arial", 12),
            width=25
        )
        self.from_currency.pack(fill='x')
        self.from_currency.set(f"NGN - {self.currencies['NGN']}")
        
        # To currency with flag
        to_frame = Frame(currency_frame, bg=self.colors['bg'])
        to_frame.pack(side=LEFT, fill='x', expand=True, padx=(10, 0))
        
        self.to_currency = ttk.Combobox(
            to_frame,
            values=[f"{code} - {self.currencies[code]}" for code in self.currencies.keys()],
            style="Currency.TCombobox",
            state='readonly',
            font=("Arial", 12),
            width=25
        )
        self.to_currency.pack(fill='x')
        self.to_currency.set(f"USD - {self.currencies['USD']}")
        
        # Exchange rate display
        self.rate_label = Label(
            main_frame,
            text="1 NGN = 0.0014 USD",
            font=("Arial", 12),
            bg=self.colors['bg'],
            fg='#8E8E8E'
        )
        self.rate_label.pack(pady=20)
        
        # Convert button (changed text from PURCHASE CURRENCY)
        convert_button = Button(
            main_frame,
            text="CONVERT",
            font=("Arial", 14, "bold"),
            bg=self.colors['button'],
            fg=self.colors['text'],
            relief='flat',
            command=self.convert,
            cursor='hand2'
        )
        convert_button.pack(fill='x', pady=20)

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get().split(' - ')[0]  # Changed split to handle hyphen format
            to_curr = self.to_currency.get().split(' - ')[0]      # Changed split to handle hyphen format
            
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            response = requests.get(url)
            data = response.json()
            
            rate = data['rates'][to_curr]
            converted_amount = amount * rate
            
            # Update result and rate labels
            currency_symbols = {'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥'}
            symbol = currency_symbols.get(to_curr, '')
            
            self.result_label.config(text=f"{symbol} {converted_amount:,.2f}")
            self.rate_label.config(text=f"1 {from_curr} = {rate:.4f} {to_curr}")
            self.sub_result_label.config(text=f"Converted Currency ({to_curr})")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch exchange rates")
        except KeyError:
            messagebox.showerror("Error", "Invalid currency selection")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CurrencyConverter()
    app.run()