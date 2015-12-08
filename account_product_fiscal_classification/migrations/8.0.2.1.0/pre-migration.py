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
from openerp import pooler, SUPERUSER_ID


logger = logging.getLogger('OpenUpgrade.account_product_fiscal_classification')

column_renames = {
    'account_product_fiscal_classification': [
        ('name', 'code'),
        ('description', 'name'),
    ],
    'account_product_fiscal_classification_template': [
        ('name', 'code'),
        ('description', 'name'),
    ],
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
]


def copy_properties(cr, pool):
    """ Fields property_fiscal_classification moved to Many2one (fiscal_classification_id).

    Write using the ORM so the fiscal_classification_id will be written on products.
    """
    template_obj = pool['product.template']
    sql = ("SELECT value_reference, res_id, company_id "
           "FROM ir_property "
           "WHERE name='property_fiscal_classification'")
    cr.execute(sql)
    logger.info(
        "Converting property_fiscal_classification to fiscal_classification_id"
        " for %d products." % (cr.rowcount))
    for value_reference, res_id, company_id in cr.fetchall():
        fiscal_classification_id = value_reference.split(',')[1]
        template_id = res_id.split(',')[1]
        template_obj.write(
            cr, SUPERUSER_ID, [template_id],
            {'fiscal_classification_id': fiscal_classification_id})


@openupgrade.migrate()
def migrate(cr, version):
    openupgrade.rename_columns(cr, column_renames)
    openupgrade.rename_xmlids(cr, xmlid_renames)
    pool = pooler.get_pool(cr.dbname)
    copy_properties(cr, pool)
