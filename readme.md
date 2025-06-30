# Passo 1:
Rodar Comandos de configuração de rede externa, para conexão com API gateway Nginx.
```bash
docker swarm init
docker network create --driver overlay --attachable nutridashboard-rede
```

# Passo 2
Criar o container e inicializa-lo
```bash
docker compose build
docker compose up -d
```