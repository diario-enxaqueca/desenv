# Configuração de Email para Recuperação de Senha

## Problema de Timeout SMTP

O erro `SMTPConnectTimeoutError: Timed out connecting to smtp.gmail.com on port 587` ocorre por várias razões em ambientes cloud/containerizados:

### Causas Principais:

1. **Bloqueio de rede em Azure Container Apps**: Alguns serviços Azure bloqueiam portas SMTP por padrão
2. **Credenciais incorretas**: Gmail requer "Senha de App" em vez de senha normal
3. **Timeout muito curto**: Conexões em cloud podem levar mais tempo
4. **Firewall/regras de rede**: Regras de segurança podem bloquear tráfego SMTP

---

## Soluções Implementadas

### 1. Timeout Aumentado
```python
conf = ConnectionConfig(
    # ... outras configurações
    TIMEOUT=120,  # 120 segundos em vez do padrão (10s)
)
```

### 2. URL dinâmica do frontend
Agora usa `settings.FRONTEND_URL` em vez de `http://localhost:3000` hardcoded.

### 3. Tratamento de erro robusto
Email é enviado em background task com logging de erros.

---

## Configuração do Gmail (RECOMENDADA)

### Passo 1: Ativar autenticação de 2 fatores
1. Acesse https://myaccount.google.com/security
2. Ative "Verificação em duas etapas"

### Passo 2: Gerar Senha de App
1. Acesse https://myaccount.google.com/apppasswords
2. Selecione "Email" e "Outro (nome personalizado)"
3. Digite "Diário Enxaqueca" 
4. Copie a senha gerada (16 caracteres)

### Passo 3: Configurar variáveis de ambiente
```bash
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx  # Senha de App (16 dígitos)
MAIL_FROM=seu-email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

---

## Alternativa: Usar serviço SMTP em cloud

Se o Gmail continuar bloqueado no Azure, considere:

### Opção 1: SendGrid (Azure)
```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=sua-api-key-sendgrid
MAIL_FROM=seu-email-verificado
```

- **Vantagens**: 100 emails grátis/dia, integração nativa Azure
- **Setup**: https://portal.azure.com → SendGrid

### Opção 2: Mailgun
```bash
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@seu-dominio.mailgun.org
MAIL_PASSWORD=sua-senha-mailgun
```

- **Vantagens**: 5.000 emails grátis/mês
- **Setup**: https://www.mailgun.com/

### Opção 3: AWS SES (se migrar para AWS)
```bash
MAIL_SERVER=email-smtp.us-east-1.amazonaws.com
MAIL_PORT=587
MAIL_USERNAME=sua-access-key-id
MAIL_PASSWORD=sua-secret-access-key
```

---

## Verificar se está funcionando

### Teste local:
```bash
cd autenticacao
python -c "
import asyncio
from fastapi_mail import FastMail, MessageSchema
from config.settings import settings
from auth.view_auth import conf

async def test():
    message = MessageSchema(
        subject='Teste',
        recipients=['seu-email@exemplo.com'],
        body='Email de teste',
        subtype='plain'
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    print('✅ Email enviado com sucesso!')

asyncio.run(test())
"
```

### Verificar logs no Azure:
```bash
az containerapp logs show \
  --name autenticacao \
  --resource-group seu-resource-group \
  --follow
```

---

## Checklist de Debug

- [ ] Variáveis de ambiente configuradas corretamente
- [ ] Usando "Senha de App" do Gmail (não senha normal)
- [ ] Firewall/NSG no Azure permite saída na porta 587
- [ ] Container tem acesso à internet
- [ ] Timeout aumentado para 120s
- [ ] Logs mostram tentativa de conexão

---

## Notas Importantes

⚠️ **Gmail tem limites**: 500 emails/dia para contas gratuitas

⚠️ **Azure pode bloquear SMTP**: Considere usar serviço gerenciado (SendGrid/Mailgun)

⚠️ **Não commitar senhas**: Use Azure Key Vault ou variáveis de ambiente seguras

✅ **Best practice**: Em produção, sempre use serviço SMTP dedicado (SendGrid, SES, etc.)
