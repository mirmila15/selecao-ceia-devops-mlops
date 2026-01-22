# Tutorial Técnico: Mini Text Service

## 1. Objetivo
Este projeto apresenta uma solução de classificação textual simples, empacotada de forma reprodutível utilizando Docker, voltada para a triagem de mensagens em categorias como perguntas, relatos ou reclamações.


## 2. Como Instalar e Executar
Para garantir que o projeto funcione em qualquer ambiente, utilizamos Docker.

   1. Construir a imagem:
    Use: docker build -t mini-text-service .
   2. Iniciar o Serviço
    docker run -p 8000:8000 mini-text-service
   

## 3. Como Testar

Após iniciar o container, você pode validar o funcionamento de três formas:
*A.* Teste de Saúde (Health Check)
Verifique se o serviço está online acessando no navegador ou via terminal:

- URL: http://localhost:8000/health 
- Comando: curl http://localhost:8000/health
- O serviço da api estará disponivél em http://localhost:8000/docs#/default/health_health_get 
- Selecione o endpoint POST /classify e clique em Try it out.
- Utilize o JSON de exemplo abaixo para validar a classificação:
    *{*
      *"text": "O sistema apresenta erro ao salvar minha petição",*
      *"strategy": "rules"*
     *}*

## 5. Decisões de DevOps/MLOps e Arquitetura

Simplicidade e Elegância: Optou-se por uma arquitetura enxuta, sem frameworks altamente opinativos, facilitando a manutenção e o entendimento do fluxo de dados.

Monitoramento e Observabilidade: Implementação de logs via logging para auditoria de predições e um endpoint de /health para verificação de integridade do serviço.

Rastreabilidade: Adição do campo model_version na resposta da API, garantindo que cada classificação possa ser rastreada até uma versão específica da lógica de negócio.

## 6. Limitações e Evoluções Futuras

Limitação Atual: A classificação utiliza heurísticas baseadas em regras (estratégia rules).


Evolução MLOps: Implementação de uma esteira de CI/CD para retreinamento automático de modelos de linguagem (LLMs) conforme a mudança no vocabulário jurídico.



Escalabilidade: Orquestração via Kubernetes para suportar múltiplos containers em períodos de alta demanda processual.

