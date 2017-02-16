from openerp import api, models, fields


class StartStopThankyou(models.TransientModel):
    """ Settings configuration for thank you timeframe."""
    _name = 'account.gift.thanks'
    _inherit = 'res.config.settings'

    start_date = fields.Date(help='from included')
    stop_date = fields.Date(help='To include')


    @api.multi
    def set_start_date(self):
        self.env['ir.config_parameter'].set_param(
            'gift_start_date',
            self.start_date)

    @api.multi
    def set_stop_date(self):
        self.env['ir.config_parameter'].set_param(
            'gift_end_date',
            self.stop_date)
    @api.model
    def get_default_values(self, _fields):
        param_obj = self.env['ir.config_parameter']
        gift_start_date = (param_obj.get_param(
            'gift_start_date', '2017-01-01'))
        gift_end_date = (param_obj.get_param(
            'gift_end_date', '2017-01-31'))

        return {'start_date': gift_start_date,'stop_date': gift_end_date}