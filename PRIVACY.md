# Política de Privacidade - IntegraEvidências

## Conformidade com LGPD

Este projeto foi desenvolvido seguindo as diretrizes da **Lei Geral de Proteção de Dados (LGPD)** brasileira.

## Dados Tratados

### Tipos de Dados
- **Dados de Configuração**: URLs, caminhos de diretórios, configurações de sistema
- **Logs de Sistema**: Registros de operações, timestamps, status de conexões
- **Arquivos de Evidência**: Documentos PDF e imagens processados pelo sistema

### Finalidade do Tratamento
- Geração automatizada de documentos de evidências
- Upload de arquivos para repositórios (Nexus)
- Integração com sistemas de documentação (Confluence)
- Logs para auditoria e troubleshooting

## Medidas de Segurança

### Proteção de Dados Sensíveis
- ✅ **Variáveis de Ambiente**: Credenciais armazenadas em arquivos `.env` (não versionados)
- ✅ **Configuração Segura**: Sistema de configuração centralizado
- ✅ **Gitignore**: Arquivos sensíveis excluídos do controle de versão
- ✅ **Logs Rotativos**: Logs mantidos apenas por 20 dias

### Dados Não Coletados
- ❌ Dados pessoais de usuários
- ❌ Informações biométricas
- ❌ Dados bancários ou financeiros
- ❌ Informações de localização

## Configuração Segura

### Arquivo .env (Obrigatório)
```bash
# Copie .env.example para .env e configure:
NEXUS_URL=sua_url_nexus
NEXUS_USERNAME=seu_usuario
CONFLUENCE_TOKEN=seu_token
# ... outras configurações
```

### Responsabilidades do Usuário
- Manter credenciais seguras no arquivo `.env`
- Não compartilhar tokens ou senhas
- Configurar acessos com menor privilégio necessário
- Revisar logs periodicamente

## Retenção de Dados

### Logs do Sistema
- **Período**: 20 dias (rotatividade automática)
- **Localização**: Pasta `logs/` (local)
- **Limpeza**: Automática na inicialização

### Arquivos Processados
- **Responsabilidade**: Do usuário final
- **Localização**: Diretórios configurados pelo usuário
- **Retenção**: Conforme política da organização

## Direitos dos Titulares

Conforme LGPD, os usuários têm direito a:
- **Acesso**: Visualizar dados tratados
- **Correção**: Corrigir dados incorretos
- **Exclusão**: Remover dados quando aplicável
- **Portabilidade**: Exportar dados em formato legível

## Contato

Para questões sobre privacidade e proteção de dados:

**Desenvolvedor**: Alessandro Luiz Mariano da Silva Melo  
**E-mail**: 1986.alessandro@gmail.com

## Atualizações

Esta política pode ser atualizada conforme necessário para manter conformidade com a LGPD e melhores práticas de segurança.

**Última atualização**: 30/09/2025