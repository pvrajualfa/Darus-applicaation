# Darus - School Management System

## Overview
Darus is a comprehensive school management desktop application built with Python and PySide6 (Qt6). It provides a complete solution for managing student information, financial transactions, fee collection, and reporting for educational institutions.

## Architecture & Technology Stack

### Core Technologies
- **Frontend**: PySide6 (Qt6 framework) for cross-platform desktop GUI
- **Database**: SQLite3 for local data storage
- **Reporting**: ReportLab for PDF generation
- **PDF Processing**: PyPDF2 for PDF manipulation
- **Python Version**: Compatible with Python 3.8+

### Project Structure
```
Darus/
├── main.py                 # Application entry point
├── backend.py              # Business logic and calculations
├── database.py             # Database operations and schema
├── ui2/                    # User interface modules
│   ├── mainwindow.py       # Main application window
│   ├── student_registration.py  # Student registration form
│   ├── vouchers.py         # Financial voucher management
│   ├── heads.py            # Income/expense heads management
│   ├── reports.py          # Comprehensive reporting system
│   └── common_form.py      # Reusable UI components
├── data/                   # Database storage directory
├── icons/                  # Application icons and assets
└── requirements.txt        # Python dependencies
```

## Core Modules & Functionality

### 1. Student Management System

#### Student Registration
- **Automated ID Generation**: Creates unique student IDs (S001, S002, etc.)
- **Comprehensive Data Capture**:
  - Personal information (name, father's name, Aadhaar, DOB)
  - Contact details (primary/secondary phone numbers)
  - Address information (location, city, full address)
  - Academic details (class, annual fees, joining date)
- **Data Validation**: 
  - 12-digit Aadhaar number validation
  - 10-digit phone number validation
  - Required field validation with visual feedback
- **CRUD Operations**: Create, read, update, and delete student records

#### Student List Management
- Searchable student database
- Quick access to student details
- Integration with fee payment system

### 2. Financial Management System

#### Voucher Entry System
- **Dual Transaction Types**: Income and Expense tracking
- **Hierarchical Categorization**:
  - Heads (main categories like "Tuition Fees", "Salary")
  - Sub-heads (sub-categories like "6th Grade Fees", "Teacher Salary")
- **Payment Methods**: Cash, Bank, UPI, PhonePe, GooglePay
- **Student-linked Transactions**: Automatic class population when student selected
- **Real-time Calculations**: EMI breakdown and balance tracking

#### EMI (Equated Monthly Installment) System
- **Automatic Fee Breakdown**: Divides annual fees into 12 monthly installments
- **Academic Year Calendar**: June to May academic schedule
- **Payment Tracking**: Monitors paid installments and remaining balance
- **Intelligent Allocation**: Automatically assigns payments to outstanding months

### 3. Heads & Sub-heads Management

#### Dynamic Category System
- **Income Heads**: Tuition fees, admission fees, transport fees, etc.
- **Expense Heads**: Salary, maintenance, utilities, supplies, etc.
- **Flexible Sub-categorization**: Create unlimited sub-heads under each main head
- **Duplicate Prevention**: Built-in constraints prevent duplicate entries
- **Real-time Updates**: Changes immediately reflected in voucher system

### 4. Comprehensive Reporting System

#### Financial Reports
- **Date-range Filtering**: Customizable reporting periods
- **Transaction Type Filtering**: Income, expense, or combined views
- **Summary Statistics**: Total income, expenses, and net balance
- **Detailed Transaction Lists**: Complete audit trail

#### Fee Management Reports
- **Student Fee Status**: Individual payment history
- **Outstanding Balances**: Real-time fee arrears tracking
- **Payment History**: Chronological payment records

#### Defaulter Reports
- **Overdue Fee Identification**: Students with outstanding payments
- **Contact Information**: Quick access to parent contact details
- **Prioritization**: Sort by amount overdue or duration

#### Collection Reports
- **Payment Method Analysis**: Cash vs digital payment breakdown
- **Period-wise Collections**: Daily, weekly, monthly collection trends
- **Revenue Tracking**: Income source analysis

#### SMS Integration
- **Contact List Generation**: Export parent contact numbers
- **Bulk Messaging Support**: CSV export for SMS campaigns
- **Targeted Communication**: Filter by class, fee status, or location

### 5. Advanced Features

#### User Experience
- **Modern UI Design**: Clean, professional interface with blue theme
- **Keyboard Navigation**: Tab-based form navigation with Enter key support
- **Responsive Layout**: Adapts to different screen sizes
- **Visual Feedback**: Color-coded buttons and validation indicators

#### Data Management
- **SQLite Database**: Reliable local data storage
- **Data Integrity**: Foreign key constraints and validation rules
- **Backup Support**: Database file location for manual backups
- **Export Capabilities**: CSV and PDF report generation

#### Security & Validation
- **Input Sanitization**: SQL injection prevention
- **Data Type Validation**: Numeric and format validation
- **Confirmation Dialogs**: Delete operations require confirmation
- **Error Handling**: Graceful error management with user feedback

## Business Logic Flow

### Student Registration Flow
1. New student ID auto-generated
2. Form completion with validation
3. Database insertion with unique constraints
4. Automatic update of voucher system student list
5. Report system refresh

### Fee Payment Flow
1. Student selection from dropdown
2. Automatic class population
3. Amount entry with EMI calculation
4. Payment method selection
5. Receipt generation option
6. Database record creation
7. Balance and EMI status update

### Reporting Flow
1. Report type selection from tabbed interface
2. Filter criteria application (dates, types, categories)
3. Database query execution
4. Data aggregation and calculation
5. Display in formatted table
6. Export to PDF/CSV option

## User Interface Design & Screens

### Design Philosophy
- **Modern Professional Theme**: Clean, intuitive interface with blue (#36ABD6) color scheme
- **Consistent Styling**: Unified design language across all components
- **Responsive Layout**: Adaptive design that works on various screen sizes
- **Accessibility-focused**: Keyboard navigation with Enter-to-Tab functionality

### Main Application Window

#### Header Section
- **Branding Header**: 140px height header with school/institution branding
- **Visual Identity**: Professional blue gradient background with logo placement
- **Navigation Breadcrumb**: Clear indication of current module/location

#### Sidebar Navigation (190px width)
- **Collapsible Student Menu**: 
  - Registration sub-item
  - Student List sub-item
  - Expandable/collapsible with visual indicators (▾/▴)
- **Quick Access Buttons**:
  - Vouchers Management
  - Heads & Sub-heads Configuration
  - Reports Center
  - Exit Application
- **Icon Integration**: Visual icons for each navigation item
- **Hover Effects**: Interactive feedback with color transitions

### Screen 1: Student Registration

#### Form Layout
- **Grid-based Form**: 2-column responsive layout with 13 input fields
- **Field Organization**:
  - **Personal Information**: ID (auto-generated), Name, Father's Name, Aadhaar
  - **Academic Details**: DOB, Join Date, Class Selection
  - **Contact Information**: Phone 1, Phone 2, Address, Location, City
  - **Financial Details**: Annual Fee

#### Input Validation & UX
- **Real-time Validation**: 
  - 12-digit Aadhaar format enforcement
  - 10-digit phone number validation
  - Required field highlighting with red borders
- **Smart Formatting**: Automatic capitalization of names and addresses
- **Focus Management**: Logical tab order with Enter key navigation
- **Visual Feedback**: Blue border focus states (#2F80ED)

#### Action Buttons
- **New**: Clear form and generate new student ID
- **Save**: Create/update student record with confirmation dialogs
- **Delete**: Remove student with confirmation prompt
- **Button Styling**: Consistent blue theme with hover effects

### Screen 2: Student List Management

#### Search & Filter Interface
- **Real-time Search**: Instant filtering as user types
- **Class Filter**: Dropdown to filter by specific grades (6th-10th)
- **Combined Filtering**: Search and class filter work simultaneously

#### Data Table Display
- **Professional Table**: Alternating row colors for readability
- **Sortable Columns**: Click headers to sort by any field
- **Centered Content**: All data centrally aligned for professional appearance
- **Column Headers**: ID, Class, Name, Father, Phone 1, Phone 2, Location, City
- **Double-click Action**: Direct edit access from table rows

#### Table Features
- **Stretch Columns**: Auto-resizing to fill available space
- **Bold Headers**: Clear visual hierarchy
- **Read-only Mode**: Prevent accidental data modification
- **Row Highlighting**: Hover effects for better UX

### Screen 3: Voucher Entry System

#### Transaction Form Layout
- **Date Selection**: Calendar popup with current date default (dd/MM/yyyy format)
- **Transaction Type**: Income/Expense dropdown with conditional field display
- **Hierarchical Selection**:
  - Head dropdown (populated based on type)
  - Sub-head dropdown (populated based on selected head)
- **Student Integration**:
  - Student dropdown (appears for income transactions)
  - Auto-populated class field (read-only)
  - Smart field visibility based on transaction type

#### Payment Processing
- **Amount Entry**: Numeric input with validation
- **Payment Methods**: Cash, Bank, UPI, PhonePe, GooglePay options
- **Notes Field**: Additional transaction details
- **Action Buttons**: Save, Print Receipt, New transaction

#### Transaction History Table
- **Comprehensive Columns**: Voucher No, Date, Type, Head, Sub, Name, Class, Amount, Mode, Description
- **Double-click Editing**: Load existing vouchers for modification
- **Real-time Updates**: Table refreshes after each transaction

### Screen 4: Heads & Sub-heads Management

#### Dual Entry Interface
- **Head Management Section**:
  - Type selection (Income/Expense)
  - Head name input with placeholder
  - Add Head button
- **Sub-head Management Section**:
  - Type selection (Income/Expense)
  - Parent head selection (dynamic dropdown)
  - Sub-head name input
  - Add Subhead button

#### Data Display Table
- **Mode Switching**: Toggle between heads and sub-heads view
- **Double-click Selection**: Load items for editing/deletion
- **Delete Functionality**: Remove selected items with confirmation
- **Real-time Updates**: Changes immediately reflect in voucher system

### Screen 5: Comprehensive Reports Center

#### Tabbed Interface
- **Professional Tabs**: Bold styling with active state indication
- **Five Report Modules**: Finance, Fees, Defaulters, Collection, SMS List

##### Finance Report Tab
- **Date Range Filters**: From/To date pickers with calendar popups
- **Type Filtering**: All/Income/Expense options
- **Summary Statistics**: Total income, expenses, net balance
- **Detailed Transaction Table**: Complete financial history
- **Export Options**: PDF generation for official documentation

##### Fee Management Tab
- **Student-wise Reports**: Individual fee payment history
- **Outstanding Balances**: Real-time fee arrears
- **Payment Status**: Clear indication of paid/unpaid installments
- **EMI Breakdown**: Monthly payment allocation details

##### Defaulters Report Tab
- **Overdue Identification**: Students with outstanding payments
- **Contact Information**: Quick access to parent phone numbers
- **Amount Sorting**: Prioritize by overdue amount
- **Export Capability**: Generate lists for follow-up actions

##### Collection Report Tab
- **Payment Analytics**: Breakdown by payment methods
- **Period Analysis**: Daily, weekly, monthly collection trends
- **Revenue Tracking**: Income source categorization
- **Visual Summaries**: Clear financial performance indicators

##### SMS List Tab
- **Contact Export**: Generate parent contact lists
- **Filtered Exports**: Target specific student groups
- **CSV Format**: Compatible with bulk SMS platforms
- **Communication Support**: Facilitate parent notifications

### UI Component Library

#### Common Form Elements
- **Input Fields**: 34px height with rounded corners (6px)
- **Focus States**: Blue border (#2F80ED) on focus
- **Dropdowns**: Consistent styling with hover effects
- **Date Pickers**: Calendar popup integration
- **Buttons**: Blue background (#36ABD6) with hover state (#1D4ED8)

#### Visual Design System
- **Color Palette**:
  - Primary Blue: #36ABD6
  - Hover Blue: #1D4ED8
  - Pressed Blue: #0F3D91
  - Focus Blue: #2F80ED
  - Background: #F8FAFC
  - Sidebar: #EEF2FF
- **Typography**: Segoe UI, Arial font family, 13px base size
- **Spacing**: Consistent 6px padding, 12px spacing between elements
- **Border Radius**: 6px for form elements, 10px for group boxes

#### Interactive Elements
- **Hover Effects**: Smooth color transitions on all interactive elements
- **Pressed States**: Visual feedback for button clicks
- **Loading States**: Progress indication during data operations
- **Error States**: Red border highlighting for validation errors
- **Success Messages**: Confirmation dialogs for completed actions

### Accessibility Features
- **Keyboard Navigation**: Full keyboard accessibility with Tab navigation
- **Enter Key Support**: Enter key behaves as Tab for form progression
- **Focus Indicators**: Clear visual focus states for all interactive elements
- **High Contrast**: Sufficient color contrast for readability
- **Screen Reader Support**: Semantic HTML structure for assistive technologies

## Technical Implementation Details

### Database Schema
- **Students Table**: 14 fields including personal, academic, and financial data
- **Heads Table**: Hierarchical category system with type and name fields
- **Sub-heads Table**: Linked to heads with foreign key relationships
- **Vouchers Table**: Complete transaction history with 10 fields

### Signal-Slot Architecture
- **Qt Signals**: Inter-module communication for real-time updates
- **Event-driven Updates**: Student additions trigger voucher and report refreshes
- **Decoupled Design**: Modules communicate through well-defined interfaces

### PDF Generation
- **ReportLab Integration**: Professional PDF report creation
- **Formatted Tables**: Structured data presentation
- **Styling**: Consistent branding and layout
- **Multiple Report Types**: Receipts, statements, and analytical reports

## Deployment & Distribution

### Build System
- **PyInstaller Configuration**: Darus.spec for executable creation
- **Single File Option**: Darus_single.py for standalone distribution
- **Resource Management**: Icons and assets bundled in executable

### Cross-platform Compatibility
- **Windows Primary**: Optimized for Windows deployment
- **Qt Framework**: Theoretically supports Linux and macOS
- **Self-contained**: No external dependencies beyond Python runtime

## Key Benefits

### For Administrators
- **Centralized Management**: Single system for all administrative tasks
- **Real-time Insights**: Current financial status and student information
- **Automated Calculations**: EMI and balance calculations eliminate manual errors
- **Professional Reporting**: Generate official documents and reports

### For Students & Parents
- **Transparent Fee Structure**: Clear payment schedules and history
- **Professional Receipts**: Official payment documentation
- **Accurate Records**: Reliable academic and financial records

### For Institutions
- **Scalable Solution**: Handles growing student populations
- **Data Security**: Local database storage ensures data privacy
- **Cost Effective**: No subscription fees or cloud dependencies
- **Customizable**: Adaptable to specific institutional requirements

## Future Enhancement Potential

### Possible Extensions
- **Multi-user Support**: Role-based access control
- **Cloud Synchronization**: Remote data backup and multi-campus support
- **Mobile Application**: Companion app for parents and students
- **Advanced Analytics**: Predictive fee collection and trend analysis
- **Integration APIs**: Connection to accounting software and government systems

### Technical Improvements
- **Database Migration**: PostgreSQL for enterprise deployment
- **Web Interface**: Browser-based access option
- **Automated Backups**: Scheduled data protection
- **Audit Logging**: Comprehensive change tracking

## Conclusion

Darus represents a mature, well-architected school management solution that combines modern GUI design with robust backend functionality. Its modular architecture, comprehensive feature set, and attention to user experience make it suitable for small to medium-sized educational institutions seeking an efficient, cost-effective management system.

The application demonstrates strong software engineering principles including separation of concerns, data validation, error handling, and maintainable code structure. Its use of established technologies like Qt6 and SQLite ensures reliability and performance while keeping the solution accessible and deployable across different environments.
