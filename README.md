# Tutorial Técnico: Mini Text Service

## 1. Objetivo
Este projeto apresenta uma solução de classificação textual simples, empacotada de forma reprodutível utilizando Docker, voltada para a triagem de mensagens em categorias como perguntas, relatos ou reclamações.


## 2. Como Instalar e Executar
Para garantir que o projeto funcione em qualquer ambiente, utilizamos Docker.

   1. Construir a imagem:
    Use: docker build -t mini-text-service .
   2. Iniciar o Serviço
    docker run -p 8000:8000 mini-text-service
   - O serviço da api estará disponivél em http://localhost:8000/docs#/default/health_health_get 

## 3. Como Testar

Após iniciar o container, você pode validar o funcionamento de três formas:
*A.* Teste de Saúde (Health Check)
Verifique se o serviço está online acessando no navegador ou via terminal:

- URL: http://localhost:8000/health 
- Comando: curl http://localhost:8000/health

{
"text": "Por que meu acesso foi negado?",
"strategy": "rules"
}