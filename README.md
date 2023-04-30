# API de Hotel

Esta API foi feita seguindo orientações de um teste para uma vaga de desenvolder na empresa Hurst Capital.

## Este projeto foi feito com:

* [Python 3.10.4](https://www.python.org/)
* [Fastapi 0.95.1](https://fastapi.tiangolo.com/)
* [MongoDB 6.0.5](https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-6.0.5-signed.msi)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Instale o MongoDB local.
* Inicie o MongoDB com as configurações padrões.
* Inicie a API.

```
git clone https://github.com/Rodrigo-Rodrigues-Silva/G-TBP-01-2023.git
cd G-TBP-01-2023
python -m venv .venv

# Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app
```

## Como ver a documentação?

A documentação técnica é gerada automaticamente pelo Swagger. Após iniciada a API, acesse: http://127.0.0.1:8000/docs#/
.

## Como rodar os testes:

```
uvicorn main:app

python -m pytest
```