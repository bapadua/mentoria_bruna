import psycopg2
from psycopg2.extras import execute_values
import pandas as pd

# Configurações
DB_CONFIG = {
    'host': '192.168.15.102',
    'database': 'poc_mvc',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

# Função para carregar dados limpos
def load_to_postgres(csv_path='transacoes_limpas.csv'):
    """
    Carrega dados do CSV limpo para o PostgreSQL
    """
    # Ler CSV limpo
    df = pd.read_csv(csv_path)
    
    # Conectar ao banco
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # SQL para INSERT com tratamento de conflito
    insert_sql = """
        INSERT INTO transactions (
            transaction_id, flag, card_number, amount, 
            date, merchant_id, transaction_type, transaction_status
        ) VALUES %s
        ON CONFLICT (transaction_id) DO UPDATE SET
            flag = EXCLUDED.flag,
            card_number = EXCLUDED.card_number,
            amount = EXCLUDED.amount,
            date = EXCLUDED.date,
            merchant_id = EXCLUDED.merchant_id,
            transaction_type = EXCLUDED.transaction_type,
            transaction_status = EXCLUDED.transaction_status
    """
    
    # Preparar dados para insert
    data = df.values.tolist()
    
    # Executar insert em batch
    execute_values(cursor, insert_sql, data)
    
    # Commit e fechar
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ {len(data)} registros carregados para o PostgreSQL!")

if __name__ == "__main__":
    load_to_postgres()