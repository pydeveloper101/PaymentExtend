
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class account_payment(models.Model):
    _inherit = "account.payment"
    
    @api.depends('line_cr_ids.amount_allocation','line_dr_ids.amount_allocation')
    def _get_writeoff_amount(self):
        # changes done by DJ 03/08/2018
        currency_obj = self.env['res.currency']
        if self.line_dr_ids:
            debit = 0.0
            for s in self:
                sign = s.payment_type == 'outbound' and -1 or 1
                for l in s.line_dr_ids:
                    debit += l.amount_allocation
                if s.currency_id == s.company_id.currency_id:
                    s.writeoff_amount = s.amount - (sign * debit)
                else:
                    s.writeoff_amount = s.amount - s.company_id.currency_id.compute(sign * debit,s.currency_id)
        if self.line_cr_ids:
            credit = 0.0
            for s in self:
                sign = s.payment_type == 'outbound' and -1 or 1
                for l in s.line_cr_ids:
                    credit += l.amount_allocation
                if s.currency_id == s.company_id.currency_id:
                    s.writeoff_amount = s.amount - (sign * credit)
                else:
                    s.writeoff_amount = s.amount - s.company_id.currency_id.compute(sign * credit,s.currency_id)
            #this code is commented by dj
            # if s.currency_id == s.company_id.currency_id:
            #     s.writeoff_amount = s.amount - sign * (credit - debit)
            # else:
            #     s.writeoff_amount = s.amount - s.company_id.currency_id.compute(sign *(credit - debit),s.currency_id )
                    
                    
    line_cr_ids = fields.One2many('account.payment.line','payment_cr_id',string='Credits')
    line_dr_ids = fields.One2many('account.payment.line','payment_dr_id','Debits')
    writeoff_amount = fields.Float(compute='_get_writeoff_amount', string='Difference Amount', readonly=True, help="Computed as the difference between the amount stated in the voucher and the sum of allocation on the voucher lines.")  
    payment_option = fields.Selection([('without_writeoff', 'Keep Open'),
                                       ('with_writeoff', 'Reconcile Payment Balance'),
                                        ], 'Payment Difference',default='without_writeoff', help="This field helps you to choose what you want to do with the eventual difference between the paid amount and the sum of allocated amounts. You can either choose to keep open this difference on the partner's account, or reconcile it with the payment(s)")
         
    writeoff_acc_id = fields.Many2one('account.account', string='Counterpart Account')
    writeoff_comment =  fields.Char(string='Counterpart Comment')

#     @api.onchange('amount','line_dr_ids','line_cr_ids')
#     def onchange_amount(self):
#         if self.payment_type == 'inbound':
    #         if self.currency_id != self.company_id.currency_id:
    #             print"we are in inbound value======>>>> "
    #             dremain = sum(crl.amount_unreconciled for crl in self.line_cr_ids if self.line_cr_ids)
    #             print"Amount reamin ====dremain==>>>>",dremain
    #             for dline in self.line_dr_ids:
    #                 if dline.amount_unreconciled <= dremain:
    #                     dline.amount_allocation = dline.amount_unreconciled
    #                     dremain -= dline.amount_allocation
    #                 else:
    #                     dline.amount_allocation = dremain
    #                     dremain -= dline.amount_allocation
    #                 dline.onchange_amount_allocation()
    #                 dline.onchange_full_allocation()
