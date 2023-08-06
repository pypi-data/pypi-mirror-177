# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brasilapy', 'brasilapy.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'brasilapy',
    'version': '1.2.2',
    'description': 'Brasil API Client for Python',
    'long_description': '![](./images/brasilapi-logo-small.png) <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="70" height="70" />\n\n# BrasilApy\nUm cliente da [Brasil  API](https://brasilapi.com.br/) em python3. Link do [repositório](https://github.com/BrasilAPI/BrasilAPI) oficial.\n\n[![codecov](https://codecov.io/gh/joepreludian/brasilapy/branch/master/graph/badge.svg?token=BKYR6XTW4N)](https://codecov.io/gh/joepreludian/brasilapy)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lipe14-ops_brasilapy&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=joepreludian_brasilapy)\n\nNesta versão `1.0.0` esse cliente possui suporte a autocomplete por meio de Typed Hints. Todos as respostas são traduzidas para objetos do Pydantic, que trazem previsibilidade ao explorar a API  através da sua IDE favorita.\n\n![](./images/autocomplete.png)\n\n## Instalação\nRode o comando `pip install brasilapy` e estará tudo pronto.\nA versão do python que é compativel com essa biblioteca é a `3.10+`.\n\n## Documentação\nDocumentação oficial da API com todas as chamadas poderão se encontradas [neste link](https://brasilapi.com.br/docs).\n\n### Código de exemplo\nPara efetuar as consultas na API, basta instanciar a classe e fazer as consultas.\n\n```py\nfrom brasilapy import BrasilAPI\n\nclient = BrasilAPI()\nestado = client.get_ibge_estado(state_uf="pb")\n\nprint(estado.id)\nprint(estado.regiao)\nprint(estado.sigla)\n\n###\n# para um caso mais complexo, temos\n###\nfrom brasilapy.constants import IBGEProvider\n\nmunicipios = client.get_ibge_municipios(state_uf="pb", providers=(IBGEProvider.DADOS_ABERTOS_BR,))\n\nfor municipio in municipios:\n    print(municipio.nome)\n    print(municipio.codigo_ibge)\n```\n\n### Métodos disponíveis do `BrasilAPI`\n\n| Método                                                                    | Detalhes |\n|---------------------------------------------------------------------------|----------|\n | get_banks()                                                               |          |\n | get_bank(code: str)                                                       |          |\n | get_cep(test_cep: str, api_version: APIVersion)                                |          |\n | get_cnpj(test_cnpj: str)                                                       |          |\n | get_ddd(test_ddd: str)                                                         |          |\n | get_feriados(year: int)                                                   |          |\n | get_fipe_veiculos(tipo_veiculos: FipeTipoVeiculo, tabela_referencia: int) |          |\n | get_fipe_precos(codigo_fipe: str, tabela_referencia: int)                 |          |\n | get_fipe_tabelas()                                                        |          |\n | get_ibge_municipios(state_uf: str, providers: tuple\\[IBGEProvider\\]       |          |\n | get_ibge_estados()                                                        |          |\n | get_registro_br_domain(fqdn: str)                                         |          |\n | get_taxas_juros()                                                         |          |\n | get_taxa_juros(taxa: TaxaJurosType)                                       |          |\n\nOs tipos de dados `APIVersion`, `FipeTipoVeiculo`, `IBGEProvider` e `TaxaJurosType` são classes de constants que podem ser importadas através do seguinte comando:\n\n```py\nfrom brasilapy.constants import APIVersion, FipeTipoVeiculo, IBGEProvider, TaxaJurosType\n```\n\n## Autores\n\n<table>\n<tbody>\n<tr>\n    <td style="text-align: center">\n        <img width=\'100\' height=\'100\' style="border-radius:50%; padding:15px; display: block; margin: 0 auto" src="https://avatars.githubusercontent.com/u/78698099?v=4" />\n        <a href="https://github.com/lipe14-ops" target="_blank">Filipe Soares</a>\n    </td>\n    <td style="text-align: center">\n        <img width=\'100\' height=\'100\' style="border-radius:50%; padding:15px; display: block; margin: 0 auto" src="https://avatars.githubusercontent.com/u/2691511?v=4" />\n        <a href="https://joepreludian.github.io" target="_blank">Jonhnatha Trigueiro</a>\n    </td>\n</tr>\n</tbody>\n</table>\n\n## Gostaria de contribuir?\n\nEscrevemos um guia que pode ser encontrado em [CONTRIBUTE.md](CONTRIBUTE.md).\n',
    'author': 'Filipe Soares',
    'author_email': 'fn697169@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
