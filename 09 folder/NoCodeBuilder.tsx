import React, { useState, useEffect, useRef } from 'react';
import {
  Plus,
  Code,
  Eye,
  EyeOff,
  Save,
  Play,
  Square,
  Settings,
  Layers,
  Database,
  Zap,
  Globe,
  Smartphone,
  Monitor,
  Tablet,
  Download,
  Upload,
  Copy,
  Trash2,
  Edit,
  Move,
  RotateCcw,
  RotateCw,
  AlignLeft,
  AlignCenter,
  AlignRight,
  Bold,
  Italic,
  Underline,
  Type,
  Image,
  Video,
  Music,
  FileText,
  Link,
  Mail,
  Phone,
  Calendar,
  MapPin,
  ShoppingCart,
  CreditCard,
  Users,
  MessageCircle,
  Bell,
  Search,
  Filter,
  Sort,
  Grid,
  List,
  BarChart,
  PieChart,
  LineChart,
  Table,
  Form,
  Button,
  Input,
  Checkbox,
  Radio,
  Select,
  Textarea,
  Slider,
  Toggle,
  DatePicker,
  TimePicker,
  ColorPicker,
  FileUpload,
  DropdownMenu,
  Modal,
  Tooltip,
  Badge,
  Avatar,
  Card,
  Tabs,
  Accordion,
  Carousel,
  Gallery,
  Map,
  Chart,
  Progress,
  Spinner,
  Alert,
  Breadcrumb,
  Pagination,
  Navigation,
  Sidebar,
  Header,
  Footer,
  Container,
  Row,
  Column,
  Spacer,
  Divider
} from 'lucide-react';

interface NoCodeBuilderProps {
  mode: 'visual' | 'code' | 'hybrid';
  platform: 'web' | 'mobile' | 'desktop';
}

interface Component {
  id: string;
  type: string;
  name: string;
  props: Record<string, any>;
  children?: Component[];
  style?: Record<string, any>;
  events?: Record<string, string>;
  code?: string;
}

interface Workflow {
  id: string;
  name: string;
  trigger: string;
  actions: WorkflowAction[];
  conditions?: WorkflowCondition[];
}

interface WorkflowAction {
  id: string;
  type: string;
  config: Record<string, any>;
  code?: string;
}

interface WorkflowCondition {
  id: string;
  field: string;
  operator: string;
  value: any;
  code?: string;
}