#                 total = 0.0
#                 remain = self.currency_id.compute(self.amount, self.company_id.currency_id) + sum(drl.amount_allocation for drl in self.line_dr_ids if self.line_dr_ids)
#                 for line in self.line_cr_ids:
#                     if line.amount_unreconciled <= remain:
#                         line.amount_allocation = line.amount_unreconciled
#                         remain -= line.amount_allocation
#                     else:
#                         line.amount_allocation = remain
#                         remain -= line.amount_allocation
# 
#                     total += line.amount_allocation
#     #
#                     line.onchange_amount_allocation()
#                     line.onchange_full_allocation()
    #         else:
    #             dremain = sum(crle.amount_unreconciled for crle in self.line_cr_ids if self.line_cr_ids)
    #             for dline in self.line_dr_ids:
    #                 if dline.amount_unreconciled <= dremain:
    #                     dline.amount_allocation = dline.amount_unreconciled
    #                     dremain -= dline.amount_allocation
    #                 else:
    #                     dline.amount_allocation = dremain
    #                     dremain -= dline.amount_allocation
    #                 dline.onchange_amount_allocation()
    #                 dline.onchange_full_allocation()
    #             total = 0.0
    #             remain = self.amount + sum(drl.amount_allocation for drl in self.line_dr_ids if self.line_dr_ids)
    #             for line in self.line_cr_ids:
    #                 if line.amount_unreconciled <= remain:
    #                     line.amount_allocation = line.amount_unreconciled
    #                     remain -= line.amount_allocation
    #                 else:
    #                     line.amount_allocation = remain
    #                     remain -= line.amount_allocation
    #
    #                 total += line.amount_allocation
    #
    #                 line.onchange_amount_allocation()
    #                 line.onchange_full_allocation()
    #
#         elif self.payment_type == 'outbound':
    #         if self.currency_id != self.company_id.currency_id:
    #             dremain = sum(drl.amount_unreconciled for drl in self.line_dr_ids if self.line_dr_ids)
    #             for dline in self.line_cr_ids:
    #                 if dline.amount_unreconciled <= dremain:
    #                     dline.amount_allocation = dline.amount_unreconciled
    #                     dremain -= dline.amount_allocation
    #                 else:
    #                     dline.amount_allocation = dremain
    #                     dremain -= dline.amount_allocation
    #                 dline.onchange_amount_allocation()
    #                 dline.onchange_full_allocation()
    #
#                 total = 0.0
#                 remain = self.currency_id.compute(self.amount, self.company_id.currency_id) + sum(cr.amount_allocation for cr in self.line_cr_ids if self.line_cr_ids)
#                 for line in self.line_dr_ids:
#                     if line.amount_unreconciled <= remain:
#                         line.amount_allocation = line.amount_unreconciled
#                         remain -= line.amount_allocation
#                     else:
#                         line.amount_allocation = remain
#                         remain -= line.amount_allocation
# 
#                     total += line.amount_allocation
#                     line.onchange_amount_allocation()
#                     line.onchange_full_allocation()
    #         else:
    #             dremain = sum(drl.amount_unreconciled for drl in self.line_dr_ids if self.line_dr_ids)
    #             for dline in self.line_cr_ids:
    #                 if dline.amount_unreconciled <= dremain:
    #                     dline.amount_allocation = dline.amount_unreconciled
    #                     dremain -= dline.amount_allocation
    #                 else:
    #                     dline.amount_allocation = dremain
    #                     dremain -= dline.amount_allocation
    #                 dline.onchange_amount_allocation()
    #                 dline.onchange_full_allocation()
    #
    #             total = 0.0
    #             remain = self.amount + sum(cr.amount_allocation for cr in self.line_cr_ids if self.line_cr_ids)
    #             for line in self.line_dr_ids:
    #                 if line.amount_unreconciled <= remain:
    #                     line.amount_allocation = line.amount_unreconciled
    #                     remain -= line.amount_allocation
    #                 else:
    #                     line.amount_allocation = remain
    #                     remain -= line.amount_allocation
    #
    #                 total += line.amount_allocation
    #                 line.onchange_amount_allocation()
    #                 line.onchange_full_allocation()
     
    @api.onchange('partner_id')
    def onchange_partner_id_li_cr_dr(self): 
        if self.partner_id:
            if self.payment_type == 'outbound':
                move_line_pay = self.env['account.move.line'].search([('partner_id','=',self.partner_id.id),
                                                              ('reconciled', '=', False),('account_id','=',self.partner_id.property_account_payable_id.id)])
            
                lst_p_lines = {}
                lst_p_lin = [(6,0,[])]
                lst_d_plines = {}
                lstd_p_lin = [(6,0,[])]
                if move_line_pay:
                    for p in move_line_pay[::-1]:
                        if p.credit > 0.00:
                            lst_p_lines = {'move_line_id':p.id,
                                                    'account_id':p.account_id.id,
                                                    'date_original': p.date,
                                                    'date_due': p.date_maturity,
                                                    'amount_original': p.credit,
                                                    'amount_unreconciled': abs(p.amount_residual),
                                                    }
                            lst_p_lin.append((0,0,lst_p_lines))
