
from django import forms
from .models import Birthday

class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        fields = ['birthday']


"""
// 聊天消息發送函數
      function sendMessage() {
        // 取得chat-input的元素存入message變數
        const message = document.getElementById('chatbox_input').value;
        // 判斷是否為空
        if (message.trim() !== '') {
          // 清空輸入框並更新聊天框
          document.getElementById('chatbox_input').value = '';
          updateChatBox(message, true);
          fetch('/chat/send/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': '{{ csrf_token }}',
            },
            body: new URLSearchParams({ message: message, chatroomId: currentChatroomId }),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                // 清空輸入框並更新聊天框

                updateChatBox(data.assistant_message, false);
              }else{
                // 顯示錯誤消息
                console.error('Failed to send message');
              }
            });
        }
      }
      """