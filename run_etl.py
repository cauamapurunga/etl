import subprocess
import sys

def run_script(script_name, description):
    print(f"\n{'='*50}")
    print(f"Executando: {description}")
    print(f"{'='*50}")
    
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=False,
        text=True
    )
    
    if result.returncode != 0:
        print(f"\nERRO ao executar {script_name}")
        sys.exit(1)
    
    print(f"\n✓ {description} concluído")

if __name__ == "__main__":
    print("\n🚀 Iniciando pipeline ETL - Modelo Medalhão\n")
    
    run_script("scripts/extract/get_data.py", "BRONZE - Extraindo dados da API ViaCEP")
    run_script("scripts/transform/normalize_data.py", "SILVER - Normalizando e convertendo para Parquet")
    run_script("scripts/load/populate_db.py", "LOAD - Carregando dados no PostgreSQL")
    run_script("scripts/load/enrich_gold.py", "GOLD - Enriquecendo dados finais")
    
    print(f"\n{'='*50}")
    print("✓ Pipeline ETL concluído com sucesso!")
    print(f"{'='*50}\n")
