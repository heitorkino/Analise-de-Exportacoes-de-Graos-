-- Views Resumo Anual 
CREATE VIEW vw_exports_summary_2023 AS
SELECT
	CO_ANO,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg,
	COUNT(DISTINCT CO_MES) AS meses_com_exportacao
FROM exportacoes_2023
GROUP BY CO_ANO;

CREATE VIEW vw_exports_summary_2024 AS
SELECT
	CO_ANO,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg,
	COUNT(DISTINCT CO_MES) AS meses_com_exportacao
FROM exportacoes_2024
GROUP BY CO_ANO;

CREATE VIEW vw_exports_summary_2025 AS
SELECT
	CO_ANO,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg,
	COUNT(DISTINCT CO_MES) AS meses_com_exportacao
FROM exportacoes_2025
GROUP BY CO_ANO;

-- Views Evolução Mensal
CREATE VIEW vw_monthly_exports_2023 AS
SELECT
	CO_ANO,
	CO_MES,
	MAKE_DATE(CO_ANO, CO_MES, 1) AS data_mes,
	SUM(VL_FOB) AS fob_mes,
	SUM(KG_LIQUIDO) AS kg_mes
FROM exportacoes_2023
GROUP BY CO_ANO, CO_MES;

CREATE VIEW vw_monthly_exports_2024 AS
SELECT
	CO_ANO,
	CO_MES,
	MAKE_DATE(CO_ANO, CO_MES, 1) AS data_mes,
	SUM(VL_FOB) AS fob_mes,
	SUM(KG_LIQUIDO) AS kg_mes
FROM exportacoes_2024
GROUP BY CO_ANO, CO_MES;

CREATE VIEW vw_monthly_exports_2025 AS
SELECT
	CO_ANO,
	CO_MES,
	MAKE_DATE(CO_ANO, CO_MES, 1) AS data_mes,
	SUM(VL_FOB) AS fob_mes,
	SUM(KG_LIQUIDO) AS kg_mes
FROM exportacoes_2025
GROUP BY CO_ANO, CO_MES;

-- Views Top 5 Destino por Ano
CREATE VIEW vw_top_5_destinations_2023 AS
SELECT
	CO_ANO,
	CO_PAIS,
	SUM(VL_FOB) AS fob
FROM exportacoes_2023
GROUP BY CO_ANO, CO_PAIS
ORDER BY CO_PAIS ASC
LIMIT 5;

CREATE VIEW vw_top_5_destinations_2024 AS
SELECT
	CO_ANO,
	CO_PAIS,
	SUM(VL_FOB) AS fob
FROM exportacoes_2024
GROUP BY CO_ANO, CO_PAIS
ORDER BY CO_PAIS ASC
LIMIT 5;

CREATE VIEW vw_top_5_destinations_2025 AS
SELECT
	CO_ANO,
	CO_PAIS,
	SUM(VL_FOB) AS fob
FROM exportacoes_2025
GROUP BY CO_ANO, CO_PAIS
ORDER BY CO_PAIS ASC
LIMIT 5;

-- Views Top 5 Produtos por Ano
CREATE VIEW vw_top_5_products_2023 AS
SELECT
	CO_ANO,
	CO_NCM,
	SUM(VL_FOB) AS fob
FROM exportacoes_2023
GROUP BY CO_ANO, CO_NCM
ORDER BY CO_NCM ASC
LIMIT 5;

CREATE VIEW vw_top_5_products_2024 AS
SELECT
	CO_ANO,
	CO_NCM,
	SUM(VL_FOB) AS fob
FROM exportacoes_2024
GROUP BY CO_ANO, CO_NCM
ORDER BY CO_NCM ASC
LIMIT 5;

CREATE VIEW vw_top_5_products_2025 AS
SELECT
	CO_ANO,
	CO_NCM,
	SUM(VL_FOB) AS fob
FROM exportacoes_2025
GROUP BY CO_ANO, CO_NCM
ORDER BY CO_NCM ASC
LIMIT 5;

-- Views Exportação Média Mensal
CREATE VIEW vw_monthly_avg_export_2023 AS
SELECT
	CO_ANO,
	AVG(FOB_MES) AS media_fob_mensal
FROM vw_monthly_exports_2023
GROUP BY CO_ANO;

CREATE VIEW vw_monthly_avg_export_2024 AS
SELECT
	CO_ANO,
	AVG(FOB_MES) AS media_fob_mensal
FROM vw_monthly_exports_2024
GROUP BY CO_ANO;

CREATE VIEW vw_monthly_avg_export_2025 AS
SELECT
	CO_ANO,
	AVG(FOB_MES) AS media_fob_mensal
