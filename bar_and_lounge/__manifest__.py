{
    'name': 'Bar and Lounge',
    'version': '1.0',
    'category': 'Services',
    'description': """
This setup is for service companies who provides all kind of service that customer can available at the Airport like Porter Service, Buggy Service, Airport Assistance etc..
This Services can be avail directly from the airport and individuals can also purchase the services from the website.
""",
    'depends': [
        'base_geolocalize',
        'base_vat',
        'calendar',
        'knowledge',
        'mrp',
        'pos_hr',
        'pos_sale',
        'purchase_stock',
        'sale_planning',
        'sale_project',
        'sale_purchase',
        'web_studio',
        'website_livechat',
        'website_partner',
        'website_sale_product_configurator',
        'website_sale_stock',
        'theme_treehouse',
    ],
    'data': [
        'data/ir_attachment_pre.xml',
        'data/ir_model.xml',
        'data/ir_model_fields.xml',
        'data/ir_ui_view.xml',
        'data/x_airline_master_view.xml',
        'data/x_airport_master_view.xml',
        'data/x_flitght_master_view.xml',
        'data/x_guest_detail_view.xml',
        'data/x_services_view.xml',
        'data/x_type_of_airport_view.xml',
        'data/ir_actions_act_window.xml',
        'data/ir_ui_menu.xml',
        'data/ir_model_access.xml',
        'data/ir_default.xml',
        'data/product_category.xml',
        'data/uom_uom.xml',
        'data/planning_role.xml',
        'data/pos_category.xml',
        'data/pos_payment_method.xml',
        'data/pos_config.xml',
        'data/product_product.xml',
        'data/mrp_bom.xml',
        'data/mrp_bom_line.xml',
        'data/knowledge_cover.xml',
        'data/knowledge_article.xml',
        'data/knowledge_article_favorite.xml',
        'data/mail_message.xml',
    ],
    'demo': [
        'demo/pos_config.xml',
        'demo/website.xml',
        'demo/res_partner.xml',
        'demo/hr_employee.xml',
        'demo/product_supplierinfo.xml',
        'demo/x_airline_master.xml',
        'demo/x_flight_master.xml',
        'demo/x_type_of_airport.xml',
        'demo/x_airport_master.xml',
        'demo/x_services.xml',
        'demo/sale_order.xml',
        'demo/sale_order_line.xml',
        'demo/sale_order_confirm.xml',
        'demo/x_guest_detail.xml',
        'demo/website_attachment.xml',
        'demo/website_view.xml',
        'demo/website_page.xml',
        'demo/website_menu.xml',
        'demo/purchase_order.xml',
        'demo/purchase_order_line.xml',
        'demo/purchase_order_confirm.xml',
        'demo/planning_slot.xml',
        'demo/website_theme_apply.xml',
    ],
    'license': 'OPL-1',
    'images': ['images/main.png'],
}
