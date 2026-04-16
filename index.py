from flask import Flask, jsonify, request
from connection import obter_conexao

app = Flask(__name__)

@app.route('/api/v1/scan', methods=['POST'])
def executar_scan():
    plsql_block = """
    DECLARE
        CURSOR c_bot_scrub IS
            SELECT i.ID AS inscricao_id, u.ID AS usuario_id, u.EMAIL, u.PRIORIDADE
            FROM INSCRICOES i
            JOIN USUARIOS u ON i.USUARIO_ID = u.ID
            WHERE i.STATUS = 'PENDING';
        v_row c_bot_scrub%ROWTYPE;
        v_contagem NUMBER := 0;
    BEGIN
        OPEN c_bot_scrub;
        LOOP
            FETCH c_bot_scrub INTO v_row;
            EXIT WHEN c_bot_scrub%NOTFOUND;
            
            IF v_row.EMAIL LIKE '%@fake.com%' OR v_row.EMAIL NOT LIKE '%@%.%' THEN
                UPDATE INSCRICOES SET STATUS = 'CANCELLED' WHERE ID = v_row.inscricao_id;
                UPDATE USUARIOS SET PRIORIDADE = GREATEST(PRIORIDADE - 15, 0) WHERE ID = v_row.usuario_id;
                INSERT INTO LOG_AUDITORIA (INSCRICAO_ID, MOTIVO, DATA)
                VALUES (v_row.inscricao_id, 'BOT DETECTADO: REST API SCAN', SYSDATE);
                v_contagem := v_contagem + 1;
            END IF;
        END LOOP;
        CLOSE c_bot_scrub;
        COMMIT;
    END;
    """
    
    conn = obter_conexao()
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    try:
        with conn.cursor() as cursor:
            cursor.execute(plsql_block)
        return jsonify({
            "status": "success",
            "message": "Varredura anti-bot concluída com sucesso.",
            "event": "Global Cyber Summit 2026"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# ENDPOINT: Listar Logs de Auditoria (GET)
@app.route('/api/v1/logs', methods=['GET'])
def listar_logs():
    conn = obter_conexao()
    if not conn:
        return jsonify({"erro": "Falha na conexão"}), 500

    try:
        with conn.cursor() as cursor:
            # Busca os logs para mostrar na API
            cursor.execute("SELECT ID, INSCRICAO_ID, MOTIVO, TO_CHAR(DATA, 'DD/MM/YYYY HH24:MI') FROM LOG_AUDITORIA ORDER BY DATA DESC")
            logs = []
            for row in cursor.fetchall():
                logs.append({
                    "id": row[0],
                    "inscricao_id": row[1],
                    "motivo": row[2],
                    "data": row[3]
                })
        return jsonify(logs), 200
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)