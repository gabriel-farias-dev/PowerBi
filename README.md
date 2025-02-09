# Repositório de Análises Power BI com Bases Aleatórias
Este repositório contém análises de dados desenvolvidas em Power BI, juntamente com bases de dados geradas aleatoriamente, evitando a exposição de informações sensíveis. As bases são criadas via scripts em Python ou geradas por meio de banco de dados simulado, permitindo a visualização dos relatórios de forma segura e preservando a confidencialidade dos dados originais.

## Índice
- [Análise de Cubagem Logística](#Análise-de-Cubagem-Logística)
  - [Descrição](#Descrição)
  - [Importância](#Importância)
  - [Sobre o DashBoard](#Sobre-o-DashBoard)
- [Validade de Estoque](#Análise-de-Validade-de-Estoque)
  - [Descrição](#Descrição-1)
  - [Importância](#Importância-1)

## Análise de Cubagem Logística
### Descrição
A análise de cubagem foca no processo logístico de separar produtos em estoque para acomodação em caixas prontas para expedição. Este processo ocorre em horários estratégicos para otimizar a eficiência de envio e o uso de recursos no centro de distribuição.

### Importância
A definição dos horários de cubagem é essencial para maximizar a eficiência logística. Por exemplo, ao concentrar a cubagem de pedidos em horários específicos — principalmente após o término do recebimento de novos pedidos — é possível otimizar o agrupamento e envio dos produtos. Assim, ao invés de cubar cada pedido isoladamente ao longo do dia, a consolidação no final do período permite expedir todos os produtos simultaneamente. Essa prática contribui para reduzir o tempo de manuseio e melhora o fluxo de saída de mercadorias, impactando diretamente na produtividade e no tempo de processamento dos pedidos.

### Sobre o DashBoard
Considerando o processo de agrupamento de pedidos para otimizar a performance da cubagem, é fundamental ter uma visão clara do momento em que a cubagem é iniciada, em comparação com a meta de início estabelecida. Isso permite verificar se o plano está sendo seguido. O dashboard a seguir apresenta esses dados de forma fictícia, incluindo a porcentagem de cubagens realizadas dentro e fora do horário planejado, organizados de acordo com os Centros de Distribuição e as rotas de expedição.

[![Gestão de cubagem](https://github.com/user-attachments/assets/8209745a-9fe4-46d5-9957-ea60f3768ea7)](https://app.powerbi.com/view?r=eyJrIjoiYzdmZjMyYTktYTU0YS00YjgzLWE2ODgtOWUzZGJmOWE3ZDc2IiwidCI6ImQ2ZTVmZTFhLTQ5YWYtNDNjNS1iMzAyLTE5MTJjODY1NzgzYyJ9)

## Análise de Validade de Estoque
### Descrição
Conhecer a validade dos produtos em estoque é fundamental para determinar a quantidade de produtos vendáveis e gerenciar as ofertas da empresa, especialmente quando a validade está próxima de expirar. Isso permite a venda de produtos antes que se tornem inviáveis para comercialização. As bases deste relatório foram criadas em Python e armazenadas em um banco de dados, permitindo a simulação de consultas (queries) dentro do sistema.

### Importância
A visão da validade do estoque é importante por diversos motivos. No caso de produtos não perecíveis, cuja validade pode durar anos, existem regulamentações que restringem a comercialização a preço cheio quando a validade se aproxima de um limite crítico (por exemplo, 4 meses). Isso obriga a empresa a realizar promoções para evitar grandes prejuízos ao liquidar o estoque. Este relatório auxilia justamente na gestão desses casos relacionados à validade.

[![Validade](https://github.com/user-attachments/assets/e78e2e04-5ed4-4fc2-9466-4a47ede80666)](https://app.powerbi.com/view?r=eyJrIjoiY2ZmNTNlNzAtOTNhMS00YWFkLTk3NTMtZWZmZmUxOWY0N2QyIiwidCI6ImQ2ZTVmZTFhLTQ5YWYtNDNjNS1iMzAyLTE5MTJjODY1NzgzYyJ9)

## Análise de Absenteismo
### Descrição e importãncia
O absenteísmo é um fator crítico a ser monitorado dentro de um centro de distribuição (CD) ou filial. A ausência pontual de um colaborador pode não impactar significativamente as operações da empresa, porém, em um cenário onde uma filial com 50 funcionários registra a falta de 10 pessoas em um único dia, isso representa 20% da equipe ausente, comprometendo diretamente a execução das atividades e a produtividade do local.

Por isso, é fundamental acompanhar tanto a porcentagem de absenteísmo quanto o número de recorrências das faltas. Essa análise possibilita a tomada de decisões estratégicas em relação aos colaboradores com altos índices de ausência, como a realização de um feedback, a aplicação de advertências e, em casos extremos, o desligamento.

Este relatório foi elaborado com dados totalmente aleatórios, incluindo nome do colaborador, gestor, departamento, motivo da ausência e registros de falta. Para garantir uma simulação realista, foi aplicada uma regra de probabilidade, onde cada funcionário tem 10% de chance de ausência em cada dia analisado. O relatório apresenta diferentes perspectivas sobre o absenteísmo na empresa, oferecendo desde análises simples até abordagens mais detalhadas, permitindo uma visão abrangente do impacto das ausências no desempenho organizacional.
[![Absenteísmo](https://app.powerbi.com/view?r=eyJrIjoiNTViYTIyYWEtNWVlZS00NDAwLWI3ZGEtNTIwYjFlZDZjOGI3IiwidCI6ImQ2ZTVmZTFhLTQ5YWYtNDNjNS1iMzAyLTE5MTJjODY1NzgzYyJ9)](https://github.com/user-attachments/assets/e65302f7-c918-4476-ab33-1d89ec2cac6f)

