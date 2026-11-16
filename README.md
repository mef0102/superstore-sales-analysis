# Análise de Faturamento — Superstore Sales Dataset
## Projeto de Recuperação — Módulo 2 — Visualização de Dados e BI

**Aluna:** Maria Eduarda Fernandes
**Turma:** Visualização de Dados e BI — 2026/1
**Data de entrega:** 16/11/2026

---

## 1. Título, Resumo e Assunto Analisado

Este projeto analisa o dataset público **Superstore Sales** (Kaggle) para identificar quais categorias, regiões e períodos concentram maior e menor faturamento em uma rede varejista fictícia dos Estados Unidos, e quais oportunidades de melhoria os dados sugerem.

---

## 2. Problema, Objetivo e Importância

**Pergunta orientadora:**
> *Quais categorias, regiões e períodos concentram maior e menor faturamento na Superstore, e quais oportunidades de melhoria os dados sugerem?*

**Público-alvo:** Times de vendas e gestores comerciais que precisam identificar onde concentrar esforços para aumentar rentabilidade.

**Relevância:** Compreender a distribuição do faturamento por categoria e região permite priorizar ações comerciais, revisar políticas de desconto e alocar recursos de forma mais eficiente.

---

## 3. Escopo e Resultados Esperados

**Dentro do escopo:**
- Análise descritiva de vendas, lucro e quantidade por categoria, subcategoria, região, segmento e período (2014–2017)
- Identificação de subcategorias com prejuízo acumulado
- Visualizações que respondem diretamente à pergunta orientadora

**Fora do escopo:**
- Modelagem preditiva ou análise de séries temporais avançada
- Dados posteriores a 2017 (não disponíveis no dataset)
- Análise de custos operacionais (não disponível na fonte)

**Entregas analíticas esperadas:**
- Script Python de ETL + EDA com comentários em português
- Dataset tratado em CSV pronto para Power BI
- 4 gráficos exportados como PNG
- Dashboard interativo no Power BI (arquivo `.pbix`)
- Este README documentando todo o processo

---

## 4. Fonte Pública de Dados

| Campo | Detalhe |
|-------|---------|
| **Nome** | Superstore Sales Dataset |
| **Plataforma** | Kaggle |
| **Link** | https://www.kaggle.com/datasets/vivek468/superstore-dataset-final |
| **Responsável** | Usuário vivek468 (Kaggle) |
| **Período dos dados** | 2014 a 2017 |
| **Campos utilizados** | 16 de 21 colunas originais (ver Etapa 5 do script) |
| **Licença** | Dados públicos para fins educacionais |
| **Método de captura** | Download manual do arquivo CSV no Kaggle |
| **Data de acesso** | Novembro de 2026 |

> Os dados brutos **não estão versionados** no repositório (pasta `data/raw/` está no `.gitignore`) para respeitar os termos da licença. Para reproduzir a análise, baixe o arquivo `Sample - Superstore.csv` no link acima e coloque-o em `data/raw/`.

---

## 5. Pipeline e Metodologia

O script `src/preparar_dados.py` executa 12 etapas documentadas:

| Etapa | Descrição | Decisão registrada |
|-------|-----------|-------------------|
| 1 | Importação das bibliotecas | pandas, matplotlib, os, warnings |
| 2 | Definição dos caminhos das pastas | Caminhos relativos à raiz do projeto |
| 3 | Leitura do arquivo bruto | Encoding `latin-1`; `dtype=str` para evitar conversão prematura |
| 4 | Verificação e remoção de duplicados | 0 duplicados encontrados; base intacta |
| 5 | Seleção e renomeação de colunas | Mantidas 16 de 21 colunas; 5 removidas (Row ID, Customer ID, Customer Name, Postal Code, Product ID) por não serem necessárias para a análise |
| 6 | Correção de tipos de dados | Datas convertidas com `format="%m/%d/%Y"`; colunas numéricas com `pd.to_numeric`; colunas `ano` e `mes` derivadas de `data_pedido` |
| 7 | Limpeza de texto | `.strip()` e remoção de espaços duplos em todas as colunas de texto |
| 8 | Verificação de nulos e inconsistências | 0 nulos; 0 vendas negativas; 0 descontos > 100%; 1.871 registros com lucro negativo mantidos (relevante para a análise) |
| 9 | EDA — estatísticas e agrupamentos | Totais por categoria, região, ano, segmento; top 10 subcategorias; top 10 com prejuízo |
| 10 | Geração de 4 gráficos PNG | Salvos em `outputs/` |
| 11 | Exportação do CSV tratado | `sep=";"`, `encoding="utf-8-sig"`, `decimal="."` para compatibilidade com Power BI |
| 12 | Verificação final | Releitura simulando leitura do Power BI; conferência das somas |