FROM vw_monthly_exports_2025
GROUP BY CO_ANO;

-- Views Série Mensal
CREATE OR REPLACE VIEW vw_monthly_timeseries_2023 AS
SELECT
	CO_ANO,
	CO_MES,
	MAKE_DATE(CO_ANO, CO_MES, 1) AS data_mes,
	SUM(VL_FOB) AS fob_mes,
	SUM(KG_LIQUIDO) AS kg_mes
FROM exportacoes_2023
GROUP BY CO_ANO, CO_MES;

CREATE OR REPLACE VIEW vw_monthly_timeseries_2024 AS
SELECT
	CO_ANO,
	CO_MES,
	MAKE_DATE(CO_ANO, CO_MES, 1) AS data_mes,
	SUM(VL_FOB) AS fob_mes,
	SUM(KG_LIQUIDO) AS kg_mes
FROM exportacoes_2024
GROUP BY CO_ANO, CO_MES;

CREATE OR REPLACE VIEW vw_monthly_timeseries_2025 AS
SELECT
	CO_ANO,
	CO_MES,
	MAKE_DATE(CO_ANO, CO_MES, 1) AS data_mes,
	SUM(VL_FOB) AS fob_mes,
	SUM(KG_LIQUIDO) AS kg_mes
FROM exportacoes_2025
GROUP BY CO_ANO, CO_MES;

-- Views Variação Ano-a-Ano Mensal
CREATE OR REPLACE VIEW vw_monthly_yoy_2023 AS
SELECT
	cur.CO_ANO,
	cur.CO_MES,
	cur.FOB_MES,
	prev.FOB_MES AS fob_mes_ano_anterior,
	(cur.FOB_MES - prev.FOB_MES) AS delta_fob,
	CASE
		WHEN prev.FOB_MES = 0 THEN NULL
		ELSE ROUND((cur.FOB_MES - prev.FOB_MES) * 100.0 / prev.FOB_MES, 2)
	END AS pct_yoy
FROM
	(SELECT CO_ANO, CO_MES, SUM(VL_FOB) AS fob_mes
	FROM exportacoes_2023
	GROUP BY CO_ANO, CO_MES) cur
LEFT JOIN
	(SELECT CO_ANO, CO_MES, SUM(VL_FOB) AS fob_mes
	FROM exportacoes_2023
	GROUP BY CO_ANO, CO_MES) prev
	ON prev.CO_ANO = cur.CO_ANO - 1
	AND prev.CO_MES = cur.CO_MES;

CREATE OR REPLACE VIEW vw_monthly_yoy_2024 AS
SELECT
	cur.CO_ANO,
	cur.CO_MES,
	cur.FOB_MES,
	prev.FOB_MES AS fob_mes_ano_anterior,
	(cur.FOB_MES - prev.FOB_MES) AS delta_fob,
	CASE
		WHEN prev.FOB_MES = 0 THEN NULL
		ELSE ROUND((cur.FOB_MES - prev.FOB_MES) * 100.0 / prev.FOB_MES, 2)
	END AS pct_yoy
FROM
	(SELECT CO_ANO, CO_MES, SUM(VL_FOB) AS fob_mes
	FROM exportacoes_2024
	GROUP BY CO_ANO, CO_MES) cur
LEFT JOIN
	(SELECT CO_ANO, CO_MES, SUM(VL_FOB) AS fob_mes
	FROM exportacoes_2024
	GROUP BY CO_ANO, CO_MES) prev
	ON prev.CO_ANO = cur.CO_ANO - 1
	AND prev.CO_MES = cur.CO_MES;

CREATE OR REPLACE VIEW vw_monthly_yoy_2025 AS
SELECT
	cur.CO_ANO,
	cur.CO_MES,
	cur.FOB_MES,
	prev.FOB_MES AS fob_mes_ano_anterior,
	(cur.FOB_MES - prev.FOB_MES) AS delta_fob,
	CASE
		WHEN prev.FOB_MES = 0 THEN NULL
		ELSE ROUND((cur.FOB_MES - prev.FOB_MES) * 100.0 / prev.FOB_MES, 2)
	END AS pct_yoy
FROM
	(SELECT CO_ANO, CO_MES, SUM(VL_FOB) AS fob_mes
	FROM exportacoes_2025
	GROUP BY CO_ANO, CO_MES) cur
LEFT JOIN
	(SELECT CO_ANO, CO_MES, SUM(VL_FOB) AS fob_mes
	FROM exportacoes_2025
	GROUP BY CO_ANO, CO_MES) prev
	ON prev.CO_ANO = cur.CO_ANO - 1
	AND prev.CO_MES = cur.CO_MES;

