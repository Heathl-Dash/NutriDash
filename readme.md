# Passo 1:
criar rede externa do nginx
essa rede deve ser criada antes de qualquer um dos serviços, pois os conecta ao nginx

```bash
docker network create gateway-shared-net
```

# Passo 2
Criar o container e inicializa-lo
```bash
docker compose build
docker compose up -d
```