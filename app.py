from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    with sqlite3.connect('inventory.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                quantity INTEGER DEFAULT 0,
                price REAL DEFAULT 0.0
            )
        ''')
        conn.commit()

# Home route - display all items
@app.route('/')
def index():
    with sqlite3.connect('inventory.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM inventory')
        items = cursor.fetchall()
    return render_template('index.html', items=items)

# Add a new inventory item
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        with sqlite3.connect('inventory.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO inventory (name, description, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (name, description, quantity, price))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Update an inventory item
@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    with sqlite3.connect('inventory.db') as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            quantity = int(request.form['quantity'])
            price = float(request.form['price'])
            cursor.execute('''
                UPDATE inventory
                SET name = ?, description = ?, quantity = ?, price = ?
                WHERE id = ?
            ''', (name, description, quantity, price, item_id))
            conn.commit()
            return redirect(url_for('index'))
        cursor.execute('SELECT * FROM inventory WHERE id = ?', (item_id,))
        item = cursor.fetchone()
    return render_template('update.html', item=item)

# Delete an inventory item
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    with sqlite3.connect('inventory.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
