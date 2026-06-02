/**
 * YouTube Ad Skipper — automatically skips pre-roll and mid-roll ads.
 *
 * Features:
 *   - Skip button auto-click
 *   - Fast-forward video to end for unskippable ads
 *   - Dismiss overlay ad banners
 *   - Remove YouTube Premium upsell banners
 *   - Mute ads (then restore volume)
 */

(function () {
  'use strict';

  if (!location.hostname.includes('youtube.com')) return;

  let lastVolume = 1;

  function skipAd() {
    const video = document.querySelector('video');
    const adShowing = document.querySelector('.ad-showing');

    // Auto-click skip button
    const skipBtn = document.querySelector(
      '.ytp-ad-skip-button, .ytp-skip-ad-button, .ytp-ad-skip-button-modern'
    );
    if (skipBtn) { skipBtn.click(); return; }

    // Fast-forward unskippable video ads
    if (adShowing && video) {
      lastVolume = video.volume;
      video.muted = true;                        // mute while skipping
      if (video.duration && isFinite(video.duration)) {
        video.currentTime = video.duration;
      }
      return;
    }

    // Restore volume after ad ends
    if (!adShowing && video && video.muted && lastVolume > 0) {
      video.muted = false;
      video.volume = lastVolume;
    }

    // Dismiss overlay ads
    document.querySelectorAll(
      '.ytp-ad-overlay-close-button, .ytp-ad-overlay-slot .ytp-ad-overlay-close'
    ).forEach(b => b.click());

    // Remove YouTube promotional banners
    const selectors = [
      'ytd-banner-promo-renderer',
      'ytd-statement-banner-renderer',
      'ytd-ad-slot-renderer',
      'ytd-promoted-video-renderer',
      'ytd-promoted-sparkles-web-renderer',
      '#masthead-ad',
      '.ytd-display-ad-renderer',
      'ytd-in-feed-ad-layout-renderer',
    ];
    selectors.forEach(s =>
      document.querySelectorAll(s).forEach(el => el.remove())
    );
  }

  // Poll every 300ms (ads load asynchronously)
  const interval = setInterval(skipAd, 300);
  // Also observe DOM for ad injection
  new MutationObserver(skipAd).observe(document.documentElement, {
    childList: true, subtree: true,
  });

  // Clean up on navigation (YouTube is a SPA)
  window.addEventListener('yt-navigate-finish', skipAd);
})();
