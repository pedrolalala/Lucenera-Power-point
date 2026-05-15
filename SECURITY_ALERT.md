# 🚨 ALERTA DE SEGURANÇA CRÍTICA

## ⚠️ CREDENCIAIS EXPOSTAS NO GITHUB

**DATA**: Maio 2026  
**SEVERIDADE**: CRÍTICA 🔴  
**STATUS**: AÇÃO NECESSÁRIA IMEDIATA

---

## 📋 PROBLEMA

As seguintes credenciais foram **expostas publicamente** no repositório GitHub:

```
Client ID: 39ef469c-7496-40cb-ac08-ba01b514cf2d
Client Secret: [REDACTED_SECRET]
Tenant ID: b68c427b-b3f8-4bba-9252-66b24ce29c9d
```

**RISCO**: Qualquer pessoa pode acessar seu SharePoint usando estas credenciais!

---

## ✅ AÇÕES NECESSÁRIAS (FAZER AGORA!)

### 1. REVOGAR CLIENT SECRET (URGENTE!)

#### Passo a Passo:

1. **Acessar Azure Portal**
   - URL: https://portal.azure.com
   - Login com conta do tenant Lucenera

2. **Navegar para App Registration**
   - Azure Active Directory (ou Microsoft Entra ID)
   - App registrations
   - Procurar aplicação: `Lucenera PowerPoint` ou ID `39ef469c-7496-40cb-ac08-ba01b514cf2d`

3. **Deletar Secret Antigo**
   - Clicar na aplicação
   - Menu lateral: "Certificates & secrets"
   - Aba: "Client secrets"
   - Localizar o secret que começa com `6vy8Q~...`
   - Clicar em "Delete" (lixeira) ❌
   - Confirmar exclusão

4. **Gerar Novo Secret**
   - Ainda em "Client secrets"
   - Clicar "New client secret"
   - Description: `Lucenera PowerPoint - Gerado em [DATA]`
   - Expires: Escolher validade (recomendado: 12 meses)
   - Clicar "Add"
   - **COPIAR O VALUE IMEDIATAMENTE** (não conseguirá ver depois!)

5. **Atualizar .env**
   ```powershell
   # Editar arquivo .env
   notepad .env
   
   # Substituir linha:
   # DE:  SHAREPOINT_CLIENT_SECRET=[REDACTED_SECRET]
   # PARA: SHAREPOINT_CLIENT_SECRET=[NOVO_SECRET_AQUI]
   ```

6. **Salvar .env** (Ctrl+S no Notepad)

---

### 2. LIMPAR HISTÓRICO DO GIT (Opcional mas Recomendado)

As credenciais antigas estão no histórico do Git. Para removê-las:

#### Opção A: BFG Repo-Cleaner (Recomendado)

```bash
# 1. Baixar BFG
# https://rtyley.github.io/bfg-repo-cleaner/

# 2. Criar arquivo com credenciais a remover
echo "[REDACTED_SECRET]" > secrets.txt

# 3. Limpar histórico
java -jar bfg.jar --replace-text secrets.txt

# 4. Forçar limpeza
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 5. Forçar push
git push --force --all
```

#### Opção B: Git Filter-Branch

```bash
# AVISO: Isso reescreve TODO o histórico!
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Forçar push
git push --force --all
```

---

### 3. VERIFICAR SEGURANÇA

#### Checklist Final:

- [ ] Secret antigo revogado no Azure Portal
- [ ] Novo secret gerado
- [ ] Arquivo `.env` atualizado com novo secret
- [ ] Arquivo `.env` está no `.gitignore`
- [ ] Testou conexão SharePoint com novo secret:
  ```powershell
  python start_production.py
  # Verificar se conecta ao SharePoint sem erro 401/403
  ```
- [ ] (Opcional) Histórico do Git limpo

---

## 🔒 BOAS PRÁTICAS PARA O FUTURO

### 1. NUNCA Commitar Credenciais

✅ **CERTO:**
```python
# Usar variáveis de ambiente
from dotenv import load_dotenv
import os

load_dotenv()
client_secret = os.getenv('SHAREPOINT_CLIENT_SECRET')
```

❌ **ERRADO:**
```python
# Hardcoded no código
client_secret = "[REDACTED_SECRET]"
```

### 2. Usar .gitignore

Arquivo `.gitignore` deve conter:
```
.env
*.secret
*.key
*.pem
credentials.json
```

### 3. Rotacionar Secrets Regularmente

- Gerar novo secret a cada 3-6 meses
- Documentar data de criação
- Revogar secrets antigos

### 4. Usar Managed Identity (Recomendado para Azure)

Se hospedar no Azure, usar **Managed Identity** ao invés de secrets:
- Não precisa armazenar credenciais
- Azure gerencia automaticamente
- Mais seguro

---

## 📞 SUPORTE

Se tiver dúvidas sobre o processo de revogação:

1. **Documentação Microsoft**
   - https://learn.microsoft.com/azure/active-directory/develop/quickstart-register-app

2. **Suporte Azure**
   - Portal Azure → Help + Support

3. **Urgência?**
   - Se houver atividade suspeita, **desabilitar a aplicação inteira** temporariamente:
   - Azure Portal → App Registrations → Sua App → Disable

---

## ✅ CONFIRMAÇÃO

Após completar as ações acima, marque aqui:

- [ ] Secret revogado
- [ ] Novo secret gerado e configurado
- [ ] Sistema testado e funcionando
- [ ] Equipe notificada
- [ ] Documentação atualizada

**Data de resolução**: _____________________

**Responsável**: _____________________

---

**IMPORTANTE**: Trate este incidente como aprendizado. Erros acontecem, o importante é corrigi-los rapidamente e aprender com eles! 💪
