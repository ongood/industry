# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval
import logging
import os
import pathlib
import re

from odoo.tests.common import tagged

from .industry_case import IndustryCase, get_industry_path

_logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 100 * 1024 * 1024  # in megabytes


@tagged('post_install', '-at_install')
class TestEnv(IndustryCase):

    def test_xml_files(self):
        for module in self.installed_modules:
            self._check_files_in_path(module)

    def _check_files_in_path(self, module):
        path = get_industry_path() + module
        is_studio_required = False
        for root, dirs, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                ext = os.path.splitext(file_path)[1].lower()
                if ext not in ['.py', '.xml']:
                    continue
                if os.path.getsize(file_path) > MAX_FILE_SIZE:
                    raise "Max file size exceeded"
                content = pathlib.Path(file_path).read_bytes().decode('utf8')
                if ext == '.py':
                    if file_name != '__manifest__.py':
                        _logger.warning(
                            "No python file is allowed in an industry module, except __manifest__.py."
                            " Please remove %s.", file_name
                        )
                    else:
                        manifest_content = content
                    continue
                self._check_xml_style(content, module, file_name)
                self._check_update_status(content, file_name)
                self._check_useless_models(content, file_name)
                self._check_useless_fields_on_models(content, file_name)
                if not is_studio_required and root.split('/')[-1] == 'data':
                    is_studio_required = self._check_studio(content, file_name)
        self._check_manifest(manifest_content, is_studio_required)

    def _check_manifest(self, s, need_studio):
        if (first_line := s.split('\n')[0]) != '{':
            message = "First line of the manifest should be the sole symbol '{'. "
            if not first_line:
                message += "No need for an empty line."
            elif "coding" in first_line:
                message += "No need to specify the encoding since python3."
            else:
                message += "Got '%s'." % first_line
            _logger.warning(message)
        dependency_list = literal_eval(s)['depends']
        base_automation = 'base_automation' in dependency_list and 'sale_subscription' not in dependency_list
        studio_required = need_studio or base_automation
        studio_dependency = any(studio in dependency_list for studio in ['web_studio', 'website_studio'])
        if studio_required and not studio_dependency:
            _logger.warning("'web_studio' is missing in the dependencies.")
        elif not studio_required and studio_dependency:
            _logger.warning("'web_studio' should not be in the dependencies.")

    def _check_studio(self, s, file_name):
        models_for_studio = [
            "ir.actions.act_window",
            "ir.actions.server",
            "ir.model",
            "ir.model.fields",
            "ir.ui.menu",
            "ir.ui.view",
        ]
        for model in models_for_studio:
            if re.search('model="' + model + '"', s) and not re.search('<field .+model="' + model, s):
                _logger.info("%s found in %s, needs studio", model, file_name)
                return True
        return False

    def _check_xml_style(self, s, module, file_name):
        starts_with = [
            "<?xml version='1.0' encoding='UTF-8'?>",
            "<?xml version='1.0' encoding=\"UTF-8\"?>",
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            "<?xml version=\"1.0\" encoding='UTF-8'?>",
        ]
        first_line = s.split('\n')[0]
        if not any(first_line == start_line for start_line in starts_with):
            _logger.warning(
                "XML files should begin with the following line: %s, but %s starts with %s",
                starts_with[0], file_name, first_line
            )

        if count := (s.count(' id="' + module + '.') + s.count(" id='" + module + '.')):
            _logger.warning(
                "Defining an xmlid with the current module name is useless, module name will be "
                "added automatically. Found %d occurence(s) of ' id=\"%s.ID' in %s.",
                count, module, file_name
            )

        count = (s.count('ref("' + module + '.') + s.count("ref('" + module + '.')) - (
            s.count('env.ref("' + module + '.') + s.count("env.ref('" + module + '.'))
        if count:
            _logger.warning(
                "Referring to an xmlid created within the current module name is useless. If none is"
                " provided, it will check in current module. Found %d occurence(s) of ref(\"%s.ID\")"
                " in %s (this remark does not apply to 'env.ref(\"%s.ID\")' where it is required).",
                count, module, file_name, module
            )
        count = (s.count('ref="' + module + '.') + s.count("ref='" + module + '.'))
        if count:
            _logger.warning(
                "Referring to an xmlid created within the current module name is useless. If none is"
                " provided, it will check in current module. Found %d occurence(s) of ref=\"%s.ID\""
                " in %s.", count, module, file_name
            )
        if s.count("x_studio"):
            _logger.warning("Please remove 'studio' from 'x_studio' in %s.", file_name)
        useless_attributes = [
            "context.get('studio')",
            "data-last-history-steps",
            "context=\"{'studio'",
        ]
        for attr in useless_attributes:
            if s.count(attr):
                _logger.warning("Please remove '%s' in %s.", attr, file_name)

        end_of_file = repr(s).split('\\')
        if 'n' not in end_of_file[-1] or len(end_of_file[-1]) > 2:
            _logger.warning("It looks like you forgot to add an empty line at the end of %s.", file_name)
        elif 'n' in end_of_file[-2] and len(end_of_file[-2]) <= 2:
            _logger.warning("One empty line at the end of %s is enough, please remove others.", file_name)

    def _check_update_status(self, s, filename):
        models_to_update = [
            "base.automation",
            "ir.actions.act_window",
            "ir.actions.server",
            "ir.model",
            "ir.model.access",
            "ir.model.fields",
            "ir.ui.view",
            "knowledge.article",
            "loyalty.generate.wizard",
        ]
        models_not_to_update = [
            "account.cash.rounding",
            "appointment.type",
            "calendar.event",
            "crm.lead",
            "crm.stage",
            "crm.tag",
            "document.document",
            "document.folder",
            "event.event.ticket",
            "helpdesk.ticket",
            "hr.applicant",
            "hr.department",
            "hr.job",
            "hr.recruitment.stage",
            "ir.attachment",
            "ir.rule",
            "knowledge.article.favorite",
            "knowledge.attachment",
            "knowledge.cover",
            "loyalty.program",
            "loyalty.reward",
            "loyalty.rule",
            "mail.template",
            "mrp.bom",
            "mrp.bom.line",
            "mrp.production",
            "mrp.routing.workcenter",
            "mrp.workcenter",
            "pos.category",
            "pos.config",
            "pos.order",
            "pos.order.line",
            "pos.payment.method",
            "pos.session",
            "pos_preparation_display.display",
            "pos_preparation_display.order",
            "pos_preparation_display.orderline",
            "product.attribute.value",
            "product.category",
            "product.packaging",
            "product.pricelist",
            "product.pricelist.item",
            "product.product",
            "product.public.category",
            "product.supplierinfo",
            "product.template",
            "product.template.attribute.line",
            "product.template.attribute.value",
            "project.project",
            "project.task",
            "project.task.type",
            "purchase.order",
            # "purchase.order.line",  # need to handle in functions
            "quality.point",
            "repair.order",
            "res.config.settings",
            "res.partner",
            "restaurant.floor",
            "restaurant.table",
            "sale.order",
            "sale.order.line",
            "sale.order.template",
            "sale.order.template.line",
            "sign.item",
            "sign.request",
            "sign.template",
            # "stock.lot",  # need to handle in functions
            "stock.quant",
            "stock.warehouse.orderpoint",
            "uom.category",
            "uom.uom",
            "website",
            "website.base.unit",
            "website.menu",
            "website.page",
        ]
        for model in models_to_update:
            if re.search('model="' + model + '"', s) and not re.search('<field .+model="' + model, s) and not s.count('<odoo>'):
                _logger.warning(
                    "Model %s should be updated, please remove 'noupdate=\"1\"' in the header of %s.",
                    model, filename,
                )
        for model in models_not_to_update:
            if (re.search('model="' + model + '"', s)
                and not re.search('<field .+model="' + model, s)
                and not re.search('<function.+model="' + model, s)
                and not s.count('<odoo noupdate="1">')
            ):
                _logger.warning(
                    "Model %s should not be updated, please add 'noupdate=\"1\"' in the header of %s.",
                    model, filename,
                )

    def _check_useless_models(self, s, filename):
        useless_models = {
            "knowledge.article.member": "Model knowledge.article.member should be replaced by write"
                " access to all users",
        }
        for model, warning in useless_models.items():
            if re.search('model="' + model, s):
                _logger.warning(warning)

    def _check_useless_fields_on_models(self, s, filename):
        useless_model_fields = {
            'account.analytic.plan': ['color'],
            'account.analytic.account': ['root_plan_id'],
            'appointment.type': [
                'has_message',
                'resource_total_capacity',
            ],
            'crm.lead': ['copied'],
            'crm.tag': ['color'],
            'hr.applicant': ['last_stage_id'],
            'ir.attachment': ['access_token'],
            'ir.model.fields': [
                'copied',
                'model',
            ],
            'knowledge.article': [
                'article_member_ids',
                'inherited_permission',
            ],
            'loyalty.reward': [
                'description',
                'is_global_discount',
                'program_type',
                'reward_product_ids',
                'reward_product_uom_id',
            ],
            'loyalty.rule': [
                'company_id',
                'currency_id',
                'mode',
                'program_type',
                'promo_barcode',
                'valid_product_ids',
            ],
            'mrp.bom.byproduct': [
                'company_id',
                'product_uom_category_id',
            ],
            'planning.role': ['color'],
            'planning.slot': [
                'access_token',
                'allocated_hours',
                'department_id',
                'sale_order_id',
                'work_address_id',
                'working_days_count',
            ],
            'product.attribute': ['product_tmpl_ids'],
            'product.attribute.value': ['color'],
            'product.packaging': ['product_uom_id'],
            'product.pricelist.item': [
                'name',
                'price',
            ],
            'product.template.attribute.line': ['value_count'],
            'product.template.attribute.value': [
                'attribute_id',
                'color',
                'product_tmpl_id',
            ],
            'project.tags': ['color'],
            'purchase.order.line': [
                'date_order',
                'name',
            ],
            'res.partner': ['tz'],
            'sale.order': [
                'access_token',
                'amount_tax',
                'amount_to_invoice',
                'amount_total',
                'amount_untaxed',
                'currency_rate',
                'date_order',
                'health',
                'invoice_status',
                'is_subscription',
                'origin',
                'partner_invoice_id',
                'partner_shipping_id',
                'percentage_satisfaction',
                'recurring_monthly',
                'recurring_total',
                'state',
                'validity_date',
            ],
            'sale.order.line': [
                'invoice_status',
                'is_service',
                # 'name',  # need to handle down payments and options & templates properly
                'order_partner_id',
                'planning_hours_planned',
                'planning_hours_to_plan',
                'price_reduce_taxinc',
                'price_reduce_taxexcl',
                'price_subtotal',
                'price_tax',
                'price_total',
                'qty_delivered',
                'qty_delivered_method',
                'qty_invoiced',
                'qty_to_invoice',
                'state',
                'untaxed_amount_invoiced',
                'untaxed_amount_to_invoice',
            ],
            # 'sale.order.template.line': ['name'],  # check as could be meaningful and different
            'sign.template': [
                'has_sign_requests',
                'is_sharing',
                'name',
                'signed_count',
            ],
            'stock.lot': ['product_uom_id'],
            'worksheet.template': ['color'],
        }
        for model, fields in useless_model_fields.items():
            if re.search('model="' + model, s):
                for field in fields:
                    if re.search('field name="' + field + '"', s):
                        _logger.warning(
                            "You shouldn't define the %s on %s (%s). Please refer to other modules for examples.",
                            field, model, filename
                        )
