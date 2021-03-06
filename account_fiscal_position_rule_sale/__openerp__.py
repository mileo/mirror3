# -*- encoding: utf-8 -*-
###############################################################################
#
#   account_fiscal_position_rule_sale for OpenERP
#   Copyright (C) 2009-TODAY Akretion <http://www.akretion.com>
#     @author Renato Lima <renato.lima@akretion.com>
#   Copyright 2012 Camptocamp SA
#     @author: Guewen Baconnier
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Account Fiscal Position Rule Sale',
    'version': '1.1',
    'category': 'Generic Modules/Accounting',
    'description': """Include a rule to decide the correct fiscal position for Sale""",
    'author': 'Akretion',
    'license': 'AGPL-3',
    'website': 'http://www.akretion.com',
    ## WHEN MERGING PLEASE LEAVE THE DEPENDENCY ON delivery BECAUSE OTHERWISE THE ONCHANGE_PARTNER_ID WILL BE TRIGGERED SOMETIMES IN DELIVERY
    'depends': ['account_fiscal_position_rule', 'sale', 'delivery'],
    'init_xml': [],
    'update_xml':
                [
                'sale_view.xml',
                'security/account_fiscal_position_rule_sale_security.xml',
                'security/ir.model.access.csv',

                ],
    'demo_xml': [],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
