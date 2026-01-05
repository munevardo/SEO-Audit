FROM python:3.9-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# 1. Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget gnupg openjdk-17-jre-headless \
    libfontconfig1 libxrender1 libxtst6 libxi6 libgl1 libasound2 \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar Screaming Frog 23.2
RUN wget https://download.screamingfrog.co.uk/products/seo-spider/screamingfrogseospider_23.2_all.deb \
    && apt-get update \
    && apt-get install -y ./screamingfrogseospider_23.2_all.deb || apt-get install -f -y \
    && rm screamingfrogseospider_23.2_all.deb

# 3. SOLUCIÓN AL ERROR "Is a directory"
# Eliminamos la carpeta conflictiva y creamos un archivo vacío con el mismo nombre
RUN rm -rf /root/.screamingfrogseospider && touch /root/.screamingfrogseospider

# 4. Configurar Licencia y EULA (Ruta con Mayúsculas para v23.2)
RUN mkdir -p /root/.ScreamingFrogSEOSpider && \
    printf "seowppmedia1\n59936B7FE9-1796860800-E9D5315C23" > /root/.ScreamingFrogSEOSpider/licence.txt && \
    echo "eula.accepted=15" > /root/.ScreamingFrogSEOSpider/spider.config

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/outputs && chmod 777 /app/outputs

EXPOSE 5000
CMD ["python", "app.py"]