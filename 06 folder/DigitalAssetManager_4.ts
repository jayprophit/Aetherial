import React, { useState, useEffect } from 'react';

/**
 * DigitalAssetManager - Manages digital assets with special handling for minors
 * 
 * Features:
 * - Digital asset tracking and management
 * - Automatic asset locking for users under 18
 * - Compounding, minting, mining, and staking capabilities
 * - Secure storage and transaction processing
 * - Integration with KYC verification system
 */
class DigitalAssetManager {
  constructor() {
    this.assetTypes = {
      REWARD_POINTS: 'reward_points',
      STAKED_ASSETS: 'staked_assets',
      MINTED_TOKENS: 'minted_tokens',
      MINING_REWARDS: 'mining_rewards'
    };
    
    this.lockingRules = {
      minAge: 18,
      compoundingRate: 0.05, // 5% compounding rate for locked assets
      mintingBonus: 0.02,    // 2% bonus for minted assets
      stakingYield: 0.08     // 8% annual yield for staked assets
    };
    
    this.userAssets = new Map();
    this.lockedAssets = new Map();
    this.transactionHistory = new Map();
  }

  /**
   * Initialize assets for a new user
   * @param {string} userId - User ID
   * @param {number} userAge - User's age
   * @param {boolean} kycVerified - Whether user has completed KYC verification
   */
  initializeUser(userId, userAge, kycVerified = false) {
    // Create initial asset structure
    const initialAssets = {
      [this.assetTypes.REWARD_POINTS]: 0,
      [this.assetTypes.STAKED_ASSETS]: 0,
      [this.assetTypes.MINTED_TOKENS]: 0,
      [this.assetTypes.MINING_REWARDS]: 0,
      totalValue: 0,
      kycVerified: kycVerified,
      age: userAge,
      assetsLocked: userAge < this.lockingRules.minAge
    };
    
    this.userAssets.set(userId, initialAssets);
    
    // Initialize locked assets if user is a minor
    if (userAge < this.lockingRules.minAge) {
      this.lockedAssets.set(userId, {
        lockedUntilAge: this.lockingRules.minAge,
        originalAge: userAge,
        assets: {
          [this.assetTypes.REWARD_POINTS]: 0,
          [this.assetTypes.STAKED_ASSETS]: 0,
          [this.assetTypes.MINTED_TOKENS]: 0,
          [this.assetTypes.MINING_REWARDS]: 0
        },
        compoundingHistory: [],
        lastCompounded: new Date()
      });
    }
    
    // Initialize transaction history
    this.transactionHistory.set(userId, []);
    
    return initialAssets;
  }

  /**
   * Get user's current assets
   * @param {string} userId - User ID
   * @returns {object|null} User's assets or null if not found
   */
  getUserAssets(userId) {
    if (!this.userAssets.has(userId)) {
      return null;
    }
    
    const assets = this.userAssets.get(userId);
    const lockedAssets = this.lockedAssets.get(userId) || null;
    
    return {
      ...assets,
      lockedAssets: lockedAssets ? lockedAssets.assets : null
    };
  }

  /**
   * Add assets to user's account
   * @param {string} userId - User ID
   * @param {string} assetType - Type of asset
   * @param {number} amount - Amount to add
   * @param {string} source - Source of the assets
   * @returns {object} Updated asset information
   */
  addAssets(userId, assetType, amount, source) {
    if (!this.userAssets.has(userId)) {
      throw new Error('User not found');
    }
    
    if (amount <= 0) {
      throw new Error('Amount must be positive');
    }
    
    const userAssets = this.userAssets.get(userId);
    
    // Check if assets should be locked
    if (userAssets.assetsLocked) {
      return this.addLockedAssets(userId, assetType, amount, source);
    }
    
    // Add assets to user's account
    userAssets[assetType] += amount;
    userAssets.totalValue = this.calculateTotalValue(userAssets);
    
    // Record transaction
    this.recordTransaction(userId, {
      type: 'add',
      assetType,
      amount,
      source,
      timestamp: new Date(),
      locked: false
    });
    
    this.userAssets.set(userId, userAssets);
    return userAssets;
  }

