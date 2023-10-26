# def _clean_reference_ids(_id):
#     _id = _id.replace(' ','')
#     list_ids = _id.split('\n')
#     # list_ids = [x.strip() for x in list_ids]
#     return list_ids[1:] if len(list_ids)>1 else []

# def _clean_article_id(_id):
#     return _id.split('\n')[0].strip()

from pandas import DataFrame, Series


class CleanPumedDataFrame:
    def _clean_id_references(self, df_row: Series) -> tuple:
        _id_original = str(df_row.pubmed_id).replace(' ', '')
        list_ids = _id_original.split('\n')
        _id = list_ids[0]
        _reference_ids = list_ids[1:] if len(list_ids) > 1 else []
        return _id, _reference_ids

    def _utf8(self, _string: str) -> str or None:
        if _string:
            return _string.encode(encoding='utf-8', errors='replace').decode('utf-8')
        return None

    def _clean_authors_affiliation(self, df_row: Series) -> tuple:
        # author_list = ast.literal_eval(df_row['authors'])
        try:
            author_list = df_row['authors'] if isinstance(df_row['authors'], list) else []
        except:
            return [], []
        # print(type(author_list))
        # print(_utf8(str(author_list)))

        authors_clean = []
        affiliation_clean = []
        for item in author_list:
            _dict_author = {}
            for key in item:
                if key != 'affiliation':
                    _dict_author[key] = self._utf8(item[key])
                else:
                    affiliation_clean.append(self._utf8(item[key]))
            # if  isinstance(_dict_author, dict) and _dict_author!={}: authors_clean.append(_dict_author)
            # if  isinstance(_dict_affiliation, dict) and _dict_affiliation!= {}: affiliation_clean.append(_dict_affiliation)
            authors_clean.append(_dict_author)
        return authors_clean, affiliation_clean

    def _clean_keywords(self, df_row: Series) -> list:
        # print(f"{type(df_row['keywords_original'])} - {df_row['keywords_original']}")
        # print(df_row.pubmed_id)
        # keywords_list = ast.literal_eval(df_row['keywords'])
        keywords_list = df_row['keywords_original'] if isinstance(df_row['keywords_original'], list) else []
        return [self._utf8(x) for x in keywords_list]

    def _clean_doi(self, df_row: Series) -> list:
        doi = str(df_row['doi_original'])
        return doi.split('\n') if doi != [] else ''

    def clean_pubmed(self, df: DataFrame) -> DataFrame:
        # df['reference_ids'] = df.pubmed_id
        # df.pubmed_id = df.pubmed_id.apply(_clean_article_id)
        # df.reference_ids = df.reference_ids.apply(_clean_reference_ids)
        df.rename(columns={"keywords": "keywords_original", 'doi': 'doi_original'}, inplace=True)
        df[['pubmed_id', 'reference_ids']] = df.apply(self._clean_id_references, axis=1, result_type='expand')
        df[['authors', 'affiliation']] = df.apply(self._clean_authors_affiliation, axis=1, result_type='expand')
        df[['keywords']] = df.apply(self._clean_keywords, axis=1)
        df[['doi']] = df.apply(self._clean_doi, axis=1)
        df.drop(axis=1, columns=['keywords_original', 'doi_original'], inplace=True)
        return df