---

## 6. Bibliotecas e Tecnologias

| Ferramenta | Versão mínima | Função |
|-----------|--------------|--------|
| Python | 3.8+ | Linguagem principal do ETL e EDA |
| pandas | 1.5.0+ | Manipulação e análise de dados tabulares |
| matplotlib | 3.5.0+ | Geração de gráficos estáticos |
| Power BI Desktop | Qualquer versão atual | Dashboard interativo |
| GitHub | — | Versionamento e entrega do código |

---

## 7. Resultados Encontrados

### Indicadores gerais

| Indicador | Valor |
|-----------|-------|
| Total de registros | 9.994 |
| Total de pedidos distintos | 5.009 |
| Período | 2014-01-03 a 2017-12-30 |
| Total de vendas | $ 2.297.200,86 |
| Total de lucro | $ 286.397,02 |
| Margem média de lucro | 12,5% |
| Ticket médio por pedido | $ 458,61 |

### Vendas e lucro por categoria

| Categoria | Vendas (USD) | Lucro (USD) | Margem |
|-----------|-------------|-------------|--------|
| Technology | $ 836.154 | $ 145.455 | 17,4% |
| Furniture | $ 741.999 | $ 18.451 | 2,5% |
| Office Supplies | $ 719.047 | $ 122.491 | 17,0% |

### Vendas por região

| Região | Vendas (USD) |
|--------|-------------|
| West | $ 725.457 |
| East | $ 678.781 |
| Central | $ 501.240 |
| South | $ 391.722 |

### Descobertas principais

- **Technology** é a categoria com maior faturamento ($836K) e maior lucro ($145K)
- **Furniture** tem alto faturamento ($742K) mas lucro muito baixo ($18K) — margem de apenas **2,5%**
- **Tables** é a subcategoria com maior prejuízo acumulado (−$17.725)
- A região **West** lidera em vendas; **South** tem o menor volume
- As vendas cresceram **51%** entre 2014 e 2017

---

## 8. Discussão e Conclusão

Os dados indicam que **Furniture**, apesar de representar 32% do faturamento total, contribui com apenas 6,4% do lucro total — sugerindo que a política de descontos nessa categoria (especialmente em Tables e Bookcases) pode estar corroendo a margem de forma sistemática.

**O que os dados permitem concluir:**
- Há uma disparidade real entre faturamento e lucratividade em Furniture
- O crescimento de vendas é consistente ao longo dos 4 anos analisados
- West e East concentram ~62% das vendas

**O que os dados não permitem concluir:**
- As causas dos prejuízos em Tables (podem ser descontos, frete, devolução — não disponíveis)
- Se a tendência de crescimento continuou após 2017
- Comparação com mercado (dataset fictício, sem benchmark externo)

---

## 9. Aplicação Profissional

Em um ambiente corporativo, este pipeline poderia ser utilizado para:

- **Revisão trimestral de margens**: automatizar o ETL para rodar com dados atualizados e alimentar o dashboard sem intervenção manual
- **Alertas de rentabilidade**: disparar notificações quando a margem de alguma subcategoria cair abaixo de um limiar
- **Requisitos de atualização**: o script depende do formato do CSV exportado pelo sistema ERP; qualquer mudança de colunas ou encoding exigiria manutenção
- **Governança**: dados de clientes (Customer Name, Customer ID) foram deliberadamente excluídos para minimizar exposição de dados pessoais
- **Manutenção**: requer Python 3.8+ e as bibliotecas listadas em `requirements.txt`

---

## 10. Relatório Power BI

O arquivo `.pbix` está incluído neste repositório.

