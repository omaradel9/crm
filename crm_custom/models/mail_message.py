# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re
import textwrap
from binascii import Error as binascii_error
from collections import defaultdict

from odoo import _, api, Command, fields, models, modules, tools
from odoo.exceptions import AccessError
from odoo.osv import expression
from odoo.tools.misc import clean_context

_logger = logging.getLogger(__name__)
_image_dataurl = re.compile(r'(data:image/[a-z]+?);base64,([a-z0-9+/\n]{3,}=*)\n*([\'"])(?: data-filename="([^"]*)")?', re.I)


class Message(models.Model):
  
    _inherit= 'mail.message'


    crm_attachment_id= fields.One2many('crm.attachments','mail_message_id')