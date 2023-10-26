# TCC - Interface RSPAPER usando QT6

Este repositório faz parte do trabalho de conclusão de curso da Universidade Federal Fluminense, no curso de Ciências da Computação. O objetivo desse projeto é criar uma interface para o software RSPAPER, utilizando o framework QT6.

## Como Rodar

Para executar a interface, siga os passos abaixo:

1. Clone o repositório na sua máquina local:

```bash
git clone https://github.com/luandiasrj/TCC-RSPAPER-QT6.git
```

2. Entre na pasta do projeto:

```bash
cd TCC-RSPAPER-QT6
```

3. Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

4. Execute o arquivo `main.py`:

```bash
python main.py
```

## To-Do

- [x] Estilização: CSS da tela principal
- [x] Estilização: CSS da tela de filtros
- [x] Estilização: CSS da tela de pesquisa avançada
- [x] Estilização: CSS da tela de abstract
- [x] Estilização: CSS das caixas de diálogo
- [x] Estilização: CSS dark mode
- [x] Implementação: resize automático da janela
- [x] Implementação: toggle para habilitar modo escuro
- [x] Implementação: abrir tela "Definir Filtros ao clicar no botão "Novo Projeto"
- [x] Implementação: abrir tela "Pesquisa Avançada" ao clicar no link pesquisa avançada dentro da tela de filtros
- [x] Implementação: consumir os artigos do CVS de exemplo na tela "Seleção de Artigos"
- [x] Implementação: paginação utilizando os artigos do csv de exemplo
- [x] Implementação: abrir tela "Abstract" ao clicar no título de um artigo
- [x] Implementação: abrir diálogo de confirmação ao clicar em "Marcar" na tela "Abstract" após clicar no título de um artigo
- [x] Implementação: abrir diálogo de confirmação ao clicar em "Descartar" na tela "Abstract" após clicar no título de um artigo
- [x] Implementação: ordenação de artigos por relevância
- [x] Implementação: vetor artigo de interesse (models)
- [x] Implementação: vetores artigos descartados (models)
- [x] Implementação: Funcionalidade botões marcar/desmarcar
- [x] Implementação: Restringir quantidade de artigos por página
- [x] Implementação: Barra de progresso nas ações abrir/novo projeto
- [x] Bug: Tratamento para adicionar na lista de descartado e remover da de interesse (vice-versa)
- [x] Bug: Tratamento para adicionar na lista de descartado/interesse somente se não existir
- [ ] Escrita: finalização da parte teórica

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Feito com ❤️ por [luandiasrj](https://github.com/luandiasrj) e [amiquilini](https://github.com/amiquilini)
