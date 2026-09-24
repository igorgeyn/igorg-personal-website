(() => {
  'use strict';
  const form = document.getElementById('unlock-form');
  const input = document.getElementById('password');
  const button = document.getElementById('unlock');
  const status = document.getElementById('status');
  const progress = document.getElementById('progress');
  const encoder = new TextEncoder();
  const decoder = new TextDecoder('utf-8', {fatal:true});
  let busy = false;
  let config;

  const bytes = value => Uint8Array.from(atob(value), c => c.charCodeAt(0));
  function message(text, error = false) {
    status.textContent = text;
    status.classList.toggle('error', error);
  }

  document.getElementById('reveal').addEventListener('click', event => {
    const show = input.type === 'password';
    input.type = show ? 'text' : 'password';
    event.currentTarget.textContent = show ? 'Hide' : 'Show';
    event.currentTarget.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
    event.currentTarget.setAttribute('aria-pressed', String(show));
  });

  async function getConfig() {
    if (config) return config;
    const response = await fetch('album.json', {cache:'no-store', credentials:'omit', referrerPolicy:'no-referrer'});
    if (!response.ok) throw new Error('load');
    const candidate = await response.json();
    if (candidate.version !== 1 || candidate.iterations !== 600000 || !/^album-[a-f0-9]{16}\.bin$/.test(candidate.file) || candidate.bytes > 64000000) throw new Error('load');
    config = candidate;
    return config;
  }

  async function downloadAlbum(settings) {
    const response = await fetch(settings.file, {credentials:'omit', referrerPolicy:'no-referrer'});
    if (!response.ok) throw new Error('load');
    if (!response.body?.getReader) return response.arrayBuffer();
    const reader = response.body.getReader();
    const chunks = [];
    let length = 0;
    progress.hidden = false;
    progress.value = 0;
    while (true) {
      const {done,value} = await reader.read();
      if (done) break;
      chunks.push(value);
      length += value.length;
      if (length > settings.bytes) { await reader.cancel(); throw new Error('load'); }
      progress.value = Math.min(100, length / settings.bytes * 100);
      message(`Opening your album… ${Math.floor(progress.value)}%`);
    }
    if (length !== settings.bytes) throw new Error('load');
    const result = new Uint8Array(length);
    let offset = 0;
    for (const chunk of chunks) { result.set(chunk, offset); offset += chunk.length; }
    return result.buffer;
  }

  function openAlbum(buffer) {
    const data = new Uint8Array(buffer);
    if (decoder.decode(data.subarray(0,8)) !== 'WALB0001') throw new Error('load');
    const manifestLength = new DataView(buffer).getUint32(8, false);
    if (manifestLength < 1 || manifestLength > 1000000 || 12 + manifestLength > data.length) throw new Error('load');
    const manifest = JSON.parse(decoder.decode(data.subarray(12,12 + manifestLength)));
    if (manifest.version !== 1 || !Array.isArray(manifest.files)) throw new Error('load');
    const start = 12 + manifestLength;
    const urls = new Map();
    const htmlFiles = new Map();
    const allowedTypes = new Set(['image/webp','image/jpeg','application/pdf','text/html']);
    for (const file of manifest.files) {
      if (!Number.isSafeInteger(file.offset) || !Number.isSafeInteger(file.length) || file.offset < 0 || file.length < 0 || start + file.offset + file.length > data.length || !allowedTypes.has(file.type)) throw new Error('load');
      const content = data.subarray(start + file.offset, start + file.offset + file.length);
      if (file.type === 'text/html') htmlFiles.set(file.path, decoder.decode(content));
      else urls.set(file.path, URL.createObjectURL(new Blob([content], {type:file.type})));
    }
    function resolve(template) {
      return template.replace(/@@ASSET:([a-zA-Z0-9_./-]+)@@/g, (_, path) => {
        if (!urls.has(path)) throw new Error('load');
        return urls.get(path);
      });
    }
    for (const [path, template] of htmlFiles) {
      if (path === manifest.entry) continue;
      urls.set(path, URL.createObjectURL(new Blob([resolve(template)], {type:'text/html'})));
    }
    if (!htmlFiles.has(manifest.entry)) throw new Error('load');
    const html = resolve(htmlFiles.get(manifest.entry));
    input.value = '';
    document.open();
    document.write(html);
    document.close();
  }

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy || !input.value) return;
    if (!window.crypto?.subtle) { message('Please open this page over HTTPS in a current browser.', true); return; }
    busy = true;
    button.disabled = true;
    input.setAttribute('aria-invalid','false');
    message('Unlocking your album…');
    try {
      const settings = await getConfig();
      const passwordBytes = encoder.encode(input.value);
      const material = await crypto.subtle.importKey('raw', passwordBytes, 'PBKDF2', false, ['deriveKey']);
      passwordBytes.fill(0);
      const key = await crypto.subtle.deriveKey({name:'PBKDF2',salt:bytes(settings.salt),iterations:settings.iterations,hash:'SHA-256'}, material, {name:'AES-GCM',length:256}, false, ['decrypt']);
      try {
        const proof = await crypto.subtle.decrypt({name:'AES-GCM',iv:bytes(settings.proofIv),additionalData:encoder.encode('wedding-album-proof:v1'),tagLength:128}, key, bytes(settings.proof));
        if (decoder.decode(proof) !== 'wedding-album-key-confirmation-v1') throw new Error('password');
      } catch { throw new Error('password'); }
      message('Opening your album…');
      const encrypted = await downloadAlbum(settings);
      const plaintext = await crypto.subtle.decrypt({name:'AES-GCM',iv:bytes(settings.iv),additionalData:encoder.encode('wedding-album:v1'),tagLength:128}, key, encrypted);
      message('Putting the finishing touches on your album…');
      openAlbum(plaintext);
    } catch (error) {
      progress.hidden = true;
      if (error.message === 'password') {
        message('That password didn’t unlock the album. Please try again.', true);
        input.setAttribute('aria-invalid','true');
        input.focus();
        input.select();
      } else message('The album couldn’t be opened. Please check your connection and try again.', true);
    } finally {
      busy = false;
      button.disabled = false;
    }
  });
})();
