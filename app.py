from flask import Flask, render_template, request

app = Flask(__name__)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedLists:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if self.head:
            new_node.next = self.head
            self.head = new_node
        else:
            self.tail = new_node
            self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head:
            self.tail.next = new_node
            self.tail = new_node
        else:
            self.head = new_node
            self.tail = new_node
    
    def remove_beginning(self):
        if self.head is None:
            return None
        deleted_data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return deleted_data 

    def remove_at_end(self):
        if self.tail is None:
            return None
        if self.head.next is None:
            deleted_data = self.head.data
            self.head = None
            self.tail = None
            return deleted_data
        
        current = self.head
        while current.next.next:
            current = current.next
        deleted_data = current.next.data
        current.next = None
        self.tail = current
        return deleted_data
    
    def remove_at(self, data):
        if not self.head:
            return None
        
        if self.head.data == data:
            deleted_data = self.head.data
            self.head = self.head.next
            if not self.head:
                self.tail = None
            return deleted_data

        current = self.head
        while current.next:
            if current.next.data == data:
                deleted_data = current.next.data
                current.next = current.next.next
                if not current.next:
                    self.tail = current
                return deleted_data
            current = current.next
        return None

    def get_linked_list(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

class Stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self, data):
        new_node = Node(data)
        if self.top:
            new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        else:
            popped_node = self.top
            self.top = self.top.next
            popped_node.next = None
            return popped_node.data

    def peek(self):
        if self.top:
            return self.top.data
        else:
            return None
            
    def get_stack_items(self):
        elements = []
        current = self.top
        while current:
            elements.append(current.data)
            current = current.next
        return elements

def shunting_yard_converter(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = Stack()
    postfix = []
    
    try:
        tokens = expression.split()
    except Exception:
        return "Invalid input expression."

    for token in tokens:
        if token.isalnum():
            postfix.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                postfix.append(stack.pop())
            if stack.is_empty():
                raise ValueError("Mismatched parentheses.")
            stack.pop() 
        else: 
            while (not stack.is_empty() and 
                   stack.peek() != '(' and 
                   precedence.get(stack.peek(), 0) >= precedence.get(token, 0)):
                postfix.append(stack.pop())
            stack.push(token)
            
    while not stack.is_empty():
        top_token = stack.pop()
        if top_token == '(':
             raise ValueError("Mismatched parentheses.")
        postfix.append(top_token)
        
    return ' '.join(postfix)

@app.route('/infix_to_postfix', methods=['GET', 'POST'])
def InfixToPostfix():
    infix_expression = ""
    postfix_expression = ""
    message = None

    if request.method == 'POST':
        infix_expression = request.form.get('infix_input', '')
        if not infix_expression:
            message = "Please enter an expression."
        else:
            try:
                postfix_expression = shunting_yard_converter(infix_expression)
            except ValueError as e:
                message = f"Error: {e}"
            except Exception as e:
                message = f"An unexpected error occurred: {e}"

    return render_template('infix_to_postfix.html',
                           infix_expression=infix_expression,
                           postfix_expression=postfix_expression,
                           message=message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/areaofcircle', methods=['GET', 'POST'])
def AreaOfCircle():
    area = None
    if request.method == 'POST':
        try:
            radius = float(request.form.get('radius', 0))
            area = round(3.14 * radius ** 2, 4)
        except ValueError:
            area = "Invalid input. Please enter a number."
    return render_template('areaofcircle.html', area=area)

@app.route('/areaoftriangle', methods=['GET', 'POST'])
def AreaOfTriangle():
    area = None
    if request.method == 'POST':
        try:
            base = float(request.form.get('base', 0))
            height = float(request.form.get('height', 0))
            area = round(0.5 * base * height, 4) 
        except ValueError:
            area = "Invalid input. Please enter valid numbers."
    return render_template('areaoftriangle.html', area=area)


@app.route('/touppercase', methods=['GET', 'POST'])
def ToUppercase():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()
    return render_template('touppercase.html', result=result)

@app.route('/lists', methods=['GET', 'POST'])
def Lists():
    message = None
    my_list = LinkedLists()
    if request.method == 'POST':
        old_list_items = request.form.getlist('list_item')
        for item in old_list_items:
            my_list.insert_at_end(item)
        action = request.form.get('action')
        data = request.form.get('data_input', '')
        try:
            if action == 'insert_beg' and data:
                my_list.insert_at_beginning(data)
                message = f"Added '{data}' to the beginning."
            elif action == 'insert_end' and data:
                my_list.insert_at_end(data)
                message = f"Added '{data}' to the end."
            elif action == 'remove_beg':
                deleted = my_list.remove_beginning()
                message = f"Removed '{deleted}'." if deleted else "List is empty."
            elif action == 'remove_end':
                deleted = my_list.remove_at_end()
                message = f"Removed '{deleted}'." if deleted else "List is empty."
            elif action == 'remove_at' and data:
                deleted = my_list.remove_at(data)
                message = f"Removed '{deleted}'." if deleted else f"'{data}' not found."
            elif not data and action in ['insert_beg', 'insert_end', 'remove_at']:
                message = "Please enter data in the text field."
        except Exception as e:
            message = f"An error occurred: {e}"
    current_list_for_html = my_list.get_linked_list()
    return render_template('lists.html', 
                           current_list=current_list_for_html, 
                           message=message)

@app.route('/stacks', methods=['GET', 'POST'])
def Stacks():
    infix_expression = ""
    postfix_expression = ""
    message = None

    if request.method == 'POST':
        infix_expression = request.form.get('infix_input', '')
        if not infix_expression:
            message = "Please enter an expression."
        else:
            try:
                postfix_expression = shunting_yard_converter(infix_expression)
            except ValueError as e:
                message = f"Error: {e}"
            except Exception as e:
                message = f"An unexpected error occurred: {e}"

    return render_template('stacks.html',
                           infix_expression=infix_expression,
                           postfix_expression=postfix_expression,
                           message=message)


if __name__ == "__main__":
    app.run(debug=True)
