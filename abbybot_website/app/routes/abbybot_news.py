from flask import Blueprint, render_template, abort
from ..utilities.db_connections import execute_query

abbybot_news_bp = Blueprint('abbybot_news', __name__)


@abbybot_news_bp.route('/abbybot-news')
def news_list():
    query = """
    SELECT news.id, news.title, news.description, news.content, news.image_url, categories.name AS category, news.created_at, news.slug
    FROM news
    LEFT JOIN categories ON news.category_id = categories.id
    ORDER BY news.created_at DESC
    """
    news_items = execute_query("api", query)
    return render_template('news_list.html', news=news_items)


@abbybot_news_bp.route('/abbybot-news/<string:slug>')
def news_detail(slug):
    query = """
    SELECT news.id, news.title, news.description, news.content, news.image_url, categories.name AS category, news.created_at
    FROM news
    LEFT JOIN categories ON news.category_id = categories.id
    WHERE news.slug = %s
    """
    news_item = execute_query("api", query, (slug,), fetchall=False)
    
    if not news_item:
        abort(404)  # If no news found, return 404
    return render_template('news_detail.html', news=news_item)