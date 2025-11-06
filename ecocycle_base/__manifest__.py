# -*- coding: utf-8 -*-
{
    "name": """EcoCycle Base""",
    "summary": """EcoCycle Base Module""",
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
        # 'code_backend_theme',
        'hide_login_manage_databases_powered_by_odoo',
        'kw_hide_discuss',
        'web_favicon',
        'web_window_title',
        'operating_unit',

        # developed addons
    ],
    "data": [
        # group
        # 'security/res_groups.xml',

        # data
        'data/ir_sequence.xml',

        # global action
        # 'views/action/action.xml',

        # view
        'views/common/waste_category.xml',
        'views/common/waste_move.xml',
        'views/common/res_partner.xml',
        'views/common/payment_method.xml',
        'views/common/delivery_method.xml',

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
        'views/action/action_menu.xml',

        # action onboarding
        # 'views/action/action_onboarding.xml',

        # menu
        'views/menu.xml',

        # security
        'security/ir.model.access.csv',
        # 'security/ir.rule.csv',

        # data
    ],
    "demo": [
        # 'demo/demo.xml',
    ],

    # For more details about the new static asset management, please go to these link:
    # https://www.odoo.com/documentation/master/developer/reference/frontend/assets.html
    # 'assets': {
    #     'web.assets_common': [
    #         'ecocycle_base/static/lib/bootstrap/**/*',
    #         'ecocycle_base/static/src/js/boot.js',
    #         'ecocycle_base/static/src/js/webclient.js',
    #     ],
        # 'web.assets_backend': [
        #     'ecocycle_base/static/src/js/**/*',
        # ],
    #     'web.assets_frontend': [
    #         'ecocycle_base/static/src/xml/**/*',
    #     ],
    #     'web.assets_qweb': [
    #         'ecocycle_base/static/src/xml/**/*',
    #     ],    # Add fields here

    #     'web.qunit_suite_tests': [
    #         'ecocycle_base/static/src/js/webclient_tests.js',
    #     ],
    #     'web.qunit_mobile_suite_tests': [
    #         'ecocycle_base/static/src/js/webclient_tests.js',
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
