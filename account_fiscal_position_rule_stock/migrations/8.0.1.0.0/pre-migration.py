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


logger = logging.getLogger('OpenUpgrade.account_fiscal_position_rule_stock')


xmlid_renames = [
    ('account_fiscal_position_rule_stock.account_fiscal_position_rule_stock_view_picking_inherit_form',
        'account_fiscal_position_rule_stock.account_fiscal_position_rule_stock_view_picking_form'),
]

@openupgrade.migrate()
def migrate(cr, version):
    openupgrade.rename_xmlids(cr, xmlid_renames)