const NoCodeBuilder: React.FC<NoCodeBuilderProps> = ({ mode, platform }) => {
  const [currentMode, setCurrentMode] = useState<'visual' | 'code' | 'hybrid'>(mode);
  const [selectedComponent, setSelectedComponent] = useState<Component | null>(null);
  const [components, setComponents] = useState<Component[]>([]);
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [activeTab, setActiveTab] = useState<'design' | 'data' | 'logic' | 'deploy'>('design');
  const [previewMode, setPreviewMode] = useState(false);
  const [codeEditor, setCodeEditor] = useState('');
  const [databases, setDatabases] = useState<any[]>([]);
  const [apis, setApis] = useState<any[]>([]);
  const [deploymentConfig, setDeploymentConfig] = useState<any>({});

  // Component library organized by categories
  const componentLibrary = {
    'Layout': [
      { type: 'container', name: 'Container', icon: Container, description: 'Responsive container' },
      { type: 'row', name: 'Row', icon: Row, description: 'Horizontal layout' },
      { type: 'column', name: 'Column', icon: Column, description: 'Vertical layout' },
      { type: 'grid', name: 'Grid', icon: Grid, description: 'CSS Grid layout' },
      { type: 'spacer', name: 'Spacer', icon: Spacer, description: 'Empty space' },
      { type: 'divider', name: 'Divider', icon: Divider, description: 'Visual separator' }
    ],
    'Navigation': [
      { type: 'header', name: 'Header', icon: Header, description: 'Page header' },
      { type: 'navbar', name: 'Navigation Bar', icon: Navigation, description: 'Main navigation' },
      { type: 'sidebar', name: 'Sidebar', icon: Sidebar, description: 'Side navigation' },
      { type: 'footer', name: 'Footer', icon: Footer, description: 'Page footer' },
      { type: 'breadcrumb', name: 'Breadcrumb', icon: Breadcrumb, description: 'Navigation path' },
      { type: 'pagination', name: 'Pagination', icon: Pagination, description: 'Page navigation' }
    ],
    'Forms': [
      { type: 'form', name: 'Form', icon: Form, description: 'Form container' },
      { type: 'input', name: 'Text Input', icon: Input, description: 'Text input field' },
      { type: 'textarea', name: 'Text Area', icon: Textarea, description: 'Multi-line text' },
      { type: 'select', name: 'Select', icon: Select, description: 'Dropdown selection' },
      { type: 'checkbox', name: 'Checkbox', icon: Checkbox, description: 'Checkbox input' },
      { type: 'radio', name: 'Radio Button', icon: Radio, description: 'Radio selection' },
      { type: 'button', name: 'Button', icon: Button, description: 'Action button' },
      { type: 'slider', name: 'Slider', icon: Slider, description: 'Range slider' },
      { type: 'toggle', name: 'Toggle', icon: Toggle, description: 'Switch toggle' },
      { type: 'datepicker', name: 'Date Picker', icon: DatePicker, description: 'Date selection' },
      { type: 'timepicker', name: 'Time Picker', icon: TimePicker, description: 'Time selection' },
      { type: 'colorpicker', name: 'Color Picker', icon: ColorPicker, description: 'Color selection' },
      { type: 'fileupload', name: 'File Upload', icon: FileUpload, description: 'File upload' }
    ],
    'Content': [
      { type: 'text', name: 'Text', icon: Type, description: 'Text content' },
      { type: 'heading', name: 'Heading', icon: Type, description: 'Heading text' },
      { type: 'paragraph', name: 'Paragraph', icon: FileText, description: 'Paragraph text' },
      { type: 'image', name: 'Image', icon: Image, description: 'Image display' },
      { type: 'video', name: 'Video', icon: Video, description: 'Video player' },
      { type: 'audio', name: 'Audio', icon: Music, description: 'Audio player' },
      { type: 'link', name: 'Link', icon: Link, description: 'Hyperlink' },
      { type: 'icon', name: 'Icon', icon: Zap, description: 'Icon display' }
    ],
    'Data Display': [
      { type: 'table', name: 'Table', icon: Table, description: 'Data table' },
      { type: 'list', name: 'List', icon: List, description: 'Item list' },
      { type: 'card', name: 'Card', icon: Card, description: 'Content card' },
      { type: 'barchart', name: 'Bar Chart', icon: BarChart, description: 'Bar chart' },
      { type: 'piechart', name: 'Pie Chart', icon: PieChart, description: 'Pie chart' },
      { type: 'linechart', name: 'Line Chart', icon: LineChart, description: 'Line chart' },
      { type: 'progress', name: 'Progress Bar', icon: Progress, description: 'Progress indicator' },
      { type: 'badge', name: 'Badge', icon: Badge, description: 'Status badge' },
      { type: 'avatar', name: 'Avatar', icon: Avatar, description: 'User avatar' }
    ],
    'Interactive': [
      { type: 'tabs', name: 'Tabs', icon: Tabs, description: 'Tab navigation' },
      { type: 'accordion', name: 'Accordion', icon: Accordion, description: 'Collapsible content' },
      { type: 'carousel', name: 'Carousel', icon: Carousel, description: 'Image carousel' },
      { type: 'gallery', name: 'Gallery', icon: Gallery, description: 'Image gallery' },
      { type: 'modal', name: 'Modal', icon: Modal, description: 'Popup modal' },
      { type: 'tooltip', name: 'Tooltip', icon: Tooltip, description: 'Hover tooltip' },
      { type: 'dropdown', name: 'Dropdown', icon: DropdownMenu, description: 'Dropdown menu' },
      { type: 'alert', name: 'Alert', icon: Alert, description: 'Alert message' }
    ],
    'E-commerce': [
      { type: 'product-card', name: 'Product Card', icon: ShoppingCart, description: 'Product display' },
      { type: 'cart', name: 'Shopping Cart', icon: ShoppingCart, description: 'Shopping cart' },
      { type: 'checkout', name: 'Checkout Form', icon: CreditCard, description: 'Payment form' },
      { type: 'price', name: 'Price Display', icon: CreditCard, description: 'Price component' }
    ],
    'Social': [
      { type: 'user-profile', name: 'User Profile', icon: Users, description: 'User profile card' },
      { type: 'comment', name: 'Comment', icon: MessageCircle, description: 'Comment component' },
      { type: 'social-share', name: 'Social Share', icon: Globe, description: 'Social sharing' },
      { type: 'notification', name: 'Notification', icon: Bell, description: 'Notification item' }
    ],
    'Maps & Location': [
      { type: 'map', name: 'Map', icon: Map, description: 'Interactive map' },
      { type: 'location', name: 'Location', icon: MapPin, description: 'Location display' }
    ],
    'Advanced': [
      { type: 'code-block', name: 'Code Block', icon: Code, description: 'Custom code' },
      { type: 'api-connector', name: 'API Connector', icon: Zap, description: 'API integration' },
      { type: 'database-query', name: 'Database Query', icon: Database, description: 'Database connection' },
      { type: 'workflow-trigger', name: 'Workflow Trigger', icon: Play, description: 'Automation trigger' }
    ]
  };

  // Workflow triggers and actions
  const workflowTriggers = [
    { type: 'page-load', name: 'Page Load', description: 'When page loads' },
    { type: 'button-click', name: 'Button Click', description: 'When button is clicked' },
    { type: 'form-submit', name: 'Form Submit', description: 'When form is submitted' },
    { type: 'data-change', name: 'Data Change', description: 'When data changes' },
    { type: 'timer', name: 'Timer', description: 'At scheduled time' },
    { type: 'webhook', name: 'Webhook', description: 'External trigger' },
    { type: 'user-action', name: 'User Action', description: 'Custom user action' }
  ];

  const workflowActions = [
    { type: 'send-email', name: 'Send Email', description: 'Send email notification' },
    { type: 'save-data', name: 'Save Data', description: 'Save to database' },
    { type: 'api-call', name: 'API Call', description: 'Call external API' },
    { type: 'show-message', name: 'Show Message', description: 'Display message' },
    { type: 'redirect', name: 'Redirect', description: 'Navigate to page' },
    { type: 'update-ui', name: 'Update UI', description: 'Update interface' },
    { type: 'calculate', name: 'Calculate', description: 'Perform calculation' },
    { type: 'condition', name: 'Condition', description: 'Conditional logic' },
    { type: 'loop', name: 'Loop', description: 'Repeat actions' },
    { type: 'custom-code', name: 'Custom Code', description: 'Execute custom code' }
  ];

  // Main interface
  const renderMainInterface = () => (
    <div className="flex h-screen bg-gray-50">
      {/* Component Library Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 overflow-y-auto">
        <div className="p-4 border-b border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900">Component Library</h2>
          <p className="text-sm text-gray-600">Drag components to canvas</p>
        </div>
        
        <div className="p-4">
          {Object.entries(componentLibrary).map(([category, components]) => (
            <div key={category} className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-3 uppercase tracking-wider">
                {category}
              </h3>
              <div className="grid grid-cols-2 gap-2">
                {components.map((component) => {
                  const IconComponent = component.icon;
                  return (
                    <button
                      key={component.type}
                      className="p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors text-left"
                      draggable
                      onDragStart={(e) => {
                        e.dataTransfer.setData('component-type', component.type);
                        e.dataTransfer.setData('component-name', component.name);
                      }}
                      onClick={() => addComponent(component.type)}
                    >
                      <IconComponent className="w-5 h-5 text-gray-600 mb-2" />
                      <p className="text-xs font-medium text-gray-900">{component.name}</p>
                      <p className="text-xs text-gray-500">{component.description}</p>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Canvas Area */}
      <div className="flex-1 flex flex-col">
        {/* Top Toolbar */}
        <div className="bg-white border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {/* Mode Toggle */}
              <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setCurrentMode('visual')}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    currentMode === 'visual' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-600'
                  }`}
                >
                  <Eye className="w-4 h-4 inline mr-2" />
                  Visual
                </button>
                <button
                  onClick={() => setCurrentMode('code')}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    currentMode === 'code' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-600'
                  }`}
                >
                  <Code className="w-4 h-4 inline mr-2" />
                  Code
                </button>
                <button
                  onClick={() => setCurrentMode('hybrid')}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    currentMode === 'hybrid' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-600'
                  }`}
                >
                  <Layers className="w-4 h-4 inline mr-2" />
                  Hybrid
                </button>
              </div>

              {/* Platform Toggle */}
              <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
                <button className="p-2 rounded-md hover:bg-white" title="Web">
                  <Globe className="w-4 h-4" />
                </button>
                <button className="p-2 rounded-md hover:bg-white" title="Mobile">
                  <Smartphone className="w-4 h-4" />
                </button>
                <button className="p-2 rounded-md hover:bg-white" title="Tablet">
                  <Tablet className="w-4 h-4" />
                </button>
                <button className="p-2 rounded-md hover:bg-white" title="Desktop">
                  <Monitor className="w-4 h-4" />
                </button>
              </div>

              {/* Tab Navigation */}
              <div className="flex items-center space-x-1">
                {['design', 'data', 'logic', 'deploy'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab as any)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-colors ${
                      activeTab === tab ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {tab === 'design' && <Layers className="w-4 h-4 inline mr-2" />}
                    {tab === 'data' && <Database className="w-4 h-4 inline mr-2" />}
                    {tab === 'logic' && <Zap className="w-4 h-4 inline mr-2" />}
                    {tab === 'deploy' && <Globe className="w-4 h-4 inline mr-2" />}
                    {tab}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <button
                onClick={() => setPreviewMode(!previewMode)}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                {previewMode ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                {previewMode ? 'Edit' : 'Preview'}
              </button>
              
              <button
(Content truncated due to size limit. Use line ranges to read in chunks)