#                         else:
#                             lst_d_plines = {'move_line_id':p.id,
#                                         'account_id':p.account_id.id,
#                                         'date_original': p.date,
#                                         'date_due': p.date_maturity,
#                                         'amount_original': p.debit,
#                                         'amount_unreconciled': abs(p.amount_residual),
#                                         }
#                             lstd_p_lin.append((0,0,lst_d_plines))
                self.line_dr_ids = lst_p_lin
#                 self.line_cr_ids = lstd_p_lin
            
            elif self.payment_type == 'inbound':    
                move_line_rec = self.env['account.move.line'].search([('partner_id','=',self.partner_id.id),
                                                              ('reconciled', '=', False),('account_id','=',self.partner_id.property_account_receivable_id.id)])
                lcrdrnes = {}
                lst_lincr = [(6,0,[])]
                lstcr_lines = {}
                lst_lindrre = [(6,0,[])]
                if move_line_rec:
                    for r in move_line_rec[::-1]:
                        if r.debit > 0.00:
                            lcrdrnes = {'move_line_id':r.id,
                                            'account_id':r.account_id.id,
                                            'date_original': r.date,
                                            'date_due': r.date_maturity,
                                            'amount_original': r.debit,
                                            'amount_unreconciled': abs(r.amount_residual),
                                            }
                            lst_lincr.append((0,0,lcrdrnes))
#                         else:
#                             lstcr_lines = {'move_line_id':r.id,
#                                                     'account_id':r.account_id.id,
#                                                     'date_original': r.date,
#                                                     'date_due': r.date_maturity,
#                                                     'amount_original': r.credit,
#                                                     'amount_unreconciled': abs(r.amount_residual),
#                                                     }
#                             lst_lindrre.append((0,0,lstcr_lines))
                self.line_cr_ids = lst_lincr
#                 self.line_dr_ids = lst_lindrre
   
            
    @api.multi
    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconciliable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted. Trying to post a payment in state %s.") % rec.state)

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # Use the right sequence to set the name
            if rec.payment_type == 'transfer':
                sequence_code = 'account.payment.transfer'
            else:
                if rec.partner_type == 'customer':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.customer.invoice'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.customer.refund'
                if rec.partner_type == 'supplier':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.supplier.refund'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.supplier.invoice'
            rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
            if not rec.name and rec.payment_type != 'transfer':
                raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()

            rec.write({'state': 'posted', 'move_name': move.name}) 
            if rec.payment_type in ['inbound', 'outbound']:
                if sum(line.amount_allocation for line in rec.line_cr_ids if rec.line_cr_ids) == rec.amount + sum(dr.amount_allocation for dr in rec.line_dr_ids if rec.line_dr_ids):
                    move_lines = []
                    move_lines = move.line_ids[1]
                    if rec.line_dr_ids:
                        for dr in rec.line_dr_ids.filtered(lambda r:r.amount_allocation):
                            move_lines |= dr.move_line_id
                    if rec.line_cr_ids:
                        for cr in rec.line_cr_ids.filtered(lambda r:r.amount_allocation):
                            move_lines |= cr.move_line_id
                    currency = False
                    for aml in move_lines:
                        if not currency and aml.currency_id.id:
                            currency = aml.currency_id.id
                        elif aml.currency_id:
                            if aml.currency_id.id == currency:
                                continue
                            raise UserError(_('Operation not allowed. You can only reconcile entries that share the same secondary currency or that don\'t have one. Edit your journal items or make another selection before proceeding any further.'))
                    #Don't consider entrires that are already reconciled
                    move_lines_filtered = move_lines.filtered(lambda aml: not aml.reconciled)
                    #Because we are making a full reconcilition in batch, we need to consider use cases as defined in the test test_manual_reconcile_wizard_opw678153
                    #So we force the reconciliation in company currency only at first
                    move_lines_filtered.with_context(skip_full_reconcile_check='amount_currency_excluded', manual_full_reconcile_currency=currency).reconcile()
                    #then in second pass the amounts in secondary currency, only if some lines are still not fully reconciled
                    move_lines_filtered = move_lines.filtered(lambda aml: not aml.reconciled)
                    if move_lines_filtered:
                        move_lines_filtered.with_context(skip_full_reconcile_check='amount_currency_only', manual_full_reconcile_currency=currency).reconcile()
                    move_lines.compute_full_after_batch_reconcile()
                else:
                    move_line = move.line_ids[1]
                    if rec.line_dr_ids:
                        for dr in rec.line_dr_ids.filtered(lambda r:r.amount_allocation):
                            move_line |= dr.move_line_id
                    if rec.line_cr_ids:
                        for cr in rec.line_cr_ids.filtered(lambda r:r.amount_allocation):
                            move_line |= cr.move_line_id
                    move_line.reconcile()
                  
    def _get_counterpart_move_line_vals(self, invoice=False):
        rest = super(account_payment, self)._get_counterpart_move_line_vals()
        if self.payment_option == 'with_writeoff':
           rest.update({'account_id': self.writeoff_acc_id.id,'name': self.writeoff_comment}) 
        return rest   
                     
