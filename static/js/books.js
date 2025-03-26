// 目錄收合功能
const toggleBtn = document.querySelector('.toggle-btn');
const sidebar = document.querySelector('.sidebar');
const tocList = document.querySelector('.toc-list');
const tocItems = document.querySelectorAll('.toc-item');

toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
});

// 目錄項目點擊事件
tocItems.forEach((item, index) => {
    item.addEventListener('click', () => {
        // 移除所有項目的 active 類別
        tocItems.forEach(item => item.classList.remove('active'));
        // 為當前項目添加 active 類別
        item.classList.add('active');
        // 更新書籍內容
        updateBookContent(index);
    });
});

// 導航按鈕功能
const prevPageBtn = document.querySelector('.prev-page');
const homeBtn = document.querySelector('.home');
const nextPageBtn = document.querySelector('.next-page');
let currentChapter = 0;

prevPageBtn.addEventListener('click', () => {
    if (currentChapter > 0) {
        currentChapter--;
        updateActiveChapter();
        updateBookContent(currentChapter);
    }
});

homeBtn.addEventListener('click', () => {
    currentChapter = 0;
    updateActiveChapter();
    updateBookContent(currentChapter);
});

nextPageBtn.addEventListener('click', () => {
    if (currentChapter < tocItems.length - 1) {
        currentChapter++;
        updateActiveChapter();
        updateBookContent(currentChapter);
    }
});

function updateActiveChapter() {
    tocItems.forEach((item, index) => {
        if (index === currentChapter) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

function updateBookContent(index) {
    const bookContent = document.querySelector('.book-content');
    const chapterContents = [
        '第一章的內容約有100個字: ' + '這是第一章的內容,隨便寫一些文字,大約100個字就可以了。這只是一個示例,實際內容應該是從後端獲取的數據。',
        '第二章的內容約有200個字: ' + '這是第二章的內容,隨便寫一些文字,大約200個字就可以了。這只是一個示例,實際內容應該是從後端獲取的數據。當然,內容可以是任何格式,包括文本、圖片、視頻等。',
    ];
    bookContent.textContent = chapterContents[index];
}