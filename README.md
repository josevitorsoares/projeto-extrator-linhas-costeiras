# 💡 SHOREXTRACTOR: Um Aplicativo Desktop Para Extração Automática De Linhas De Costa

Este projeto foi construído para apresentação do meu `Trabalho de Conclusão de Curso` e para outorga do título de `Tecnológo em Análise e Desenvolvimento de Sistemas`. O mesmo tem o objetivo realizar a construção de uma `ferramenta desktop` para `extração de linhas de costa de forma automática`, utilizando de `técnicas de processamento digital de imagens`, entre elas o filtro para detecção de bordas Canny, em imagens provenientes da utilização de sensoriamento remoto, com a intenção de detectar processos de erosão costeira.

<!-- # Tópicos -->

- [💡 SHOREXTRACTOR: Um Aplicativo Desktop Para Extração Automática De Linhas De Costa](#-shorextractor-um-aplicativo-desktop-para-extração-automática-de-linhas-de-costa)
  - [Status do Projeto](#status-do-projeto)
  - [Artigo Científico](#artigo-científico)
  - [Funcionalidades](#funcionalidades)
  - [Últimas Atualizações](#últimas-atualizações)
  - [Tecnologias Utilizadas](#tecnologias-utilizadas)

## Status do Projeto

Atualmente o projeto encontra-se com o status de `Concluído`, pois a apresentação deste Trabalho de Conclusão de Curso aconteceu no dia 21 de dezembro do ano de 2022.

Este projeto está como `Encerrado` por mim, mas ainda necessita de algumas melhorias e da adição da funcionalidade responsável por exportar a linha de costa gerada de forma automática no formato Shapefile, para uma melhor utilização nos Sistema de Informações Geográficas (SIGs).

## Artigo Científico

O artigo científico utilizado para apresentar esta aplicação encontra-se no arquivo `SHOREXTRACTOR: Um Aplicativo Desktop Para Extração Automática De Linhas De Costa.pdf`.

## Funcionalidades

- [x] Abrir/Importar imagem GeoTIFF dentro da aplicação.
- [x] Aplicar filtro de Binarização.
- [x] Aplicar filtro Gaussiano.
- [x] Aplicar filtro de Transformação Morfológica.
- [x] Exibir uma nova linha de costa, com base nos filtros aplicados a GeoTIFF inicial.
- [x] Exportar a linha de costa gerada automaticamente como uma nova GeoTIFF.

## Últimas Atualizações

- [x] Adicionar `checkbox` para filtro de binarização.
- [x] Criação de um [novo design de UI](https://www.figma.com/file/nJtpNbYZZpwegbp1ECO3lB/Interface-White-(UPDATE)?t=NaHfAyMjEXdRr4vT-1) com o Figma.
- [x] Geração da nova UI com a utilização da ferramenta [Tkinter Designer](https://github.com/ParthJadhav/Tkinter-Designer).
- [x] Alteração da Interface de Usuário.
- [x] Alteração do filtro detector de bordas Sobel para o filtro Canny.

## Tecnologias Utilizadas

- `Python`
- `Tkinter`
- `Figma`
- `Tkinter Designer`
