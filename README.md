# Plataforma TechParaTodos

Este projeto é uma plataforma educacional desenvolvida em Python com interface gráfica usando CustomTkinter. Ela foi criada como parte do Projeto Integrado Multidisciplinar (PIM I) do curso de Análise e Desenvolvimento de Sistemas (ADS) — 1º semestre.

Seu objetivo é promover a inclusão digital, oferecendo uma interface simples para cadastro de usuários, acesso a conteúdos educacionais em vídeo e geração de relatórios estatísticos com base nos dados dos usuários.

## 📌 Funcionalidades

- Tela de login e cadastro de usuários
- Validação de campos e e-mail
- Armazenamento dos dados em arquivo local JSON
- Acesso a conteúdos educacionais (vídeos sobre lógica, Python e segurança da informação)
- Relatório com estatísticas (média, mediana, moda das idades e proporção de sexo)
- Visualização de imagens por URL
- Interface amigável e acessível

## 🔧 Tecnologias utilizadas

- Python 3
- CustomTkinter
- Pillow (PIL)
- Requests e urllib (para imagens via internet)
- JSON (persistência dos dados)
- Statistics (análise estatística)
- Regex (validação de e-mail)
- Webbrowser (para abrir vídeos)

## 🧠 Conteúdo Educacional Integrado

- Lógica de Programação – Curso em vídeo (YouTube)
- Introdução ao Python – Curso gratuito (YouTube)
- Segurança da Informação – Playlist completa

Todos os vídeos são gratuitos e voltados ao público iniciante.

## 🛠️ Como executar

1. Instale as dependências:

   ```bash
   pip install customtkinter pillow requests

2. Execute o arquivo principal
   `python pim.py`

Um arquivo `usuarios.json` será criado automaticamente para armazenar os dados dos usuários.  
**Observação:** Para acessar a função de relatório, cadastre um usuário com e-mail contendo "@admin" (ex: joao@admin.com).

## 📊 Relatório de Usuários
Disponível apenas para administradores. Exibe:
- Total de usuários
- Média, moda e mediana das idades
- Porcentagem de homens e mulheres cadastrados
- Com opção de salvar como `relatorio.json`.

## 🔒 Segurança e LGPD
- Dados armazenados localmente
- Não são exibidas senhas na interface
- Dados sensíveis não são incluídos no relatório exportado
- O sistema segue boas práticas de privacidade e segurança da informação para fins educacionais

## 📸 Prints
Imagens da interface e funcionamento estão disponíveis no diretório `/prints` 

## 👥 Equipe  
- F3620J8 – ANDERSON RAULINO DA SILVA
- R427FB0 – FREDSON SILVA DOS SANTOS
- R603CJ7 – FERNANDA CRISTINA DA SILVA
- R512ED7 – MARIA EDUARDA RODRIGUES ROMÃO
- R658384 – PEDRO LEONILDO DA SILVA TEIXEIRA


## 📚 Licença
Este projeto foi desenvolvido para fins educacionais no curso de Análise e Desenvolvimento de Sistemas (ADS) – Universidade Paulista (UNIP).
