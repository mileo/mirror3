# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 KMEE INFORMATICA LTDA - Luis Felipe Miléo
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from openerp.openupgrade import openupgrade


logger = logging.getLogger('OpenUpgrade.account_product_fiscal_classification')

column_renames = {
    'account_product_fiscal_classification': [
        ('name', 'code'),
        ('description', 'name'),
        # ('purchase_base_tax_ids', 'purchase_base_tax_ids'),
        # ('sale_base_tax_ids', 'sale_tax_ids')
    ],
    'account_product_fiscal_classification_template': [
        ('name', 'code'),
        ('description', 'name'),
        # ('purchase_base_tax_ids', 'purchase_base_tax_ids'),
        # ('sale_base_tax_ids', 'sale_tax_ids')
    ],
    # TODO: this works?
    # 'product_template': [
    #     ('property_fiscal_classification', 'fiscal_classification_id'),
    # ],
}

xmlid_renames = [
    ('account_product_fiscal_classification.product_fiscal_classification_product_normal_form_view',
        'account_product_fiscal_classification.view_product_template_form'),
    ('account_product_fiscal_classification.fiscal_classification_normal_form_view_form',
        'account_product_fiscal_classification.view_account_product_fiscal_classification_form'),
    ('account_product_fiscal_classification.fiscal_classification_normal_form_view_tree',
        'account_product_fiscal_classification.view_account_product_fiscal_classification_tree'),
    ('account_product_fiscal_classification.fiscal_classification_template_normal_form_view_form',
        'account_product_fiscal_classification.view_account_product_fiscal_classification_template_form'),
    ('account_product_fiscal_classification.fiscal_classification_template_normal_form_view_tree',
        'account_product_fiscal_classification.view_account_product_fiscal_classification_template_tree'),
    ('account_product_fiscal_classification.product_fiscal_classifications_template_action',
        'account_product_fiscal_classification.action_template_list_by_fiscal_classification'),
    ('account_product_fiscal_classification.product_fiscal_classifications_action',
        'account_product_fiscal_classification.action_account_product_fiscal_classification'),
    # ('account_product_fiscal_classification.',
    #     'account_product_fiscal_classification.action_account_product_fiscal_classification_template'),
    # ('account_product_fiscal_classification.',
    #     'account_product_fiscal_classification.action_account_product_fiscal_classification'),
    # ('account_product_fiscal_classification.',
    #     'account_product_fiscal_classification.action_wizard_change_fiscal_classification'),
    # ('account_product_fiscal_classification.',
    #     'account_product_fiscal_classification.action_wizard_account_product_fiscal_classification'),
]

def copy_properties(cr, pool):
    """ Fields property_fiscal_classification moved to Many2one (fiscal_classification_id).

    Write using the ORM so the fiscal_classification_id will be written on products.
    """
    template_obj = pool['product.template']
    sql = ("SELECT id, %s FROM product_template" %
           openupgrade.get_legacy_name('standard_price'))
    cr.execute(sql)
    logger.info(
        "Creating product_template.standard_price properties"
        " for %d products." % (cr.rowcount))
    for template_id, std_price in cr.fetchall():
        template_obj.write(cr, SUPERUSER_ID, [template_id],
                           {'standard_price': std_price})
    # make properties global
    sql = ("""
        UPDATE ir_property
        SET company_id = null
        WHERE res_id like 'product.template,%%'
        AND name = 'standard_price'""")
    openupgrade.logged_query(cr, sql)

    # product.price.history entries have been generated with a value for
    # today, we want a value for the past as well, write a bogus date to
    # be sure that we have an historic value whenever we want
    cr.execute("UPDATE product_price_history SET "
               # calling a field 'datetime' is not really a good idea
               "datetime = '1970-01-01 00:00:00+00'")

@openupgrade.migrate()
def migrate(cr, version):
    openupgrade.rename_columns(cr, column_renames)
    openupgrade.rename_xmlids(cr, xmlid_renames)
