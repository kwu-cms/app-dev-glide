// アプリデータ
let apps = [];
let slickCarousel = null;

// DOM要素の取得
const appsContainer = document.getElementById('apps-container');
const modal = document.getElementById('modal');
const closeBtn = document.querySelector('.close');
const slickCarouselContainer = document.getElementById('slick-carousel');
const modalAppName = document.getElementById('modal-app-name');
const modalAppDescription = document.getElementById('modal-app-description');
const modalMainContent = document.getElementById('modal-main-content');
const carouselContainer = document.getElementById('carousel-container');
const modalPdfLink = document.getElementById('modal-pdf-link');
const modalAppUrl = document.getElementById('modal-app-url');
const modalQrcode = document.getElementById('modal-qrcode');

// CSVファイルを読み込んでパース
function loadCSV() {
    const csvPath = 'data.csv';

    Papa.parse(csvPath, {
        download: true,
        header: true,
        skipEmptyLines: true,
        encoding: 'UTF-8',
        complete: function (results) {
            console.log('CSV読み込み成功:', results.data.length, '件');
            console.log('列名:', results.meta.fields);
            processCSVData(results.data);
        },
        error: function (error) {
            console.error('CSV読み込みエラー:', error);
            appsContainer.innerHTML = '<p style="text-align: center; color: #ef4444; padding: 40px;">CSVファイルの読み込みに失敗しました。<br>data.csvファイルが存在するか確認してください。</p>';
        }
    });
}

// CSVデータを処理してアプリ配列に変換
function processCSVData(csvData) {
    apps = csvData
        .filter(row => row['アプリのURL'] && row['アプリのURL'].trim() !== '')
        .map((row, index) => {
            const id = row['ID'] || (index + 1).toString();
            return {
                id: id,
                year: row['年度'] || '',
                grade: row['履修時の年次'] || '',
                uuid: row['UUID'] || '',
                url: row['アプリのURL'].trim(),
                name: row['アプリ名'] || `アプリ ${id}`,
                description: row['アプリの説明'] || '',
                pdf: row['pdf'] || '',
                screenshot: `images/screenshots/app-${id}.png`,
                qrcode: row['QRコード'] || ''
            };
        });

    renderApps();
}

// アプリカードをレンダリング
function renderApps() {
    appsContainer.innerHTML = '';

    apps.forEach((app, index) => {
        const card = document.createElement('div');
        card.className = 'app-card';
        card.addEventListener('click', () => openModal(index));

        // 説明文を3行に制限
        const description = app.description.length > 100
            ? app.description.substring(0, 100) + '...'
            : app.description;

        const qrcodeHtml = app.qrcode ? `<div class="app-card-qrcode"><img src="${app.qrcode}" alt="QRコード"></div>` : '';

        card.innerHTML = `
            <div class="app-card-image-container">
                <div class="app-card-phone-mockup">
                    <div class="app-card-phone-frame">
                        <div class="app-card-phone-screen">
                            <img src="${app.screenshot}" alt="アプリ ${app.id}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22402%22 height=%22874%22%3E%3Crect fill=%22%236366f1%22 width=%22402%22 height=%22874%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 fill=%22white%22 text-anchor=%22middle%22 dy=%22.3em%22 font-size=%2224%22%3E画像を読み込み中...%3C/text%3E%3C/svg%3E'">
                        </div>
                    </div>
                </div>
                ${qrcodeHtml}
            </div>
            <div class="app-card-content">
                <h3 class="app-card-name">${escapeHtml(app.name)}</h3>
                <p class="app-card-description">${escapeHtml(description)}</p>
                <a href="${app.url}" target="_blank" class="app-card-link" onclick="event.stopPropagation()">アプリを見る →</a>
            </div>
        `;

        appsContainer.appendChild(card);
    });
}

