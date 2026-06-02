/**
 * URL Cleaner — strip tracking query parameters from navigation URLs.
 *
 * Uses the backend /api/filters/check which now returns cleaned_url.
 * Also has a local fast-path list for common UTM params.
 */

const TRACKING_PARAMS = new Set([
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
  'utm_id', 'utm_reader', 'gclid', 'gclsrc', 'dclid', '_ga', '_gl',
  'fbclid', 'fb_action_ids', 'twclid', 'msclkid',
  'mc_cid', 'mc_eid', 'mkt_tok', 'yclid', 'trk',
  'igshid', 'epik', 'ttclid', 'ScCid', 'li_fat_id',
]);

const TRACKING_PREFIXES = ['utm_', 'hsa_', 'bsft_', 'oly_'];

export class URLCleaner {
  /**
   * Clean a URL locally (fast path, no backend call).
   * Returns { cleanedUrl, removedParams }.
   */
  clean(urlString) {
    try {
      const url = new URL(urlString);
      if (!url.search) return { cleanedUrl: urlString, removedParams: [] };

      const removed = [];
      for (const key of [...url.searchParams.keys()]) {
        if (this._isTracking(key)) {
          url.searchParams.delete(key);
          removed.push(key);
        }
      }
      return {
        cleanedUrl: removed.length ? url.toString() : urlString,
        removedParams: removed,
      };
    } catch (_) {
      return { cleanedUrl: urlString, removedParams: [] };
    }
  }

  hasTracking(urlString) {
    try {
      const url = new URL(urlString);
      for (const key of url.searchParams.keys()) {
        if (this._isTracking(key)) return true;
      }
      return false;
    } catch (_) {
      return false;
    }
  }

  _isTracking(key) {
    return TRACKING_PARAMS.has(key) ||
      TRACKING_PREFIXES.some(p => key.startsWith(p));
  }
}