  /**
   * Add assets to user's locked account (for minors)
   * @param {string} userId - User ID
   * @param {string} assetType - Type of asset
   * @param {number} amount - Amount to add
   * @param {string} source - Source of the assets
   * @returns {object} Updated asset information
   */
  addLockedAssets(userId, assetType, amount, source) {
    if (!this.lockedAssets.has(userId)) {
      throw new Error('Locked assets not initialized for user');
    }
    
    const lockedData = this.lockedAssets.get(userId);
    
    // Add assets to locked account
    lockedData.assets[assetType] += amount;
    
    // Record transaction
    this.recordTransaction(userId, {
      type: 'add',
      assetType,
      amount,
      source,
      timestamp: new Date(),
      locked: true
    });
    
    this.lockedAssets.set(userId, lockedData);
    
    // Update user assets summary
    const userAssets = this.userAssets.get(userId);
    userAssets.totalValue = this.calculateTotalValue(userAssets, lockedData.assets);
    this.userAssets.set(userId, userAssets);
    
    return {
      ...userAssets,
      lockedAssets: lockedData.assets
    };
  }

  /**
   * Compound locked assets for minors
   * @param {string} userId - User ID
   * @returns {object} Compounding results
   */
  compoundLockedAssets(userId) {
    if (!this.lockedAssets.has(userId)) {
      throw new Error('No locked assets found for user');
    }
    
    const lockedData = this.lockedAssets.get(userId);
    const now = new Date();
    
    // Calculate time since last compounding (in days)
    const daysSinceLastCompound = (now - lockedData.lastCompounded) / (1000 * 60 * 60 * 24);
    
    // Only compound if at least 1 day has passed
    if (daysSinceLastCompound < 1) {
      return {
        compounded: false,
        message: 'Assets can only be compounded once per day',
        lockedAssets: lockedData.assets
      };
    }
    
    // Calculate compounding for each asset type
    const compoundingResults = {};
    let totalAdded = 0;
    
    for (const [assetType, amount] of Object.entries(lockedData.assets)) {
      if (amount > 0) {
        // Calculate compounding interest (daily rate)
        const dailyRate = this.lockingRules.compoundingRate / 365;
        const interestEarned = amount * dailyRate * daysSinceLastCompound;
        
        lockedData.assets[assetType] += interestEarned;
        compoundingResults[assetType] = interestEarned;
        totalAdded += interestEarned;
      }
    }
    
    // Update last compounded date
    lockedData.lastCompounded = now;
    
    // Record compounding history
    lockedData.compoundingHistory.push({
      date: now,
      daysSinceLastCompound,
      results: compoundingResults,
      totalAdded
    });
    
    this.lockedAssets.set(userId, lockedData);
    
    // Update user assets summary
    const userAssets = this.userAssets.get(userId);
    userAssets.totalValue = this.calculateTotalValue(userAssets, lockedData.assets);
    this.userAssets.set(userId, userAssets);
    
    // Record transaction
    this.recordTransaction(userId, {
      type: 'compound',
      amount: totalAdded,
      timestamp: now,
      locked: true,
      details: compoundingResults
    });
    
    return {
      compounded: true,
      daysSinceLastCompound,
      added: compoundingResults,
      totalAdded,
      lockedAssets: lockedData.assets
    };
  }

  /**
   * Stake assets for rewards
   * @param {string} userId - User ID
   * @param {number} amount - Amount to stake
   * @returns {object} Staking results
   */
  stakeAssets(userId, amount) {
    if (!this.userAssets.has(userId)) {
      throw new Error('User not found');
    }
    
    const userAssets = this.userAssets.get(userId);
    
    // Check if user has enough reward points to stake
    if (userAssets[this.assetTypes.REWARD_POINTS] < amount) {
      throw new Error('Insufficient reward points for staking');
    }
    
    // Check if assets should be locked
    if (userAssets.assetsLocked) {
      return this.stakeLockedAssets(userId, amount);
    }
    
    // Transfer from reward points to staked assets
    userAssets[this.assetTypes.REWARD_POINTS] -= amount;
    userAssets[this.assetTypes.STAKED_ASSETS] += amount;
    
    // Record transaction
    this.recordTransaction(userId, {
      type: 'stake',
      amount,
      timestamp: new Date(),
      locked: false
    });
    
    this.userAssets.set(userId, userAssets);
    
    return {
      staked: true,
      amount,
      newStakedBalance: userAssets[this.assetTypes.STAKED_ASSETS],
      newRewardPointsBalance: userAssets[this.assetTypes.REWARD_POINTS]
    };
  }

