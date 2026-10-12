(function () {
  // ★ここから setupWheelColumn などは、今のコードをそのままコピー★
  // const ITEM_HEIGHT = 36; ... function setupWheelColumn(...) { ... }

  const modalEl = document.getElementById('DatePickerModal');
  if (!modalEl) return;   // モーダルが無いページでは何もしない

  // ...(currentYear, renderDays, yearCol, monthCol, dayCol, renderAll も今のまま)...

  modalEl.addEventListener('shown.bs.modal', renderAll);

  // ★変更点: ID決め打ちをやめて、data-date-picker 属性を持つ全入力欄を対象にする
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