class account_payment_line(models.Model):
    _name = "account.payment.line" 
    
    payment_cr_id = fields.Many2one('account.payment', 'Payment Cr')
    payment_dr_id = fields.Many2one('account.payment', 'Payment Dr')
    name = fields.Char('Description')
    account_id = fields.Many2one('account.account',string='Account', required=True)
    partner_id = fields.Many2one(related='payment_cr_id.partner_id', string='Partner')
    untax_amount = fields.Float('Untax Amount')
    full_allocation = fields.Boolean('Full Allocation')
    reconcile = fields.Boolean('Full Reconcile')
    type = fields.Selection([('dr','Debit'),('cr','Credit')], string='Dr/Cr',store=True)
    state = fields.Selection([('draft', 'Draft'), ('posted', 'Posted'), ('sent', 'Sent'), ('reconciled', 'Reconciled')],related="payment_cr_id.state", readonly=True, default='draft', copy=False, string="Status")

    account_analytic_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    move_line_id = fields.Many2one('account.move.line', string='Journal Item', copy=False)
    date_original = fields.Date(relation='move_line_id.date', string='Date', readonly=1)
    date_due = fields.Date(relation='move_line_id.date_maturity', string='Due Date', readonly=1)
    amount_original = fields.Float(string='Original Amount', store=True)
    amount_allocation = fields.Float(string=' Allocation', store=True)#store= True Removed by DJ
    company_id = fields.Many2one(relation='payment_cr_id.company_id', string='Company', store=True, readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    amount_unreconciled= fields.Float(store=True, string='Open Balance')
    
    @api.multi
    @api.onchange('amount_allocation','amount_original')
    def onchange_amount_allocation(self):
        if self.amount_allocation > 0 and self.amount_allocation == self.amount_unreconciled:
            self.full_allocation = True
        else:
            self.full_allocation = False


    
    @api.multi
    @api.onchange('full_allocation')
    def onchange_full_allocation(self):
        if self.full_allocation:
            self.amount_allocation = self.amount_unreconciled
    
class account_abstract_payment(models.AbstractModel):
    _inherit = "account.abstract.payment"
    
    
    @api.one
    @api.constrains('amount')
    def _check_amount(self):
        if self.amount <= 0.0 and not self.line_dr_ids and  not self.line_cr_ids:
            raise ValidationError(_('The payment amount must be strictly positive.'))
