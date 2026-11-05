(() => {
  'use strict';

  const form = document.getElementById('preferences');
  const prompt = document.getElementById('prompt');
  const status = document.getElementById('copy-status');
  const copyLabel = document.getElementById('copy-label');
  const more = document.getElementById('more-options');
  const byId = (id) => document.getElementById(id);
  const idleMessage = '上传完整参考图，再粘贴这段指令。';
  const openings = {
    restore: '使用 $paper-figure-to-figma，将附图还原为可编辑矢量图。',
    modify: '使用 $paper-figure-to-figma，参照附图制作可编辑矢量图，优先完成我指定的修改。',
    layout: '使用 $paper-figure-to-figma，将附图重建为可编辑矢量图，优化排版，保留原有内容和科学关系。',
  };
  const placeholders = {
    restore: '例如：把模块 A 改名为 Encoder；将图例移到右下角；保留所有箭头的方向。',
    modify: '例如：把右侧三个模块合并成一组；将红色箭头改成虚线；保留其余部分的布局。',
    layout: '例如：将上下布局改为左右布局；统一模块间距；放大图例中的文字。',
  };

  function showStatus(message, state = '') {
    status.textContent = message;
    status.dataset.state = state;
  }

  function syncCustomField(id) {
    const active = byId(id).value === 'custom';
    byId(`${id}-custom-field`).hidden = !active;
    byId(`${id}-custom`).disabled = !active;
    byId(`${id}-custom`).required = active;
  }

  function validate() {
    const width = byId('paper-width');
    const url = byId('figma-url');
    width.setCustomValidity('');
    url.setCustomValidity('');
    if (width.value && (!Number.isFinite(Number(width.value)) || Number(width.value) < 1)) {
      width.setCustomValidity('请填写大于或等于 1 的图宽，单位为 mm。');
    }
    if (!url.disabled && url.value.trim()) {
      try {
        const parsed = new URL(url.value.trim());
        const isFigma = parsed.hostname === 'figma.com' || parsed.hostname.endsWith('.figma.com');
        if (parsed.protocol !== 'https:' || !isFigma || !/^\/(design|file)\/[^/]+/.test(parsed.pathname)) {
          throw new Error('Invalid destination');
        }
      } catch {
        url.setCustomValidity('请填写完整的 Figma Design 文件链接。');
      }
    }
    const controls = [byId('font-custom'), byId('color-custom'), width, url];
    for (const control of controls) {
      control.removeAttribute('aria-invalid');
      if (!control.disabled && control.required && !control.value.trim()) {
        control.setCustomValidity('请填写自定义要求，或选择默认选项。');
      } else if (control.id.endsWith('-custom')) {
        control.setCustomValidity('');
      }
    }
    return controls.filter((control) => !control.disabled && !control.checkValidity());
  }

  function render() {
    syncCustomField('font');
    syncCustomField('color');
    const localOnly = ['local', 'pptx'].includes(byId('delivery').value);
    byId('figma-url').disabled = localOnly;
    byId('figma-hint').hidden = !localOnly;
    const data = new FormData(form);
    const task = data.get('task');
    const lines = [openings[task] || openings.restore];
    byId('changes').placeholder = placeholders[task] || placeholders.restore;

    if (data.get('font') === 'original') lines.push('字体：沿用原图字体。');
    if (data.get('font') === 'comic') lines.push('标题字体：Comic Sans MS。');
    if (data.get('font') === 'custom' && data.get('fontCustom').trim()) {
      lines.push(`字体：${data.get('fontCustom').trim()}`);
    }
    if (data.get('color') === 'accessible') lines.push('配色：调整为色盲友好配色，保留颜色表达的原有含义。');
    if (data.get('color') === 'grayscale') lines.push('配色：适合灰度打印，保持分组和类别可区分。');
    if (data.get('color') === 'custom' && data.get('colorCustom').trim()) {
      lines.push(`配色：${data.get('colorCustom').trim()}`);
    }
    if (data.get('paperWidth') && Number(data.get('paperWidth')) > 0) {
      lines.push(`论文中的图宽：${Number(data.get('paperWidth'))} mm，请按此尺寸检查可读性。`);
    }
    if (data.get('delivery') === 'paper') lines.push('交付：Figma 可编辑图层、SVG 和 PDF。');
    if (data.get('delivery') === 'local') lines.push('交付：仅本地 SVG 和 PDF。');
    if (data.get('delivery') === 'pptx') lines.push('交付：可编辑 PPTX 和 PowerPoint 实际预览。文字和主要图形使用原生对象，复杂插画保留独立 SVG。');
    const destination = (data.get('figmaUrl') || '').trim();
    if (!localOnly && destination) lines.push(`Figma 目标文件：${destination}`);
    if (data.get('changes').trim()) lines.push(`补充要求：\n${data.get('changes').trim()}`);

    prompt.value = lines.join('\n');
    copyLabel.textContent = '复制 Prompt';
    showStatus(idleMessage);
    validate();
  }

  form.addEventListener('input', render);
  form.addEventListener('change', render);
  form.addEventListener('submit', (event) => event.preventDefault());
  form.addEventListener('reset', () => {
    more.open = false;
    // Read the values after the browser completes the form's default reset action.
    setTimeout(render, 0);
  });

  byId('copy').addEventListener('click', async () => {
    const invalid = validate();
    if (invalid.length) {
      const first = invalid[0];
      if (more.contains(first)) more.open = true;
      for (const control of invalid) control.setAttribute('aria-invalid', 'true');
      showStatus(first.validationMessage, 'error');
      first.focus();
      return;
    }

    const text = prompt.value;
    let copied = false;
    if (navigator.clipboard?.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        copied = true;
      } catch {
        // Local files and browser permissions can require the selection fallback.
      }
    }
    if (!copied) {
      prompt.focus();
      prompt.select();
      try { copied = document.execCommand('copy'); } catch { /* Keep the text selected. */ }
    }
    if (copied && prompt.value === text) {
      copyLabel.textContent = '已复制';
      showStatus('已复制，连同完整参考图一起发送。', 'success');
    } else if (copied) {
      showStatus('已复制先前内容；选项有更新，请重新复制。');
    } else {
      showStatus('请手动复制已选中的指令。');
    }
  });

  render();
})();
