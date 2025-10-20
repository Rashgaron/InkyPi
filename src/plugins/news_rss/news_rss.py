from plugins.base_plugin.base_plugin import BasePlugin
from utils.app_utils import resolve_path
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
from utils.image_utils import resize_image
from io import BytesIO
from datetime import datetime
import requests
import logging
import textwrap
import os
import feedparser


logger = logging.getLogger(__name__)

class NewsRSS(BasePlugin):
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params['style_settings'] = True
        return template_params

    def generate_image(self, settings, device_config):
        try:
            prompt_response = "This is a placeholder response from the AI model."
            rss_url = "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/ultimas-noticias/portada"
            feed = feedparser.parse(rss_url)

        except Exception as e:
            logger.error(f"Failed to make Open AI request: {str(e)}")
            raise RuntimeError("Open AI request failure, please check logs.")

        dimensions = device_config.get_resolution()

        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        image_template_params = {
            "content": prompt_response,
            "plugin_settings": settings,
            "rss_items": feed.entries[:10],
        }

        image = self.render_image(dimensions, "news_rss.html", "news_rss.css", image_template_params)

        return image
   