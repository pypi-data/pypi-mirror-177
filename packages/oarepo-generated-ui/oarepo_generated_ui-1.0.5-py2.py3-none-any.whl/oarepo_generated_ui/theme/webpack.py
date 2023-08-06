# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS bundles for oarepo-generated-ui.

You include one of the bundles in a page like the example below (using
``base`` bundle as an example):

 .. code-block:: html

    {{ webpack['base.js']}}

"""

from invenio_assets.webpack import WebpackThemeBundle

generated_ui = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "oarepo_generated_ui": "./js/oarepo_generated_ui/index.js",
            },
            dependencies={
                "lodash": "^4.17.0",
                "react": "^16.13.0",
                "react-dom": "^16.13.0",
                "clsx": "^1.1.1",
            },
            devDependencies={
            },
            aliases={
                '@js/oarepo_generated_ui': 'js/oarepo_generated_ui',
                '@uijs/oarepo_generated_ui': 'js/oarepo_generated_ui/ui_components'
            }
        )
    },
)
