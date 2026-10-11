$(function(){
    var year = new Date().getFullYear();
    var month = new Date().getMonth();+1
    var day = new Date().getDate();
    $("date1").html(year + "年" + month + "月" + date + "日" 
});


<script>
document.addEventListener('DOMContentLoaded', function() {
    // ボタンのIDをあなたが決めた "preset-image" に合わせて取得します
    const btnShowPresets = document.getElementById('preset-image'); 
    const btnBackToMenu = document.getElementById('btn-back-to-menu');
    const menuView = document.getElementById('modal-menu-view');
    const presetView = document.getElementById('modal-preset-view');

    // 「アプリ内の画像から選択（id="preset-image"）」ボタンが押されたとき
    if (btnShowPresets) {
        btnShowPresets.addEventListener('click', function() {
            menuView.style.display = 'none';   // メニュー画面を消す
            presetView.style.display = 'block'; // 画像一覧画面を出す
        });
    }

    // 「戻る」ボタンが押されたとき
    if (btnBackToMenu) {
        btnBackToMenu.addEventListener('click', function() {
            presetView.style.display = 'none';  // 画像一覧画面を消す
            menuView.style.display = 'block';   // メニュー画面を出す
        });
    }

    // モーダルを閉じたときに表示を最初（メニュー）に戻す設定
    const myModal = document.getElementById('BackImageModal');
    if (myModal) {
        myModal.addEventListener('hidden.bs.modal', function () {
            menuView.style.display = 'block';
            presetView.style.display = 'none';
        });
    }
});
</script>
