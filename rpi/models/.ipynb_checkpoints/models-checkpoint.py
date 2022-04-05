# -*- coding: utf-8 -*-
from odoo import models, fields, api ,tools , _
from odoo.tools import image_process
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = ['product.template']
    
    detailed_type = fields.Selection(selection_add=[
        ('proprty', 'Proprty')
    ], tracking=True, ondelete={'proprty': 'set consu'})
    type = fields.Selection(selection_add=[
        ('proprty', 'Proprty')
    ], ondelete={'proprty': 'set consu'})
    
    

    

class Countries(models.Model):
    _name = 'rpi.rpi'
    _description = 'rpi.rpi'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Country Name')
    density = fields.Integer(string='Population Density')
    area = fields.Float( string='Land Area m^2')
    city = fields.One2many('rpi.cities', 'country_id', string = 'Cities')
    region = fields.One2many('rpi.regions', 'country_id', string = 'Regions')
    land = fields.One2many('rpi.land', 'country_id', string = 'Regions')
    bulding = fields.One2many('rpi.bulding', 'country_id', string = 'Bulding')
    unit = fields.One2many('rpi.unit', 'country_id', string = 'Bulding')
    
    
    
    
class Cities(models.Model):
    _name = 'rpi.cities'
    _inherit = ['mail.thread','mail.activity.mixin']
    name = fields.Char(string='Full Name')
    density = fields.Integer(string ='Population Density')
    area = fields.Float(string='Land Area m^2')
    region = fields.One2many('rpi.regions' , 'city_id' , string = 'Regions')
    land = fields.One2many('rpi.land' , 'city_id' , string = 'Regions')
    bulding = fields.One2many('rpi.bulding' , 'city_id' , string = 'Bulding')
    country_id = fields.Many2one('rpi.rpi', string = 'Country ')
    unit = fields.One2many('rpi.unit', 'city_id', string = 'Bulding')
    
    def unlink(self):
        for city in self:
            if len(city.region) > 0:
                raise ValidationError('This record is linked to another,cannot be deleted.')
        return super(Cities, self).unlink()
    
    
    
                                                                                                    
class Regions(models.Model):
    _name = 'rpi.regions'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    def _get_default_currency_id(self):
        return self.env.company.currency_id.id
    
    currency_id = fields.Many2one("res.currency", string="Valuta", required=True ,default = _get_default_currency_id)
    name = fields.Char(string='Region Name')
    area = fields.Float(string='Land Area m^2')
    land = fields.One2many('rpi.land' ,'region_id' , string = 'Lands' )
    city_id = fields.Many2one('rpi.cities', string = 'City')
    country_id = fields.Many2one('rpi.rpi', string = 'Country ')
    unit = fields.One2many('rpi.unit', 'region_id', string = 'Bulding')    
    
    
    
    
class Land(models.Model):
    _name = 'rpi.land'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    
    def _get_default_currency_id(self):
        return self.env.company.currency_id.id
    currency_id = fields.Many2one("res.currency", string="Valuta", required=True, default = _get_default_currency_id)
    name = fields.Char(string='Land Name')
    area = fields.Float(string='Land Area m^2')
    owner = fields.Many2one ('res.partner' , string = 'Owner')
    city_id = fields.Many2one('rpi.cities', string = 'City')
    country_id = fields.Many2one('rpi.rpi', string = 'Country ')
    region_id = fields.Many2one ('rpi.regions', string = 'Region')
    license_code = fields.Char(string = 'License Code')
    date_notarization = fields.Datetime(string= 'Date added license notarization')
    license_notarization = fields.Char(string = 'License notarization')
    license_date = fields.Datetime(string="License Date")
    price = fields.Monetary(string = 'Price',currency_field="currency_id")
    land_sketch=fields.Image(string='Land sketch')
    attachments = fields.Many2many('ir.attachment', string = 'Real estate certificate')
    land_stutes_id = fields.Many2one('rpi.building.stutes',string= 'Stutes')
    contract_id =  fields.Many2one('contracts.contracts',string= 'Proprty contract')
    

    
    land_type = fields.Selection([
        ('internalf', 'Internal fixed assets'),
        ('internali', 'Internal investment assets'),
        ('external', 'External proprties'),
        ], string='Type')
    related_product = fields.Many2one('product.product')
    related_asset = fields.Many2one('account.asset')
    
    @api.model
    def create(self, vals):
        if vals['land_type'] == 'internali':
            product_info ={'name':vals['name']}
            vals['related_product'] = self.env['product.product'].create(product_info).id
        if vals['land_type'] == 'internalf':
            product_info ={'name':vals['name'], 'asset_type': 'purchase'}
            vals['related_asset'] = self.env['account.asset'].create(product_info).id
        result = super(Land,self).create(vals)
        return result     
    

    
    
    def unlink(self):
        for land in self:
            self.env['product.product'].browse(land.related_product.id).unlink()
            self.env['account.asset'].browse(land.related_asset.id).unlink()
        return super(Land,self).unlink()     
    
    
    
    
    
    
    
    
