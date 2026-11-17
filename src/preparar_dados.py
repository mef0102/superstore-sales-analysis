# =============================================================================
# Projeto de Recuperacao - Modulo 2
# Visualizacao de Dados e Business Intelligence - SENAI Lab 365
# Aluna: Maria Eduarda Fernandes
# =============================================================================
#
# Pergunta de negocio:
# Quais categorias, regioes e periodos concentram maior e menor faturamento,
# e quais oportunidades de melhoria os dados sugerem?
#
# Fonte dos dados:
# Superstore Sales Dataset - Kaggle (dados publicos)
# Link: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
# Licenca: dados de uso publico para fins educacionais
# Metodo de obtencao: download manual do arquivo CSV no Kaggle
# =============================================================================

# ETAPA 1 - Importacao das bibliotecas
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

# ETAPA 2 - Definicao dos caminhos
# Pasta onde este script esta salvo (src/)
pasta_src = os.path.dirname(os.path.abspath(__file__))
# Raiz do projeto (um nivel acima de src/)
pasta_raiz = os.path.join(pasta_src, "..")
# Pasta dos dados brutos (arquivo original baixado do Kaggle)
pasta_raw = os.path.join(pasta_raiz, "data", "raw")
# Pasta onde vamos salvar o arquivo tratado
pasta_processed = os.path.join(pasta_raiz, "data", "processed")
# Pasta onde vamos salvar os graficos (separada dos dados)
pasta_outputs = os.path.join(pasta_raiz, "outputs")
# Garante que as pastas existem
os.makedirs(pasta_processed, exist_ok=True)
os.makedirs(pasta_outputs, exist_ok=True)

# Caminho completo do arquivo de entrada
arquivo_entrada = os.path.join(pasta_raw, "Sample - Superstore.csv")
# Caminho completo do arquivo de saida
arquivo_saida = os.path.join(pasta_processed, "superstore_MariaEduarda.csv")

print("=" * 60)
print("INICIO DO ETL - SUPERSTORE SALES")
print("=" * 60)

# =============================================================================
# ETAPA 3 - Leitura do arquivo bruto
# =============================================================================
print("\nETAPA 3 - Carregando o arquivo bruto...")

# O arquivo usa encoding latin-1 (padrao para arquivos exportados do Excel)
# dtype=str garante que nao haja conversao automatica errada nos primeiros passos
df = pd.read_csv(arquivo_entrada, encoding="latin-1", dtype=str)

print(f"Arquivo carregado com sucesso!")
print(f"Linhas: {len(df)}")
print(f"Colunas: {df.shape[1]}")
print(f"Nomes das colunas: {df.columns.tolist()}")

# =============================================================================
# ETAPA 4 - Verificacao de duplicados
# =============================================================================
print("\nETAPA 4 - Verificando duplicados...")

duplicados = df.duplicated().sum()
print(f"Registros duplicados encontrados: {duplicados}")

if duplicados > 0:
    df = df.drop_duplicates()
    print(f"Duplicados removidos. Total de linhas agora: {len(df)}")
else:
    print("Nenhum duplicado encontrado. Base limpa!")

# =============================================================================
# ETAPA 5 - Selecao e renomeacao das colunas
# =============================================================================
print("\nETAPA 5 - Selecionando e renomeando colunas...")

# Mantemos apenas as colunas necessarias para a analise
colunas_manter = [
    "Order ID",
    "Order Date",
    "Ship Date",
    "Ship Mode",
    "Segment",
    "Country",
    "City",
    "State",
    "Region",
    "Category",
    "Sub-Category",
    "Product Name",
    "Sales",
    "Quantity",
    "Discount",
    "Profit"
]

df = df[colunas_manter]

# Renomeando as colunas para portugues (facilita entendimento no Power BI)
df = df.rename(columns={
    "Order ID":      "id_pedido",
    "Order Date":    "data_pedido",
    "Ship Date":     "data_envio",
    "Ship Mode":     "modo_envio",
    "Segment":       "segmento",
    "Country":       "pais",
    "City":          "cidade",
    "State":         "estado",
    "Region":        "regiao",
    "Category":      "categoria",
    "Sub-Category":  "subcategoria",
    "Product Name":  "nome_produto",
    "Sales":         "vendas",
    "Quantity":      "quantidade",
    "Discount":      "desconto",
    "Profit":        "lucro"
})

print(f"Colunas apos renomeacao: {df.columns.tolist()}")

# =============================================================================
# ETAPA 6 - Correcao dos tipos de dados
# =============================================================================
print("\nETAPA 6 - Corrigindo tipos de dados...")

# Converte datas
df["data_pedido"] = pd.to_datetime(df["data_pedido"], format="%m/%d/%Y", errors="coerce")
df["data_envio"]  = pd.to_datetime(df["data_envio"],  format="%m/%d/%Y", errors="coerce")

# Cria coluna de ano e mes a partir da data do pedido (util para filtros no Power BI)
df["ano"]  = df["data_pedido"].dt.year
df["mes"]  = df["data_pedido"].dt.month