// HTMLエスケープ
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// モーダルを開く
function openModal(index) {
    // Slickカルーセルを初期化
    initSlickCarousel(index);

    // モーダル情報を更新
    updateModalInfo(index);

    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

// モーダルを閉じる
function closeModal() {
    // Slickカルーセルを破棄
    if (slickCarousel) {
        slickCarousel.slick('unslick');
        slickCarousel = null;
    }

    modal.classList.remove('show');
    document.body.style.overflow = '';
}

// Slickカルーセルを初期化
function initSlickCarousel(initialIndex) {
    // 既存のカルーセルを破棄
    if (slickCarousel) {
        slickCarousel.slick('unslick');
    }

    // スライドを生成
    slickCarouselContainer.innerHTML = '';
    apps.forEach((app, index) => {
        const slide = document.createElement('div');
        slide.className = 'slick-slide-item';
        slide.innerHTML = `
            <div class="phone-mockup">
                <div class="phone-frame">
                    <div class="phone-screen">
                        <img src="${app.screenshot}" alt="アプリ ${app.id}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22402%22 height=%22874%22%3E%3Crect fill=%22%236366f1%22 width=%22402%22 height=%22874%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 fill=%22white%22 text-anchor=%22middle%22 dy=%22.3em%22 font-size=%2224%22%3E画像が見つかりません%3C/text%3E%3C/svg%3E'">
                    </div>
                </div>
            </div>
        `;
        slickCarouselContainer.appendChild(slide);
    });

    // Slickカルーセルを初期化
    slickCarousel = $(slickCarouselContainer).slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        initialSlide: initialIndex,
        arrows: true,
        prevArrow: '<button type="button" class="slick-prev carousel-btn"><i class="fas fa-chevron-left"></i></button>',
        nextArrow: '<button type="button" class="slick-next carousel-btn"><i class="fas fa-chevron-right"></i></button>',
        dots: false,
        swipe: true,
        touchMove: true,
        adaptiveHeight: false,
        speed: 300,
        fade: false,
        centerMode: false,
        variableWidth: false
    });

    // スライド変更時にモーダル情報を更新
    $(slickCarouselContainer).on('afterChange', function (event, slick, currentSlide) {
        updateModalInfo(currentSlide);
    });
}

// モーダルの情報を更新
function updateModalInfo(index) {
    const app = apps[index];

    modalAppName.textContent = app.name;
    modalAppDescription.textContent = app.description;
    modalAppUrl.href = app.url;

    // PDFリンクを表示
    if (app.pdf && app.pdf.trim() !== '') {
        modalPdfLink.href = app.pdf;
        modalPdfLink.style.display = 'inline-block';
    } else {
        modalPdfLink.style.display = 'none';
    }

    // QRコードを表示
    if (app.qrcode && app.qrcode.trim() !== '') {
        modalQrcode.innerHTML = `<img src="${app.qrcode}" alt="QRコード" class="modal-qrcode-image">`;
        modalQrcode.style.display = 'block';
    } else {
        modalQrcode.style.display = 'none';
    }
}


// キーボードイベント
function handleKeyPress(event) {
    if (!modal.classList.contains('show')) return;

    if (event.key === 'ArrowLeft' && slickCarousel) {
        slickCarousel.slick('slickPrev');
    } else if (event.key === 'ArrowRight' && slickCarousel) {
        slickCarousel.slick('slickNext');
    } else if (event.key === 'Escape') {
        closeModal();
    }
}

// イベントリスナーの設定
closeBtn.addEventListener('click', closeModal);
document.addEventListener('keydown', handleKeyPress);

// モーダルの背景をクリックしたら閉じる
modal.addEventListener('click', (event) => {
    if (event.target === modal) {
        closeModal();
    }
});

// ページ読み込み時にCSVを読み込む
if (typeof Papa !== 'undefined') {
    loadCSV();
} else {
    console.error('PapaParseが読み込まれていません');
    appsContainer.innerHTML = '<p style="text-align: center; color: #ef4444; padding: 40px;">ライブラリの読み込みに失敗しました。</p>';
}
