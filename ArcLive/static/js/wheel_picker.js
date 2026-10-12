(function () {
  const ITEM_HEIGHT = 36;
  const PADDING_COUNT = 2;

  function daysInMonth(year, month) {
    return new Date(year, month, 0).getDate();
  }

  /** 慣性スクロール(速度を毎フレーム減衰させながらscrollTopを動かす) */
  function inertiaScroll(el, initialSpeed, onFinish) {
    let speed = initialSpeed;
    let frameId;
    function frame() {
      el.scrollTop += speed;
      speed *= 0.85;
      if (Math.abs(speed) < 0.5) {
        onFinish();
        return;
      }
      frameId = requestAnimationFrame(frame);
    }
    frame();
    return () => { if (frameId != null) cancelAnimationFrame(frameId); };
  }

  function scrollToIndex(el, index, animate) {
    const top = index * ITEM_HEIGHT;
    if (animate) el.scrollTo({ top, behavior: 'smooth' });
    else el.scrollTop = top;
  }

  /**
   * 1カラム分のホイールピッカーをセットアップする(イベント登録は1度だけ)
   * onSelect(value) は値が確定した時に呼ばれる
   * 戻り値の setValues(values, selectedValue) で表示項目を更新する
   */
  function setupWheelColumn(el, onSelect) {
    let values = [];
    let startPosY = null, startScrollTop = null;
    let touchStartTime = null, touchLastMoveTime = null;
    let cancelInertia = null;
    let wheelTimer = null;
    let downPos = null;

    function finishScroll() {
      const centerIndex = Math.round(el.scrollTop / ITEM_HEIGHT);
      const clamped = Math.max(0, Math.min(values.length - 1, centerIndex));
      scrollToIndex(el, clamped, true);
      if (values[clamped]) onSelect(values[clamped].value);
    }

    // マウスホイール操作
    el.addEventListener('wheel', (e) => {
      e.preventDefault();
      if (cancelInertia) { cancelInertia(); cancelInertia = null; }
      el.scrollTop += e.deltaY;
      clearTimeout(wheelTimer);
      wheelTimer = setTimeout(finishScroll, 100);
    }, { passive: false });

    // タッチ/マウスドラッグ開始・移動・終了
    function handleStart(e) {
      e.preventDefault();
      if (cancelInertia) { cancelInertia(); cancelInertia = null; }
      const y = 'touches' in e ? e.touches[0].clientY : e.clientY;
      startPosY = y;
      startScrollTop = el.scrollTop;
      touchStartTime = performance.now();
      touchLastMoveTime = touchStartTime;
      // マウス操作のときだけ、documentレベルでドラッグを追跡する
      if (!('touches' in e)) {
        document.addEventListener('mousemove', handleMove);
        document.addEventListener('mouseup', handleEnd);
      }
    }

    function handleMove(e) {
      if (startPosY == null) return;
      const y = 'touches' in e ? e.touches[0].clientY : e.clientY;
      el.scrollTop = startScrollTop + (startPosY - y);
      touchLastMoveTime = performance.now();
    }

    function handleEnd(e) {
      if (startPosY == null) return;
      e.preventDefault();

      // マウス操作の場合、documentに登録していたリスナーを解除する
      if (!('touches' in e)) {
        document.removeEventListener('mousemove', handleMove);
        document.removeEventListener('mouseup', handleEnd);
      }

      const endTime = performance.now();
      // 最後の移動から間が空きすぎていたら慣性スクロールせずその場で確定
      if ((endTime - touchLastMoveTime) > 50) {
        startPosY = null;
        finishScroll();
        return;
      }
      const elapsed = endTime - touchStartTime || 1;
      const distance = el.scrollTop - startScrollTop;
      startPosY = null;
      cancelInertia = inertiaScroll(el, (20 * distance) / elapsed, finishScroll);
    }

    el.addEventListener('touchstart', handleStart, { passive: false });
    el.addEventListener('touchmove', handleMove, { passive: false });
    el.addEventListener('touchend', handleEnd, { passive: false });
    el.addEventListener('mousedown', handleStart);

    // タップで直接選択(ドラッグと区別するため移動量5px以内のみタップ扱い)
    el.addEventListener('pointerdown', (e) => { downPos = { x: e.clientX, y: e.clientY }; });
    el.addEventListener('pointerup', (e) => {
      if (!downPos) return;
      const dx = downPos.x - e.clientX;
      const dy = downPos.y - e.clientY;
      downPos = null;
      if (Math.abs(dx) > 5 || Math.abs(dy) > 5) return;
      const target = e.target.closest('.wheel-item:not(.wheel-spacer)');
      if (!target) return;
      const items = Array.from(el.querySelectorAll('.wheel-item:not(.wheel-spacer)'));
      const idx = items.indexOf(target);
      if (idx === -1 || !values[idx]) return;
      setTimeout(() => {
        scrollToIndex(el, idx, true);
        onSelect(values[idx].value);
      });
    });

    return {
      setValues(newValues, selectedValue) {
        values = newValues;
        el.innerHTML = '';
        for (let i = 0; i < PADDING_COUNT; i++) {
          const spacer = document.createElement('div');
          spacer.className = 'wheel-item wheel-spacer';
          el.appendChild(spacer);
        }
        values.forEach(v => {
          const item = document.createElement('div');
          item.className = 'wheel-item';
          item.textContent = v.label;
          el.appendChild(item);
        });
        for (let i = 0; i < PADDING_COUNT; i++) {
          const spacer = document.createElement('div');
          spacer.className = 'wheel-item wheel-spacer';
          el.appendChild(spacer);
        }
        const idx = Math.max(0, values.findIndex(v => v.value === selectedValue));
        scrollToIndex(el, idx, false);
      }
    };
  }

  const modalEl = document.getElementById('DatePickerModal');
  if (!modalEl) return;   // モーダルが無いページでは何もしない

  let currentYear = new Date().getFullYear();
  let currentMonth = new Date().getMonth() + 1;
  let currentDay = new Date().getDate();
  let activeInput = null;

  // 年・月が変わったときは「日」だけ作り直す(操作中の列は触らない)
  function renderDays() {
    const dCount = daysInMonth(currentYear, currentMonth);
    if (currentDay > dCount) currentDay = dCount;
    const days = Array.from({ length: dCount }, (_, i) => ({ value: i + 1, label: `${i + 1}日` }));
    dayCol.setValues(days, currentDay);
  }

  const yearCol  = setupWheelColumn(document.getElementById('wheel-year'),  (v) => { currentYear = v;  renderDays(); });
  const monthCol = setupWheelColumn(document.getElementById('wheel-month'), (v) => { currentMonth = v; renderDays(); });
  const dayCol   = setupWheelColumn(document.getElementById('wheel-day'),   (v) => { currentDay = v; });

  // モーダルを開いたときに3列すべてを描画する
  function renderAll() {
    const thisYear = new Date().getFullYear();
    const years = Array.from({ length: 50 }, (_, i) => {
      const y = thisYear - 35 + i;
      return { value: y, label: `${y}年` };
    });
    const months = Array.from({ length: 12 }, (_, i) => ({ value: i + 1, label: `${i + 1}月` }));

    yearCol.setValues(years, currentYear);
    monthCol.setValues(months, currentMonth);
    renderDays();
  }

  // 描画は「モーダルが完全に表示された後」に行う
  // (display:none の間は scrollTop の設定が無視されるため)
  modalEl.addEventListener('shown.bs.modal', renderAll);

  // data-date-picker 属性を持つ全入力欄でモーダルを開く
  document.querySelectorAll('[data-date-picker]').forEach(input => {
    input.readOnly = true;  // スマホでキーボードが出ないように
    input.addEventListener('click', () => {
      activeInput = input;
      if (input.value) {
        const [y, m, d] = input.value.split('-').map(Number);
        currentYear = y; currentMonth = m; currentDay = d;
      } else {
        const now = new Date();
        currentYear = now.getFullYear();
        currentMonth = now.getMonth() + 1;
        currentDay = now.getDate();
      }
      bootstrap.Modal.getOrCreateInstance(modalEl).show();
    });
  });

  document.getElementById('confirmDateBtn').addEventListener('click', () => {
    if (!activeInput) return;
    const mm = String(currentMonth).padStart(2, '0');
    const dd = String(currentDay).padStart(2, '0');
    activeInput.value = `${currentYear}-${mm}-${dd}`;
    bootstrap.Modal.getOrCreateInstance(modalEl).hide();
  });
})();