"""
Association Rule Mining module for discovering item combinations.
"""

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder


def create_basket_matrix(transaction_items_df):
    """
    Create a basket matrix for association rule mining.
    
    Args:
        transaction_items_df: DataFrame with transaction_id and item_name
    
    Returns:
        Binary basket matrix (transactions x items)
    """
    # Pivot to create transaction-item matrix
    basket = transaction_items_df.groupby(
        ['transaction_id', 'item_name']
    )['quantity'].sum().unstack().fillna(0)
    
    # Convert to binary
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)
    
    return basket


def mine_frequent_itemsets(basket_df, min_support=0.02, use_fpgrowth=True):
    """
    Find frequent itemsets using Apriori or FP-Growth algorithm.
    
    Args:
        basket_df: Binary basket matrix
        min_support: Minimum support threshold
        use_fpgrowth: Use FP-Growth (faster) if True, else Apriori
    
    Returns:
        DataFrame with frequent itemsets
    """
    if use_fpgrowth:
        frequent_itemsets = fpgrowth(basket_df, min_support=min_support, use_colnames=True)
    else:
        frequent_itemsets = apriori(basket_df, min_support=min_support, use_colnames=True)
    
    return frequent_itemsets


def generate_association_rules(frequent_itemsets, min_confidence=0.3, metric='confidence'):
    """
    Generate association rules from frequent itemsets.
    
    Args:
        frequent_itemsets: DataFrame with frequent itemsets
        min_confidence: Minimum confidence threshold
        metric: Metric to filter rules
    
    Returns:
        DataFrame with association rules
    """
    if len(frequent_itemsets) == 0:
        return pd.DataFrame()
    
    rules = association_rules(
        frequent_itemsets, 
        metric=metric, 
        min_threshold=min_confidence
    )
    
    # Sort by lift
    rules = rules.sort_values('lift', ascending=False)
    
    return rules


def get_top_associations(rules_df, n=10):
    """
    Get top N association rules by lift.
    
    Args:
        rules_df: DataFrame with association rules
        n: Number of top rules to return
    
    Returns:
        DataFrame with top rules (formatted)
    """
    if len(rules_df) == 0:
        return pd.DataFrame()
    
    top_rules = rules_df.head(n).copy()
    
    # Format antecedents and consequents
    top_rules['antecedents'] = top_rules['antecedents'].apply(
        lambda x: ', '.join(list(x))
    )
    top_rules['consequents'] = top_rules['consequents'].apply(
        lambda x: ', '.join(list(x))
    )
    
    # Round metrics
    for col in ['support', 'confidence', 'lift']:
        top_rules[col] = top_rules[col].round(4)
    
    return top_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]


def get_combo_recommendations(rules_df, n=5):
    """
    Generate combo meal recommendations based on association rules.
    
    Args:
        rules_df: DataFrame with association rules
        n: Number of recommendations
    
    Returns:
        List of combo suggestions
    """
    if len(rules_df) == 0:
        return []
    
    combos = []
    top_rules = rules_df.head(n)
    
    for _, rule in top_rules.iterrows():
        antecedent = list(rule['antecedents'])
        consequent = list(rule['consequents'])
        items = antecedent + consequent
        confidence = rule['confidence']
        lift = rule['lift']
        
        combo = {
            'items': items,
            'confidence': round(confidence * 100, 1),
            'lift': round(lift, 2),
            'description': f"{', '.join(antecedent)} + {', '.join(consequent)}"
        }
        combos.append(combo)
    
    return combos


def analyze_item_associations(basket_df, item_name, rules_df):
    """
    Find all items associated with a specific item.
    
    Args:
        basket_df: Binary basket matrix
        item_name: Name of the item to analyze
        rules_df: DataFrame with association rules
    
    Returns:
        DataFrame with related items
    """
    related = []
    
    for _, rule in rules_df.iterrows():
        antecedent = list(rule['antecedents'])
        consequent = list(rule['consequents'])
        
        if item_name in antecedent:
            for item in consequent:
                related.append({
                    'related_item': item,
                    'confidence': rule['confidence'],
                    'lift': rule['lift'],
                    'direction': 'leads to'
                })
        elif item_name in consequent:
            for item in antecedent:
                related.append({
                    'related_item': item,
                    'confidence': rule['confidence'],
                    'lift': rule['lift'],
                    'direction': 'follows'
                })
    
    if related:
        return pd.DataFrame(related).drop_duplicates(subset=['related_item'])
    return pd.DataFrame()


def get_rule_statistics(rules_df):
    """
    Get summary statistics of association rules.
    
    Args:
        rules_df: DataFrame with association rules
    
    Returns:
        Dictionary with statistics
    """
    if len(rules_df) == 0:
        return {}
    
    stats = {
        'total_rules': len(rules_df),
        'avg_support': round(rules_df['support'].mean(), 4),
        'avg_confidence': round(rules_df['confidence'].mean(), 4),
        'avg_lift': round(rules_df['lift'].mean(), 4),
        'max_lift': round(rules_df['lift'].max(), 4),
        'rules_with_high_confidence': len(rules_df[rules_df['confidence'] >= 0.5]),
        'rules_with_high_lift': len(rules_df[rules_df['lift'] >= 2.0])
    }
    
    return stats
