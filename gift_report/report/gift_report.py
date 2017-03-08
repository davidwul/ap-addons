# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: David Wulliamoz <dwulliamoz@compassion.ch>
#
#    The licence is in the file __openerp__.py
#
##############################################################################

from openerp import tools
from openerp import api, models,fields

        
class AccountGiftReport(models.Model):
    _name = "account.gift.report"
    _description = "Gift report for mail merge"
    _auto = False

    partner_id = fields.Many2one('res.partner', string='raison_sociale', readonly=True)
    # parent_id = fields.Many2one('res.partner', string='partner', related='partner_id.parent_id',readonly=True)
    raison_sociale = fields.Char(string='raison_sociale',related='partner_id.name')
    title_id = fields.Many2one('res.partner.title', string='titre-id', readonly=True)
    titre = fields.Char(string='titre',related='title_id.name')
    prenom = fields.Char(string='prenom', readonly=True)
    # nom = fields.Char(string='nom',related='partner_id.lastname')
    nom = fields.Char(string='nom', readonly=True)
    adresse = fields.Char(string='adresse', readonly=True)
    code_postal = fields.Char(string='code_postal', readonly=True)
    ville = fields.Char(readonly=True)
    country_id = fields.Many2one('res.country',string='pays', readonly=True)
    montant = fields.Float(readonly=True)
    liste_projets = fields.Char(readonly=True)
    compte_destinataire = fields.Char(readonly=True)
    projet1 = fields.Char(readonly=True)
    projet2 = fields.Char(readonly=True)
    projet3 = fields.Char(readonly=True)
    projet4 = fields.Char(readonly=True)
    projet5 = fields.Char(readonly=True)
    projet6 = fields.Char(readonly=True)
    projet7 = fields.Char(readonly=True)
    projet8 = fields.Char(readonly=True)
    projet9 = fields.Char(readonly=True)
    projet10 = fields.Char(readonly=True)

    def init(self, cr):
        # self._table = Account_Gift_Report
        print "refresh gift view"
        tools.drop_view_if_exists(cr, self._table)
        # self.env['ir.config_parameter'].get_param('gift_date')
        cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT
                    rp.id as id ,
                    case when is_company then id else parent_id end as partner_id ,
                    rp.firstname as prenom,
                    case when is_company then '' else rp.lastname end as nom ,
                    rp.title as title_id,
                    CASE WHEN rp.street ='' THEN rp.street2 ELSE rp.street END as adresse,rp.zip as code_postal,rp.city as ville,
                    rp.country_id,(SELECT SUM(s) FROM UNNEST(aml.montant) s) as montant,
                    '' as compte_destinataire,(SELECT string_agg(distinct s,',') FROM UNNEST(aml.projet) s) as liste_projets,
                    CASE WHEN aml.projet[1] IS NULL THEN '' ELSE concat(aml.projet[1], '(',aml.montant[1],')') END  as projet1,
                    CASE WHEN aml.projet[2] IS NULL THEN '' ELSE concat(aml.projet[2], '(',aml.montant[2],')') END  as projet2,
                    CASE WHEN aml.projet[3] IS NULL THEN '' ELSE concat(aml.projet[3], '(',aml.montant[3],')') END  as projet3,
                    CASE WHEN aml.projet[4] IS NULL THEN '' ELSE concat(aml.projet[4], '(',aml.montant[4],')') END  as projet4,
                    CASE WHEN aml.projet[5] IS NULL THEN '' ELSE concat(aml.projet[5], '(',aml.montant[5],')') END  as projet5,
                    CASE WHEN aml.projet[6] IS NULL THEN '' ELSE concat(aml.projet[6], '(',aml.montant[6],')') END  as projet6,
                    CASE WHEN aml.projet[7] IS NULL THEN '' ELSE concat(aml.projet[7], '(',aml.montant[7],')') END  as projet7,
                    CASE WHEN aml.projet[8] IS NULL THEN '' ELSE concat(aml.projet[8], '(',aml.montant[8],')') END  as projet8,
                    CASE WHEN aml.projet[9] IS NULL THEN '' ELSE concat(aml.projet[9], '(',aml.montant[9],')') END  as projet9,
                    CASE WHEN aml.projet[10] IS NULL THEN '' ELSE concat(aml.projet[10], '(',aml.montant[10],')') END  as projet10
            FROM res_partner rp
            inner join (
                    select 	aml.partner_id,account_id,array_agg(aml.credit) as montant,
                        array_agg(aaa.name) as projet
                    from account_move_line aml
                    left outer join account_analytic_account aaa on aaa.id=aml.analytic_account_id
                    where aml.date >= (SELECT value FROM public.ir_config_parameter where key='gift_start_date')::date
                    and aml.date <= (SELECT value FROM public.ir_config_parameter where key='gift_end_date')::date
                    group by aml.partner_id,aml.account_id
                    ) aml on aml.partner_id=rp.id
            where account_id=189
        )""" % (self._table))

