#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Build an in-memory Index over a Dictionary of Classifications """


from typing import Dict

from baseblock import FileIO
from baseblock import BaseObject

from schema_classification.dmo import IndexScoring
from schema_classification.dmo import IndexExcludeAllOf
from schema_classification.dmo import IndexExcludeOneOf
from schema_classification.dmo import IndexIncludeAllOf
from schema_classification.dmo import IndexIncludeOneOf
from schema_classification.dmo import IndexStartsWith
from schema_classification.dto import RawSchema
from schema_classification.dto import NormalizedSchema


class ReadMapping(BaseObject):
    """ Build an in-memory Index over a Dictionary of Classifications """

    def __init__(self,
                 d_schema: Dict):
        """ Initialize Manifest Indicer

        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/167
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   read schema in-memory
                https://github.com/grafflr/deepnlu/issues/45
        Updated:
            26-Jul-2022
            craigtrim@gmail.com
            *   remove 'schema-name' and 'absolute-path' as parameters, and instead
                pass the full absolute path of a schema file, in pursuit of
                https://bast-ai.atlassian.net/browse/COR-12
        Updated:
            26-Sept-2022
            craigtrim@gmail.com
            *   pass in d-schema as dict rather than a filepath
                https://github.com/craigtrim/schema-classification/issues/1

        Args:
            d_schema (Dict): the schema JSON
        """
        BaseObject.__init__(self, __name__)
        self._d_index = self._create_index(d_schema)

    def _create_index(self,
                      d_schema: RawSchema) -> NormalizedSchema:
        """ Create Index

        Args:
            d_schema (dict): _description_
            Sample Input:
                {
                    'Favorite_Animal_Response#1': [
                        {
                            'include_all_of': ['favorite', 'animal']
                        }
                    ]
                }

        Raises:
            ValueError: _description_

        Returns:
            InMemoryIndex: _description_
        """

        return {
            'scoring': IndexScoring(d_schema).process(),
            'include_one_of': IndexIncludeOneOf(d_schema).process(),
            'include_all_of': IndexIncludeAllOf(d_schema).process(),
            'exclude_one_of': IndexExcludeOneOf(d_schema).process(),
            'exclude_all_of': IndexExcludeAllOf(d_schema).process(),
            'startswith': IndexStartsWith(d_schema).process(),
            'mapping': d_schema,
        }

    def index(self) -> NormalizedSchema:
        return self._d_index