  /**
   * Stake locked assets for minors
   * @param {string} userId - User ID
   * @param {number} amount - Amount to stake
   * @returns {object} Staking results
   */
  stakeLockedAssets(userId, amount) {
    if (!this.lockedAssets.has(userId)) {
      throw new Error('Locked assets not initialized for user');
    }
    
    const lockedData = this.lockedAssets.get(userId);
    
    // Check if user has enough locked reward points
    if (lockedData.assets[this.assetTypes.REWARD_POINTS] < amount) {
      throw new Error('Insufficient locked reward points for staking');
    }
    
    // Transfer from locked reward points to locked staked assets
    lockedData.assets[this.assetTypes.REWARD_POINTS] -= amount;
    lockedData.assets[this.assetTypes.STAKED_ASSETS] += amount;
    
    // Record transaction
    this.recordTransaction(userId, {
      type: 'stake',
      amount,
      timestamp: new Date(),
      locked: true
    });
    
    this.lockedAssets.set(userId, lockedData);
    
    return {
      staked: true,
      amount,
      locked: true,
      newStakedBalance: lockedData.assets[this.assetTypes.STAKED_ASSETS],
      newRewardPointsBalance: lockedData.assets[this.assetTypes.REWARD_POINTS]
    };
  }

  /**
   * Mint new tokens from existing assets
   * @param {string} userId - User ID
   * @param {number} amount - Amount of reward points to convert
   * @returns {object} Minting results
   */
  mintTokens(userId, amount) {
    if (!this.userAssets.has(userId)) {
      throw new Error('User not found');
    }
    
    const userAssets = this.userAssets.get(userId);
    
    // Check if user has enough reward points
    if (userAssets[this.assetTypes.REWARD_POINTS] < amount) {
      throw new Error('Insufficient reward points for minting');
    }
    
    // Check if assets should be locked
    if (userAssets.assetsLocked) {
      return this.mintLockedTokens(userId, amount);
    }
    
    // Calculate minting bonus
    const mintingBonus = amount * this.lockingRules.mintingBonus;
    const totalMinted = amount + mintingBonus;
    
    // Transfer from reward points to minted tokens
    userAssets[this.assetTypes.REWARD_POINTS] -= amount;
    userAssets[this.assetTypes.MINTED_TOKENS] += totalMinted;
    
    // Record transaction
    this.recordTransaction(userId, {
      type: 'mint',
      amount,
      bonus: mintingBonus,
      totalMinted,
      timestamp: new Date(),
      locked: false
    });
    
    this.userAssets.set(userId, userAssets);
    
    return {
      minted: true,
      amount,
      bonus: mintingBonus,
      totalMinted,
      newMintedBalance: userAssets[this.assetTypes.MINTED_TOKENS],
      newRewardPointsBalance: userAssets[this.assetTypes.REWARD_POINTS]
    };
  }

