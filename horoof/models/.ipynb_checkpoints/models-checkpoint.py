# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inhert = ['sale.order']

    related_project = fields.Many2one('project.project')
    related_task = fields.Many2one('project.task')
    
    
    @api.model
    def create(self, vals):
        product_info ={'name':vals['name']}
        vals['related_project'] = self.env['project.project'].create(product_info).id 
        for line in order_line :
            product_info ={'name':vals['name'], 'project_id': vals['related_project']}
            vals['related_project'] = self.env['project.task'].create(product_info).id 
        result = super(Unit,self).create(vals)
        return result