# Converte colunas numericas
df["vendas"]    = pd.to_numeric(df["vendas"],    errors="coerce")
df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
df["desconto"]  = pd.to_numeric(df["desconto"],   errors="coerce")
df["lucro"]     = pd.to_numeric(df["lucro"],      errors="coerce")

# Formata a data para YYYY-MM-DD antes de salvar
df["data_pedido"] = df["data_pedido"].dt.strftime("%Y-%m-%d")
df["data_envio"]  = df["data_envio"].dt.strftime("%Y-%m-%d")

print("Tipos de dados apos correcao:")
print(df.dtypes)

# =============================================================================
# ETAPA 7 - Limpeza de texto
# =============================================================================
print("\nETAPA 7 - Limpando campos de texto...")

colunas_texto = [
    "id_pedido", "modo_envio", "segmento", "pais",
    "cidade", "estado", "regiao", "categoria",
    "subcategoria", "nome_produto"
]

for col in colunas_texto:
    # Remove espacos extras no inicio e fim
    # Substitui multiplos espacos por um unico espaco
    df[col] = df[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

print("Limpeza de texto concluida!")

# =============================================================================
# ETAPA 8 - Verificacao de valores nulos e inconsistencias
# =============================================================================
print("\nETAPA 8 - Verificando valores nulos e inconsistencias...")

nulos = df.isnull().sum()
print("Valores nulos por coluna:")
print(nulos.to_string())

# Verifica vendas negativas (nao deveriam existir)
vendas_negativas = (df["vendas"] < 0).sum()
print(f"\nVendas negativas: {vendas_negativas}")

# Verifica descontos acima de 100% (seria um erro)
desconto_invalido = (df["desconto"] > 1).sum()
print(f"Descontos acima de 100%: {desconto_invalido}")

# Lucro pode ser negativo (venda com prejuizo) - e esperado na base
lucro_negativo = (df["lucro"] < 0).sum()
print(f"Registros com lucro negativo (esperado): {lucro_negativo}")

# =============================================================================
# ETAPA 9 - Analise Exploratoria (EDA)
# =============================================================================
print("\n" + "=" * 60)
print("ETAPA 9 - ANALISE EXPLORATORIA (EDA)")
print("=" * 60)

# --- 9.1 Estatisticas descritivas gerais ---
print("\n--- Estatisticas descritivas ---")
print(f"Total de registros: {len(df):,}")
print(f"Total de pedidos distintos: {df['id_pedido'].nunique():,}")
print(f"Periodo: {df['data_pedido'].min()} a {df['data_pedido'].max()}")
print(f"Total de vendas (USD): $ {df['vendas'].sum():,.2f}")
print(f"Total de lucro (USD): $ {df['lucro'].sum():,.2f}")
print(f"Margem media de lucro: {(df['lucro'].sum() / df['vendas'].sum() * 100):.1f}%")
print(f"Ticket medio por pedido: $ {df.groupby('id_pedido')['vendas'].sum().mean():,.2f}")

# --- 9.2 Vendas por categoria ---
print("\n--- Vendas por Categoria ---")
vendas_categoria = (
    df.groupby("categoria")["vendas"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
vendas_categoria.columns = ["Categoria", "Total Vendas (USD)"]
print(vendas_categoria.to_string(index=False))

# --- 9.3 Lucro por categoria ---
print("\n--- Lucro por Categoria ---")
lucro_categoria = (
    df.groupby("categoria")["lucro"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
lucro_categoria.columns = ["Categoria", "Lucro Total (USD)"]
print(lucro_categoria.to_string(index=False))

# --- 9.4 Vendas por regiao ---
print("\n--- Vendas por Regiao ---")
vendas_regiao = (
    df.groupby("regiao")["vendas"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
vendas_regiao.columns = ["Regiao", "Total Vendas (USD)"]
print(vendas_regiao.to_string(index=False))

# --- 9.5 Evolucao anual ---
print("\n--- Evolucao Anual de Vendas ---")
vendas_ano = (
    df.groupby("ano")["vendas"]
    .sum()
    .reset_index()
)
vendas_ano.columns = ["Ano", "Total Vendas (USD)"]
print(vendas_ano.to_string(index=False))

# --- 9.6 Top 10 subcategorias por vendas ---
print("\n--- Top 10 Subcategorias por Vendas ---")
top10_sub = (
    df.groupby("subcategoria")["vendas"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top10_sub.columns = ["Subcategoria", "Total Vendas (USD)"]
print(top10_sub.to_string(index=False))

# --- 9.7 Segmentos ---
print("\n--- Vendas por Segmento ---")
vendas_segmento = (
    df.groupby("segmento")["vendas"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
vendas_segmento.columns = ["Segmento", "Total Vendas (USD)"]
print(vendas_segmento.to_string(index=False))

# --- 9.8 Produtos com prejuizo ---
print("\n--- Top 10 Subcategorias com Maior Prejuizo ---")
prejuizo_sub = (
    df.groupby("subcategoria")["lucro"]
    .sum()
    .sort_values()
    .head(10)
    .reset_index()
)
prejuizo_sub.columns = ["Subcategoria", "Lucro Total (USD)"]
print(prejuizo_sub.to_string(index=False))

# =============================================================================
# ETAPA 10 - Geracao de graficos para o relatorio
# =============================================================================
print("\nETAPA 10 - Gerando graficos...")

pasta_graficos = pasta_outputs

# Grafico 1: Vendas por Categoria
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(vendas_categoria["Categoria"], vendas_categoria["Total Vendas (USD)"], color=["#2196F3", "#4CAF50", "#FF9800"])
ax.set_title("Vendas Totais por Categoria (USD)", fontsize=13, fontweight="bold")
ax.set_xlabel("Categoria")
ax.set_ylabel("Total de Vendas (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"$ {x:,.0f}"))
plt.tight_layout()
plt.savefig(os.path.join(pasta_graficos, "grafico_vendas_categoria.png"), dpi=120)
plt.close()
print("  Grafico 1 salvo: grafico_vendas_categoria.png")

# Grafico 2: Vendas por Regiao
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(vendas_regiao["Regiao"], vendas_regiao["Total Vendas (USD)"], color=["#1565C0", "#42A5F5", "#90CAF9", "#BBDEFB"])
ax.set_title("Vendas Totais por Regiao (USD)", fontsize=13, fontweight="bold")
ax.set_xlabel("Regiao")
ax.set_ylabel("Total de Vendas (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"$ {x:,.0f}"))
plt.tight_layout()
plt.savefig(os.path.join(pasta_graficos, "grafico_vendas_regiao.png"), dpi=120)
plt.close()
print("  Grafico 2 salvo: grafico_vendas_regiao.png")

# Grafico 3: Evolucao anual de vendas
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(vendas_ano["Ano"], vendas_ano["Total Vendas (USD)"], marker="o", linewidth=2.5, color="#1565C0")
ax.set_title("Evolucao Anual de Vendas (USD)", fontsize=13, fontweight="bold")
ax.set_xlabel("Ano")
ax.set_ylabel("Total de Vendas (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"$ {x:,.0f}"))
ax.set_xticks(vendas_ano["Ano"])
plt.tight_layout()
plt.savefig(os.path.join(pasta_graficos, "grafico_evolucao_anual.png"), dpi=120)
plt.close()
print("  Grafico 3 salvo: grafico_evolucao_anual.png")

# Grafico 4: Lucro x Vendas por Categoria
lucro_vendas = df.groupby("categoria")[["vendas", "lucro"]].sum().reset_index()
x = range(len(lucro_vendas))
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar([i - 0.2 for i in x], lucro_vendas["vendas"], width=0.4, label="Vendas", color="#42A5F5")
ax.bar([i + 0.2 for i in x], lucro_vendas["lucro"], width=0.4, label="Lucro", color="#66BB6A")
ax.set_title("Vendas vs Lucro por Categoria (USD)", fontsize=13, fontweight="bold")
ax.set_xticks(list(x))
ax.set_xticklabels(lucro_vendas["categoria"])
ax.set_ylabel("Valor (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"$ {x:,.0f}"))
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta_graficos, "grafico_vendas_vs_lucro_categoria.png"), dpi=120)
plt.close()
print("  Grafico 4 salvo: grafico_vendas_vs_lucro_categoria.png")

# =============================================================================
# ETAPA 11 - Exportacao do arquivo tratado
# =============================================================================
print("\nETAPA 11 - Salvando arquivo tratado...")

df.to_csv(arquivo_saida, index=False, sep=";", encoding="utf-8-sig", decimal=",")

print(f"Arquivo salvo em: {arquivo_saida}")
print(f"Total de linhas salvas: {len(df):,}")

# =============================================================================
# ETAPA 12 - Verificacao final (simula leitura do Power BI)
# =============================================================================
print("\nETAPA 12 - Verificacao final (simulando leitura do Power BI)...")

df_check = pd.read_csv(arquivo_saida, sep=";", encoding="utf-8-sig", dtype=str)

print(f"Linhas: {len(df_check):,}")
print(f"Colunas: {df_check.shape[1]}")
print(f"Nomes das colunas: {df_check.columns.tolist()}")

# Confirma que as colunas numericas podem ser lidas como numero
for col in ["vendas", "quantidade", "desconto", "lucro"]:
    total = pd.to_numeric(df_check[col], errors="coerce").sum()
    print(f"  {col}: soma = {total:,.4f}")

print("\n" + "=" * 60)
print("ETL CONCLUIDO COM SUCESSO!")
print("=" * 60)
print("\nIndicadores para conferir no Power BI:")
print(f"  Total de registros: {len(df):,}")
print(f"  Total de vendas: $ {df['vendas'].sum():,.2f}")
print(f"  Total de lucro:  $ {df['lucro'].sum():,.2f}")
print(f"  Total de pedidos: {df['id_pedido'].nunique():,}")
print(f"  Periodo: {df['data_pedido'].min()} a {df['data_pedido'].max()}")
