"""
Comprehensive Enterprise Resource Planning (ERP) System
Advanced business management platform with integrated modules
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import uuid

class ModuleType(Enum):
    FINANCIAL = "financial"
    HUMAN_RESOURCES = "human_resources"
    SUPPLY_CHAIN = "supply_chain"
    CUSTOMER_RELATIONSHIP = "customer_relationship"
    INVENTORY = "inventory"
    MANUFACTURING = "manufacturing"
    PROJECT_MANAGEMENT = "project_management"
    BUSINESS_INTELLIGENCE = "business_intelligence"
    COMPLIANCE = "compliance"
    ASSET_MANAGEMENT = "asset_management"

@dataclass
class ERPModule:
    module_id: str
    name: str
    type: ModuleType
    version: str
    status: str
    dependencies: List[str]
    configuration: Dict[str, Any]
    permissions: Dict[str, List[str]]

class FinancialModule:
    """Comprehensive Financial Management Module"""
    
    def __init__(self):
        self.accounts = {}
        self.transactions = []
        self.budgets = {}
        self.reports = {}
        
    def create_account(self, account_data: Dict) -> str:
        """Create new financial account"""
        account_id = str(uuid.uuid4())
        self.accounts[account_id] = {
            'id': account_id,
            'name': account_data['name'],
            'type': account_data['type'],  # asset, liability, equity, revenue, expense
            'balance': account_data.get('balance', 0),
            'currency': account_data.get('currency', 'USD'),
            'created_at': datetime.now(),
            'status': 'active'
        }
        return account_id
    
    def record_transaction(self, transaction_data: Dict) -> str:
        """Record financial transaction with double-entry bookkeeping"""
        transaction_id = str(uuid.uuid4())
        transaction = {
            'id': transaction_id,
            'date': transaction_data.get('date', datetime.now()),
            'description': transaction_data['description'],
            'reference': transaction_data.get('reference', ''),
            'entries': transaction_data['entries'],  # List of debit/credit entries
            'total_amount': sum(entry['amount'] for entry in transaction_data['entries']),
            'status': 'posted',
            'created_by': transaction_data.get('created_by', 'system')
        }
        
        # Validate double-entry (debits = credits)
        debits = sum(entry['amount'] for entry in transaction['entries'] if entry['type'] == 'debit')
        credits = sum(entry['amount'] for entry in transaction['entries'] if entry['type'] == 'credit')
        
        if abs(debits - credits) > 0.01:  # Allow for rounding
            raise ValueError("Transaction not balanced: debits != credits")
        
        # Update account balances
        for entry in transaction['entries']:
            account_id = entry['account_id']
            if account_id in self.accounts:
                if entry['type'] == 'debit':
                    self.accounts[account_id]['balance'] += entry['amount']
                else:
                    self.accounts[account_id]['balance'] -= entry['amount']
        
        self.transactions.append(transaction)
        return transaction_id
    
    def generate_financial_reports(self) -> Dict:
        """Generate comprehensive financial reports"""
        return {
            'balance_sheet': self._generate_balance_sheet(),
            'income_statement': self._generate_income_statement(),
            'cash_flow': self._generate_cash_flow(),
            'trial_balance': self._generate_trial_balance(),
            'aged_receivables': self._generate_aged_receivables(),
            'aged_payables': self._generate_aged_payables()
        }
    
    def _generate_balance_sheet(self) -> Dict:
        """Generate balance sheet"""
        assets = {k: v for k, v in self.accounts.items() if v['type'] == 'asset'}
        liabilities = {k: v for k, v in self.accounts.items() if v['type'] == 'liability'}
        equity = {k: v for k, v in self.accounts.items() if v['type'] == 'equity'}
        
        return {
            'assets': {
                'current_assets': sum(acc['balance'] for acc in assets.values() if 'current' in acc.get('subtype', '')),
                'fixed_assets': sum(acc['balance'] for acc in assets.values() if 'fixed' in acc.get('subtype', '')),
                'total_assets': sum(acc['balance'] for acc in assets.values())
            },
            'liabilities': {
                'current_liabilities': sum(acc['balance'] for acc in liabilities.values() if 'current' in acc.get('subtype', '')),
                'long_term_liabilities': sum(acc['balance'] for acc in liabilities.values() if 'long_term' in acc.get('subtype', '')),
                'total_liabilities': sum(acc['balance'] for acc in liabilities.values())
            },
            'equity': {
                'total_equity': sum(acc['balance'] for acc in equity.values())
            }
        }

class HumanResourcesModule:
    """Comprehensive Human Resources Management Module"""
    
    def __init__(self):
        self.employees = {}
        self.departments = {}
        self.positions = {}
        self.payroll = {}
        self.performance_reviews = {}
        self.training_programs = {}
        
    def create_employee(self, employee_data: Dict) -> str:
        """Create new employee record"""
        employee_id = str(uuid.uuid4())
        self.employees[employee_id] = {
            'id': employee_id,
            'personal_info': {
                'first_name': employee_data['first_name'],
                'last_name': employee_data['last_name'],
                'email': employee_data['email'],
                'phone': employee_data.get('phone', ''),
                'address': employee_data.get('address', {}),
                'emergency_contact': employee_data.get('emergency_contact', {})
            },
            'employment_info': {
                'employee_number': employee_data.get('employee_number', employee_id[:8]),
                'hire_date': employee_data['hire_date'],
                'department_id': employee_data['department_id'],
                'position_id': employee_data['position_id'],
                'manager_id': employee_data.get('manager_id'),
                'employment_type': employee_data.get('employment_type', 'full_time'),
                'status': 'active'
            },
            'compensation': {
                'salary': employee_data.get('salary', 0),
                'currency': employee_data.get('currency', 'USD'),
                'pay_frequency': employee_data.get('pay_frequency', 'monthly'),
                'benefits': employee_data.get('benefits', [])
            },
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        return employee_id
    
    def process_payroll(self, period_start: datetime, period_end: datetime) -> Dict:
        """Process payroll for specified period"""
        payroll_id = str(uuid.uuid4())
        payroll_data = {
            'id': payroll_id,
            'period_start': period_start,
            'period_end': period_end,
            'employee_payments': {},
            'total_gross': 0,
            'total_deductions': 0,
            'total_net': 0,
            'processed_at': datetime.now()
        }
        
        for emp_id, employee in self.employees.items():
            if employee['employment_info']['status'] == 'active':
                payment = self._calculate_employee_payment(employee, period_start, period_end)
                payroll_data['employee_payments'][emp_id] = payment
                payroll_data['total_gross'] += payment['gross_pay']
                payroll_data['total_deductions'] += payment['total_deductions']
                payroll_data['total_net'] += payment['net_pay']
        
        self.payroll[payroll_id] = payroll_data
        return payroll_data
    
    def _calculate_employee_payment(self, employee: Dict, start_date: datetime, end_date: datetime) -> Dict:
        """Calculate individual employee payment"""
        days_in_period = (end_date - start_date).days
        salary = employee['compensation']['salary']
        
        # Calculate gross pay based on pay frequency
        if employee['compensation']['pay_frequency'] == 'monthly':
            gross_pay = salary
        elif employee['compensation']['pay_frequency'] == 'bi_weekly':
            gross_pay = salary * 2
        else:  # weekly
            gross_pay = salary * 4
        
        # Calculate deductions
        deductions = {
            'tax': gross_pay * 0.2,  # Simplified tax calculation
            'social_security': gross_pay * 0.062,
            'medicare': gross_pay * 0.0145,
            'insurance': 200,  # Fixed insurance premium
            'retirement': gross_pay * 0.05
        }
        
        total_deductions = sum(deductions.values())
        net_pay = gross_pay - total_deductions
        
        return {
            'gross_pay': gross_pay,
            'deductions': deductions,
            'total_deductions': total_deductions,
            'net_pay': net_pay,
            'pay_period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        }

class SupplyChainModule:
    """Comprehensive Supply Chain Management Module"""
    
    def __init__(self):
        self.suppliers = {}
        self.purchase_orders = {}
        self.inventory_items = {}
        self.warehouses = {}
        self.shipments = {}
        
    def create_supplier(self, supplier_data: Dict) -> str:
        """Create new supplier record"""
        supplier_id = str(uuid.uuid4())
        self.suppliers[supplier_id] = {
            'id': supplier_id,
            'name': supplier_data['name'],
            'contact_info': supplier_data['contact_info'],
            'payment_terms': supplier_data.get('payment_terms', 'net_30'),
            'rating': supplier_data.get('rating', 0),
            'categories': supplier_data.get('categories', []),
            'status': 'active',
            'created_at': datetime.now()
        }
        return supplier_id
    
    def create_purchase_order(self, po_data: Dict) -> str:
        """Create purchase order"""
        po_id = str(uuid.uuid4())
        self.purchase_orders[po_id] = {
            'id': po_id,
            'po_number': po_data.get('po_number', f"PO-{po_id[:8]}"),
            'supplier_id': po_data['supplier_id'],
            'order_date': po_data.get('order_date', datetime.now()),
            'expected_delivery': po_data.get('expected_delivery'),
            'items': po_data['items'],
            'total_amount': sum(item['quantity'] * item['unit_price'] for item in po_data['items']),
            'status': 'pending',
            'created_by': po_data.get('created_by', 'system')
        }
        return po_id
    
    def track_shipment(self, shipment_id: str) -> Dict:
        """Track shipment status and location"""
        if shipment_id in self.shipments:
            shipment = self.shipments[shipment_id]
            # Simulate tracking updates
            tracking_info = {
                'shipment_id': shipment_id,
                'current_location': shipment.get('current_location', 'In Transit'),
                'status': shipment.get('status', 'shipped'),
                'estimated_delivery': shipment.get('estimated_delivery'),
                'tracking_history': shipment.get('tracking_history', [])
            }
            return tracking_info
        return {'error': 'Shipment not found'}

class CustomerRelationshipModule:
    """Comprehensive Customer Relationship Management Module"""
    
    def __init__(self):
        self.customers = {}
        self.leads = {}
        self.opportunities = {}
        self.interactions = {}
        self.campaigns = {}
        
    def create_customer(self, customer_data: Dict) -> str:
        """Create new customer record"""
        customer_id = str(uuid.uuid4())
        self.customers[customer_id] = {
            'id': customer_id,
            'name': customer_data['name'],
            'type': customer_data.get('type', 'individual'),  # individual, business
            'contact_info': customer_data['contact_info'],
            'preferences': customer_data.get('preferences', {}),
            'lifetime_value': 0,
            'status': 'active',
            'created_at': datetime.now(),
            'last_interaction': None
        }
        return customer_id
    
    def create_lead(self, lead_data: Dict) -> str:
        """Create new sales lead"""
        lead_id = str(uuid.uuid4())
        self.leads[lead_id] = {
            'id': lead_id,
            'name': lead_data['name'],
            'contact_info': lead_data['contact_info'],
            'source': lead_data.get('source', 'unknown'),
            'score': lead_data.get('score', 0),
            'status': 'new',
            'assigned_to': lead_data.get('assigned_to'),
            'created_at': datetime.now()
        }
        return lead_id
    
    def track_interaction(self, interaction_data: Dict) -> str:
        """Track customer interaction"""
        interaction_id = str(uuid.uuid4())
        self.interactions[interaction_id] = {
            'id': interaction_id,
            'customer_id': interaction_data['customer_id'],
            'type': interaction_data['type'],  # call, email, meeting, support
            'description': interaction_data['description'],
            'outcome': interaction_data.get('outcome'),
            'follow_up_required': interaction_data.get('follow_up_required', False),
            'created_by': interaction_data.get('created_by'),
            'created_at': datetime.now()
        }
        
        # Update customer last interaction
        customer_id = interaction_data['customer_id']
        if customer_id in self.customers:
            self.customers[customer_id]['last_interaction'] = datetime.now()
        
        return interaction_id

class ERPSystem:
    """Main ERP System Orchestrator"""
    
    def __init__(self):
        self.modules = {}
        self.users = {}
        self.permissions = {}
        self.audit_log = []
        self.system_config = {}
        
        # Initialize core modules
        self._initialize_modules()
    
    def _initialize_modules(self):
        """Initialize all ERP modules"""
        self.modules = {
            'financial': FinancialModule(),
            'hr': HumanResourcesModule(),
            'supply_chain': SupplyChainModule(),
            'crm': CustomerRelationshipModule(),
            'inventory': self._create_inventory_module(),
            'manufacturing': self._create_manufacturing_module(),
            'project_management': self._create_project_module(),
            'business_intelligence': self._create_bi_module(),
            'compliance': self._create_compliance_module(),
            'asset_management': self._create_asset_module()
        }
    
    def _create_inventory_module(self):
        """Create inventory management module"""
        return {
            'items': {},
            'locations': {},
            'movements': [],
            'stock_levels': {},
            'reorder_points': {},
            'abc_analysis': {}
        }
    
    def _create_manufacturing_module(self):
        """Create manufacturing module"""
        return {
            'work_orders': {},
            'bill_of_materials': {},
            'production_schedules': {},
            'quality_control': {},
            'machine_maintenance': {},
            'capacity_planning': {}
        }
    
    def _create_project_module(self):
        """Create project management module"""
        return {
            'projects': {},
            'tasks': {},
            'resources': {},
            'timesheets': {},
            'budgets': {},
            'milestones': {}
        }
 
(Content truncated due to size limit. Use line ranges to read in chunks)