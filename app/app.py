from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection (use environment variables in Docker)
def get_db_connection():
    conn = psycopg2.connect(
        dbname='telecom_inventory',
        user='postgres',
        password='your_secure_password',
        host='db'
    )
    return conn

# Helper to execute queries
def execute_query(query, params=None, fetch=False):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query, params)
        if fetch:
            result = cur.fetchall() if fetch == 'all' else cur.fetchone()
            conn.commit()
            return result
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

# NSO Trunks CRUD
@app.route('/nso_trunks', methods=['GET'])
def get_nso_trunks():
    trunks = execute_query("SELECT * FROM nso_trunks", fetch='all')
    return jsonify(trunks)

@app.route('/nso_trunks', methods=['POST'])
def create_nso_trunk():
    data = request.json
    query = """
        INSERT INTO nso_trunks (trunk_name, channels_count, description)
        VALUES (%s, %s, %s) RETURNING id
    """
    result = execute_query(query, (data['trunk_name'], data['channels_count'], data.get('description')), fetch='one')
    return jsonify({'id': result['id']}), 201

@app.route('/nso_trunks/<int:id>', methods=['PUT'])
def update_nso_trunk(id):
    data = request.json
    query = """
        UPDATE nso_trunks SET trunk_name=%s, channels_count=%s, description=%s
        WHERE id=%s RETURNING id
    """
    result = execute_query(query, (data['trunk_name'], data['channels_count'], data.get('description'), id), fetch='one')
    return jsonify({'id': result['id']})

@app.route('/nso_trunks/<int:id>', methods=['DELETE'])
def delete_nso_trunk(id):
    execute_query("DELETE FROM nso_trunks WHERE id=%s", (id,))
    return '', 204

# Customer Trunks CRUD (similar pattern)
@app.route('/customer_trunks', methods=['GET'])
def get_customer_trunks():
    trunks = execute_query("SELECT * FROM customer_trunks", fetch='all')
    return jsonify(trunks)

@app.route('/customer_trunks', methods=['POST'])
def create_customer_trunk():
    data = request.json
    query = """
        INSERT INTO customer_trunks (customer_name, trunk_name, channels_count, description)
        VALUES (%s, %s, %s, %s) RETURNING id
    """
    result = execute_query(query, (data['customer_name'], data['trunk_name'], data['channels_count'], data.get('description')), fetch='one')
    return jsonify({'id': result['id']}), 201

# Add more endpoints for customer_trunks (PUT, DELETE), nso_dids, customer_dids, mappings as needed...

# NSO to VNO Mappings
@app.route('/mappings', methods=['GET'])
def get_mappings():
    mappings = execute_query("""
        SELECT m.id, n.trunk_name as nso_trunk, c.trunk_name as customer_trunk, m.mapping_type
        FROM nso_to_vno_mappings m
        JOIN nso_trunks n ON m.nso_trunk_id = n.id
        JOIN customer_trunks c ON m.customer_trunk_id = c.id
    """, fetch='all')
    return jsonify(mappings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
