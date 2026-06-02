"""
URL Tracking Parameter Cleaner — strip known UTM / ad-click parameters.

Based on ClearURLs project rules (https://github.com/ClearURLs/Rules).
Strips params before they hit the backend stats — prevents polluted analytics.
"""
from __future__ import annotations
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

# Full set of known tracking query parameters
TRACKING_PARAMS: frozenset[str] = frozenset([
    # Google
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "utm_reader", "utm_name", "utm_cid", "utm_source_platform",
    "gclid", "gclsrc", "dclid", "_ga", "_gl",
    # Facebook / Meta
    "fbclid", "fb_action_ids", "fb_action_types", "fb_source", "fb_ref",
    "fbid", "_fbc", "_fbp",
    # Twitter / X
    "twclid", "t",
    # Microsoft Ads
    "msclkid",
    # Amazon
    "tag", "linkCode", "linkId", "psc", "ref_", "pd_rd_r", "pd_rd_w",
    "pf_rd_i", "pf_rd_m", "pf_rd_p", "pf_rd_r", "pf_rd_s", "pf_rd_t",
    # Adobe Analytics
    "s_cid", "s_kwcid", "ef_id",
    # HubSpot
    "_hsenc", "_hsmi", "hsa_cam", "hsa_grp", "hsa_mt", "hsa_src",
    "hsa_ad", "hsa_acc", "hsa_net", "hsa_kw", "hsa_tgt", "hsa_ver",
    # Marketo
    "mkt_tok",
    # LinkedIn
    "trk", "trkCampaign", "trkInfo", "li_fat_id",
    # Mailchimp
    "mc_cid", "mc_eid",
    # Yandex
    "yclid", "ymclid",
    # Snapchat
    "ScCid",
    # Pinterest
    "epik",
    # TikTok
    "ttclid",
    # Generic
    "cmpid", "cid", "cmp", "campaign_id", "campaign",
    "adgroupid", "adid", "adposition", "adtype",
    "clickid", "click_id", "ad_click_id",
    "referrer", "affiliate", "promo", "coupon",
    "source", "medium", "creative", "keyword",
    "igshid",  # Instagram
    "vero_conv", "vero_id",  # Vero
    "rb_clickid",  # RocketBrain
    "bsft_aaid", "bsft_clkid",  # Blueshift
    "wickedid",  # Wicked Reports
    "mktcid", "mktcval",  # IBM Watson Campaign Automation
    "irclickid",  # Impact Radius
    "mkwid", "pcrid", "pdv",  # Marin Software
    "ef_id", "s_kwcid",  # Adobe Advertising Cloud
])

# Tracking param prefixes (catch dynamic names)
TRACKING_PREFIXES: tuple[str, ...] = (
    "utm_", "mc_", "hsa_", "bsft_", "oly_", "vero_",
)


class URLCleaner:
    def clean(self, url: str) -> tuple[str, list[str]]:
        """
        Strip tracking params from URL.
        Returns (clean_url, list_of_removed_params).
        """
        try:
            parsed = urlparse(url)
            if not parsed.query:
                return url, []

            params = parse_qs(parsed.query, keep_blank_values=True)
            removed: list[str] = []
            kept: dict = {}

            for key, value in params.items():
                if self._is_tracking(key):
                    removed.append(key)
                else:
                    kept[key] = value

            if not removed:
                return url, []

            new_query = urlencode(kept, doseq=True)
            new_url = urlunparse(parsed._replace(query=new_query))
            return new_url, removed

        except Exception:
            return url, []

    def has_tracking_params(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            if not parsed.query:
                return False
            params = parse_qs(parsed.query)
            return any(self._is_tracking(k) for k in params)
        except Exception:
            return False

    def _is_tracking(self, key: str) -> bool:
        return key in TRACKING_PARAMS or any(
            key.startswith(p) for p in TRACKING_PREFIXES
        )
