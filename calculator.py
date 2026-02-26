import tkinter as tk


class Calculator:
    """
    A simple GUI calculator built with tkinter.

    Provides basic arithmetic operations (addition, subtraction,
    multiplication, division, percentage, and sign toggle) with a
    dark-themed interface.

    Attributes:
        root (tk.Tk): The root tkinter window.
        expression (str): The current mathematical expression being built.
        displayVar (tk.StringVar): The string variable bound to the display label.
    """

    def __init__(self, root):
        """
        Initialize the Calculator.

        Sets up the root window properties, initialises internal state,
        and builds the UI.

        Args:
            root (tk.Tk): The root tkinter window to attach the calculator to.
        """
        # root (tk.Tk): Main application window
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg="#2b2b2b")

        # expression (str): Accumulates the current input/expression
        self.expression = ""

        # displayVar (tk.StringVar): Observable variable driving the display label
        self.displayVar = tk.StringVar(value="0")

        self._buildUi()

    def _buildUi(self):
        """
        Build and lay out all UI widgets for the calculator.

        Creates the display label and all calculator buttons, arranging
        them in a grid inside the root window.

        Returns:
            None
        """
        # displayFrame (tk.Frame): Container for the output display label
        displayFrame = tk.Frame(self.root, bg="#2b2b2b", pady=10, padx=10)
        displayFrame.pack(fill="x")

        # display (tk.Label): Shows the current expression or result
        display = tk.Label(
            displayFrame,
            textvariable=self.displayVar,
            anchor="e",
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Segoe UI", 28, "bold"),
            padx=15,
            pady=15,
            relief="flat",
            bd=0,
        )
        display.pack(fill="x")

        # buttons (list[list[str]]): 2-D grid of button labels in display order
        buttons = [
            ["C", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "⌫", "="],
        ]

        # btnFrame (tk.Frame): Container for the button grid
        btnFrame = tk.Frame(self.root, bg="#2b2b2b", padx=10, pady=5)
        btnFrame.pack()

        for rowIdx, row in enumerate(buttons):
            for colIdx, label in enumerate(row):
                # btn (tk.Button): Individual calculator button
                btn = tk.Button(
                    btnFrame,
                    text=label,
                    font=("Segoe UI", 18, "bold"),
                    width=4,
                    height=2,
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    bg=self._btnColor(label),
                    fg=self._btnFg(label),
                    activebackground=self._btnActive(label),
                    activeforeground="#ffffff",
                    command=lambda l=label: self._onClick(l),
                )
                btn.grid(row=rowIdx, column=colIdx, padx=5, pady=5, ipadx=4)

    def _btnColor(self, label):
        """
        Return the background colour for a button based on its label.

        Args:
            label (str): The text displayed on the button.

        Returns:
            str: A hex colour string for the button background.
        """
        if label == "=":
            return "#ff9500"
        if label in ("÷", "×", "−", "+"):
            return "#ff9500"
        if label in ("C", "±", "%"):
            return "#505050"
        return "#3a3a3a"

    def _btnFg(self, label):
        """
        Return the foreground (text) colour for a button.

        Args:
            label (str): The text displayed on the button.

        Returns:
            str: A hex colour string for the button text.
        """
        return "#ffffff"

    def _btnActive(self, label):
        """
        Return the active (hover/press) background colour for a button.

        Args:
            label (str): The text displayed on the button.

        Returns:
            str: A hex colour string for the active button background.
        """
        if label == "=":
            return "#e08800"
        if label in ("÷", "×", "−", "+"):
            return "#e08800"
        if label in ("C", "±", "%"):
            return "#707070"
        return "#555555"

    def _onClick(self, label):
        """
        Handle a button press event.

        Dispatches to the appropriate action based on the button label:
        clear, backspace, sign toggle, percentage, equals, or digit/operator.

        Args:
            label (str): The text of the button that was clicked.

        Returns:
            None
        """
        if label == "C":
            # Clear the entire expression and reset the display
            self.expression = ""
            self.displayVar.set("0")

        elif label == "⌫":
            # Remove the last character from the expression
            self.expression = self.expression[:-1]
            self.displayVar.set(self.expression if self.expression else "0")

        elif label == "±":
            # Toggle the sign of the current expression
            if self.expression and self.expression not in ("0", ""):
                if self.expression.startswith("-"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "-" + self.expression
                self.displayVar.set(self.expression)

        elif label == "%":
            # Convert the current value to a percentage (divide by 100)
            try:
                value = str(float(self.expression) / 100)
                self.expression = value
                self.displayVar.set(self._format(float(value)))
            except Exception:
                self.displayVar.set("Error")
                self.expression = ""

        elif label == "=":
            # Evaluate the current expression and display the result
            try:
                result = eval(self.expression)
                self.displayVar.set(self._format(result))
                self.expression = str(result)
            except ZeroDivisionError:
                self.displayVar.set("÷0 Error")
                self.expression = ""
            except Exception:
                self.displayVar.set("Error")
                self.expression = ""

        else:
            # opMap (dict[str, str]): Maps display operator symbols to Python operators
            opMap = {"÷": "/", "×": "*", "−": "-"}
            # char (str): The Python-compatible character to append to the expression
            char = opMap.get(label, label)
            self.expression += char
            self.displayVar.set(self.expression)

    def _format(self, value):
        """
        Format a numeric value for display, removing unnecessary decimals.

        Converts whole-number floats (e.g. 4.0) to integers (e.g. 4)
        before converting to a string.

        Args:
            value (int | float): The numeric result to format.

        Returns:
            str: The formatted string representation of the value.
        """
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)


if __name__ == "__main__":
    # root (tk.Tk): Top-level application window
    root = tk.Tk()
    # app (Calculator): The running calculator instance
    app = Calculator(root)
    root.mainloop()