-- Views Sazonalidade
CREATE OR REPLACE VIEW vw_seasonality_heatmap_2023 AS
SELECT
	CO_MES,
	CO_ANO,
	SUM(VL_FOB) AS fob_total
FROM exportacoes_2023
GROUP BY CO_MES, CO_ANO;

CREATE OR REPLACE VIEW vw_seasonality_heatmap_2024 AS
SELECT
	CO_MES,
	CO_ANO,
	SUM(VL_FOB) AS fob_total
FROM exportacoes_2024
GROUP BY CO_MES, CO_ANO;

CREATE OR REPLACE VIEW vw_seasonality_heatmap_2025 AS
SELECT
	CO_MES,
	CO_ANO,
	SUM(VL_FOB) AS fob_total
FROM exportacoes_2025
GROUP BY CO_MES, CO_ANO;

-- Views Acumulado de Ano-Corrente
CREATE OR REPLACE VIEW vw_ytd_export_2023 AS
SELECT
	CO_ANO,
	CO_MES,
	SUM(SUM(VL_FOB)) OVER (
		PARTITION BY CO_ANO
		ORDER BY CO_MES
		ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
	) AS fob_ytd,
	SUM(SUM(KG_LIQUIDO)) OVER (
		PARTITION BY CO_ANO
		ORDER BY CO_MES
		ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
	) AS kg_ytd
FROM exportacoes_2023
GROUP BY CO_ANO, CO_MES;

CREATE OR REPLACE VIEW vw_ytd_export_2024 AS
SELECT
	CO_ANO,
	CO_MES,
	SUM(SUM(VL_FOB)) OVER (
		PARTITION BY CO_ANO
		ORDER BY CO_MES
		ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
	) AS fob_ytd,
	SUM(SUM(KG_LIQUIDO)) OVER (
		PARTITION BY CO_ANO
		ORDER BY CO_MES
		ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
	) AS kg_ytd
FROM exportacoes_2024
GROUP BY CO_ANO, CO_MES;

CREATE OR REPLACE VIEW vw_ytd_export_2025 AS
SELECT
	CO_ANO,
	CO_MES,
	SUM(SUM(VL_FOB)) OVER (
		PARTITION BY CO_ANO
		ORDER BY CO_MES
		ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
	) AS fob_ytd,
	SUM(SUM(KG_LIQUIDO)) OVER (
		PARTITION BY CO_ANO
		ORDER BY CO_MES
		ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
	) AS kg_ytd
FROM exportacoes_2025
GROUP BY CO_ANO, CO_MES;

-- Views Exportação por Destino
CREATE OR REPLACE VIEW vw_export_by_country_2023 AS
SELECT
	CO_PAIS,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg
FROM exportacoes_2023
GROUP BY CO_PAIS;

CREATE OR REPLACE VIEW vw_export_by_country_2024 AS
SELECT
	CO_PAIS,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg
FROM exportacoes_2024
GROUP BY CO_PAIS;

CREATE OR REPLACE VIEW vw_export_by_country_2025 AS
SELECT
	CO_PAIS,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg
FROM exportacoes_2025
GROUP BY CO_PAIS;

-- Views Fluxo Origem -> Destino
CREATE OR REPLACE VIEW vw_origin_destination_flow_2023 AS
SELECT
	SG_UF_NCM AS uf_origem,
	CO_PAIS AS pais_destino,
	SUM(VL_FOB) AS fob_fluxo,
	SUM(KG_LIQUIDO) AS kg_fluxo
FROM exportacoes_2023
GROUP BY SG_UF_NCM, CO_PAIS;

CREATE OR REPLACE VIEW vw_origin_destination_flow_2024 AS
SELECT
	SG_UF_NCM AS uf_origem,
	CO_PAIS AS pais_destino,
	SUM(VL_FOB) AS fob_fluxo,
	SUM(KG_LIQUIDO) AS kg_fluxo
FROM exportacoes_2024
GROUP BY SG_UF_NCM, CO_PAIS;

CREATE OR REPLACE VIEW vw_origin_destination_flow_2025 AS
SELECT
	SG_UF_NCM AS uf_origem,
	CO_PAIS AS pais_destino,
	SUM(VL_FOB) AS fob_fluxo,
	SUM(KG_LIQUIDO) AS kg_fluxo
FROM exportacoes_2025
GROUP BY SG_UF_NCM, CO_PAIS;

