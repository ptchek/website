# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

import logging

_logger = logging.getLogger(__name__)
from openerp import models, api


class product_template(models.Model):
    """ Adds a method to product.template to copy some fields
    into the descriptions.
    """
    _inherit = 'product.template'
    fields_to_copy = []

    @api.model
    def action_update_description_sale(self, ids):
        assert self.fields_to_copy, \
            'At least one field is required in self.field_to_copy'
        for rec in self.browse(ids):
            rec.copy_into_description_sale(self.fields_to_copy)

    def copy_into_description_sale(self, fields_to_copy):
        """ Update the description with the title and the value of
        the given fields.

        :param fields_to_copy: names of the field to copy
        :return: None
        """
        assert isinstance(fields_to_copy, (list, tuple)), \
            'Wrong argument type. Should be list or tuple got {}.'.format(
                type(fields_to_copy)
            )
        copy_field_target_field = 'description'
        # checking the target is a field of the model.
        # Checking the target is not a source too.
        msg = '{} cannot be set as a field to be copied'.format(
            copy_field_target_field)
        assert copy_field_target_field not in fields_to_copy, msg

        member_msg = '{} has to be the name of a field of {}'
        # Checking all the fields to copy are fields of the model
        # and there are string, not field it self.
        for field in fields_to_copy:
            assert hasattr(self, field), \
                member_msg.format(field, self._inherit)

        self.description_sale = self.build_description_sale(fields_to_copy)

    def build_description_sale(self, fields_to_copy):
        """ Build the new description with the current description and the new
         values

        :param fields_to_copy: names of the field to copy
        :return: text
        """
        assert isinstance(fields_to_copy, (list, tuple)), \
            'Wrong argument type. Should be list or tuple got {}.'.format(
                type(fields_to_copy)
            )
        fields = {}
        for field_name in fields_to_copy:
            attribute = getattr(self, field_name)

            # Checking if the attribute is a field or not
            try:
                attribute = attribute.name
            except AttributeError:
                pass

            fields[field_name] = attribute

        return '\n'.join(
            [
                u'{}: {}'.format(name, value)
                for name, value in fields.iteritems()
            ]
        )