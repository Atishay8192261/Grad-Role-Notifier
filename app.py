from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
DB_PATH = "data/companies.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    companies = conn.execute("SELECT * FROM companies ORDER BY name").fetchall()
    conn.close()
    return render_template('index.html', companies=companies)

@app.route('/add', methods=['POST'])
def add_company():
    name = request.form['name'].strip()
    url = request.form['url'].strip()
    
    if not url:
        flash('Please provide a valid URL', 'error')
        return redirect(url_for('index'))
    
    # Auto-generate name from URL if not provided
    if not name:
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace('www.', '')
            name = domain.split('.')[0].capitalize()
        except:
            name = 'Unknown Company'
    
    try:
        conn = get_db_connection()
        conn.execute("INSERT OR IGNORE INTO companies (name, url) VALUES (?, ?)", (name, url))
        conn.commit()
        conn.close()
        flash(f'Successfully added {name} to monitoring list!', 'success')
    except Exception as e:
        flash('Error adding company. Please try again.', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_company(id):
    try:
        conn = get_db_connection()
        # Get company name for flash message
        company = conn.execute("SELECT name FROM companies WHERE id = ?", (id,)).fetchone()
        conn.execute("DELETE FROM companies WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        
        company_name = company['name'] if company else 'Company'
        flash(f'Successfully removed {company_name} from monitoring list.', 'success')
    except Exception as e:
        flash('Error removing company. Please try again.', 'error')
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