-- Views Participação por Modal
CREATE OR REPLACE VIEW vw_transport_mode_2023 AS
SELECT
	CO_VIA,
	CASE CO_VIA
		WHEN '1' THEN 'Marítima'
		WHEN '2' THEN 'Rodoviária'
		WHEN '3' THEN 'Fluial'
		WHEN '4' THEN 'Aérea'
		ELSE 'Outros'
	END AS modalidade,
	SUM(VL_FOB) AS fob_modal,
	SUM(KG_LIQUIDO) AS kg_modal
FROM exportacoes_2023
GROUP BY CO_VIA;

CREATE OR REPLACE VIEW vw_transport_mode_2024 AS
SELECT
	CO_VIA,
	CASE CO_VIA
		WHEN '1' THEN 'Marítima'
		WHEN '2' THEN 'Rodoviária'
		WHEN '3' THEN 'Fluial'
		WHEN '4' THEN 'Aérea'
		ELSE 'Outros'
	END AS modalidade,
	SUM(VL_FOB) AS fob_modal,
	SUM(KG_LIQUIDO) AS kg_modal
FROM exportacoes_2024
GROUP BY CO_VIA;

CREATE OR REPLACE VIEW vw_transport_mode_2025 AS
SELECT
	CO_VIA,
	CASE CO_VIA
		WHEN '1' THEN 'Marítima'
		WHEN '2' THEN 'Rodoviária'
		WHEN '3' THEN 'Fluial'
		WHEN '4' THEN 'Aérea'
		ELSE 'Outros'
	END AS modalidade,
	SUM(VL_FOB) AS fob_modal,
	SUM(KG_LIQUIDO) AS kg_modal
FROM exportacoes_2025
GROUP BY CO_VIA;

-- Views Ranking URF
CREATE OR REPLACE VIEW vw_urf_summary_2023 AS
SELECT
	CO_URF,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg,
	COUNT(DISTINCT CO_ANO)*12 + COUNT(DISTINCT CO_MES) AS freq_registros
FROM exportacoes_2023
GROUP BY CO_URF;

CREATE OR REPLACE VIEW vw_urf_summary_2024 AS
SELECT
	CO_URF,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg,
	COUNT(DISTINCT CO_ANO)*12 + COUNT(DISTINCT CO_MES) AS freq_registros
FROM exportacoes_2024
GROUP BY CO_URF;

CREATE OR REPLACE VIEW vw_urf_summary_2025 AS
SELECT
	CO_URF,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg,
	COUNT(DISTINCT CO_ANO)*12 + COUNT(DISTINCT CO_MES) AS freq_registros
FROM exportacoes_2025
GROUP BY CO_URF;

-- Views Ranking por UF de Origem
CREATE OR REPLACE VIEW vw_uf_origin_summary_2023 AS
SELECT
	SG_UF_NCM AS uf_origem,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg
FROM exportacoes_2023
GROUP BY SG_UF_NCM;

CREATE OR REPLACE VIEW vw_uf_origin_summary_2024 AS
SELECT
	SG_UF_NCM AS uf_origem,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg
FROM exportacoes_2024
GROUP BY SG_UF_NCM;

CREATE OR REPLACE VIEW vw_uf_origin_summary_2025 AS
SELECT
	SG_UF_NCM AS uf_origem,
	SUM(VL_FOB) AS total_fob,
	SUM(KG_LIQUIDO) AS total_kg
FROM exportacoes_2025
GROUP BY SG_UF_NCM;

-- Views Detalhadas para Drill_through
CREATE OR REPLACE VIEW vw_export_detail_2023 AS
SELECT
	CO_ANO,
	CO_MES,
	SG_UF_NCM AS uf_origem,
	CO_PAIS AS pais_destino,
	CO_NCM AS produto_ncm,
	QT_ESTAT AS qtd_estat,
	KG_LIQUIDO AS kg_liq,
	VL_FOB AS fob,
	CO_VIA,
	CO_URF
FROM exportacoes_2023;

CREATE OR REPLACE VIEW vw_export_detail_2024 AS
SELECT
	CO_ANO,
	CO_MES,
	SG_UF_NCM AS uf_origem,
	CO_PAIS AS pais_destino,
	CO_NCM AS produto_ncm,
	QT_ESTAT AS qtd_estat,
	KG_LIQUIDO AS kg_liq,
	VL_FOB AS fob,
	CO_VIA,
	CO_URF
FROM exportacoes_2024;

CREATE OR REPLACE VIEW vw_export_detail_2025 AS
SELECT
	CO_ANO,
	CO_MES,
	SG_UF_NCM AS uf_origem,
	CO_PAIS AS pais_destino,
	CO_NCM AS produto_ncm,
	QT_ESTAT AS qtd_estat,
	KG_LIQUIDO AS kg_liq,
	VL_FOB AS fob,
	CO_VIA,
	CO_URF
FROM exportacoes_2025;