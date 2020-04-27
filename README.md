#FLASK-TEMPLATE

Esse template serve para inicializar uma API rapidamente em Python.
Nele há uma pasta chamada sqlalchemy (e futuramente outras pastas). Cada pasta é uma aplicação diferente e pode ser "rodada" independentemente, sendo selecionada a melhor pasta para o projeto em questão.
Para flexibilidade, usamos o sqlalchemy (que é um ORM). Para simplicidade/performance, usamos psycopg2 (que é o driver para postgresql)

#Como iniciar?
Há algumas formas de iniciar o projeto.
- A mais simples é docker-compose.yaml! Basta navegar para a pasta flask-template e executar o comando "docker-compose up". Isso irá construir uma imagem docker e rodar ela! Para um rápido teste, acesse a url "localhost:8085". Use "docker-compose stop" para pausar (ou aperte Ctrl+C que ele pausa automaticamente);

- Também é possível rodar sem o docker! Para tal, primeiro navegue para a pasta desejada ("cd sqlalchemy", por exemplo) crie um ambiente chamado .env ("python -m venv .env"), ative o ambiente (no cmd é ".env\Scripts\activate"). Agora podemos instalar as dependências com "pip install -r requirements.txt. Se tudo ocorrer bem, rode a aplicação com o comando "python application.py".

Comandos úteis:
    Para docker:
        - docker image prune -a (deleta todas as imagens não usadas ou "dangling")
        - docker images (lista as imagens)
        - docker container ls -a (mostra TODOS os containers)
        - docker stop my_container (para o container my_container)