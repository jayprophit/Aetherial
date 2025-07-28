"""
Enterprise Resource Planning (ERP) System
Comprehensive business management and resource planning platform
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import os
from decimal import Decimal
import hashlib
from pathlib import Path

class ERPModule(Enum):
    ACCOUNTING = "accounting"
    INVENTORY = "inventory"
    SALES = "sales"
    PURCHASING = "purchasing"
    MANUFACTURING = "manufacturing"
    HR = "hr"
    CRM = "crm"
    PROJECT_MANAGEMENT = "project_management"
    SUPPLY_CHAIN = "supply_chain"
    QUALITY_MANAGEMENT = "quality_management"
    ASSET_MANAGEMENT = "asset_management"
    BUSINESS_INTELLIGENCE = "business_intelligence"

class TransactionType(Enum):
    SALE = "sale"
    PURCHASE = "purchase"
    PAYMENT = "payment"
    RECEIPT = "receipt"
    JOURNAL = "journal"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"

class DocumentStatus(Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Company:
    id: str
    name: str
    legal_name: str
    tax_id: str
    address: Dict[str, str]
    contact_info: Dict[str, str]
    currency: str
    fiscal_year_start: datetime
    industry: str
    size: str
    settings: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class ChartOfAccounts:
    id: str
    company_id: str
    account_code: str
    account_name: str
    account_type: str
    parent_account_id: Optional[str]
    is_active: bool = True
    balance: Decimal = Decimal('0')
    description: Optional[str] = None

@dataclass
class Transaction:
    id: str
    company_id: str
    transaction_type: TransactionType
    reference_number: str
    date: datetime
    description: str
    total_amount: Decimal
    currency: str
    status: DocumentStatus
    created_by: str
    journal_entries: List[Dict[str, Any]] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Product:
    id: str
    company_id: str
    sku: str
    name: str
    description: str
    category: str
    unit_of_measure: str
    cost_price: Decimal
    selling_price: Decimal
    reorder_level: int
    max_stock_level: int
    current_stock: int = 0
    is_active: bool = True
    specifications: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Customer:
    id: str
    company_id: str
    customer_code: str
    name: str
    contact_person: str
    email: str
    phone: str
    address: Dict[str, str]
    credit_limit: Decimal
    payment_terms: str
    tax_id: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Supplier:
    id: str
    company_id: str
    supplier_code: str
    name: str
    contact_person: str
    email: str
    phone: str
    address: Dict[str, str]
    payment_terms: str
    tax_id: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Employee:
    id: str
    company_id: str
    employee_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    department: str
    position: str
    hire_date: datetime
    salary: Decimal
    employment_type: str
    manager_id: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Project:
    id: str
    company_id: str
    project_code: str
    name: str
    description: str
    client_id: str
    manager_id: str
    start_date: datetime
    end_date: datetime
    budget: Decimal
    status: str
    priority: Priority
    team_members: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

class ERP:
    """
    Enterprise Resource Planning System
    Comprehensive business management platform
    """
    
    def __init__(self, data_dir: str = "./erp_data"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "erp.db")
        
        # Initialize database
        os.makedirs(data_dir, exist_ok=True)
        self._init_database()
        
        # Module configurations
        self.modules = {
            ERPModule.ACCOUNTING: {
                "enabled": True,
                "features": ["general_ledger", "accounts_payable", "accounts_receivable", "financial_reporting"]
            },
            ERPModule.INVENTORY: {
                "enabled": True,
                "features": ["stock_management", "warehouse_management", "barcode_scanning", "lot_tracking"]
            },
            ERPModule.SALES: {
                "enabled": True,
                "features": ["quotations", "sales_orders", "invoicing", "customer_management"]
            },
            ERPModule.PURCHASING: {
                "enabled": True,
                "features": ["purchase_requests", "purchase_orders", "vendor_management", "receiving"]
            },
            ERPModule.MANUFACTURING: {
                "enabled": True,
                "features": ["bom_management", "production_planning", "work_orders", "quality_control"]
            },
            ERPModule.HR: {
                "enabled": True,
                "features": ["employee_management", "payroll", "attendance", "performance_management"]
            },
            ERPModule.CRM: {
                "enabled": True,
                "features": ["lead_management", "opportunity_tracking", "customer_service", "marketing"]
            },
            ERPModule.PROJECT_MANAGEMENT: {
                "enabled": True,
                "features": ["project_planning", "task_management", "time_tracking", "resource_allocation"]
            }
        }
        
        # Integration capabilities
        self.integrations = {
            "payment_gateways": ["stripe", "paypal", "square"],
            "shipping": ["fedex", "ups", "dhl"],
            "banks": ["plaid", "yodlee"],
            "ecommerce": ["shopify", "woocommerce", "magento"],
            "email": ["gmail", "outlook", "sendgrid"],
            "storage": ["aws_s3", "google_drive", "dropbox"]
        }
        
        # Reporting and analytics
        self.reporting_enabled = True
        self.real_time_analytics = True
        self.dashboard_enabled = True
        
        # Compliance and security
        self.audit_trail_enabled = True
        self.data_encryption_enabled = True
        self.role_based_access = True
    
    def _init_database(self):
        """Initialize SQLite database for ERP"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Companies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                legal_name TEXT NOT NULL,
                tax_id TEXT UNIQUE,
                address TEXT NOT NULL,
                contact_info TEXT NOT NULL,
                currency TEXT NOT NULL,
                fiscal_year_start DATE NOT NULL,
                industry TEXT,
                size TEXT,
                settings TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chart of accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chart_of_accounts (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                account_code TEXT NOT NULL,
                account_name TEXT NOT NULL,
                account_type TEXT NOT NULL,
                parent_account_id TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                balance DECIMAL(15, 2) DEFAULT 0,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                FOREIGN KEY (parent_account_id) REFERENCES chart_of_accounts (id),
                UNIQUE(company_id, account_code)
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                reference_number TEXT NOT NULL,
                date DATE NOT NULL,
                description TEXT NOT NULL,
                total_amount DECIMAL(15, 2) NOT NULL,
                currency TEXT NOT NULL,
                status TEXT NOT NULL,
                created_by TEXT NOT NULL,
                journal_entries TEXT,
                attachments TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                UNIQUE(company_id, reference_number)
            )
        ''')
        
        # Journal entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journal_entries (
                id TEXT PRIMARY KEY,
                transaction_id TEXT NOT NULL,
                account_id TEXT NOT NULL,
                debit_amount DECIMAL(15, 2) DEFAULT 0,
                credit_amount DECIMAL(15, 2) DEFAULT 0,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (transaction_id) REFERENCES transactions (id),
                FOREIGN KEY (account_id) REFERENCES chart_of_accounts (id)
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                sku TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                unit_of_measure TEXT NOT NULL,
                cost_price DECIMAL(10, 2) NOT NULL,
                selling_price DECIMAL(10, 2) NOT NULL,
                reorder_level INTEGER DEFAULT 0,
                max_stock_level INTEGER DEFAULT 0,
                current_stock INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                specifications TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                UNIQUE(company_id, sku)
            )
        ''')
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                customer_code TEXT NOT NULL,
                name TEXT NOT NULL,
                contact_person TEXT,
                email TEXT,
                phone TEXT,
                address TEXT NOT NULL,
                credit_limit DECIMAL(15, 2) DEFAULT 0,
                payment_terms TEXT,
                tax_id TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                UNIQUE(company_id, customer_code)
            )
        ''')
        
        # Suppliers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                supplier_code TEXT NOT NULL,
                name TEXT NOT NULL,
                contact_person TEXT,
                email TEXT,
                phone TEXT,
                address TEXT NOT NULL,
                payment_terms TEXT,
                tax_id TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                UNIQUE(company_id, supplier_code)
            )
        ''')
        
        # Employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                employee_id TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                hire_date DATE NOT NULL,
                salary DECIMAL(10, 2) NOT NULL,
                employment_type TEXT NOT NULL,
                manager_id TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                FOREIGN KEY (manager_id) REFERENCES employees (id),
                UNIQUE(company_id, employee_id)
            )
        ''')
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                project_code TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                client_id TEXT,
                manager_id TEXT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                budget DECIMAL(15, 2) NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                team_members TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                FOREIGN KEY (client_id) REFERENCES customers (id),
                FOREIGN KEY (manager_id) REFERENCES employees (id),
                UNIQUE(company_id, project_code)
            )
        ''')
        
        # Inventory movements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_movements (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                movement_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_cost DECIMAL(10, 2),
                reference_document TEXT,
                warehouse_location TEXT,
                notes TEXT,
                created_by TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Sales orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales_orders (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                order_number TEXT NOT NULL,
                customer_id TEXT NOT NULL,
                order_date DATE NOT NULL,
                delivery_date DATE,
                status TEXT NOT NULL,
                subtotal DECIMAL(15, 2) NOT NULL,
                tax_amount DECIMAL(15, 2) DEFAULT 0,
                total_amount DECIMAL(15, 2) NOT NULL,
                currency TEXT NOT NULL,
                notes TEXT,
                created_by TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id),
     
(Content truncated due to size limit. Use line ranges to read in chunks)