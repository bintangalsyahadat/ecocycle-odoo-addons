# -*- coding: utf-8 -*-
{
    "name": """EcoCycle API""",
    "summary": """EcoCycle API Module""",
    "category": "Extra Tools",
    "version": "18.0.0.0.0",
    "development_status": "Alpha",  # Options: Alpha|Beta|Production/Stable|Mature
    "auto_install": False,
    "installable": True,
    "application": False,
    "author": "Munn",
    "website": "https://munn.web.id",
    "license": "OPL-1",
    # "images": [
    #     'publish/images/main_screenshot.png'
    # ],

    "depends": [
        # odoo addons
        'base',

        # third party addons
        'fastapi_auth_jwt',

        # developed addons
        'ecocycle_base',
    ],
    "data": [
        # group
        'security/res_groups.xml',

        # data
        'data/fastapi_endpoint_data.xml',

        # global action
        # 'views/action/action.xml',

        # view
        # 'views/common/views.xml',

        # qweb template
        # 'views/template/template.xml',

        # wizard
        # 'views/wizard/wizard.xml',

        # report paperformat
        # 'data/report_paperformat.xml',

        # report/printout template
        # 'views/report/report_tmpl_name.xml',
        # 'views/report/printout_tmpl_name.xml',

        # report/printout action
        # 'views/action/action_report.xml',

        # onboarding action
        # 'views/action/action_onboarding.xml',

        # action menu
        # 'views/action/action_menu.xml',

        # action onboarding
        # 'views/action/action_onboarding.xml',

        # menu
        # 'views/menu.xml',

        # security
        'security/ir.model.access.csv',
        'security/ir.rule.csv',

        # data
    ],
    "demo": [
        # 'demo/demo.xml',
    ],

    # For more details about the new static asset management, please go to these link:
    # https://www.odoo.com/documentation/master/developer/reference/frontend/assets.html
    # 'assets': {
    #     'web.assets_common': [
    #         'ecocycle_api/static/lib/bootstrap/**/*',
    #         'ecocycle_api/static/src/js/boot.js',
    #         'ecocycle_api/static/src/js/webclient.js',
    #     ],
    #     'web.assets_backend': [
    #         'ecocycle_api/static/src/xml/**/*',
    #     ],
    #     'web.assets_frontend': [
    #         'ecocycle_api/static/src/xml/**/*',
    #     ],
    #     'web.assets_qweb': [
    #         'ecocycle_api/static/src/xml/**/*',
    #     ],
    #     'web.qunit_suite_tests': [
    #         'ecocycle_api/static/src/js/webclient_tests.js',
    #     ],
    #     'web.qunit_mobile_suite_tests': [
    #         'ecocycle_api/static/src/js/webclient_tests.js',
    #     ],
    # },

    "post_load": None,
    # "pre_init_hook": "pre_init_hook",
    # "post_init_hook": "post_init_hook",
    "uninstall_hook": None,

    "external_dependencies": {"python": [], "bin": []},

    # "live_test_url": "",
    # "demo_title": "{MODULE_NAME}",
    # "demo_addons": [
    # ],
    # "demo_addons_hidden": [
    # ],
    # "demo_url": "DEMO-URL",
    # "demo_summary": "{SHORT_DESCRIPTION_OF_THE_MODULE}",
    # "demo_images": [
    #    "publish/images/MAIN_IMAGE",
    # ]
}