  /**
   * Mint new tokens from locked assets for minors
   * @param {string} userId - User ID
   * @param {number} amount - Amount of reward points to convert
   * @returns {object} Minting results
   */
  mintLockedTokens(userId, amount) {
    if (!this.lockedAssets.has(userId)) {
      throw new Error('Locked assets not initialized for user');
    }
    
    const lockedData = this.lockedAssets.get(userId);
    
    // Check if user has enough locked reward points
    if (lockedData.assets[this.assetTypes.REWARD_POINTS] < amount) {
      throw new Error('Insufficient locked reward points for minting');
    }
    
    // Calculate minting bonus (higher for locked assets)
    const mintingBonus = amount * (this.lockingRules.mintingBonus * 1.5); // 50% higher bonus for locked assets
    const totalMinted = amount + mintingBonus;
    
    // Transfer from locked reward points to locked minted tokens
    lockedData.assets[this.assetTypes.REWARD_POINTS] -= amount;
    lockedData.assets[this.assetTypes.MINTED_TOKENS] += totalMinted;
    
    // Record transaction
    this.recordTransaction(userId, {
      type: 'mint',
      amount,
      bonus: mintingBonus,
      totalMinted,
      timestamp: new Date(),
      locked: true
    });
    
    this.lockedAssets.set(userId, lockedData);
    
    return {
      minted: true,
      amount,
      bonus: mintingBonus,
      totalMinted,
      locked: true,
      newMintedBalance: lockedData.assets[this.assetTypes.MINTED_TOKENS],
      newRewardPointsBalance: lockedData.assets[this.assetTypes.REWARD_POINTS]
    };
  }

  /**
   * Add mining rewards to user's account
   * @param {string} userId - User ID
   * @param {number} amount - Amount of mining rewards
   * @returns {object} Mining results
   */
  addMiningRewards(userId, amount) {
    if (!this.userAssets.has(userId)) {
      throw new Error('User not found');
    }
    
    // Check if assets should be locked
    const userAssets = this.userAssets.get(userId);
    if (userAssets.assetsLocked) {
      // Add to locked mining rewards
      const lockedData = this.lockedAssets.get(userId);
      lockedData.assets[this.assetTypes.MINING_REWARDS] += amount;
      
      // Record transaction
      this.recordTransaction(userId, {
        type: 'mining',
        amount,
        timestamp: new Date(),
        locked: true
      });
      
      this.lockedAssets.set(userId, lockedData);
      
      // Update user assets summary
      userAssets.totalValue = this.calculateTotalValue(userAssets, lockedData.assets);
      this.userAssets.set(userId, userAssets);
      
      return {
        mined: true,
        amount,
        locked: true,
        newMiningBalance: lockedData.assets[this.assetTypes.MINING_REWARDS]
      };
    } else {
      // Add to regular mining rewards
      userAssets[this.assetTypes.MINING_REWARDS] += amount;
      userAssets.totalValue = this.calculateTotalValue(userAssets);
      
      // Record transaction
      this.recordTransaction(userId, {
        type: 'mining',
        amount,
        timestamp: new Date(),
        locked: false
      });
      
      this.userAssets.set(userId, userAssets);
      
      return {
        mined: true,
        amount,
        locked: false,
        newMiningBalance: userAssets[this.assetTypes.MINING_REWARDS]
      };
    }
  }

  /**
   * Update user's age and check if locked assets should be released
   * @param {string} userId - User ID
   * @param {number} newAge - User's new age
   * @returns {object} Update results
   */
  updateUserAge(userId, newAge) {
    if (!this.userAssets.has(userId)) {
      throw new Error('User not found');
    }
    
    const userAssets = this.userAssets.get(userId);
    userAssets.age = newAge;
    
    // Check if user has reached minimum age and has locked assets
    if (newAge >= this.lockingRules.minAge && this.lockedAssets.has(userId)) {
      return this.releaseLockedAssets(userId);
    }
    
    // Update locking status
    userAssets.assetsLocked = newAge < this.lockingRules.minAge;
    this.userAssets.set(userId, userAssets);
    
    return {
      updated: true,
      newAge,
      assetsLocked: userAssets.assetsLocked
    };
  }

  /**
   * Release locked assets when user reaches minimum age
   * @param {string} userId - User ID
   * @returns {object} Release results
   */
  releaseLockedAssets(userId) {
    if (!this.lockedAssets.has(userId)) {
      throw new Error('No locked assets found for user');
    }
    
    const userAssets = this.userAssets.get(userId);
    const lockedData = this.lockedAssets.get(userId);
    
    // Transfer all locked assets to regular asse
(Content truncated due to size limit. Use line ranges to read in chunks)