class Bulding(models.Model):
    _name = 'rpi.bulding'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    
    def _get_default_currency_id(self):
        return self.env.company.currency_id.id
    
    currency_id = fields.Many2one("res.currency", string="Valuta", required=True, default = _get_default_currency_id)
    name = fields.Char(string='Bulding Name')
    code = fields.Char(string='Code')
    land_area = fields.Float(string='Land Area m^2')
    building_area = fields.Float(string='Building Area m^3')
    construction_year = fields.Integer(string = 'Construction Year')
    lift = fields.Boolean (string='Lift')
    purchase_date = fields.Datetime(string = "Purchase Date")
    sale_date = fields.Datetime(string="Sate Date")
 #   active = fields.Boolean (string = "Active")
    bulding_unit = fields.One2many ('rpi.unit', 'bulding_id', string = 'Units')
    owner = fields.Many2one ('res.partner' , string = 'Owner')
    region_id = fields.Many2one ('rpi.regions', string = 'Region')
    city_id = fields.Many2one('rpi.cities', string = 'City')
    country_id = fields.Many2one('rpi.rpi', string = 'Country ')
    bulding_stutes_id = fields.Many2one('rpi.building.stutes',string= 'Stutes')
    license_code = fields.Char(string = 'License Code')
    license_date = fields.Datetime(string="License Date")
    date_notarization = fields.Datetime(string= 'Date added license notarization')
    license_notarization = fields.Char(string = 'License notarization')
    note = fields.Html(string='Note')
    price = fields.Monetary(string = 'Price',currency_field="currency_id")
    surface = fields.Integer(string ='Surface')
    garage = fields.Integer(string ='Garage Included') 
    garden = fields.Float(string='Garden m^2')   
    bulding_sketch=fields.Image(string='Bulding sketch')
    attachments = fields.Many2many('ir.attachment', string = 'Real estate certificate')

    
    bulding_type = fields.Selection([
        ('internalf', 'Internal fixed assets'),
        ('internali', 'Internal investment assets'),
        ('external', 'External proprties'),
        ], string='Type')
    related_product = fields.Many2one('product.product')
    related_asset = fields.Many2one('account.asset')
    
    @api.model
    def create(self, vals):
        if vals['bulding_type'] == 'internali':
            product_info ={'name':vals['name']}
            vals['related_product'] = self.env['product.product'].create(product_info).id
        if vals['bulding_type'] == 'internalf':
            product_info ={'name':vals['name'], 'asset_type': 'purchase'}
            vals['related_asset'] = self.env['account.asset'].create(product_info).id
        result = super(Bulding,self).create(vals)
        return result  
    
  
    def unlink(self):
        for building in self:
            self.env['product.product'].browse(building.related_product.id).unlink()
            self.env['account.asset'].browse(building.related_asset.id).unlink()
        return super(Bulding,self).unlink() 
    

    
class MultiImage(models.Model):
    _inherit = "product.image"
    proprty_tmpl_id = fields.Many2one('rpi.unit', "Propprty Template", index=True, ondelete='cascade')
    name = fields.Char("Name", required=False)
    image_1920 = fields.Image(required=False)

    
   
    
    
