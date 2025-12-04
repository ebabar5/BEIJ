from typing import List, Dict, Any
from app.services.view_history_service import get_view_history
from app.repositories.products_repo import load_all
from app.repositories.users_repo import get_user_by_id
from app.schemas.product import Product
from app.error_handling import NotFound
from app.services.product_service import with_placeholders, _load_products_models
from collections import Counter
import statistics

def get_recommendations(user_id: str, limit: int = 8, exclude_product_id: str = None) -> List[Product]:
    """Get product recommendations for a user based on viewing history"""
    
    # Get user's viewing history
    view_history = get_view_history(user_id)
    
    # If no viewing history, return top-rated products as fallback
    if not view_history:
        return _get_top_rated_products(limit, exclude_product_id)
    
    # Get all products
    all_products = _load_products_models()
    
    # Get viewed product IDs
    viewed_product_ids = {v["product_id"] for v in view_history}
    
    # Get details of viewed products
    viewed_products = []
    for product in all_products:
        if product.product_id in viewed_product_ids:
            viewed_products.append(product)
    
    if not viewed_products:
        return _get_top_rated_products(limit, exclude_product_id)
    
    # Calculate average metrics from viewed products
    avg_price = statistics.mean([p.discounted_price for p in viewed_products])
    avg_rating = statistics.mean([p.rating for p in viewed_products])
    
    # Get all categories from viewed products
    viewed_categories = []
    for product in viewed_products:
        if product.category:
            viewed_categories.extend(product.category)
    category_counter = Counter(viewed_categories)
    total_category_views = sum(category_counter.values())
    
    # Score all products
    scored_products = []
    for product in all_products:
        # Skip if already viewed or is the current product
        if product.product_id in viewed_product_ids or product.product_id == exclude_product_id:
            continue
        
        score = 0.0
        
        # Category match (40% weight)
        if product.category and viewed_categories:
            product_categories = set(product.category)
            viewed_categories_set = set(viewed_categories)
            overlap = len(product_categories & viewed_categories_set)
            if overlap > 0:
                # Calculate category similarity
                category_score = overlap / max(len(product_categories), len(viewed_categories_set))
                score += 0.4 * category_score
        
        # Price similarity (30% weight)
        if avg_price > 0:
            price_diff = abs(product.discounted_price - avg_price) / avg_price
            if price_diff < 0.3:  # Within 30%
                price_score = 1 - (price_diff / 0.3)
                score += 0.3 * price_score
        
        # Rating similarity (20% weight)
        if avg_rating > 0:
            rating_diff = abs(product.rating - avg_rating)
            if rating_diff < 1.0:  # Within 1 star
                rating_score = 1 - (rating_diff / 1.0)
                score += 0.2 * rating_score
        
        # Recency bonus (10% weight) - products viewed more recently get higher weight
        # This is already handled by the order of view_history (most recent first)
        # We can add a small bonus for products in similar price/rating range
        if score > 0:
            score += 0.1
        
        scored_products.append((score, product))
    
    # Sort by score (descending) and return top products
    scored_products.sort(key=lambda x: x[0], reverse=True)
    
    # If we don't have enough recommendations, fill with top-rated products
    recommendations = [product for _, product in scored_products[:limit]]
    
    if len(recommendations) < limit:
        top_rated = _get_top_rated_products(limit - len(recommendations), exclude_product_id, exclude_ids=[p.product_id for p in recommendations] + list(viewed_product_ids))
        recommendations.extend(top_rated)
    
    return recommendations[:limit]

def _get_top_rated_products(limit: int, exclude_product_id: str = None, exclude_ids: List[str] = None) -> List[Product]:
    """Get top-rated products as fallback recommendations"""
    all_products = _load_products_models()
    
    exclude_set = set(exclude_ids or [])
    if exclude_product_id:
        exclude_set.add(exclude_product_id)
    
    # Filter out excluded products
    available_products = [p for p in all_products if p.product_id not in exclude_set]
    
    # Sort by rating * rating_count (popularity score)
    sorted_products = sorted(
        available_products,
        key=lambda p: p.rating * p.rating_count,
        reverse=True
    )
    
    return sorted_products[:limit]

