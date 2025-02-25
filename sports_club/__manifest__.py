{
    'name': 'Sports Club',
    'version': '1.0',
    'category': 'Services',
    'description': """
        This setup is for sports clubs that rent courts to their players, handle some basic gears and have a cafeteria.
        As a small company, The Club still has quite a lot of activities to manage and does all this with Odoo.
    """,
    'depends': [
        'appointment_crm',
        'knowledge',
        'planning',
        'payment_demo',
        'point_of_sale',
        'pos_restaurant',
        'project_sms',
        'sale_crm',
        'social_push_notifications',
        'website_appointment',
        'website_crm',
        'website_sale_picking',
        'website_sale_product_configurator',
        'website_sale_stock',
    ],
    'data': [
        'data/res_config_settings.xml',
        'data/pos_category.xml',
        'data/restaurant_floor.xml',
        'data/restaurant_table.xml',
        'data/pos_payment_method.xml',
        'data/pos_config.xml',
        'data/ir_attachment_pre.xml',
        'data/product_public_category.xml',
        'data/planning_role.xml',
        'data/product_template.xml',
        'data/product_product.xml',
        'data/knowledge_cover.xml',
        'data/knowledge_article.xml',
        'data/knowledge_article_favorite.xml',
        'data/mail_message.xml',
        'data/resource_calendar.xml',
        'data/appointment_resource.xml',
        'data/appointment_type.xml',
        'data/payment_provider_demo.xml',
    ],
    'demo': [
        'demo/pos_config.xml',
        'demo/res_partner.xml',
        'demo/hr_employee.xml',
        'demo/crm_team.xml',
        'demo/crm_lead.xml',
        'demo/sale_order.xml',
        'demo/sale_order_line.xml',
        'demo/sale_order_post.xml',
        'demo/planning_slot.xml',
        'demo/appointment_invite.xml',
        'demo/calendar_event.xml',
        'demo/appointment_booking_line.xml',
        'demo/website.xml',
        'demo/website_view.xml',
        'demo/website_page.xml',
        'demo/website_menu.xml',
        'demo/website_theme_apply.xml',
        'demo/website_ir_attachments.xml',
        'demo/payment_provider_demo.xml',
    ],
    'license': 'OPL-1',
    'images': ['images/main.png'],
}
