"""Load the bundled checkpoint, with a download fallback when it is absent."""

import io
from pathlib import Path

import pyjs
import torch


WEIGHTS_URL = 'https://raw.githubusercontent.com/Anutosh21/modnet/1f5f74af269dc755d865ee1cbeef349ea948b971/content/modnet_photographic_portrait_matting.ckpt'
SHA256 = '7c22235f0925deba15d4d63e53afcb654c47055bbcd98f56e393ab2584007ed8'
CACHE_NAME = 'modnet-portrait-weights-v1'

_FETCH = '''async (url, expectedHash, cacheName) => {
    let cache = null;
    let response;
    try {
        cache = await caches.open(cacheName);
        response = await cache.match(url);
    } catch { cache = null; }
    const cached = Boolean(response);
    if (!response) response = await fetch(url);
    if (!response.ok) throw Error(`Weights download failed: HTTP ${response.status}`);
    const data = await response.arrayBuffer();
    const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', data)),
        byte => byte.toString(16).padStart(2, '0')).join('');
    if (hash !== expectedHash) {
        if (cache) await cache.delete(url);
        throw Error('Pretrained weights failed the SHA-256 check; rerun to download again.');
    }
    let saved = cached;
    if (cache && !cached) {
        try {
            await cache.put(url, new Response(data));
            saved = true;
        } catch { /* Downloaded weights remain usable if storage is unavailable. */ }
    }
    return {data, cached, saved};
}'''


async def load_checkpoint():
    """Load the original FP32 checkpoint from the bundle when available."""
    checkpoint = Path(__file__).with_name(
        'modnet_photographic_portrait_matting.ckpt')
    if checkpoint.is_file():
        print('Loading bundled pretrained weights.', flush=True)
        return torch.load(checkpoint, map_location='cpu', weights_only=True)

    print('Loading pretrained weights (first download: 25.0 MiB)...', flush=True)
    result = await pyjs.js.eval(_FETCH)(WEIGHTS_URL, SHA256, CACHE_NAME)
    if pyjs.to_py(result.cached):
        print('Using verified cached weights.', flush=True)
    elif pyjs.to_py(result.saved):
        print('Weights verified and saved in the browser cache.', flush=True)
    else:
        print('Weights verified; browser storage is unavailable for caching.', flush=True)
    data = bytes(pyjs.to_py(result.data))
    return torch.load(io.BytesIO(data), map_location='cpu', weights_only=True)