class Unit(models.Model):
    _name = 'rpi.unit'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    def _get_default_currency_id(self):
        return self.env.company.currency_id.id
    proprty_template_image_ids = fields.One2many('product.image', 'proprty_tmpl_id', string="Extra Product Media", copy=True)
    currency_id = fields.Many2one("res.currency", string="Valuta", required=True, default = _get_default_currency_id)    
    name = fields.Char(string='Unit Name')
    bulding_id = fields.Many2one ('rpi.bulding',string = 'Bulding')
    owner = fields.Many2one ('res.partner' , string = 'Owner')
    region_id = fields.Many2one ('rpi.regions', string = 'Region')
    unit_stutes_id = fields.Many2one('rpi.building.stutes',string= 'Stutes')
   # active = fields.Boolean(string='Active')
    publish = fields.Boolean(string='Website published')
    rental_fee = fields.Monetary(string = 'Rental fee', currency_field="currency_id")
    insurance_fee = fields.Monetary(string = ' Insurance fee', currency_field="currency_id") 
    building_unit_area = fields.Float(string='Building unit Area m^2')
    net_area = fields.Float(string='Net Area m^2')
    land_area = fields.Float(string='Land Area m^2')
    construction_year = fields.Integer(string = 'Construction Year')
    lift = fields.Boolean (string='Lift')
    air_condition = fields.Selection([
        ('non', 'Non'),
        ('exist', 'Exist'),])
    no_rooms = fields.Integer(string ='Rooms')
    telephone = fields.Boolean (string = "Telephone")
    internet = fields.Boolean (string = "Internet")
    price = fields.Monetary(string = 'Price',currency_field="currency_id")
    floor = fields.Integer(string ='Floor')
    surface = fields.Integer(string ='Surface')
    garage = fields.Integer(string ='Garage Included') 
    garden = fields.Float(string='Garden m^2')
    balaconies = fields.Float(string='Balaconies m^2')
    solar = fields.Boolean (string='Solac Electric sustem')
    heating_source = fields.Selection([
        ('non', 'Non'),
        ('exist', 'Exist'),])
    electricity_meter = fields.Integer(string ='Electricity meter')
    water_meter = fields.Integer(string ='Water meter')
    license_code = fields.Char(string = 'License Code')
    license_date = fields.Datetime(string="License Date")
    date_notarization = fields.Datetime(string= 'Date added license notarization')
    license_notarization = fields.Char(string = 'License notarization')
    contacts = fields.Many2one ('res.partner' , string = 'Contacts')
    region_id = fields.Many2one ('rpi.regions', string = 'Region')
    city_id = fields.Many2one('rpi.cities', string = 'City')
    bulding_id = fields.Many2one('rpi.rpi', string = 'Bulding ')
    country_id = fields.Many2one('rpi.rpi', string = 'Country ')
    code = fields.Char(string='Code')
    unit_sketch=fields.Image( string='Unit sketch') 
    attachments = fields.Many2many('ir.attachment', string = 'Real estate certificate')
    unit_type = fields.Selection([
        ('internalf', 'Internal fixed assets'),
        ('internali', 'Internal investment assets'),
        ('external', 'External proprties'),
        ], string='Type')
    related_product = fields.Many2one('product.product')
    related_asset = fields.Many2one('account.asset')
    
    @api.model
    def create(self, vals):
        if vals['unit_type'] == 'internali':
            product_info ={'name':vals['name']}
            vals['related_product'] = self.env['product.product'].create(product_info).id
        if vals['unit_type'] == 'internalf':
            product_info ={'name':vals['name'], 'asset_type': 'purchase'}
            vals['related_asset'] = self.env['account.asset'].create(product_info).id
        result = super(Unit,self).create(vals)
        return result   
    
    def unlink(self):
        for unit in self:
            self.env['product.product'].browse(unit.related_product.id).unlink()
            self.env['account.asset'].browse(unit.related_asset.id).unlink()
        return super(Unit,self).unlink()    
    
class BuildingStatus(models.Model):
    _name = 'rpi.building.stutes'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Building Stutes'
    _order = 'sequence'
    bulding_stutes=fields.One2many('rpi.bulding','bulding_stutes_id',string='Stutes')
    unit_stutes= fields.One2many('rpi.unit','unit_stutes_id',string='Stutes')
    land_stutes= fields.One2many('rpi.land','land_stutes_id',string='Stutes')

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Type name already exists !"),
        
    ]    
    
    
    
    
    
class BuildingType(models.Model):
    _name = 'rpi.building.type'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Building Type'
    _order = 'sequence'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Type name already exists !"),
    ]