**Como abrir e navegar:**
1. Instale o Power BI Desktop (gratuito em powerbi.microsoft.com)
2. Abra o arquivo `.pbix`
3. Se necessário, atualize o caminho da fonte: `Transformar Dados > Configurações da Fonte`; aponte para `data/processed/superstore_MariaEduarda.csv`
4. Clique em **Atualizar** para recarregar os dados
5. Use os filtros de Ano, Categoria e Região para explorar os resultados

**Componentes do dashboard:**
- KPIs: Total de Vendas, Total de Lucro, Margem Média, Total de Pedidos
- Gráfico de barras: Vendas por Categoria
- Gráfico de barras: Vendas por Região
- Gráfico de linhas: Evolução Anual de Vendas
- Gráfico de barras agrupadas: Vendas vs. Lucro por Categoria
- Filtros interativos: Ano, Categoria, Região, Segmento

---

## 11. Como Executar

**Pré-requisitos:**
- Python 3.8 ou superior
- Arquivo `Sample - Superstore.csv` em `data/raw/` (download no Kaggle — link na seção 4)

**Instalação das dependências:**
```bash
pip install -r requirements.txt
```

**Execução:**
```bash
python src/preparar_dados.py
```

**Saídas geradas:**
- `data/processed/superstore_MariaEduarda.csv` — dataset tratado para o Power BI
- `outputs/grafico_vendas_categoria.png`
- `outputs/grafico_vendas_regiao.png`
- `outputs/grafico_evolucao_anual.png`
- `outputs/grafico_vendas_vs_lucro_categoria.png`

---

## 12. Estrutura de Pastas

```
Projeto_Recuperacao_MariaEduarda/
├── README.md                          # Este arquivo
├── requirements.txt                   # Dependências Python
├── .gitignore                         # Arquivos excluídos do versionamento
├── data/
│   ├── raw/                           # Dados brutos (não versionados — ver .gitignore)
│   │   └── Sample - Superstore.csv
│   └── processed/                     # Dados tratados (prontos para o Power BI)
│       └── superstore_MariaEduarda.csv
├── src/
│   └── preparar_dados.py              # Script Python de ETL + EDA
├── outputs/                           # Gráficos gerados pelo script
│   ├── grafico_vendas_categoria.png
│   ├── grafico_vendas_regiao.png
│   ├── grafico_evolucao_anual.png
│   └── grafico_vendas_vs_lucro_categoria.png
├── notebooks/                         # (reservado para exploração futura)
└── docs/                              # (reservado para documentação adicional)
```

---

## 13. Limitações e Melhorias Futuras

**Limitações:**
- Dataset fictício (Superstore é uma empresa simulada) — resultados não representam uma empresa real
- Dados abrangem apenas 2014–2017; tendências recentes não estão representadas
- A análise é descritiva — correlações observadas não implicam causalidade
- Dados de custo operacional e detalhes de devolução não estão disponíveis
- Variável `Profit` já é o lucro calculado na fonte, sem acesso à margem bruta real

**Melhorias futuras:**
- Incluir dados de devoluções para calcular taxa de cancelamento por categoria
- Adicionar análise por cliente (RFM — Recência, Frequência, Valor Monetário)
- Automatizar o pipeline com agendamento e alerta de anomalias
- Expandir o dashboard com análise de sazonalidade mensal

---

## 14. Créditos e Referências

- **Fonte dos dados:** Vivek468. *Superstore Dataset*. Kaggle, 2022. Disponível em: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
- **Biblioteca pandas:** McKinney, W. et al. *pandas: powerful Python data analysis toolkit*. https://pandas.pydata.org/
- **Biblioteca matplotlib:** Hunter, J. D. *Matplotlib: A 2D graphics environment*. https://matplotlib.org/
- **Power BI Desktop:** Microsoft Corporation. https://powerbi.microsoft.com/

---

## 15. Links de Entrega

- **Repositório GitHub (pessoal):** *(adicionar link após criar o repositório)*
- **Arquivo .pbix:** incluído no repositório
- **Dashboard Power BI Service:** *(opcional — adicionar link se publicado)*

---

*Projeto desenvolvido para o Módulo 2 do curso de Visualização de Dados e BI — SENAI Lab 365*
