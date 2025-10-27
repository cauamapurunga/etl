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
    print("\nIniciando pipeline ETL - Modelo Medalhão\n")
    
    run_script("scripts/extract/get_data.py", "EXTRACT → Bronze (dados brutos)")
    run_script("scripts/transform/normalize_data.py", "TRANSFORM → Silver (dados validados)")
    run_script("scripts/load/populate_db.py", "LOAD → Gold (Parte 1: Carrega no PostgreSQL)")
    run_script("scripts/load/enrich_data.py", "LOAD → Gold (Parte 2: Enriquece e exporta)")
    
    print(f"\n{'='*50}")
    print("✓ Pipeline ETL concluído com sucesso!")
    print(f"{'='*50}\n")
