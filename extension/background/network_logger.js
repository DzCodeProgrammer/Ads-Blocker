/**
 * Network Logger — records every blocked/allowed request to the backend log.
 *
 * Sends log entries asynchronously — non-blocking, fire-and-forget.
 * Batches entries to reduce HTTP overhead.
 */

const BACKEND = 'http://127.0.0.1:8765';
const BATCH_INTERVAL_MS = 2000;

export class NetworkLogger {
  constructor() {
    this._queue = [];
    this._timer = null;
  }

  start() {
    this._timer = setInterval(() => this._flush(), BATCH_INTERVAL_MS);
  }

  stop() {
    if (this._timer) clearInterval(this._timer);
    this._flush();
  }

  log({
    url, domain, tabUrl = null, status = 'blocked',
    contentType = 'other', ruleMatched = null,
    isTracker = false, isThirdParty = false,
    isCnameCloaked = false, cnameRealDomain = null,
    cleanedUrl = null,
  }) {
    this._queue.push({
      url, domain,
      tab_url: tabUrl,
      status,
      content_type: contentType,
      rule_matched: ruleMatched,
      is_tracker: isTracker,
      is_third_party: isThirdParty,
      is_cname_cloaked: isCnameCloaked,
      cname_real_domain: cnameRealDomain,
      cleaned_url: cleanedUrl,
    });
    // Flush immediately if queue is large
    if (this._queue.length >= 20) this._flush();
  }

  async _flush() {
    if (!this._queue.length) return;
    const batch = this._queue.splice(0, this._queue.length);
    for (const entry of batch) {
      fetch(`${BACKEND}/api/logs/record`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry),
      }).catch(() => {});
    }
  }
}
