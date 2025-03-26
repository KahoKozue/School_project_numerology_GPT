
function showHealthy(generatedText) {
  // 处理动态生成的文本
  console.log(generatedText);
  // 这里可以写您的逻辑，例如显示相应内容

  // 更新下方显示的典籍内容
  var contentDiv = document.getElementById('content');
  contentDiv.innerHTML = '<h2>{{ category }}</h2><p>' + generatedText + '</p>';
}
  function showjob(category, content) {
    // 在這裡處理點擊事件，可以根據類別執行不同的操作
    console.log('點擊了類別：', category);
    // 這裡可以添加顯示相應內容的邏輯
  
    // 更新下方顯示的典籍內容
    var contentDiv = document.getElementById('content');
    contentDiv.innerHTML = '<h2>' + category + '</h2><p>' 
  }
  
  function showmoney(category, content) {
    // 在這裡處理點擊事件，可以根據類別執行不同的操作
    console.log('點擊了類別：', category);
    // 這裡可以添加顯示相應內容的邏輯
  
    // 更新下方顯示的典籍內容
    var contentDiv = document.getElementById('content');
    contentDiv.innerHTML = '<h2>' + category + '</h2><p>' 
  }
  
  

  
  
  function showlove(category, content) {
    // 在這裡處理點擊事件，可以根據類別執行不同的操作
    console.log('點擊了類別：', category);
    // 這裡可以添加顯示相應內容的邏輯
  
    // 更新下方顯示的典籍內容
    var contentDiv = document.getElementById('content');
    contentDiv.innerHTML = '<h2>' + category + '</h2><p>' 
  }
