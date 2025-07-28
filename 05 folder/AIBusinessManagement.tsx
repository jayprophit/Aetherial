import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useAIBusinessAgent } from '../../ai/services/AIBusinessAgent';
import Button from '../ui/Button';

interface AIBusinessManagementProps {
  userId: string;
  isBusinessAccount: boolean;
}

const AIBusinessManagement: React.FC<AIBusinessManagementProps> = ({ userId, isBusinessAccount }) => {
  const aiAgent = useAIBusinessAgent();
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  
  // Sales management
  const [salesData, setSalesData] = useState<any[]>([]);
  const [inventoryData, setInventoryData] = useState<any[]>([]);
  const [customerRequests, setCustomerRequests] = useState<any[]>([]);
  const [invoices, setInvoices] = useState<any[]>([]);
  
  // Digital assets
  const [rewardPoints, setRewardPoints] = useState<number>(1250);
  const [stakedAssets, setStakedAssets] = useState<number>(500);
  const [mintedAssets, setMintedAssets] = useState<number>(10);
  const [miningOperations, setMiningOperations] = useState<any[]>([]);
  
  // Form states
  const [question, setQuestion] = useState<string>('');
  const [productId, setProductId] = useState<string>('');
  const [quantity, setQuantity] = useState<number>(1);
  const [customerId, setCustomerId] = useState<string>('');
  const [stakeAmount, setStakeAmount] = useState<number>(100);
  const [mintName, setMintName] = useState<string>('');
  const [mintQuantity, setMintQuantity] = useState<number>(1);
  const [miningPower, setMiningPower] = useState<number>(10);
  const [miningDuration, setMiningDuration] = useState<number>(24);

  useEffect(() => {
    if (isBusinessAccount) {
      // Load mock data for business dashboard
      setSalesData([
        { id: 'sale-1', date: '2025-05-28', amount: 1250.00, customer: 'Customer A', status: 'completed' },
        { id: 'sale-2', date: '2025-05-27', amount: 750.50, customer: 'Customer B', status: 'completed' },
        { id: 'sale-3', date: '2025-05-26', amount: 2100.75, customer: 'Customer C', status: 'processing' }
      ]);
      
      setInventoryData([
        { id: 'prod-1', name: 'Product A', stock: 45, price: 99.99 },
        { id: 'prod-2', name: 'Product B', stock: 32, price: 149.99 },
        { id: 'prod-3', name: 'Product C', stock: 18, price: 199.99 },
        { id: 'prod-4', name: 'Product D', stock: 7, price: 299.99 }
      ]);
      
      setCustomerRequests([
        { id: 'req-1', date: '2025-05-28', type: 'product_info', status: 'pending' },
        { id: 'req-2', date: '2025-05-27', type: 'shipping', status: 'resolved' },
        { id: 'req-3', date: '2025-05-26', type: 'returns', status: 'pending' }
      ]);
      
      setInvoices([
        { id: 'inv-1', date: '2025-05-28', amount: 1250.00, customer: 'Customer A', status: 'paid' },
        { id: 'inv-2', date: '2025-05-27', amount: 750.50, customer: 'Customer B', status: 'paid' },
        { id: 'inv-3', date: '2025-05-26', amount: 2100.75, customer: 'Customer C', status: 'pending' }
      ]);
    }
    
    // Load mining operations
    setMiningOperations([
      { id: 'mining-1', power: 15, duration: 24, startDate: '2025-05-28', endDate: '2025-05-29', expectedReward: 36 },
      { id: 'mining-2', power: 10, duration: 48, startDate: '2025-05-27', endDate: '2025-05-29', expectedReward: 48 }
    ]);
  }, [isBusinessAccount]);

  const handleAskQuestion = async () => {
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const answer = await aiAgent.answerQuestion(question);
      
      setSuccessMessage(answer);
      setQuestion('');
    } catch (err) {
      setError('Failed to process your question. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleProcessSale = async () => {
    if (!productId.trim() || !customerId.trim() || quantity <= 0) {
      setError('Please fill in all required fields');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const result = await aiAgent.handleSales(productId, quantity, customerId);
      
      if (result.success) {
        setSuccessMessage(`Sale processed successfully! Sale ID: ${result.saleId}`);
        setProductId('');
        setQuantity(1);
        setCustomerId('');
        
        // Update sales data
        const newSale = {
          id: result.saleId,
          date: new Date().toISOString().split('T')[0],
          amount: 99.99 * quantity, // Mock price
          customer: customerId,
          status: 'completed'
        };
        setSalesData([newSale, ...salesData]);
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError('Failed to process sale. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleManageInventory = async (action: string, prodId: string, qty: number) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await aiAgent.manageInventory(action as any, prodId, qty);
      
      if (result.success) {
        setSuccessMessage(result.message);
        
        // Update inventory data
        const updatedInventory = inventoryData.map(item => {
          if (item.id === prodId) {
            return { ...item, stock: result.currentStock };
          }
          return item;
        });
        setInventoryData(updatedInventory);
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError('Failed to manage inventory. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleStakeAssets = async () => {
    if (stakeAmount <= 0 || stakeAmount > rewardPoints) {
      setError('Please enter a valid stake amount');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const result = await aiAgent.manageStaking('stake', userId, stakeAmount);
      
      if (result.success) {
        setSuccessMessage(result.message);
        setRewardPoints(rewardPoints - stakeAmount);
        setStakedAssets(stakedAssets + stakeAmount);
        setStakeAmount(100);
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError('Failed to stake assets. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleMintAssets = async () => {
    if (!mintName.trim() || mintQuantity <= 0) {
      setError('Please fill in all required fields');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const assetData = {
        name: mintName,
        description: `Minted ${mintName}`,
        type: 'NFT',
        quantity: mintQuantity,
        metadata: {
          creator: userId,
          creationDate: new Date().toISOString()
        }
      };
      
      const result = await aiAgent.manageMinting('mint', userId, assetData);
      
      if (result.success) {
        setSuccessMessage(result.message);
        setMintedAssets(mintedAssets + mintQuantity);
        setMintName('');
        setMintQuantity(1);
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError('Failed to mint assets. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleStartMining = async () => {
    if (miningPower <= 0 || miningDuration <= 0) {
      setError('Please enter valid mining parameters');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const miningData = {
        power: miningPower,
        duration: miningDuration,
        algorithm: 'standard'
      };
      
      const result = await aiAgent.manageMining('start', userId, miningData);
      
      if (result.success) {
        setSuccessMessage(result.message);
        
        // Add new mining operation
        const newMining = {
          id: result.miningId,
          power: miningPower,
          duration: miningDuration,
          startDate: new Date().toISOString().split('T')[0],
          endDate: new Date(result.completionTime).toISOString().split('T')[0],
          expectedReward: result.expectedReward
        };
        setMiningOperations([newMining, ...miningOperations]);
        
        setMiningPower(10);
        setMiningDuration(24);
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError('Failed to start mining operation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderDashboard = () => (
    <DashboardGrid>
      <DashboardCard>
        <CardTitle>Sales Overview</CardTitle>
        <StatGrid>
          <StatItem>
            <StatLabel>Total Sales</StatLabel>
            <StatValue>${salesData.reduce((sum, sale) => sum + sale.amount, 0).toFixed(2)}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Orders</StatLabel>
            <StatValue>{salesData.length}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Pending</StatLabel>
            <StatValue>{salesData.filter(sale => sale.status === 'processing').length}</StatValue>
          </StatItem>
        </StatGrid>
      </DashboardCard>
      
      <DashboardCard>
        <CardTitle>Inventory Status</CardTitle>
        <StatGrid>
          <StatItem>
            <StatLabel>Products</StatLabel>
            <StatValue>{inventoryData.length}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Low Stock</StatLabel>
            <StatValue>{inventoryData.filter(item => item.stock < 10).length}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Total Value</StatLabel>
            <StatValue>
              ${inventoryData.reduce((sum, item) => sum + (item.stock * item.price), 0).toFixed(2)}
            </StatValue>
          </StatItem>
        </StatGrid>
      </DashboardCard>
      
      <DashboardCard>
        <CardTitle>Digital Assets</CardTitle>
        <StatGrid>
          <StatItem>
            <StatLabel>Reward Points</StatLabel>
            <StatValue>{rewardPoints}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Staked</StatLabel>
            <StatValue>{stakedAssets}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Minted NFTs</StatLabel>
            <StatValue>{mintedAssets}</StatValue>
          </StatItem>
        </StatGrid>
      </DashboardCard>
      
      <DashboardCard>
        <CardTitle>Customer Requests</CardTitle>
        <StatGrid>
          <StatItem>
            <StatLabel>Total</StatLabel>
            <StatValue>{customerRequests.length}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Pending</StatLabel>
            <StatValue>{customerRequests.filter(req => req.status === 'pending').length}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Resolved</StatLabel>
            <StatValue>{customerRequests.filter(req => req.status === 'resolved').length}</StatValue>
          </StatItem>
        </StatGrid>
      </DashboardCard>
    </DashboardGrid>
  );

  const renderSales = () => (
    <Section>
      <SectionTitle>Process New Sale</SectionTitle>
      <FormGrid>
        <FormGroup>
          <Label>Product ID</Label>
          <Input
            type="text"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
            placeholder="Enter product ID"
          />
        </FormGroup>
        
        <FormGroup>
          <Label>Quantity</Label>
          <Input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value) || 0)}
            min="1"
          />
        </FormGroup>
        
        <FormGroup>
          <Label>Customer ID</Label>
          <Input
            type="text"
            value={customerId}
            onChange={(e) => setCustomerId(e.target.value)}
            placeholder="Enter customer ID"
          />
        </FormGroup>
      </FormGrid>
      
      <ButtonContainer>
        <Button $variant="primary" onClick={handleProcessSale} disabled={loading}>
          {loading ? 'Processing...' : 'Process Sale'}
        </Button>
      </ButtonContainer>
      
      <SectionTitle>Recent Sales</SectionTitle>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableHeader>Sale ID</TableHeader>
              <TableHeader>Date</TableHeader>
              <TableHeader>Customer</TableHeader>
              <TableHeader>Amount</TableHeader>
              <TableHeader>Status</TableHeader>
            </TableRow>
          </TableHead>
          <TableBody>
            {salesData.map((sale) => (
              <TableRow key={sale.id}>
                <TableCell>{sale.id}</TableCell>
                <TableCell>{sale.date}</TableCell>
                <TableCell>{sale.customer}</TableCell>
                <TableCell>${sale.amount.toFixed(2)}</TableCell>
                <TableCell>
                  <StatusBadge status={sale.status}>
                    {sale.status === 'completed' ? 'Completed' : 'Processing'}
                  </StatusBadge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Section>
  );

  const renderInventory = () => (
    <Section>
      <SectionTitle>Inventory Management</SectionTitle>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableHeader>Product ID</TableHeader>
              <TableHeader>Name</TableHeader>
              <TableHeader>Stock</TableHeader>
              <TableHeader>Price</TableHeader>
              <TableHeader>Actions</TableHeader>
            </TableRow>
          </TableHead>
          <TableBody>
            {inventoryData.map((product) => (
              <TableRow key={product.id}>
                <TableCell>{product.id}</TableCell>
                <TableCell>{product.name}</TableCell>
                <TableCell>
                  <StockIndicator low={product.stock < 10}>{product.stock}</StockIndicator>
                </TableCell>
                <TableCell>${product.price.toFixed(2)}</TableCell>
                <TableCell>
                  <ActionButtons>
                    <ActionButton onClick={() => handleManageInventory('add', product.id, 10)}>
                      +10
                    </ActionButton>
                    <ActionButton onClick={() => handleManageInventory('remove', product.id, 1)}>
                      -1
                    </ActionButton>
                  </ActionButtons>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Section>
  );

  const renderDigitalAssets = () => (
    <>
      <Section>
        <SectionTitle>Digital Asset Management</SectionTitle>
        <AssetSummary>
          <AssetSummaryItem>
            <AssetSummaryLabel>Reward Points</AssetSummaryLabel>
            <AssetSummaryValue>{rewardPoints}</AssetSummaryValue>
          </AssetSummaryItem>
          <AssetSummaryItem>
            <AssetSummaryLabel>Staked Assets</AssetSummaryLabel>
            <AssetSummaryValue>{stakedAssets}</AssetSummaryValue>
          </AssetSummaryItem>
          <AssetSummaryItem>
            <AssetSummaryLabel>Minted NFTs</AssetSummaryLabel>
            <AssetSummaryValue>{mintedAssets}</AssetSummaryValue>
          </AssetSummaryItem>
        </AssetSummary>
      </Section>
      
      <Section>
        <SectionTitle>Stake Assets</SectionTitle>
        <FormGroup>
          <Label>Amount to Stake
(Content truncated due to size limit. Use line ranges to read in chunks)