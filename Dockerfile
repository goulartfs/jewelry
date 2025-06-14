# Imagem base
FROM python:3.8-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Define o comando de inicialização
CMD ["uvicorn", "src.joias.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 