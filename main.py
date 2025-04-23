import streamlit as st
import requests
import pandas as pd


def obter_frequencia_nome(nome: str):
    URL = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'

    response = requests.get(URL)

    try:
        response.raise_for_status()
        # retornando um None para o caso de não encontrar resultado
        if not response.json():
            return None
        else:
            # retornando os valores caso encontre algum resultado
            frequencia_por_decada = response.json()[0].get('res')
            return frequencia_por_decada
    except requests.HTTPError as e:
        print(f'Erro na requisição : {e}')


def main():
    # header
    st.header(
        body='Web App Nomes',
        divider=True,
        help='Para utilizar este sistema, basta inserir o nome desejado.'
    )
    # texto
    st.markdown("Acesse o [site do IBGE](https:servicodados.ibge.gov.br/api/docs/nomes?versao=2) para mais informações.")
    # obtendo o nome a ser consultado
    nome = st.text_input('Consulte um nome')
    # parando o sistema caso não tenha nome a ser pesquisado
    if not nome:
        st.stop()
    resultados = obter_frequencia_nome(nome)
    # parando o sistema caso não existam resultados para o nome pesquisado
    if not resultados:
        st.error('Nome não encontrado!')
        st.stop()
    # carregando o dataframe
    df = pd.DataFrame(resultados)
    # ajustando o nome das colunas
    df.columns = ['Período', 'Frequência']
    # definindo duas colunas e sua proporção
    col1, col2 = st.columns([3, 7])
    # coluna um
    with col1:
        st.write('Frequência por década')
        st.dataframe(df, hide_index=True)
    # coluna dois
    with col2:
        st.write('Evolução no tempo')
        st.line_chart(data=df.set_index('Período'))


if __name__ == '__main__':
    main()
